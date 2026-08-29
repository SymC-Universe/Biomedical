from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_network import compute_module_metrics_with_eigengenes

EXPECTED_CACHE_SHA256 = "e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63"
EXPECTED_MEMBERSHIP_SHA256 = "bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900"
GLOBAL_SEED = 20260829
FIXED_N = 30
RESAMPLES = 100
MIN_MODULE_GENES = 15

_CACHE = None
_MODULES = None


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def parse_gmt(path: Path) -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            parts = line.rstrip("\n\r").split("\t")
            if len(parts) >= 3:
                name = parts[0].strip()
                genes = [g.strip() for g in parts[2:] if g.strip()]
                if name and genes:
                    modules[name] = list(dict.fromkeys(genes))
    if len(modules) != 50 or any(not k.startswith("HALLMARK_") for k in modules):
        raise ValueError(f"Expected exactly 50 HALLMARK_ modules; found {len(modules)}")
    return modules


def _init_worker(cache_path: str, membership_path: str) -> None:
    global _CACHE, _MODULES
    _CACHE = np.load(cache_path, allow_pickle=True)
    _MODULES = parse_gmt(Path(membership_path))


def _one_cancer(cancer: str, seed: int) -> tuple[str, list[dict]]:
    assert _CACHE is not None and _MODULES is not None
    cancer_types = _CACHE["cancer_types"].astype(str)
    genes = _CACHE["gene_symbols"].astype(str)
    xall = _CACHE["expression_log2p1"]
    idx = np.flatnonzero(cancer_types == str(cancer))
    if len(idx) < FIXED_N:
        raise ValueError(f"{cancer}: only {len(idx)} samples, below fixed n={FIXED_N}")
    x = xall[idx]
    rng = np.random.default_rng(int(seed))
    rows: list[dict] = []
    for rep in range(RESAMPLES):
        sub = rng.choice(len(idx), size=FIXED_N, replace=False)
        metrics, _ = compute_module_metrics_with_eigengenes(
            x[sub], genes, _MODULES,
            minimum_mapped_genes=MIN_MODULE_GENES,
            minimum_gene_finite_fraction=0.95,
            minimum_gene_finite_samples=20,
            minimum_pairwise_overlap_fraction=0.80,
            minimum_pairwise_overlap_samples=20,
        )
        for m in metrics:
            rows.append({
                "cancer_type": cancer,
                "resample": rep,
                "module": m.module,
                "n_genes": m.n_genes,
                "cin_pairwise_median_abs": m.cin_pairwise_median_abs,
                "cin_pc1_variance_fraction": m.cin_pc1_variance_fraction,
                "cout_eigengene_median_abs": m.cout_eigengene_median_abs,
                "pc1_imputed_fraction": m.pc1_imputed_fraction,
            })
    return cancer, rows


def _q05(s: pd.Series) -> float:
    return float(s.quantile(0.05))


def _q95(s: pd.Series) -> float:
    return float(s.quantile(0.95))


