from __future__ import annotations

import argparse, csv, gzip, hashlib, json
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_network_accel import compute_module_metrics_accelerated

METRICS = ["cin_pairwise_median_abs", "cin_pc1_variance_fraction", "cout_eigengene_median_abs"]
G = {}


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_seed(global_seed: int, *parts: str) -> int:
    payload = (str(global_seed) + "|" + "|".join(parts)).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little", signed=False)


def load_modules(gmt_path: str | Path):
    modules = {}
    with open(gmt_path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3:
                modules[p[0]] = p[2:]
    return modules


def _ids(series: pd.Series):
    s = series.astype(str)
    return pd.DataFrame({
        "source_id": s,
        "patient_id": s.str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})", expand=False),
        "sample_root": s.str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", expand=False),
        "sample_type": s.str.extract(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})", expand=False),
    })


def attach_source(stage: pd.DataFrame, source: pd.DataFrame, id_col: str, value_cols: list[str]) -> pd.DataFrame:
    ids = _ids(source[id_col])
    src = pd.concat([source.reset_index(drop=True), ids], axis=1)
    src = src[src.sample_type.eq("01")].copy()
    for c in value_cols:
        src[c] = pd.to_numeric(src[c], errors="coerce")
    root_counts = src.dropna(subset=["sample_root"]).groupby("sample_root").size()
    unique_roots = set(root_counts[root_counts == 1].index)
    root_src = src[src.sample_root.isin(unique_roots)].set_index("sample_root")
    pat_counts = src.groupby("patient_id").size()
    unique_pats = set(pat_counts[pat_counts == 1].index)
    pat_src = src[src.patient_id.isin(unique_pats)].set_index("patient_id")
    out = stage.copy()
    for c in value_cols:
        vals = np.full(len(out), np.nan, dtype=float)
        methods = np.full(len(out), "none", dtype=object)
        for i, row in enumerate(out.itertuples(index=False)):
            if row.sample_root in root_src.index:
                v = root_src.at[row.sample_root, c]
                if isinstance(v, pd.Series):
                    raise ValueError(f"non-unique root unexpectedly survived for {row.sample_root}")
                if np.isfinite(v):
                    vals[i] = float(v); methods[i] = "exact_sample_root"
            elif row.patient_id in pat_src.index:
                v = pat_src.at[row.patient_id, c]
                if isinstance(v, pd.Series):
                    raise ValueError(f"non-unique patient unexpectedly survived for {row.patient_id}")
                if np.isfinite(v):
                    vals[i] = float(v); methods[i] = "unique_patient_fallback"
        out[c] = vals
        out[c + "__match_method"] = methods
    return out


def build_context(sample_ids, patient_ids, cancer_types, absolute_path, seg_path, b1_context_path):
    stage = pd.DataFrame({"sample_id": sample_ids, "patient_id": patient_ids, "cancer_type": cancer_types})
    stage["sample_root"] = stage.sample_id.str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", expand=False)
    a = pd.read_csv(absolute_path, sep="\t", dtype=str)
    stage = attach_source(stage, a, a.columns[0], ["AS", "LOH_n_seg", "LOH_frac_altered"])
    s = pd.read_csv(seg_path, sep="\t", dtype=str)
    stage = attach_source(stage, s, "Sample", ["n_segs", "frac_altered"])
    b1 = pd.read_csv(b1_context_path)
    required = {"sample_id", "patient_id", "cancer_type", "purity", "leukocyte_fraction"}
    if not required.issubset(b1.columns):
        raise ValueError("Stage B1 context file missing required columns")
    if b1.sample_id.duplicated().any():
        raise ValueError("Stage B1 context file not unique by sample_id")
    before = stage.sample_id.to_numpy(str).copy()
    stage = stage.merge(b1[["sample_id", "purity", "leukocyte_fraction"]], on="sample_id", how="left", validate="one_to_one")
    if not np.array_equal(stage.sample_id.to_numpy(str), before):
        raise ValueError("Stage B1 context merge changed Stage A sample order")
    return stage


