from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import re
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

CHUNK_BYTES = 8 * 1024 * 1024
TCGA_ROOT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}[-.][0-9]{2}[A-Z]", re.I)
NA_VALUES = ["", "NA", "N/A", "NaN", "nan", "NULL", "null"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK_BYTES), b""):
            h.update(block)
    return h.hexdigest()


def normalize_barcode(value: str) -> str:
    return str(value).upper().replace(".", "-")


def sample_root(value: str) -> str | None:
    m = TCGA_ROOT_RE.search(str(value))
    return normalize_barcode(m.group(0)) if m else None


def nonblank(value: str | None) -> bool:
    if value is None:
        return False
    s = str(value).strip()
    return bool(s) and s.upper() not in {"NA", "NAN", "NONE"}


def split_tokens(value: str | None) -> list[str]:
    if value is None:
        return [""]
    return [x.strip() for x in str(value).split(";")]


def parse_hallmarks(path: Path, expected_sha: str, expected_modules: int) -> dict[str, list[str]]:
    actual = sha256_file(path)
    if actual != expected_sha:
        raise ValueError(f"Hallmark membership SHA mismatch: {actual} != {expected_sha}")
    modules: dict[str, list[str]] = {}
    with path.open("r", encoding="utf-8", errors="strict") as fh:
        for line in fh:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) < 3:
                continue
            name = parts[0].strip()
            genes = [g.strip() for g in parts[2:] if g.strip()]
            if name:
                modules[name] = list(dict.fromkeys(genes))
    if len(modules) != expected_modules or any(not x.startswith("HALLMARK_") for x in modules):
        raise ValueError(f"Expected {expected_modules} HALLMARK_ modules; found {len(modules)}")
    return modules


