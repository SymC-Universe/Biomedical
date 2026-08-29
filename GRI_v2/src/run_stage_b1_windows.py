from __future__ import annotations

import argparse, gzip, json, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd
import numpy as np

from src.run_stage_b1 import G, _init_worker, _task, _model_covariates, sha256_file, summarize


def work(item):
    idx, model, cancer, task_dir = item
    result = _task(model, cancer)
    p = Path(task_dir) / f"{idx:03d}_{model}_{cancer}.csv.gz"
    pd.DataFrame(result["rows"]).to_csv(p, index=False, compression="gzip")
    return {
        "task_index": idx, "model_id": model, "cancer_type": cancer,
        "eligible_n": result["eligible_n"], "valid_resamples": result["valid_resamples"],
        "rows": len(result["rows"]), "path": str(p),
    }


def combine(files, dest):
    first = True
    with gzip.open(dest, "wt", newline="") as out:
        for p in files:
            with gzip.open(p, "rt") as src:
                header = src.readline()
                if first:
                    out.write(header)
                    first = False
                shutil.copyfileobj(src, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True); ap.add_argument("--gmt", required=True)
    ap.add_argument("--purity", required=True); ap.add_argument("--leukocyte", required=True)
    ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text())
    checks = {
        "stage_a_profile_cache_sha256": sha256_file(args.cache),
        "absolute_purity_sha256": sha256_file(args.purity),
        "leukocyte_fraction_sha256": sha256_file(args.leukocyte),
        "hallmark_membership_sha256": sha256_file(args.gmt),
    }
    for key, actual in checks.items():
        if actual != plan["inputs"][key]:
            raise ValueError(f"SHA mismatch for {key}: {actual}")

    _init_worker(args.cache, args.gmt, args.purity, args.leukocyte, args.plan)
    cancers = sorted(set(G["cancer_types"]))
    tasks = []
    for model in [m["id"] for m in plan["models"]]:
        covs = _model_covariates(model)
        for cancer in cancers:
            mask = G["context"].cancer_type.to_numpy() == cancer
            for cov in covs:
                mask &= np.isfinite(G["context"][cov].to_numpy(float))
            if mask.sum() >= plan["fixed_n_design"]["n"]:
                tasks.append((model, cancer))

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    task_dir = out / "_task_cache"; task_dir.mkdir(exist_ok=True)
    items = [(i, model, cancer, str(task_dir)) for i, (model, cancer) in enumerate(tasks)]
    metas = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        for meta in ex.map(work, items):
            metas.append(meta)
            print(f"completed {meta['model_id']} {meta['cancer_type']} ({meta['valid_resamples']}/100)", flush=True)

    expected_reps = int(plan["fixed_n_design"]["resamples_per_cancer_model"])
    if any(m["valid_resamples"] != expected_reps for m in metas):
        raise RuntimeError("At least one cancer/model did not produce all frozen resamples")

    files = [m["path"] for m in sorted(metas, key=lambda z: z["task_index"])]
    raw = out / "stage_b1_resample_metrics.csv.gz"
    combine(files, raw)
    df, module, cancer = summarize(raw, out)
    summary = {
        "status": "DEVELOPMENT_COMPOSITION_ADJUSTED_STATIC_MAP_ONLY",
        "claim_ceiling": plan["claim_ceiling"],
        "chi_present": False, "cv2_used": False, "composite_score_present": False,
        "fixed_n": plan["fixed_n_design"]["n"],
        "resamples_per_cancer_model": expected_reps,
        "models": sorted({m["model_id"] for m in metas}),
        "cancer_model_tasks": len(metas),
        "tasks_by_model": pd.Series([m["model_id"] for m in metas]).value_counts().sort_index().astype(int).to_dict(),
        "minimum_valid_resamples": min(m["valid_resamples"] for m in metas),
        "raw_resample_rows": sum(m["rows"] for m in metas),
        "module_summary_rows": len(module), "cancer_summary_rows": len(cancer),
        "source_sha256": checks,
    }
    (out / "STAGE_B1_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    for p in files:
        Path(p).unlink(missing_ok=True)
    task_dir.rmdir()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