def residualize_expression(x: np.ndarray, covariates: np.ndarray):
    x = np.asarray(x, dtype=float)
    c = np.asarray(covariates, dtype=float)
    if c.ndim == 1:
        c = c[:, None]
    if not np.isfinite(c).all():
        return None
    c = c - c.mean(axis=0, keepdims=True)
    sd = c.std(axis=0, ddof=1)
    if np.any(~np.isfinite(sd)) or np.any(sd <= 0):
        return None
    c = c / sd
    design = np.column_stack([np.ones(len(c)), c])
    if np.linalg.matrix_rank(design) < design.shape[1]:
        return None
    out = np.full_like(x, np.nan, dtype=float)
    finite = np.isfinite(x)
    full = finite.all(axis=0)
    if np.any(full):
        beta = np.linalg.lstsq(design, x[:, full], rcond=None)[0]
        out[:, full] = x[:, full] - design @ beta
    for j in np.flatnonzero(~full):
        mask = finite[:, j]
        if mask.sum() < design.shape[1] + 2:
            continue
        d = design[mask]
        if np.linalg.matrix_rank(d) < d.shape[1]:
            continue
        beta = np.linalg.lstsq(d, x[mask, j], rcond=None)[0]
        out[mask, j] = x[mask, j] - d @ beta
    return out


def metrics_to_dict(metrics):
    return {m.module: {k: float(getattr(m, k)) for k in METRICS} for m in metrics}


def metric_kwargs():
    return dict(
        minimum_mapped_genes=15,
        minimum_gene_finite_fraction=0.95,
        minimum_gene_finite_samples=20,
        minimum_pairwise_overlap_fraction=0.80,
        minimum_pairwise_overlap_samples=20,
    )


def compute_metrics(x: np.ndarray):
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all():
        return metrics_to_dict(compute_module_metrics_accelerated(x, G["genes"], G["modules"], **metric_kwargs()))
    n = x.shape[0]
    means = x.mean(axis=0)
    sds = x.std(axis=0, ddof=1)
    valid = np.isfinite(sds) & (sds > 0)
    z = np.full_like(x, np.nan, dtype=float)
    z[:, valid] = (x[:, valid] - means[valid]) / sds[valid]
    info = []
    eigengenes = []
    for module_name, base_idx in G["module_indices"].items():
        idx = base_idx[valid[base_idx]]
        if len(idx) < 15:
            continue
        zm = z[:, idx]
        corr = zm.T @ zm / float(n - 1)
        iu = np.triu_indices(len(idx), k=1)
        cin_pair = float(np.median(np.abs(corr[iu])))
        gram = zm @ zm.T
        vals, vecs = np.linalg.eigh(gram)
        j = int(np.argmax(vals))
        lam = max(float(vals[j]), 0.0)
        eig = vecs[:, j] * np.sqrt(lam)
        mean_state = np.mean(zm, axis=1)
        if np.std(eig, ddof=1) > 0 and np.std(mean_state, ddof=1) > 0 and np.corrcoef(eig, mean_state)[0, 1] < 0:
            eig = -eig
        pc1 = float(lam / np.trace(gram)) if np.trace(gram) > 0 else float("nan")
        info.append((module_name, idx, cin_pair, pc1))
        eigengenes.append(eig)
    E = np.column_stack(eigengenes)
    Ez = (E - E.mean(axis=0)) / E.std(axis=0, ddof=1)
    corr_all = Ez.T @ z / float(n - 1)
    out = {}
    for k, (module_name, idx, cin_pair, pc1) in enumerate(info):
        outside = valid.copy(); outside[idx] = False
        out[module_name] = {
            "cin_pairwise_median_abs": cin_pair,
            "cin_pc1_variance_fraction": pc1,
            "cout_eigengene_median_abs": float(np.median(np.abs(corr_all[k, outside]))),
        }
    return out


