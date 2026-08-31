from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

CHUNK_BYTES = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK_BYTES), b""):
            h.update(block)
    return h.hexdigest()


def parse_gmt(path: Path, expected_modules: int) -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    with path.open("r", encoding="utf-8", errors="strict") as fh:
        for line in fh:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) < 3:
                continue
            name = parts[0].strip()
            genes = [g.strip() for g in parts[2:] if g.strip()]
            if name:
                if name in modules:
                    raise ValueError(f"duplicate Hallmark name in GMT: {name}")
                modules[name] = list(dict.fromkeys(genes))
    if len(modules) != int(expected_modules):
        raise ValueError(f"expected {expected_modules} Hallmark modules; found {len(modules)}")
    if any(not name.startswith("HALLMARK_") for name in modules):
        raise ValueError("non-HALLMARK module found in frozen membership snapshot")
    return modules


def load_discovery_identity(scores_path: Path, cfg: dict) -> pd.DataFrame:
    if sha256_file(scores_path) != cfg["d1_methylation_discovery_scores_sha256"]:
        raise ValueError("D1 discovery score SHA-256 mismatch")
    usecols = ["cancer_type", "participant_root", "track", "hallmark"]
    scores = pd.read_csv(scores_path, compression="gzip", usecols=usecols, dtype=str)
    cancers = sorted(scores["cancer_type"].unique().tolist())
    if cancers != sorted(cfg["fully_evaluable_cancers"]):
        raise ValueError("D1 discovery score cancer set drift")
    participants = scores[["cancer_type", "participant_root"]].drop_duplicates()
    if len(participants) != int(cfg["discovery_participants"]):
        raise ValueError(f"D1 discovery participant count drift: {len(participants)}")
    counts = participants.groupby("cancer_type").size().to_dict()
    if counts != {k: int(v) for k, v in cfg["expected_discovery_n_by_cancer"].items()}:
        raise ValueError(f"D1 discovery participant counts drift: {counts}")
    per_group = scores.groupby(["cancer_type", "track"])["participant_root"].nunique()
    for (cancer, _track), n in per_group.items():
        if int(n) != int(cfg["expected_discovery_n_by_cancer"][cancer]):
            raise ValueError(f"track-specific participant drift for {cancer}")
    return participants.sort_values(["cancer_type", "participant_root"], kind="mergesort").reset_index(drop=True)


def load_d1_hallmark_eligibility(path: Path, cfg: dict) -> pd.DataFrame:
    if sha256_file(path) != cfg["d1_hallmark_eligibility_sha256"]:
        raise ValueError("D1 Hallmark eligibility SHA-256 mismatch")
    df = pd.read_csv(path, dtype={"cancer_type": str, "track": str, "hallmark": str})
    required = {
        "cancer_type", "track", "hallmark", "mapped_gene_count",
        "contributing_probe_count", "eligible_by_frozen_mapping_rule", "pc1_status"
    }
    if not required.issubset(df.columns):
        raise ValueError("D1 Hallmark eligibility schema drift")
    if df.duplicated(["cancer_type", "track", "hallmark"]).any():
        raise ValueError("duplicate D1 Hallmark eligibility row")
    expected_rows = len(cfg["fully_evaluable_cancers"]) * 2 * int(cfg["expected_hallmark_modules"])
    if len(df) != expected_rows:
        raise ValueError(f"D1 Hallmark eligibility row-count drift: {len(df)} != {expected_rows}")
    eligible = df["eligible_by_frozen_mapping_rule"].astype(bool)
    counts = eligible.groupby([df["cancer_type"], df["track"]]).sum()
    if not np.all(counts.to_numpy() == int(cfg["expected_d1_source_eligible_hallmarks_per_track"])):
        raise ValueError("D1 source-eligible Hallmark count drift")
    return df


def orient_pc1(scores: np.ndarray, loadings: np.ndarray, uncentered: np.ndarray) -> tuple[np.ndarray, np.ndarray, str]:
    module_mean = np.mean(uncentered, axis=1)
    if np.std(scores) > 0 and np.std(module_mean) > 0:
        corr = float(np.corrcoef(scores, module_mean)[0, 1])
    else:
        corr = float("nan")
    if np.isfinite(corr) and corr != 0.0:
        if corr < 0:
            return -scores, -loadings, "NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN"
        return scores, loadings, "NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN"
    j = int(np.argmax(np.abs(loadings)))
    if loadings[j] < 0:
        return -scores, -loadings, "LARGEST_ABSOLUTE_LOADING_POSITIVE_FALLBACK"
    return scores, loadings, "LARGEST_ABSOLUTE_LOADING_POSITIVE_FALLBACK"