def load_annotation(annotation_path: Path, chen_path: Path, cfg: dict) -> tuple[set[str], dict[str, tuple[str, ...]], set[str], set[str], set[str]]:
    c1a = cfg["c1a_assets"]
    ann_sha = sha256_file(annotation_path)
    chen_sha = sha256_file(chen_path)
    if ann_sha != c1a["annotation_export_sha256"]:
        raise ValueError(f"C1A annotation export SHA mismatch: {ann_sha} != {c1a['annotation_export_sha256']}")
    if chen_sha != c1a["chen_ids_sha256"]:
        raise ValueError(f"C1A Chen-ID SHA mismatch: {chen_sha} != {c1a['chen_ids_sha256']}")
    chen = {x.strip() for x in chen_path.read_text(encoding="utf-8").splitlines() if x.strip()}
    annotation_ids: set[str] = set()
    tss200_by_probe: dict[str, tuple[str, ...]] = {}
    common_snp: set[str] = set()
    tuple_mismatch: set[str] = set()
    with gzip.open(annotation_path, "rt", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        required = {"probe_id", "UCSC_RefGene_Name", "UCSC_RefGene_Accession", "UCSC_RefGene_Group", "CpG_rs", "SBE_rs"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"annotation export missing required columns: {sorted(missing)}")
        for row in reader:
            pid = (row.get("probe_id") or "").strip()
            if not pid:
                continue
            if pid in annotation_ids:
                raise ValueError(f"duplicate annotation probe ID {pid}")
            annotation_ids.add(pid)
            genes = split_tokens(row.get("UCSC_RefGene_Name"))
            accs = split_tokens(row.get("UCSC_RefGene_Accession"))
            groups = split_tokens(row.get("UCSC_RefGene_Group"))
            mismatch = not (len(genes) == len(accs) == len(groups))
            if mismatch:
                tuple_mismatch.add(pid)
            else:
                tss200: list[str] = []
                for gene, _acc, group in zip(genes, accs, groups):
                    if gene and group == "TSS200" and gene not in tss200:
                        tss200.append(gene)
                if tss200:
                    tss200_by_probe[pid] = tuple(tss200)
            if nonblank(row.get("CpG_rs")) or nonblank(row.get("SBE_rs")):
                common_snp.add(pid)
    return annotation_ids, tss200_by_probe, common_snp, tuple_mismatch, chen


def validate_eligibility(summary_path: Path, sample_path: Path, counts_path: Path, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    e = cfg["p0_eligibility"]
    checks = {
        "summary_sha256": (summary_path, e["summary_sha256"]),
        "sample_eligibility_sha256": (sample_path, e["sample_eligibility_sha256"]),
        "partition_counts_sha256": (counts_path, e["partition_counts_sha256"]),
    }
    for label, (path, expected) in checks.items():
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(f"{label} mismatch: {actual} != {expected}")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("status") != "P0_SAMPLE_ELIGIBILITY_COMPLETE":
        raise ValueError("P0 eligibility summary is not COMPLETE")
    if int(summary.get("eligible_records", -1)) != int(e["eligible_records"]):
        raise ValueError("P0 eligible-record count drift")
    if list(summary.get("fully_evaluable_cancer_types", [])) != list(e["fully_evaluable_cancers"]):
        raise ValueError("P0 fully-evaluable cancer set drift")
    if summary.get("pan_cancer_promotion_possible_under_p0") is not False:
        raise ValueError("P0 pan-cancer promotion must remain unavailable")
    sample = pd.read_csv(sample_path, dtype=str)
    counts = pd.read_csv(counts_path, dtype=str)
    expected_records = int(e.get("records", 9460))
    if len(sample) != expected_records:
        raise ValueError(f"P0 sample eligibility row count drift: {len(sample)} != {expected_records}")
    required = {"cancer_type", "participant_root", "methylation_sample_root", "partition", "eligible_primary_95pct"}
    if not required.issubset(sample.columns):
        raise ValueError("P0 sample eligibility schema drift")
    return sample, counts


def discovery_rows(sample: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    cancers = list(cfg["p0_eligibility"]["fully_evaluable_cancers"])
    x = sample[
        sample["cancer_type"].isin(cancers)
        & (sample["partition"] == "DISCOVERY")
        & (sample["eligible_primary_95pct"].str.lower() == "true")
    ].copy()
    x["participant_root"] = x["participant_root"].map(normalize_barcode)
    x["methylation_sample_root"] = x["methylation_sample_root"].map(normalize_barcode)
    expected_counts = cfg["p0_eligibility"]["eligible_discovery_counts"]
    actual_counts = x.groupby("cancer_type").size().to_dict()
    if actual_counts != {k: int(v) for k, v in expected_counts.items()}:
        raise ValueError(f"eligible discovery counts drift: {actual_counts} != {expected_counts}")
    if len(x) != int(cfg["p0_eligibility"]["eligible_discovery_total"]):
        raise ValueError("eligible discovery total drift")
    if x["participant_root"].duplicated().any() or x["methylation_sample_root"].duplicated().any():
        raise ValueError("discovery identity uniqueness firewall failed")
    return x


def read_source_header(source: Path, cfg: dict) -> tuple[list[str], dict[str, list[int]]]:
    src = cfg["methylation_source"]
    if source.stat().st_size != int(src["size_bytes"]):
        raise ValueError(f"methylation source size mismatch: {source.stat().st_size} != {src['size_bytes']}")
    actual_sha = sha256_file(source)
    if actual_sha != src["sha256"]:
        raise ValueError(f"methylation source SHA mismatch: {actual_sha} != {src['sha256']}")
    with source.open("rb") as fh:
        raw = fh.readline()
    header = raw.decode("utf-8", errors="strict").rstrip("\r\n").split("\t")
    if len(header) != int(src["header_columns"]):
        raise ValueError(f"methylation header column drift: {len(header)} != {src['header_columns']}")
    roots: dict[str, list[int]] = defaultdict(list)
    for idx, label in enumerate(header[1:], start=1):
        root = sample_root(label)
        if root:
            roots[root].append(idx)
    return header, dict(roots)


def bind_discovery_columns(discovery: pd.DataFrame, root_to_indices: dict[str, list[int]], cfg: dict) -> tuple[list[int], dict[str, list[int]], dict[str, list[str]]]:
    source_to_row: dict[int, tuple[str, str]] = {}
    for r in discovery.itertuples(index=False):
        root = str(r.methylation_sample_root)
        indices = root_to_indices.get(root, [])
        if len(indices) != 1:
            raise ValueError(f"discovery methylation root {root} resolves to {len(indices)} source columns, expected exactly 1")
        idx = int(indices[0])
        if idx in source_to_row:
            raise ValueError(f"two discovery rows resolve to source column {idx}")
        source_to_row[idx] = (str(r.cancer_type), str(r.participant_root))
    ordered = sorted(source_to_row)
    positions_by_cancer: dict[str, list[int]] = defaultdict(list)
    participants_by_cancer: dict[str, list[str]] = defaultdict(list)
    for pos, src_idx in enumerate(ordered):
        cancer, participant = source_to_row[src_idx]
        positions_by_cancer[cancer].append(pos)
        participants_by_cancer[cancer].append(participant)
    for cancer, expected in cfg["p0_eligibility"]["eligible_discovery_counts"].items():
        if len(positions_by_cancer[cancer]) != int(expected):
            raise ValueError(f"{cancer}: bound discovery count drift")
    return ordered, dict(positions_by_cancer), dict(participants_by_cancer)


def _fit_pc1(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, str] | None:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[0] < 2 or X.shape[1] < 1 or not np.isfinite(X).all():
        return None
    means = X.mean(axis=0)
    Xc = X - means
    energy = float(np.sum(Xc * Xc))
    if not np.isfinite(energy) or energy <= 0.0:
        return None
    _u, s, vt = np.linalg.svd(Xc, full_matrices=False)
    if len(s) == 0 or not np.isfinite(s).all() or float(np.sum(s * s)) <= 0.0:
        return None
    loading = vt[0].astype(float, copy=True)
    scores = Xc @ loading
    module_mean = X.mean(axis=1)
    corr = float("nan")
    if np.std(scores) > 0 and np.std(module_mean) > 0:
        corr = float(np.corrcoef(scores, module_mean)[0, 1])
    if np.isfinite(corr) and corr != 0.0:
        if corr < 0:
            loading *= -1.0
            scores *= -1.0
        orient = "NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN"
    else:
        j = int(np.argmax(np.abs(loading)))
        if loading[j] < 0:
            loading *= -1.0
            scores *= -1.0
        orient = "LARGEST_ABSOLUTE_LOADING_POSITIVE_FALLBACK"
    explained = float((s[0] * s[0]) / np.sum(s * s))
    return means, loading, explained, orient


def run(config_path: Path, eligibility_summary_path: Path, sample_eligibility_path: Path, partition_counts_path: Path,
        source_path: Path, annotation_path: Path, chen_path: Path, hallmark_path: Path, out_dir: Path,
        chunksize: int = 64) -> dict:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    access = cfg["value_access"]
    if access.get("methylation_partitions_allowed") != ["DISCOVERY"]:
        raise ValueError("D1 may access methylation values for DISCOVERY only")
    for key in ("replication_methylation_values_allowed", "final_holdout_methylation_values_allowed",
                "rna_expression_values_allowed", "predictive_target_values_allowed",
                "biological_association_allowed", "biological_chi_allowed"):
        if access.get(key) is not False:
            raise ValueError(f"D1 freeze drift: {key} must be false")

    sample, _counts = validate_eligibility(eligibility_summary_path, sample_eligibility_path, partition_counts_path, cfg)
    disc = discovery_rows(sample, cfg)
    modules = parse_hallmarks(hallmark_path, cfg["hallmark_membership"]["sha256"], int(cfg["hallmark_membership"]["modules"]))
    annotation_ids, tss200_by_probe, common_snp_ids, tuple_mismatch_ids, chen = load_annotation(annotation_path, chen_path, cfg)
    _header, root_to_indices = read_source_header(source_path, cfg)
    source_indices, positions_by_cancer, participants_by_cancer = bind_discovery_columns(disc, root_to_indices, cfg)

    out_dir.mkdir(parents=True, exist_ok=True)
    probe_path = out_dir / "p0_d1_probe_eligibility.csv.gz"
    hall_path = out_dir / "p0_d1_hallmark_eligibility.csv"
    transform_path = out_dir / "p0_d1_methylation_pc1_transforms.csv.gz"
    score_path = out_dir / "p0_d1_methylation_discovery_scores.csv.gz"

    gene_vectors: dict[tuple[str, str], dict[str, list[tuple[str, np.ndarray]]]] = defaultdict(lambda: defaultdict(list))
    source_probe_ids: list[str] = []
    source_probe_seen: set[str] = set()
    c1a_counts = Counter()
    rows_seen = 0

    threshold = float(cfg["discovery_probe_rule"]["finite_fraction_min"])
    ordered_numeric_cols = source_indices
    dtype_map = {0: str}
    dtype_map.update({idx: np.float64 for idx in ordered_numeric_cols})

    with gzip.open(probe_path, "wt", encoding="utf-8", newline="") as pfh:
        fields = ["cancer_type", "probe_id", "discovery_n", "finite_n", "retained_primary_95pct",
                  "discovery_imputation_median", "technical_mask_union", "retained_masked_technical", "tss200_gene_count"]
        writer = csv.DictWriter(pfh, fieldnames=fields)
        writer.writeheader()
        reader = pd.read_csv(
            source_path, sep="\t", header=None, skiprows=1, usecols=[0] + ordered_numeric_cols,
            dtype=dtype_map, chunksize=chunksize, engine="c", keep_default_na=True,
            na_values=NA_VALUES, low_memory=False,
        )
        chunk_no = 0
        for chunk in reader:
            chunk_no += 1
            pids = [str(x).strip().strip('"') for x in chunk[0].tolist()]
            arr = chunk[ordered_numeric_cols].to_numpy(dtype=np.float64, copy=False)
            if arr.shape[1] != len(ordered_numeric_cols):
                raise ValueError("selected discovery matrix column drift")
            for pid in pids:
                if not pid or pid in source_probe_seen:
                    raise ValueError(f"blank or duplicate methylation probe ID {pid!r}")
                source_probe_seen.add(pid)
                source_probe_ids.append(pid)
                if pid in annotation_ids:
                    c1a_counts["annotation_overlap"] += 1
                if pid in tuple_mismatch_ids:
                    c1a_counts["tuple_mismatch"] += 1
                if pid in tss200_by_probe:
                    c1a_counts["tss200"] += 1
                if pid in common_snp_ids:
                    c1a_counts["common_snp"] += 1
                if pid in chen:
                    c1a_counts["chen"] += 1
                if (pid in chen) or (pid in common_snp_ids):
                    c1a_counts["mask_union"] += 1
            for cancer in cfg["p0_eligibility"]["fully_evaluable_cancers"]:
                pos = positions_by_cancer[cancer]
                sub = arr[:, pos]
                n = sub.shape[1]
                min_finite = int(math.ceil(threshold * n))
                finite_n = np.isfinite(sub).sum(axis=1, dtype=np.int64)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    medians = np.nanmedian(sub, axis=1)
                for i, pid in enumerate(pids):
                    genes = tss200_by_probe.get(pid, tuple())
                    masked = bool(pid in chen or pid in common_snp_ids)
                    retained = bool(finite_n[i] >= min_finite)
                    median = float(medians[i]) if retained else float("nan")
                    if retained and not np.isfinite(median):
                        raise ValueError(f"{cancer}/{pid}: retained probe has nonfinite discovery median")
                    writer.writerow({
                        "cancer_type": cancer,
                        "probe_id": pid,
                        "discovery_n": n,
                        "finite_n": int(finite_n[i]),
                        "retained_primary_95pct": str(retained).lower(),
                        "discovery_imputation_median": "" if not retained else format(median, ".17g"),
                        "technical_mask_union": str(masked).lower(),
                        "retained_masked_technical": str(bool(retained and not masked)).lower(),
                        "tss200_gene_count": len(genes),
                    })
                    if retained and genes:
                        vec = sub[i].astype(float, copy=True)
                        vec[~np.isfinite(vec)] = median
                        for gene in genes:
                            gene_vectors[(cancer, "PRIMARY_PUBLICATION")][gene].append((pid, vec))
                            if not masked:
                                gene_vectors[(cancer, "MASKED_TECHNICAL")][gene].append((pid, vec))
            rows_seen += len(pids)
            if chunk_no == 1 or chunk_no % 25 == 0:
                print(f"D1 methylation scan: {rows_seen:,}/{cfg['methylation_source']['probe_rows']:,} probe rows", flush=True)

    if rows_seen != int(cfg["methylation_source"]["probe_rows"]):
        raise ValueError(f"methylation probe-row count drift: {rows_seen} != {cfg['methylation_source']['probe_rows']}")
    if len(source_probe_seen) != rows_seen:
        raise ValueError("source probe uniqueness drift")
    expected_c1a = cfg["c1a_assets"]
    observed_c1a = {
        "annotation_overlap": c1a_counts["annotation_overlap"],
        "tss200": c1a_counts["tss200"],
        "chen": c1a_counts["chen"],
        "common_snp": c1a_counts["common_snp"],
        "mask_union": c1a_counts["mask_union"],
    }
    expected_cmp = {
        "annotation_overlap": int(expected_c1a["source_annotation_overlap"]),
        "tss200": int(expected_c1a["source_tss200_probe_count"]),
        "chen": int(expected_c1a["source_chen_overlap"]),
        "common_snp": int(expected_c1a["source_common_snp_overlap"]),
        "mask_union": int(expected_c1a["source_technical_mask_union"]),
    }
    if observed_c1a != expected_cmp:
        raise ValueError(f"C1A source-bound inventory drift: {observed_c1a} != {expected_cmp}")
    if c1a_counts["tuple_mismatch"] != 0:
        raise ValueError(f"source-bound annotation tuple mismatch count drift: {c1a_counts['tuple_mismatch']} != 0")

    hall_rows: list[dict[str, object]] = []
    transform_rows: list[dict[str, object]] = []
    score_rows: list[dict[str, object]] = []
    track_summary: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    min_genes = int(cfg["source_representation"]["minimum_mapped_genes_per_hallmark"])
    min_probes = int(cfg["source_representation"]["minimum_contributing_probes_per_hallmark"])

    for cancer in cfg["p0_eligibility"]["fully_evaluable_cancers"]:
        participants = participants_by_cancer[cancer]
        for track in cfg["technical_tracks"]:
            by_gene = gene_vectors[(cancer, track)]
            gene_scores: dict[str, np.ndarray] = {}
            gene_probe_ids: dict[str, set[str]] = {}
            for gene, entries in by_gene.items():
                unique: dict[str, np.ndarray] = {}
                for pid, vec in entries:
                    unique.setdefault(pid, vec)
                mat = np.vstack(list(unique.values()))
                gene_scores[gene] = np.median(mat, axis=0)
                gene_probe_ids[gene] = set(unique)
            mapping_eligible = 0
            pc1_evaluable = 0
            for hallmark, module_genes in modules.items():
                mapped = [g for g in module_genes if g in gene_scores]
                contributing = set()
                for gene in mapped:
                    contributing.update(gene_probe_ids[gene])
                by_rule = len(mapped) >= min_genes and len(contributing) >= min_probes
                pc1 = None
                status = "NOT_ELIGIBLE_MAPPING_RULE"
                if by_rule:
                    mapping_eligible += 1
                    X = np.column_stack([gene_scores[g] for g in mapped])
                    pc1 = _fit_pc1(X)
                    status = "PC1_EVALUABLE" if pc1 is not None else "NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE"
                if pc1 is not None:
                    pc1_evaluable += 1
                    means, loading, explained, orient = pc1
                    X = np.column_stack([gene_scores[g] for g in mapped])
                    scores = (X - means) @ loading
                    for g, mean, load in zip(mapped, means, loading):
                        transform_rows.append({
                            "cancer_type": cancer, "track": track, "hallmark": hallmark,
                            "gene_symbol": g, "discovery_gene_mean": format(float(mean), ".17g"),
                            "pc1_loading": format(float(load), ".17g"),
                            "explained_variance_fraction": format(explained, ".17g"),
                            "orientation_method": orient,
                        })
                    for participant, value in zip(participants, scores):
                        score_rows.append({
                            "cancer_type": cancer, "participant_root": participant, "track": track,
                            "hallmark": hallmark, "methylation_pc1": format(float(value), ".17g"),
                        })
                hall_rows.append({
                    "cancer_type": cancer, "track": track, "hallmark": hallmark,
                    "mapped_gene_count": len(mapped), "contributing_probe_count": len(contributing),
                    "eligible_by_frozen_mapping_rule": str(bool(by_rule)).lower(),
                    "pc1_status": status,
                })
            track_summary[cancer][track] = {
                "mapping_eligible_hallmarks": mapping_eligible,
                "pc1_evaluable_hallmarks": pc1_evaluable,
                "tss200_mapped_genes": len(gene_scores),
            }

    with hall_path.open("w", newline="", encoding="utf-8") as fh:
        fields = ["cancer_type", "track", "hallmark", "mapped_gene_count", "contributing_probe_count", "eligible_by_frozen_mapping_rule", "pc1_status"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(hall_rows)
    with gzip.open(transform_path, "wt", newline="", encoding="utf-8") as fh:
        fields = ["cancer_type", "track", "hallmark", "gene_symbol", "discovery_gene_mean", "pc1_loading", "explained_variance_fraction", "orientation_method"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(transform_rows)
    with gzip.open(score_path, "wt", newline="", encoding="utf-8") as fh:
        fields = ["cancer_type", "participant_root", "track", "hallmark", "methylation_pc1"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(score_rows)

    summary = {
        "schema": "gri-v2-p0-d1-discovery-source-result-v0.1",
        "status": "P0_D1_DISCOVERY_SOURCE_PREPROCESS_COMPLETE",
        "methylation_source_sha256": cfg["methylation_source"]["sha256"],
        "methylation_source_size_bytes": source_path.stat().st_size,
        "hallmark_membership_sha256": sha256_file(hallmark_path),
        "annotation_export_sha256": sha256_file(annotation_path),
        "chen_ids_sha256": sha256_file(chen_path),
        "sample_eligibility_sha256": sha256_file(sample_eligibility_path),
        "fully_evaluable_cancers": len(cfg["p0_eligibility"]["fully_evaluable_cancers"]),
        "fully_evaluable_cancer_types": list(cfg["p0_eligibility"]["fully_evaluable_cancers"]),
        "discovery_participants_processed": len(disc),
        "methylation_probe_rows_seen": rows_seen,
        "source_bound_c1a_counts": observed_c1a,
        "technical_tracks": list(cfg["technical_tracks"]),
        "track_hallmark_summary": track_summary,
        "probe_eligibility_sha256": sha256_file(probe_path),
        "hallmark_eligibility_sha256": sha256_file(hall_path),
        "methylation_pc1_transforms_sha256": sha256_file(transform_path),
        "methylation_discovery_scores_sha256": sha256_file(score_path),
        "methylation_values_read_partitions": ["DISCOVERY"],
        "replication_methylation_values_read": False,
        "final_holdout_methylation_values_read": False,
        "rna_expression_values_read": False,
        "predictive_target_values_read": False,
        "biological_association_performed": False,
        "biological_chi_used": False,
        "partition_reassignment_performed": False,
        "stage_c1_science_modified": False,
        "pan_cancer_promotion_possible_under_p0": False,
        "claim_ceiling": cfg["claim_ceiling"],
        "next_gate": "audit D1; then freeze/test RNA target construction and discovery audit/model implementation before any held-out target evaluation"
    }
    summary_path = out_dir / "P0_D1_DISCOVERY_SOURCE_PREPROCESS_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksum_path = out_dir / "SHA256SUMS.txt"
    artifacts = [summary_path, probe_path, hall_path, transform_path, score_path]
    checksum_path.write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in artifacts), encoding="ascii")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--eligibility-summary", type=Path, required=True)
    ap.add_argument("--sample-eligibility", type=Path, required=True)
    ap.add_argument("--partition-counts", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--annotation", type=Path, required=True)
    ap.add_argument("--chen", type=Path, required=True)
    ap.add_argument("--hallmarks", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=64)
    args = ap.parse_args()
    result = run(args.config, args.eligibility_summary, args.sample_eligibility, args.partition_counts,
                 args.source, args.annotation, args.chen, args.hallmarks, args.out, args.chunksize)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