def _init_worker(cache_path, gmt_path, absolute_path, seg_path, b1_context_path, plan_path):
    npz = np.load(cache_path, allow_pickle=True)
    G["sample_ids"] = npz["sample_ids"].astype(str)
    G["patient_ids"] = npz["patient_ids"].astype(str)
    G["cancer_types"] = npz["cancer_types"].astype(str)
    G["genes"] = npz["gene_symbols"].astype(str)
    G["X"] = npz["expression_log2p1"]
    G["modules"] = load_modules(gmt_path)
    G["plan"] = json.loads(Path(plan_path).read_text())
    G["context"] = build_context(G["sample_ids"], G["patient_ids"], G["cancer_types"], absolute_path, seg_path, b1_context_path)
    G["coord_map"] = {c["id"]: c["source_column"] for c in G["plan"]["genomic_coordinates"] if c["primary"]}
    symbol_index = {str(g): i for i, g in enumerate(G["genes"])}
    G["module_indices"] = {name: np.asarray([symbol_index[g] for g in G["modules"][name] if g in symbol_index], dtype=int) for name in sorted(G["modules"])}


def _task_star(args):
    return _task(*args)


def _task(analysis_mode: str, coordinate_id: str, cancer: str):
    plan = G["plan"]
    fixed_n = int(plan["genomic_primary_decomposition"]["fixed_n"])
    reps = int(plan["genomic_primary_decomposition"]["resamples_per_cancer_coordinate"])
    seed = int(plan["genomic_primary_decomposition"]["global_seed"])
    col = G["coord_map"][coordinate_id]
    ctx = G["context"]
    mask = (ctx.cancer_type.to_numpy() == cancer) & np.isfinite(ctx[col].to_numpy(float))
    if analysis_mode == "INCREMENT_B1":
        mask &= np.isfinite(ctx.purity.to_numpy(float)) & np.isfinite(ctx.leukocyte_fraction.to_numpy(float))
    eligible = np.flatnonzero(mask)
    if len(eligible) < fixed_n:
        return {"analysis_mode": analysis_mode, "coordinate_id": coordinate_id, "cancer_type": cancer, "eligible_n": len(eligible), "valid_resamples": 0, "rows": []}
    sample_rng = np.random.default_rng(stable_seed(seed, "sample", analysis_mode, coordinate_id, cancer))
    rows = []
    valid = 0
    for r in range(reps):
        selected = np.sort(sample_rng.choice(eligible, size=fixed_n, replace=False))
        x = G["X"][selected].astype(float, copy=False)
        g = ctx.loc[selected, col].to_numpy(float)[:, None]
        perm_rng = np.random.default_rng(stable_seed(seed, "perm", analysis_mode, coordinate_id, cancer, str(r)))
        g_perm = g[perm_rng.permutation(fixed_n), :]
        if analysis_mode == "PRIMARY":
            reference_x = x
            actual_x = residualize_expression(x, g)
            null_x = residualize_expression(x, g_perm)
        elif analysis_mode == "INCREMENT_B1":
            c = ctx.loc[selected, ["purity", "leukocyte_fraction"]].to_numpy(float)
            reference_x = residualize_expression(x, c)
            actual_x = residualize_expression(x, np.column_stack([c, g]))
            null_x = residualize_expression(x, np.column_stack([c, g_perm]))
        else:
            raise KeyError(analysis_mode)
        if reference_x is None or actual_x is None or null_x is None:
            continue
        reference = compute_metrics(reference_x)
        actual = compute_metrics(actual_x)
        null = compute_metrics(null_x)
        modules = sorted(set(reference) & set(actual) & set(null))
        if len(modules) != 50:
            continue
        valid += 1
        g_med = float(np.median(g[:, 0]))
        g_iqr = float(np.quantile(g[:, 0], 0.75) - np.quantile(g[:, 0], 0.25))
        for module in modules:
            row = {
                "analysis_mode": analysis_mode, "coordinate_id": coordinate_id, "source_column": col,
                "cancer_type": cancer, "eligible_n": len(eligible), "resample": r, "module": module,
                "genomic_median": g_med, "genomic_iqr": g_iqr,
            }
            for metric in METRICS:
                ref = reference[module][metric]; a = actual[module][metric]; n = null[module][metric]
                row[f"reference__{metric}"] = ref
                row[f"actual__{metric}"] = a
                row[f"null__{metric}"] = n
                row[f"actual_delta__{metric}"] = a - ref
                row[f"null_delta__{metric}"] = n - ref
                row[f"specific_delta__{metric}"] = a - n
            rows.append(row)
    return {"analysis_mode": analysis_mode, "coordinate_id": coordinate_id, "cancer_type": cancer, "eligible_n": len(eligible), "valid_resamples": valid, "rows": rows}