def run(
    config_path: Path,
    cache_path: Path,
    gmt_path: Path,
    d1_scores_path: Path,
    d1_hallmark_path: Path,
    out_dir: Path,
) -> dict:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if cfg.get("heldout_target_scores_allowed") is not False:
        raise ValueError("D2 may not generate held-out target scores")
    if cfg.get("partition_reassignment_allowed") is not False:
        raise ValueError("D2 may not reassign partitions")
    if cfg.get("biological_chi_allowed") is not False:
        raise ValueError("D2 may not use biological chi")
    if cfg.get("stage_c1_modification_allowed") is not False:
        raise ValueError("D2 may not modify Stage C1")

    cache_sha = sha256_file(cache_path)
    gmt_sha = sha256_file(gmt_path)
    if cache_sha != cfg["stage_a_profile_cache_sha256"]:
        raise ValueError(f"Stage A profile cache SHA-256 mismatch: {cache_sha}")
    if gmt_sha != cfg["hallmark_membership_sha256"]:
        raise ValueError(f"Hallmark membership SHA-256 mismatch: {gmt_sha}")

    modules = parse_gmt(gmt_path, int(cfg["expected_hallmark_modules"]))
    participants = load_discovery_identity(d1_scores_path, cfg)
    d1_hall = load_d1_hallmark_eligibility(d1_hallmark_path, cfg)

    z = np.load(cache_path, allow_pickle=True)
    required_arrays = {"sample_ids", "patient_ids", "cancer_types", "gene_symbols", "expression_log2p1"}
    if not required_arrays.issubset(set(z.files)):
        raise ValueError(f"Stage A cache missing required arrays: {sorted(required_arrays.difference(z.files))}")
    patient_ids = z["patient_ids"].astype(str)
    cancer_types = z["cancer_types"].astype(str)
    gene_symbols = z["gene_symbols"].astype(str)
    expression_all = z["expression_log2p1"]
    if expression_all.ndim != 2 or expression_all.shape[0] != len(patient_ids) or expression_all.shape[1] != len(gene_symbols):
        raise ValueError("Stage A cache expression shape mismatch")
    if len(set(gene_symbols.tolist())) != len(gene_symbols):
        raise ValueError("Stage A cache gene symbols are not unique")

    cache_key_to_index: dict[tuple[str, str], int] = {}
    for i, (cancer, patient) in enumerate(zip(cancer_types, patient_ids)):
        key = (str(cancer), str(patient))
        if key in cache_key_to_index:
            raise ValueError(f"duplicate cancer/participant in Stage A cache: {key}")
        cache_key_to_index[key] = i

    selected_indices: list[int] = []
    for row in participants.itertuples(index=False):
        key = (str(row.cancer_type), str(row.participant_root))
        if key not in cache_key_to_index:
            raise ValueError(f"D1 DISCOVERY participant missing from Stage A cache: {key}")
        selected_indices.append(cache_key_to_index[key])
    if len(set(selected_indices)) != len(selected_indices):
        raise ValueError("D2 selected duplicate Stage A rows")

    # Only these frozen DISCOVERY rows are selected into D2 computation.
    discovery_expression = np.asarray(expression_all[np.asarray(selected_indices, dtype=int), :], dtype=float)
    del expression_all
    z.close()

    gene_index = {g: i for i, g in enumerate(gene_symbols)}
    participant_pos = participants.copy()
    participant_pos["_row"] = np.arange(len(participant_pos), dtype=int)

    finite_fraction_min = float(cfg["rna_gene_finite_fraction_min"])
    finite_samples_min = int(cfg["rna_gene_finite_samples_min"])
    hallmark_genes_min = int(cfg["rna_hallmark_retained_genes_min"])

    eligibility_rows: list[dict[str, object]] = []
    transform_rows: list[dict[str, object]] = []
    score_rows: list[dict[str, object]] = []

    for cancer in cfg["fully_evaluable_cancers"]:
        crows = participant_pos[participant_pos["cancer_type"] == cancer]
        row_idx = crows["_row"].to_numpy(dtype=int)
        cparticipants = crows["participant_root"].astype(str).to_numpy()
        x_cancer = discovery_expression[row_idx, :]
        n_discovery = len(row_idx)
        if n_discovery != int(cfg["expected_discovery_n_by_cancer"][cancer]):
            raise ValueError(f"D2 discovery n drift for {cancer}")

        for hallmark in sorted(modules):
            cache_genes = [g for g in modules[hallmark] if g in gene_index]
            retained_genes: list[str] = []
            retained_cols: list[int] = []
            retained_means: list[float] = []
            for gene in cache_genes:
                j = gene_index[gene]
                vals = x_cancer[:, j]
                finite = np.isfinite(vals)
                finite_n = int(finite.sum())
                if finite_n < finite_samples_min or finite_n / n_discovery < finite_fraction_min:
                    continue
                finite_vals = vals[finite]
                if finite_vals.size < 2 or not np.isfinite(finite_vals).all():
                    continue
                if float(np.var(finite_vals, ddof=0)) <= 0.0:
                    continue
                retained_genes.append(gene)
                retained_cols.append(j)
                retained_means.append(float(np.mean(finite_vals)))

            mapping_eligible = len(retained_genes) >= hallmark_genes_min
            status = "NOT_ELIGIBLE_MAPPING_RULE"
            explained = float("nan")
            orientation = "NOT_EVALUABLE"

            if mapping_eligible:
                raw = x_cancer[:, retained_cols].astype(float, copy=True)
                means = np.asarray(retained_means, dtype=float)
                bad = ~np.isfinite(raw)
                if bad.any():
                    raw[bad] = np.broadcast_to(means, raw.shape)[bad]
                centered = raw - means[None, :]
                if not np.isfinite(centered).all() or float(np.sum(centered * centered)) <= 0.0:
                    status = "NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE"
                else:
                    _u, s, vt = np.linalg.svd(centered, full_matrices=False)
                    total_ss = float(np.sum(s * s))
                    if len(s) == 0 or not np.isfinite(s[0]) or s[0] <= 0 or not np.isfinite(total_ss) or total_ss <= 0:
                        status = "NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE"
                    else:
                        loadings = vt[0].astype(float, copy=True)
                        pc1 = centered @ loadings
                        if not np.isfinite(pc1).all() or float(np.var(pc1, ddof=0)) <= 0:
                            status = "NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE"
                        else:
                            pc1, loadings, orientation = orient_pc1(pc1, loadings, raw)
                            explained = float((s[0] * s[0]) / total_ss)
                            status = "PC1_EVALUABLE"
                            for gene, mean, loading in zip(retained_genes, means, loadings):
                                transform_rows.append({
                                    "cancer_type": cancer,
                                    "hallmark": hallmark,
                                    "gene_symbol": gene,
                                    "discovery_gene_mean": float(mean),
                                    "pc1_loading": float(loading),
                                    "explained_variance_fraction": explained,
                                    "orientation_method": orientation,
                                })
                            for participant, value in zip(cparticipants, pc1):
                                score_rows.append({
                                    "cancer_type": cancer,
                                    "participant_root": participant,
                                    "hallmark": hallmark,
                                    "rna_pc1": float(value),
                                })

            eligibility_rows.append({
                "cancer_type": cancer,
                "hallmark": hallmark,
                "cache_mapped_gene_count": len(cache_genes),
                "retained_discovery_gene_count": len(retained_genes),
                "eligible_by_frozen_mapping_rule": bool(mapping_eligible),
                "pc1_status": status,
            })

    out_dir.mkdir(parents=True, exist_ok=True)
    eligibility = pd.DataFrame(eligibility_rows).sort_values(["cancer_type", "hallmark"], kind="mergesort")
    transforms = pd.DataFrame(transform_rows).sort_values(["cancer_type", "hallmark", "gene_symbol"], kind="mergesort")
    scores_out = pd.DataFrame(score_rows).sort_values(["cancer_type", "hallmark", "participant_root"], kind="mergesort")

    eligibility_path = out_dir / "RNA_Target_Eligibility.csv"
    transforms_path = out_dir / "RNA_Target_Transforms.csv.gz"
    scores_path = out_dir / "RNA_Discovery_Scores.csv.gz"
    eligibility.to_csv(eligibility_path, index=False)
    transforms.to_csv(transforms_path, index=False, compression="gzip")
    scores_out.to_csv(scores_path, index=False, compression="gzip")

    d1_small = d1_hall[["cancer_type", "track", "hallmark", "eligible_by_frozen_mapping_rule"]].copy()
    d1_small = d1_small.rename(columns={"eligible_by_frozen_mapping_rule": "d1_source_mapping_eligible"})
    common = d1_small.merge(
        eligibility[["cancer_type", "hallmark", "eligible_by_frozen_mapping_rule", "pc1_status"]],
        on=["cancer_type", "hallmark"], how="left", validate="many_to_one"
    ).rename(columns={"eligible_by_frozen_mapping_rule": "rna_mapping_eligible", "pc1_status": "rna_pc1_status"})
    common["common_eligible"] = (
        common["d1_source_mapping_eligible"].astype(bool)
        & common["rna_mapping_eligible"].astype(bool)
        & common["rna_pc1_status"].eq("PC1_EVALUABLE")
    )
    common = common.sort_values(["cancer_type", "track", "hallmark"], kind="mergesort")
    common_path = out_dir / "Common_Hallmarks.csv"
    common.to_csv(common_path, index=False)

    common_counts = common.groupby(["cancer_type", "track"])["common_eligible"].sum().astype(int)
    semantic_floor = int(cfg["minimum_common_hallmarks_for_semantic_branch"])
    common_summary: dict[str, dict[str, dict[str, object]]] = {}
    for (cancer, track), n in common_counts.items():
        common_summary.setdefault(cancer, {})[track] = {
            "common_eligible_hallmarks": int(n),
            "semantic_branch_evaluable": bool(int(n) >= semantic_floor),
        }

    status_counts = eligibility.groupby("cancer_type")["pc1_status"].value_counts().unstack(fill_value=0)
    status_summary = {
        cancer: {str(k): int(v) for k, v in row.items() if int(v) != 0}
        for cancer, row in status_counts.iterrows()
    }

    outputs = [eligibility_path, transforms_path, scores_path, common_path]
    output_hashes = {p.name: sha256_file(p) for p in outputs}
    result = {
        "schema": "gri-v2-p0-d2-rna-discovery-target-result-v0.1",
        "status": "P0_D2_RNA_DISCOVERY_TARGET_COMPLETE",
        "claim_ceiling": "DISCOVERY-only RNA target construction; no predictive, held-out, biological chi, clinical, causal, temporal, or pan-cancer promotion claim",
        "stage_a_profile_cache_sha256": cache_sha,
        "hallmark_membership_sha256": gmt_sha,
        "d1_methylation_discovery_scores_sha256": sha256_file(d1_scores_path),
        "d1_hallmark_eligibility_sha256": sha256_file(d1_hallmark_path),
        "discovery_participants_processed": int(len(participants)),
        "fully_evaluable_cancers": int(len(cfg["fully_evaluable_cancers"])),
        "rna_values_used_partitions": ["DISCOVERY"],
        "replication_target_scores_generated": False,
        "final_holdout_target_scores_generated": False,
        "heldout_values_used_for_fit_or_decision": False,
        "partition_reassignment_performed": False,
        "biological_chi_used": False,
        "stage_c1_science_modified": False,
        "rna_gene_finite_fraction_min": finite_fraction_min,
        "rna_gene_finite_samples_min": finite_samples_min,
        "rna_hallmark_retained_genes_min": hallmark_genes_min,
        "minimum_common_hallmarks_for_semantic_branch": semantic_floor,
        "target_pc1_status_by_cancer": status_summary,
        "common_hallmark_summary": common_summary,
        "output_sha256": output_hashes,
        "next_gate": "audit D2; then implement/freeze discovery audit-state machinery and P1 discovery model fitting before any held-out target score generation",
    }
    summary_path = out_dir / "RUN_SUMMARY.json"
    summary_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_hashes[summary_path.name] = sha256_file(summary_path)
    sums_path = out_dir / "SHA256SUMS.txt"
    sums_path.write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(output_hashes.items())), encoding="utf-8")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--gmt", type=Path, required=True)
    ap.add_argument("--d1-scores", type=Path, required=True)
    ap.add_argument("--d1-hallmarks", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = run(args.config, args.cache, args.gmt, args.d1_scores, args.d1_hallmarks, args.out)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
