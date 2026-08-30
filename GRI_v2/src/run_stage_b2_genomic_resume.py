from __future__ import annotations

import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from src.run_stage_b2_genomic import G, METRICS, _init_worker, _task, sha256_file, spearman


def q05(s): return s.quantile(0.05)
def q95(s): return s.quantile(0.95)
q05.__name__ = "p05"; q95.__name__ = "p95"


def task_slug(index: int, mode: str, coord: str, cancer: str) -> str:
    return f"{index:04d}__{mode}__{coord}__{cancer}"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def summarize_task(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    if df.empty:
        raise ValueError("cannot summarize empty B2 genomic task")
    key_cols = ["analysis_mode", "coordinate_id", "cancer_type"]
    if any(df[c].nunique(dropna=False) != 1 for c in key_cols):
        raise ValueError("task dataframe must contain one mode/coordinate/cancer")
    value_cols = [c for c in df.columns if any(c.startswith(p) for p in ["reference__", "actual__", "null__", "actual_delta__", "null_delta__", "specific_delta__"])]
    agg = df.groupby("module", sort=True)[value_cols].agg(["median", q05, q95])
    agg.columns = [f"{a}__{b}" for a, b in agg.columns]
    module = agg.reset_index()
    mode = str(df.analysis_mode.iloc[0]); coord = str(df.coordinate_id.iloc[0]); cancer = str(df.cancer_type.iloc[0])
    module.insert(0, "cancer_type", cancer); module.insert(0, "coordinate_id", coord); module.insert(0, "analysis_mode", mode)
    row = {
        "analysis_mode": mode, "coordinate_id": coord, "cancer_type": cancer,
        "module_count": int(len(module)), "eligible_n": int(df.eligible_n.iloc[0]),
        "valid_resamples": int(df["resample"].nunique()),
    }
    for metric in METRICS:
        ref = module[f"reference__{metric}__median"]
        actual = module[f"actual__{metric}__median"]
        row[f"reference_vs_actual_module_rank_rho__{metric}"] = spearman(ref, actual)
        row[f"median_actual_delta__{metric}"] = float(module[f"actual_delta__{metric}__median"].median())
        row[f"median_null_delta__{metric}"] = float(module[f"null_delta__{metric}__median"].median())
        row[f"median_specific_delta__{metric}"] = float(module[f"specific_delta__{metric}__median"].median())
        row[f"median_abs_specific_delta__{metric}"] = float(module[f"specific_delta__{metric}__median"].abs().median())
    row["reference_cin_vs_cout_rho"] = spearman(module["reference__cin_pairwise_median_abs__median"], module["reference__cout_eigengene_median_abs__median"])
    row["actual_cin_vs_cout_rho"] = spearman(module["actual__cin_pairwise_median_abs__median"], module["actual__cout_eigengene_median_abs__median"])
    return module, row


def task_paths(task_dir: Path, slug: str) -> dict[str, Path]:
    return {
        "raw": task_dir / f"{slug}.csv.gz",
        "module": task_dir / f"{slug}.module.csv",
        "diagnostic": task_dir / f"{slug}.diagnostic.json",
        "meta": task_dir / f"{slug}.meta.json",
    }


def task_complete(task_dir: Path, item: tuple[int, str, str, str], reps: int) -> bool:
    index, mode, coord, cancer = item
    p = task_paths(task_dir, task_slug(index, mode, coord, cancer))
    if not all(x.exists() and x.stat().st_size > 0 for x in p.values()): return False
    try:
        meta = json.loads(p["meta"].read_text())
        if meta.get("task_index") != index or meta.get("analysis_mode") != mode or meta.get("coordinate_id") != coord or meta.get("cancer_type") != cancer: return False
        if int(meta.get("valid_resamples", -1)) != reps or int(meta.get("rows", -1)) != reps * 50: return False
        if meta.get("raw_sha256") != file_sha256(p["raw"]): return False
        if meta.get("module_sha256") != file_sha256(p["module"]): return False
        if meta.get("diagnostic_sha256") != file_sha256(p["diagnostic"]): return False
        module = pd.read_csv(p["module"])
        if len(module) != 50 or module.module.nunique() != 50: return False
    except Exception:
        return False
    return True


def atomic_write(final_path: Path, writer) -> None:
    tmp = final_path.with_name(final_path.name + ".tmp")
    if tmp.exists(): tmp.unlink()
    writer(tmp)
    os.replace(tmp, final_path)


def execute_task(task_dir: Path, item: tuple[int, str, str, str], reps: int) -> dict:
    index, mode, coord, cancer = item
    result = _task(mode, coord, cancer)
    if int(result["valid_resamples"]) != reps:
        raise RuntimeError(f"{mode} {coord} {cancer} produced {result['valid_resamples']}/{reps} valid resamples")
    df = pd.DataFrame(result["rows"])
    if len(df) != reps * 50 or df.module.nunique() != 50 or df["resample"].nunique() != reps:
        raise RuntimeError(f"{mode} {coord} {cancer} produced an incomplete task table")
    module, diagnostic = summarize_task(df)
    p = task_paths(task_dir, task_slug(index, mode, coord, cancer))
    atomic_write(p["raw"], lambda tmp: df.to_csv(tmp, index=False, compression={"method": "gzip", "compresslevel": 1}))
    atomic_write(p["module"], lambda tmp: module.to_csv(tmp, index=False))
    atomic_write(p["diagnostic"], lambda tmp: tmp.write_text(json.dumps(diagnostic, indent=2, sort_keys=True) + "\n"))
    meta = {
        "task_index": index, "analysis_mode": mode, "coordinate_id": coord, "cancer_type": cancer,
        "eligible_n": int(result["eligible_n"]), "valid_resamples": reps, "rows": int(len(df)),
        "raw_sha256": file_sha256(p["raw"]), "module_sha256": file_sha256(p["module"]),
        "diagnostic_sha256": file_sha256(p["diagnostic"]),
    }
    tmp = p["meta"].with_name(p["meta"].name + ".tmp")
    tmp.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n"); os.replace(tmp, p["meta"])
    return meta


def build_tasks(plan: dict, modes: list[str], coords: list[str], cancers: list[str]) -> list[tuple[int, str, str, str]]:
    tasks = []; minimum_n = int(plan["matching"]["minimum_cancer_n"])
    for mode in modes:
        for coord in coords:
            col = G["coord_map"][coord]
            for cancer in cancers:
                mask = (G["context"].cancer_type.to_numpy() == cancer) & np.isfinite(G["context"][col].to_numpy(float))
                if mode == "INCREMENT_B1": mask &= np.isfinite(G["context"].purity.to_numpy(float)) & np.isfinite(G["context"].leukocyte_fraction.to_numpy(float))
                if int(mask.sum()) >= minimum_n: tasks.append((len(tasks), mode, coord, cancer))
    return tasks


def finalize(out: Path, task_dir: Path, tasks: list[tuple[int, str, str, str]], plan: dict, checks: dict, reps: int) -> dict:
    modules = []; diagnostics = []; status = []
    for item in tasks:
        index, mode, coord, cancer = item
        p = task_paths(task_dir, task_slug(index, mode, coord, cancer))
        status.append(json.loads(p["meta"].read_text()))
        modules.append(pd.read_csv(p["module"]))
        diagnostics.append(json.loads(p["diagnostic"].read_text()))
    module_df = pd.concat(modules, ignore_index=True).sort_values(["analysis_mode", "coordinate_id", "cancer_type", "module"])
    diagnostic_df = pd.DataFrame(diagnostics).sort_values(["analysis_mode", "coordinate_id", "cancer_type"])
    status_df = pd.DataFrame(status).sort_values("task_index")
    module_df.to_csv(out / "stage_b2_genomic_module_effects.csv", index=False)
    diagnostic_df.to_csv(out / "stage_b2_genomic_cancer_diagnostic.csv", index=False)
    status_df.to_csv(out / "stage_b2_genomic_task_status.csv", index=False)
    all_coords = [c["id"] for c in plan["genomic_coordinates"] if c["primary"]]
    summary = {
        "status": "DEVELOPMENT_ORTHOGONAL_STATIC_GENOMIC_INTEGRATION_ONLY", "claim_ceiling": plan["claim_ceiling"],
        "chi_present": False, "cv2_used": False, "composite_score_present": False,
        "coordinates": [x for x in all_coords if x in set(status_df.coordinate_id)],
        "analysis_modes": sorted(status_df.analysis_mode.unique().tolist()),
        "fixed_n": int(plan["genomic_primary_decomposition"]["fixed_n"]), "resamples_per_task": reps,
        "tasks": int(len(status_df)), "tasks_by_mode": status_df.groupby("analysis_mode").size().astype(int).to_dict(),
        "tasks_by_coordinate": {f"{k[0]}::{k[1]}": int(v) for k, v in status_df.groupby(["analysis_mode", "coordinate_id"]).size().items()},
        "minimum_valid_resamples": int(status_df.valid_resamples.min()), "raw_rows": int(status_df.rows.sum()),
        "raw_storage": "atomic per-task gzip files retained under _task_cache for restartability and audit",
        "module_summary_rows": int(len(module_df)), "cancer_summary_rows": int(len(diagnostic_df)), "source_sha256": checks,
    }
    (out / "STAGE_B2_GENOMIC_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True); ap.add_argument("--gmt", required=True); ap.add_argument("--absolute", required=True); ap.add_argument("--seg", required=True)
    ap.add_argument("--b1-context", required=True); ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--mode", choices=["PRIMARY", "INCREMENT_B1", "BOTH"], default="BOTH"); ap.add_argument("--coordinates", default="ALL"); ap.add_argument("--cancers", default="ALL")
    args = ap.parse_args(); plan = json.loads(Path(args.plan).read_text())
    checks = {
        "stage_a_profile_cache_sha256": sha256_file(args.cache), "hallmark_membership_sha256": sha256_file(args.gmt),
        "stage_b1_context_matched_sha256": sha256_file(args.b1_context), "absolute_scores_sha256": sha256_file(args.absolute), "seg_based_scores_sha256": sha256_file(args.seg),
    }
    for key, actual in checks.items():
        if actual != plan["inputs"][key]: raise ValueError(f"SHA mismatch for {key}: {actual}")
    _init_worker(args.cache, args.gmt, args.absolute, args.seg, args.b1_context, args.plan)
    all_coords = [c["id"] for c in plan["genomic_coordinates"] if c["primary"]]
    coords = all_coords if args.coordinates == "ALL" else [x for x in args.coordinates.split(",") if x]
    unknown = sorted(set(coords) - set(all_coords))
    if unknown: raise ValueError(f"unknown coordinates: {unknown}")
    all_cancers = sorted(set(G["cancer_types"]))
    cancers = all_cancers if args.cancers == "ALL" else [x for x in args.cancers.split(",") if x]
    unknown = sorted(set(cancers) - set(all_cancers))
    if unknown: raise ValueError(f"unknown cancers: {unknown}")
    modes = [args.mode] if args.mode != "BOTH" else ["PRIMARY", "INCREMENT_B1"]
    reps = int(plan["genomic_primary_decomposition"]["resamples_per_cancer_coordinate"])
    tasks = build_tasks(plan, modes, coords, cancers)
    if not tasks: raise RuntimeError("no eligible B2 genomic tasks")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); task_dir = out / "_task_cache"; task_dir.mkdir(exist_ok=True)
    complete = [item for item in tasks if task_complete(task_dir, item, reps)]
    pending = [item for item in tasks if item not in complete]
    print(f"B2 genomic tasks: total={len(tasks)} complete={len(complete)} pending={len(pending)}", flush=True)
    if pending:
        with ThreadPoolExecutor(max_workers=max(1, int(args.workers))) as ex:
            futures = {ex.submit(execute_task, task_dir, item, reps): item for item in pending}
            done = len(complete)
            for fut in as_completed(futures):
                meta = fut.result(); done += 1
                print(f"[{done}/{len(tasks)}] {meta['analysis_mode']} {meta['coordinate_id']} {meta['cancer_type']} n={meta['eligible_n']} valid={meta['valid_resamples']}/{reps}", flush=True)
    incomplete = [item for item in tasks if not task_complete(task_dir, item, reps)]
    if incomplete: raise RuntimeError(f"B2 genomic checkpoint incomplete after execution: {incomplete[:5]}")
    summary = finalize(out, task_dir, tasks, plan, checks, reps)
    print("STAGE B2 GENOMIC COMPLETE", flush=True); print(json.dumps(summary, indent=2, sort_keys=True), flush=True)

if __name__ == "__main__":
    main()