def _q05(s): return s.quantile(0.05)
def _q95(s): return s.quantile(0.95)
_q05.__name__ = "p05"; _q95.__name__ = "p95"


def spearman(x, y):
    x = pd.Series(x, dtype=float); y = pd.Series(y, dtype=float)
    good = x.notna() & y.notna()
    if good.sum() < 3: return float("nan")
    return float(x[good].rank().corr(y[good].rank(), method="pearson"))


def summarize(raw_path: Path, out_dir: Path):
    df = pd.read_csv(raw_path, compression="gzip")
    value_cols = [c for c in df.columns if any(c.startswith(p) for p in ["reference__", "actual__", "null__", "actual_delta__", "null_delta__", "specific_delta__"])]
    agg = df.groupby(["analysis_mode", "coordinate_id", "cancer_type", "module"], sort=True)[value_cols].agg(["median", _q05, _q95])
    agg.columns = [f"{a}__{b}" for a,b in agg.columns]
    module = agg.reset_index()
    module.to_csv(out_dir / "stage_b2_genomic_module_effects.csv", index=False)
    cancer_rows = []
    for (mode, coord, cancer), g in module.groupby(["analysis_mode", "coordinate_id", "cancer_type"], sort=True):
        rawg = df[(df.analysis_mode == mode) & (df.coordinate_id == coord) & (df.cancer_type == cancer)]
        row = {"analysis_mode": mode, "coordinate_id": coord, "cancer_type": cancer, "module_count": len(g), "eligible_n": int(rawg.eligible_n.iloc[0]), "valid_resamples": int(rawg["resample"].nunique())}
        for metric in METRICS:
            ref = g[f"reference__{metric}__median"]
            actual = g[f"actual__{metric}__median"]
            row[f"reference_vs_actual_module_rank_rho__{metric}"] = spearman(ref, actual)
            row[f"median_actual_delta__{metric}"] = float(g[f"actual_delta__{metric}__median"].median())
            row[f"median_null_delta__{metric}"] = float(g[f"null_delta__{metric}__median"].median())
            row[f"median_specific_delta__{metric}"] = float(g[f"specific_delta__{metric}__median"].median())
            row[f"median_abs_specific_delta__{metric}"] = float(g[f"specific_delta__{metric}__median"].abs().median())
        row["reference_cin_vs_cout_rho"] = spearman(g["reference__cin_pairwise_median_abs__median"], g["reference__cout_eigengene_median_abs__median"])
        row["actual_cin_vs_cout_rho"] = spearman(g["actual__cin_pairwise_median_abs__median"], g["actual__cout_eigengene_median_abs__median"])
        cancer_rows.append(row)
    cancer_df = pd.DataFrame(cancer_rows).sort_values(["analysis_mode", "coordinate_id", "cancer_type"])
    cancer_df.to_csv(out_dir / "stage_b2_genomic_cancer_diagnostic.csv", index=False)
    return df, module, cancer_df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True); ap.add_argument("--gmt", required=True)
    ap.add_argument("--absolute", required=True); ap.add_argument("--seg", required=True)
    ap.add_argument("--b1-context", required=True); ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=1); ap.add_argument("--mode", choices=["PRIMARY", "INCREMENT_B1", "BOTH"], default="BOTH")
    ap.add_argument("--coordinates", default="ALL"); ap.add_argument("--cancers", default="ALL")
    args = ap.parse_args()
    plan = json.loads(Path(args.plan).read_text())
    expected = plan["inputs"]
    checks = {
        "stage_a_profile_cache_sha256": sha256_file(args.cache), "hallmark_membership_sha256": sha256_file(args.gmt),
        "stage_b1_context_matched_sha256": sha256_file(args.b1_context), "absolute_scores_sha256": sha256_file(args.absolute),
        "seg_based_scores_sha256": sha256_file(args.seg),
    }
    for key, actual in checks.items():
        if actual != expected[key]: raise ValueError(f"SHA mismatch for {key}: {actual} != {expected[key]}")
    _init_worker(args.cache, args.gmt, args.absolute, args.seg, args.b1_context, args.plan)
    coords = [c["id"] for c in plan["genomic_coordinates"] if c["primary"]]
    if args.coordinates != "ALL":
        wanted = [x for x in args.coordinates.split(",") if x]
        unknown = sorted(set(wanted) - set(coords))
        if unknown: raise ValueError(f"unknown coordinates: {unknown}")
        coords = wanted
    cancers = sorted(set(G["cancer_types"]))
    if args.cancers != "ALL":
        wanted = [x for x in args.cancers.split(",") if x]
        unknown = sorted(set(wanted) - set(cancers))
        if unknown: raise ValueError(f"unknown cancers: {unknown}")
        cancers = wanted
    modes = [args.mode] if args.mode != "BOTH" else ["PRIMARY", "INCREMENT_B1"]
    task_list = []
    for mode in modes:
        for coord in coords:
            col = G["coord_map"][coord]
            for cancer in cancers:
                ctx = G["context"]
                mask = (ctx.cancer_type.to_numpy() == cancer) & np.isfinite(ctx[col].to_numpy(float))
                if mode == "INCREMENT_B1": mask &= np.isfinite(ctx.purity.to_numpy(float)) & np.isfinite(ctx.leukocyte_fraction.to_numpy(float))
                if int(mask.sum()) >= int(plan["matching"]["minimum_cancer_n"]): task_list.append((mode, coord, cancer))
    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "stage_b2_genomic_resample_metrics.csv.gz"
    task_meta = []
    with gzip.open(raw_path, "wt", newline="") as gz:
        writer = None
        if args.workers > 1:
            ctx = get_context("spawn")
            with ctx.Pool(args.workers, initializer=_init_worker, initargs=(args.cache, args.gmt, args.absolute, args.seg, args.b1_context, args.plan)) as pool:
                iterator = pool.starmap(_task, task_list)
        else:
            iterator = (_task(*t) for t in task_list)
        for i, result in enumerate(iterator, start=1):
            task_meta.append({k: result[k] for k in ["analysis_mode", "coordinate_id", "cancer_type", "eligible_n", "valid_resamples"]})
            for row in result["rows"]:
                if writer is None:
                    writer = csv.DictWriter(gz, fieldnames=list(row.keys())); writer.writeheader()
                writer.writerow(row)
            print(f"[{i}/{len(task_list)}] {result['analysis_mode']} {result['coordinate_id']} {result['cancer_type']} n={result['eligible_n']} valid={result['valid_resamples']}", flush=True)
    df, module, cancer = summarize(raw_path, out_dir)
    meta = pd.DataFrame(task_meta); meta.to_csv(out_dir / "stage_b2_genomic_task_status.csv", index=False)
    summary = {
        "status": "DEVELOPMENT_ORTHOGONAL_STATIC_GENOMIC_INTEGRATION_ONLY", "claim_ceiling": plan["claim_ceiling"],
        "chi_present": False, "cv2_used": False, "composite_score_present": False, "coordinates": coords, "analysis_modes": modes,
        "fixed_n": int(plan["genomic_primary_decomposition"]["fixed_n"]), "resamples_per_task": int(plan["genomic_primary_decomposition"]["resamples_per_cancer_coordinate"]),
        "tasks": int(len(meta)), "tasks_by_mode": meta.groupby("analysis_mode").size().astype(int).to_dict(),
        "tasks_by_coordinate": {f"{k[0]}::{k[1]}": int(v) for k,v in meta.groupby(["analysis_mode", "coordinate_id"]).size().items()},
        "minimum_valid_resamples": int(meta.valid_resamples.min()), "raw_rows": int(len(df)), "module_summary_rows": int(len(module)), "cancer_summary_rows": int(len(cancer)), "source_sha256": checks,
    }
    (out_dir / "STAGE_B2_GENOMIC_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