def run(cache_path: Path, membership_path: Path, out_dir: Path, workers: int) -> dict:
    cache_path = cache_path.resolve()
    membership_path = membership_path.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    cache_sha = sha256_file(cache_path)
    membership_sha = sha256_file(membership_path)
    if cache_sha != EXPECTED_CACHE_SHA256:
        raise ValueError("Cache SHA-256 does not match the completed Stage A1 handoff")
    if membership_sha != EXPECTED_MEMBERSHIP_SHA256:
        raise ValueError("Hallmark membership snapshot SHA-256 does not match the completed Stage A1 handoff")

    modules = parse_gmt(membership_path)
    z = np.load(cache_path, allow_pickle=True)
    cancer_types = z["cancer_types"].astype(str)
    cancers = sorted(np.unique(cancer_types).tolist())
    counts = {c: int(np.sum(cancer_types == c)) for c in cancers}
    if len(cancers) != 32:
        raise ValueError(f"Expected 32 cancers in A1 cache; found {len(cancers)}")
    if min(counts.values()) < FIXED_N:
        raise ValueError("At least one cancer has fewer than the frozen fixed-n sample count")
    del z

    seed_rng = np.random.default_rng(GLOBAL_SEED)
    seeds = seed_rng.integers(0, 2**63 - 1, size=len(cancers), dtype=np.int64)
    cancer_seeds = {c: int(s) for c, s in zip(cancers, seeds)}

    all_rows: list[dict] = []
    use_workers = max(1, min(int(workers), len(cancers)))
    print(f"A1.1 fixed-n calibration: {len(cancers)} cancers x {RESAMPLES} resamples at n={FIXED_N}; workers={use_workers}", flush=True)
    with ProcessPoolExecutor(max_workers=use_workers, initializer=_init_worker, initargs=(str(cache_path), str(membership_path))) as ex:
        futs = {ex.submit(_one_cancer, c, cancer_seeds[c]): c for c in cancers}
        completed = 0
        for fut in as_completed(futs):
            c, rows = fut.result()
            all_rows.extend(rows)
            completed += 1
            print(f"completed {completed:02d}/{len(cancers)}: {c} ({len(rows):,} module-resample rows)", flush=True)

    raw = pd.DataFrame(all_rows).sort_values(["cancer_type", "module", "resample"], kind="mergesort")
    raw.to_csv(out_dir / "stage_a1_1_resample_metrics.csv.gz", index=False, compression="gzip")

    metrics = ["cin_pairwise_median_abs", "cin_pc1_variance_fraction", "cout_eigengene_median_abs"]
    agg_spec = {
        "valid_resamples": ("resample", "nunique"),
        "n_genes_median": ("n_genes", "median"),
        "pc1_imputed_fraction_median": ("pc1_imputed_fraction", "median"),
    }
    for field in metrics:
        agg_spec[field + "_median"] = (field, "median")
        agg_spec[field + "_q05"] = (field, _q05)
        agg_spec[field + "_q95"] = (field, _q95)
    cal = raw.groupby(["cancer_type", "module"], as_index=False).agg(**agg_spec)
    cal = cal.sort_values(["cancer_type", "module"], kind="mergesort")
    cal.to_csv(out_dir / "stage_a1_1_fixed_n_calibration.csv", index=False)

    cancer_n = pd.Series(counts, name="original_n").rename_axis("cancer_type").reset_index()
    metric_by_cancer = cal.groupby("cancer_type")[[m + "_median" for m in metrics]].median().reset_index()
    diag = cancer_n.merge(metric_by_cancer, on="cancer_type", how="left")
    diag.to_csv(out_dir / "stage_a1_1_cancer_level_diagnostic.csv", index=False)
    corrs = {}
    for field in [m + "_median" for m in metrics]:
        corrs[field] = float(diag[["original_n", field]].corr(method="spearman").iloc[0, 1])

    summary = {
        "status": "DEVELOPMENT_FIXED_N_CALIBRATION_ONLY",
        "cache_sha256": cache_sha,
        "membership_sha256": membership_sha,
        "global_seed": GLOBAL_SEED,
        "fixed_n": FIXED_N,
        "resamples_per_cancer": RESAMPLES,
        "cancers": len(cancers),
        "hallmark_modules": len(modules),
        "calibration_rows": int(len(cal)),
        "minimum_valid_resamples_per_cancer_module": int(cal["valid_resamples"].min()),
        "maximum_pc1_imputed_fraction_median": float(cal["pc1_imputed_fraction_median"].max()),
        "original_n_spearman_after_fixed_n": corrs,
        "chi_present": False,
        "cv2_used": False,
        "composite_score_present": False,
        "claim_ceiling": "sample-size-calibrated static network map only",
    }
    (out_dir / "STAGE_A1_1_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cache", type=Path)
    ap.add_argument("membership", type=Path)
    ap.add_argument("--out", type=Path, default=Path("stage_a1_1_outputs"))
    ap.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2) - 1)))
    args = ap.parse_args()
    run(args.cache, args.membership, args.out, args.workers)


if __name__ == "__main__":
    main()
