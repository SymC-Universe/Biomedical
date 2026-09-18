from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple

import numpy as np
import pandas as pd

from src.materialize_conglomerate_chi_c1 import load_schema, validate_row

REGISTRY_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
PANEL_REL = Path("GRI_v2/development_outputs/stage_b2_rppa/stage_b2_rppa_common_panel.txt")
OUTDIR_REL = Path("GRI_v2/artifacts/conglomerate_c1_egp_fragment_20260918")

PATIENT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})")
ROOT_RE = re.compile(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])")
TYPE_RE = re.compile(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GRI-Conglomerate-C1-EGP/1.0"},
    )
    with urllib.request.urlopen(req, timeout=240) as resp, path.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def source_map(registry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {s["id"]: s for s in registry["sources"]}


def patient_id(value: str) -> str | None:
    m = PATIENT_RE.search(str(value).replace(".", "-"))
    return m.group(1) if m else None


def sample_root(value: str) -> str | None:
    m = ROOT_RE.search(str(value).replace(".", "-"))
    return m.group(1) if m else None


def sample_type(value: str) -> str | None:
    m = TYPE_RE.search(str(value).replace(".", "-"))
    return m.group(1) if m else None


def combine_cancer_maps(
    leuk: pd.DataFrame,
    rppa: pd.DataFrame,
) -> Tuple[Dict[str, str], Dict[str, Any]]:
    candidates: Dict[str, set[str]] = defaultdict(set)

    for r in leuk.itertuples(index=False):
        pid = patient_id(r.sample)
        cancer = str(r.cancer).strip()
        if pid and cancer:
            candidates[pid].add(cancer)

    for r in rppa[["SampleID", "TumorType"]].itertuples(index=False):
        pid = patient_id(r.SampleID)
        cancer = str(r.TumorType).strip()
        if pid and cancer and cancer.lower() != "nan":
            candidates[pid].add(cancer)

    conflicts = {p: sorted(v) for p, v in candidates.items() if len(v) > 1}
    mapping = {p: next(iter(v)) for p, v in candidates.items() if len(v) == 1}
    return mapping, {
        "mapped_patients": len(mapping),
        "conflicting_patients": len(conflicts),
        "conflict_preview": dict(list(sorted(conflicts.items()))[:25]),
    }


def row_template(
    *,
    entity_id: str,
    system_id: str,
    sample_id_value: str,
    block: str,
    feature: str,
    value: float,
    role: str,
    source_id: str,
    source_digest: str,
    transform_id: str,
) -> Dict[str, str]:
    return {
        "entity_id": entity_id,
        "cohort_id": "TCGA_PANCAN",
        "system_id": system_id,
        "sample_id": sample_id_value,
        "block_id": block,
        "feature_id": feature,
        "value": repr(float(value)),
        "value_status": "OBSERVED",
        "uncertainty_value": "",
        "uncertainty_kind": "NONE",
        "local_embedded_role": role,
        "time_index": "",
        "time_order_known": "FALSE",
        "evidence_class": "P0-D",
        "independence_role": "DEVELOPMENT",
        "source_id": source_id,
        "source_digest_or_run": f"sha256:{source_digest}",
        "transform_id": transform_id,
    }


def iter_leukocyte_rows(
    leuk: pd.DataFrame,
    digest: str,
) -> Iterator[Dict[str, str]]:
    x = leuk.copy()
    x["pid"] = x["sample"].map(patient_id)
    x["root"] = x["sample"].map(sample_root)
    x["stype"] = x["sample"].map(sample_type)
    x["value"] = pd.to_numeric(x["value"], errors="coerce")
    x = x[x["pid"].notna() & x["root"].notna() & x["stype"].eq("01") & x["value"].notna()].copy()
    x = (
        x.groupby(["pid", "root", "cancer"], as_index=False, sort=True)
        .agg(value=("value", "median"))
    )
    for r in x.itertuples(index=False):
        yield row_template(
            entity_id=r.pid,
            system_id=str(r.cancer),
            sample_id_value=r.root,
            block="E",
            feature="LEUKOCYTE_FRACTION",
            value=float(r.value),
            role="CONTEXT",
            source_id="LEUKOCYTE_FRACTION",
            source_digest=digest,
            transform_id="B0_PRIMARY01_PATIENT_SAMPLE_ROOT_MEDIAN",
        )


def iter_purity_rows(
    purity: pd.DataFrame,
    cancer_map: Dict[str, str],
    digest: str,
) -> Tuple[Iterator[Dict[str, str]], Dict[str, int]]:
    x = purity.copy()
    x["pid"] = x["sample"].map(patient_id)
    x["root"] = x["sample"].map(sample_root)
    x["stype"] = x["sample"].map(sample_type)
    x["numeric"] = pd.to_numeric(x["purity"], errors="coerce")
    x = x[
        x["pid"].notna()
        & x["stype"].eq("01")
        & x["call status"].astype(str).str.lower().eq("called")
        & x["numeric"].notna()
    ].copy()
    patient_counts = x.groupby("pid").size()
    unique_patients = set(patient_counts[patient_counts == 1].index)
    x = x[x["pid"].isin(unique_patients)].copy()
    x["cancer"] = x["pid"].map(cancer_map)
    missing_cancer = int(x["cancer"].isna().sum())
    x = x[x["cancer"].notna()].copy()

    def _iter() -> Iterator[Dict[str, str]]:
        for r in x.sort_values(["pid", "sample"]).itertuples(index=False):
            sid = r.root if isinstance(r.root, str) and r.root else str(r.sample)
            yield row_template(
                entity_id=r.pid,
                system_id=str(r.cancer),
                sample_id_value=sid,
                block="E",
                feature="ABSOLUTE_PURITY",
                value=float(r.numeric),
                role="CONTEXT",
                source_id="ABSOLUTE_PURITY",
                source_digest=digest,
                transform_id="B0_CALLED_PRIMARY01_UNIQUE_PATIENT_CANCER_METADATA_JOIN",
            )

    return _iter(), {
        "eligible_unique_primary_called": int(len(x) + missing_cancer),
        "excluded_missing_cancer_identity": missing_cancer,
        "emitted": int(len(x)),
    }


def unique_matchable_source_rows(df: pd.DataFrame, id_col: str) -> pd.DataFrame:
    x = df.copy()
    x["pid"] = x[id_col].map(patient_id)
    x["root"] = x[id_col].map(sample_root)
    x["stype"] = x[id_col].map(sample_type)
    x = x[x["pid"].notna() & x["stype"].eq("01")].copy()

    root_counts = x[x["root"].notna()].groupby("root").size()
    unique_roots = set(root_counts[root_counts == 1].index)
    pat_counts = x.groupby("pid").size()
    unique_pats = set(pat_counts[pat_counts == 1].index)

    keep = x["root"].isin(unique_roots) | x["pid"].isin(unique_pats)
    return x[keep].copy()


def iter_genomic_rows(
    absolute: pd.DataFrame,
    seg: pd.DataFrame,
    cancer_map: Dict[str, str],
    abs_digest: str,
    seg_digest: str,
) -> Tuple[Iterator[Dict[str, str]], Dict[str, int]]:
    specs = [
        (
            unique_matchable_source_rows(absolute, absolute.columns[0]),
            absolute.columns[0],
            "ANEUPLOIDY_LOH",
            abs_digest,
            [
                ("ANEUPLOIDY_AS", "AS"),
                ("LOH_SEGMENT_COUNT", "LOH_n_seg"),
                ("LOH_GENOME_FRACTION", "LOH_frac_altered"),
            ],
        ),
        (
            unique_matchable_source_rows(seg, "Sample"),
            "Sample",
            "CNV_BURDEN",
            seg_digest,
            [
                ("SCNA_SEGMENT_COUNT", "n_segs"),
                ("SCNA_ALTERED_FRACTION", "frac_altered"),
            ],
        ),
    ]

    stats = {"candidate_source_rows": 0, "excluded_missing_cancer_identity": 0, "emitted_values": 0}

    def _iter() -> Iterator[Dict[str, str]]:
        for x, id_col, source_id, digest, features in specs:
            x = x.copy()
            x["cancer"] = x["pid"].map(cancer_map)
            stats["candidate_source_rows"] += int(len(x))
            stats["excluded_missing_cancer_identity"] += int(x["cancer"].isna().sum())
            x = x[x["cancer"].notna()].copy()
            for r in x.sort_values(["pid", id_col]).itertuples(index=False, name=None):
                pass

            for _, r in x.sort_values(["pid", id_col]).iterrows():
                sid = r["root"] if isinstance(r["root"], str) and r["root"] else str(r[id_col])
                for feature_id, col in features:
                    v = pd.to_numeric(pd.Series([r[col]]), errors="coerce").iloc[0]
                    if not np.isfinite(v):
                        continue
                    stats["emitted_values"] += 1
                    yield row_template(
                        entity_id=str(r["pid"]),
                        system_id=str(r["cancer"]),
                        sample_id_value=sid,
                        block="G",
                        feature=feature_id,
                        value=float(v),
                        role="CONTEXT",
                        source_id=source_id,
                        source_digest=digest,
                        transform_id="B2_PRIMARY01_UNIQUE_ROOT_OR_UNIQUE_PATIENT_CANCER_METADATA_JOIN",
                    )

    return _iter(), stats


def iter_rppa_rows(
    rppa: pd.DataFrame,
    panel: List[str],
    digest: str,
) -> Tuple[Iterator[Dict[str, str]], Dict[str, int]]:
    x = rppa.copy()
    x["pid"] = x["SampleID"].map(patient_id)
    x["root"] = x["SampleID"].map(sample_root)
    x["stype"] = x["SampleID"].map(sample_type)
    x = x[x["pid"].notna() & x["root"].notna() & x["stype"].eq("01")].copy()

    root_counts = x.groupby("root").size()
    unique_roots = set(root_counts[root_counts == 1].index)
    x = x[x["root"].isin(unique_roots)].copy()

    missing_panel = [p for p in panel if p not in x.columns]
    if missing_panel:
        raise ValueError(f"Frozen RPPA panel columns missing from source: {missing_panel[:10]}")
    if len(panel) != 189 or len(set(panel)) != 189:
        raise ValueError(f"Frozen RPPA panel expected 189 unique features, got {len(panel)}")

    stats = {
        "unique_primary_sample_roots": int(len(x)),
        "panel_features": len(panel),
        "emitted_values": 0,
        "nonfinite_panel_values_skipped": 0,
    }

    def _iter() -> Iterator[Dict[str, str]]:
        for _, r in x.sort_values(["pid", "root"]).iterrows():
            cancer = str(r["TumorType"]).strip()
            if not cancer or cancer.lower() == "nan":
                continue
            for feature in panel:
                v = pd.to_numeric(pd.Series([r[feature]]), errors="coerce").iloc[0]
                if not np.isfinite(v):
                    stats["nonfinite_panel_values_skipped"] += 1
                    continue
                stats["emitted_values"] += 1
                yield row_template(
                    entity_id=str(r["pid"]),
                    system_id=cancer,
                    sample_id_value=str(r["root"]),
                    block="P",
                    feature=f"RPPA::{feature}",
                    value=float(v),
                    role="LOCAL",
                    source_id="RPPA_FINAL",
                    source_digest=digest,
                    transform_id="B2_RPPA_PRIMARY01_FROZEN_COMMON_PANEL_189",
                )

    return _iter(), stats


def main() -> None:
    root = repo_root()
    registry = json.loads((root / REGISTRY_REL).read_text(encoding="utf-8"))
    smap = source_map(registry)
    panel_path = root / PANEL_REL
    panel = [x.strip() for x in panel_path.read_text(encoding="utf-8").splitlines() if x.strip()]

    work = Path("_c1_egp_sources")
    work.mkdir(exist_ok=True)

    ids = ["ABSOLUTE_PURITY", "LEUKOCYTE_FRACTION", "ANEUPLOIDY_LOH", "CNV_BURDEN", "RPPA_FINAL"]
    paths: Dict[str, Path] = {}
    observed_hashes: Dict[str, str] = {}
    for sid in ids:
        s = smap[sid]
        p = work / s["file_name"]
        download(s["url"], p)
        observed = sha256_file(p)
        expected = s["expected_sha256"]
        if observed != expected:
            raise ValueError(f"{sid}: SHA mismatch {observed} != {expected}")
        paths[sid] = p
        observed_hashes[sid] = observed

    purity = pd.read_csv(paths["ABSOLUTE_PURITY"], sep="\t", dtype=str)
    leuk = pd.read_csv(
        paths["LEUKOCYTE_FRACTION"],
        sep="\t",
        header=None,
        names=["cancer", "sample", "value"],
        dtype=str,
    )
    absolute = pd.read_csv(paths["ANEUPLOIDY_LOH"], sep="\t", dtype=str)
    seg = pd.read_csv(paths["CNV_BURDEN"], sep="\t", dtype=str)
    rppa = pd.read_csv(paths["RPPA_FINAL"], sep="\t", dtype=str)

    cancer_map, cancer_map_stats = combine_cancer_maps(leuk, rppa)
    if cancer_map_stats["conflicting_patients"] != 0:
        raise ValueError(
            "Cancer identity metadata conflicts between leukocyte and RPPA sources: "
            + json.dumps(cancer_map_stats["conflict_preview"], sort_keys=True)
        )

    purity_iter, purity_stats = iter_purity_rows(
        purity, cancer_map, observed_hashes["ABSOLUTE_PURITY"]
    )
    genomic_iter, genomic_stats = iter_genomic_rows(
        absolute,
        seg,
        cancer_map,
        observed_hashes["ANEUPLOIDY_LOH"],
        observed_hashes["CNV_BURDEN"],
    )
    rppa_iter, rppa_stats = iter_rppa_rows(
        rppa, panel, observed_hashes["RPPA_FINAL"]
    )

    outdir = root / OUTDIR_REL
    outdir.mkdir(parents=True, exist_ok=True)
    fragment = outdir / "conglomerate_c1_egp_fragment.csv.gz"
    schema = load_schema(root)
    counts_block = Counter()
    counts_feature = Counter()
    entities = set()
    keys = set()
    row_count = 0

    streams: List[Iterable[Dict[str, str]]] = [
        iter_leukocyte_rows(leuk, observed_hashes["LEUKOCYTE_FRACTION"]),
        purity_iter,
        genomic_iter,
        rppa_iter,
    ]

    with gzip.open(fragment, "wt", encoding="utf-8", newline="", compresslevel=6) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=schema["required_columns"],
            lineterminator="\n",
        )
        writer.writeheader()
        for stream in streams:
            for row in stream:
                key = validate_row(row, row_count + 2, schema)
                if key in keys:
                    raise ValueError(f"Duplicate C1 carrier key: {key}")
                keys.add(key)
                writer.writerow(row)
                row_count += 1
                entities.add(row["entity_id"])
                counts_block[row["block_id"]] += 1
                counts_feature[row["feature_id"]] += 1

    manifest = {
        "schema": "gri-conglomerate-c1-egp-fragment-v1",
        "date": "2026-09-18",
        "status": "C1_EGP_RAW_BLOCK_FRAGMENT_MATERIALIZED",
        "blocks": ["E", "G", "P"],
        "rows_total": row_count,
        "entities_total": len(entities),
        "rows_by_block": dict(sorted(counts_block.items())),
        "features_total": len(counts_feature),
        "source_sha256": observed_hashes,
        "rppa_common_panel_path": str(PANEL_REL),
        "rppa_common_panel_sha256": sha256_file(panel_path),
        "rppa_common_panel_count": len(panel),
        "cancer_identity_mapping": cancer_map_stats,
        "purity_stats": purity_stats,
        "genomic_stats": genomic_stats,
        "rppa_stats": rppa_stats,
        "fragment_file": fragment.name,
        "fragment_sha256": sha256_file(fragment),
        "cross_block_aggregation_performed": False,
        "diagnostic_or_predictive_model_fit": False,
        "biological_outcome_opened": False,
        "claim_ceiling": (
            "raw/frozen E-G-P block materialization only; no diagnostic, predictive, "
            "causal, temporal, scalar-Chi, or clinical claim"
        ),
    }
    manifest_path = outdir / "conglomerate_c1_egp_fragment_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
