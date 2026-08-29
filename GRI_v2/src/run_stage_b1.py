from __future__ import annotations

import argparse, csv, gzip, hashlib, json
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_network_accel import compute_module_metrics_accelerated

METRICS = ["cin_pairwise_median_abs", "cin_pc1_variance_fraction", "cout_eigengene_median_abs"]
G = {}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_seed(global_seed, *parts):
    payload = (str(global_seed) + "|" + "|".join(parts)).encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little", signed=False)


def load_modules(gmt_path):
    modules = {}
    with open(gmt_path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3:
                modules[p[0]] = p[2:]
    return modules


def build_context(sample_ids, patient_ids, cancer_types, purity_path, leukocyte_path):
    stage = pd.DataFrame({"sample_id": sample_ids, "patient_id": patient_ids, "cancer_type": cancer_types})
    stage["sample_root"] = stage.sample_id.str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", expand=False)

    a = pd.read_csv(purity_path, sep="\t", dtype=str)
    a["patient_id"] = a["sample"].str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})", expand=False)
    a["sample_root"] = a["sample"].str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", expand=False)
    a["sample_type"] = a["sample"].str.extract(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})", expand=False)
    a["value"] = pd.to_numeric(a["purity"], errors="coerce")
    a = a[(a["call status"].str.lower() == "called") & a.value.notna() & (a.sample_type == "01")].copy()
    if a.patient_id.nunique() != len(a):
        raise ValueError("ABSOLUTE primary called table is not unique by patient under frozen filter")

    l = pd.read_csv(leukocyte_path, sep="\t", header=None, names=["source_cancer", "sample", "value"])
    l["patient_id"] = l["sample"].str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})", expand=False)
    l["sample_root"] = l["sample"].str.extract(r"(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z])", expand=False)
    l["sample_type"] = l["sample"].str.extract(r"TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-([0-9]{2})", expand=False)
    l["value"] = pd.to_numeric(l["value"], errors="coerce")
    l = l[l.value.notna() & (l.sample_type == "01")].copy()
    l = l.groupby(["patient_id", "sample_root"], as_index=False).agg(value=("value", "median"))

    def attach(src):
        root_map = src.drop_duplicates("sample_root").set_index("sample_root")["value"].to_dict()
        counts = src.groupby("patient_id").size()
        unique_patients = set(counts[counts == 1].index)
        pat_map = src[src.patient_id.isin(unique_patients)].set_index("patient_id")["value"].to_dict()
        vals = np.full(len(stage), np.nan, dtype=float)
        for i, r in enumerate(stage.itertuples(index=False)):
            if r.sample_root in root_map:
                vals[i] = float(root_map[r.sample_root])
            elif r.patient_id in pat_map:
                vals[i] = float(pat_map[r.patient_id])
        return vals

    stage["purity"] = attach(a)
    stage["leukocyte_fraction"] = attach(l)
    return stage


def residualize_expression(x, covariates):
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


def _init_worker(cache_path, gmt_path, purity_path, leukocyte_path, plan_path):
    npz = np.load(cache_path, allow_pickle=True)
    G["sample_ids"] = npz["sample_ids"].astype(str)
    G["patient_ids"] = npz["patient_ids"].astype(str)
    G["cancer_types"] = npz["cancer_types"].astype(str)
    G["genes"] = npz["gene_symbols"].astype(str)
    G["X"] = npz["expression_log2p1"]
    G["modules"] = load_modules(gmt_path)
    G["plan"] = json.loads(Path(plan_path).read_text())
    G["context"] = build_context(G["sample_ids"], G["patient_ids"], G["cancer_types"], purity_path, leukocyte_path)


def _model_covariates(model_id):
    if model_id == "PURITY": return ["purity"]
    if model_id == "LEUKOCYTE": return ["leukocyte_fraction"]
    if model_id == "JOINT_INDEPENDENT": return ["purity", "leukocyte_fraction"]
    raise KeyError(model_id)


def _task(model_id, cancer):
    plan = G["plan"]
    fixed_n = int(plan["fixed_n_design"]["n"])
    reps = int(plan["fixed_n_design"]["resamples_per_cancer_model"])
    seed = int(plan["fixed_n_design"]["global_seed"])
    cov_names = _model_covariates(model_id)
    ctx = G["context"]
    mask = ctx.cancer_type.to_numpy() == cancer
    for cov in cov_names:
        mask &= np.isfinite(ctx[cov].to_numpy(dtype=float))
    eligible = np.flatnonzero(mask)
    if len(eligible) < fixed_n:
        return {"model_id": model_id, "cancer_type": cancer, "eligible_n": len(eligible), "rows": [], "valid_resamples": 0}

    sample_rng = np.random.default_rng(stable_seed(seed, "sample", model_id, cancer))
    rows = []
    valid_resamples = 0
    for r in range(reps):
        selected = np.sort(sample_rng.choice(eligible, size=fixed_n, replace=False))
        x = G["X"][selected].astype(float, copy=False)
        c = ctx.loc[selected, cov_names].to_numpy(dtype=float)
        actual_x = residualize_expression(x, c)
        perm_rng = np.random.default_rng(stable_seed(seed, "perm", model_id, cancer, str(r)))
        c_perm = c[perm_rng.permutation(fixed_n), :]
        null_x = residualize_expression(x, c_perm)
        if actual_x is None or null_x is None:
            continue
        kwargs = dict(
            minimum_mapped_genes=15,
            minimum_gene_finite_fraction=0.95,
            minimum_gene_finite_samples=20,
            minimum_pairwise_overlap_fraction=0.80,
            minimum_pairwise_overlap_samples=20,
        )
        baseline = metrics_to_dict(compute_module_metrics_accelerated(x, G["genes"], G["modules"], **kwargs))
        actual = metrics_to_dict(compute_module_metrics_accelerated(actual_x, G["genes"], G["modules"], **kwargs))
        null = metrics_to_dict(compute_module_metrics_accelerated(null_x, G["genes"], G["modules"], **kwargs))
        modules = sorted(set(baseline) & set(actual) & set(null))
        if len(modules) != 50:
            continue
        valid_resamples += 1
        for module in modules:
            row = {"model_id": model_id, "cancer_type": cancer, "eligible_n": len(eligible), "resample": r, "module": module}
            for metric in METRICS:
                b, a, n = baseline[module][metric], actual[module][metric], null[module][metric]
                row[f"baseline__{metric}"] = b
                row[f"actual__{metric}"] = a
                row[f"null__{metric}"] = n
                row[f"actual_delta__{metric}"] = a - b
                row[f"null_delta__{metric}"] = n - b
                row[f"context_specific_delta__{metric}"] = a - n
            rows.append(row)
    return {"model_id": model_id, "cancer_type": cancer, "eligible_n": len(eligible), "rows": rows, "valid_resamples": valid_resamples}


def _q05(s): return s.quantile(0.05)
def _q95(s): return s.quantile(0.95)
_q05.__name__ = "p05"; _q95.__name__ = "p95"


def spearman(x, y):
    x = pd.Series(x, dtype=float); y = pd.Series(y, dtype=float)
    good = x.notna() & y.notna()
    if good.sum() < 3: return float("nan")
    return float(x[good].rank().corr(y[good].rank(), method="pearson"))


def summarize(raw_path, out_dir):
    df = pd.read_csv(raw_path, compression="gzip")
    prefixes = ["baseline__", "actual__", "null__", "actual_delta__", "null_delta__", "context_specific_delta__"]
    value_cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes)]
    agg = df.groupby(["model_id", "cancer_type", "module"], sort=True)[value_cols].agg(["median", _q05, _q95])
    agg.columns = [f"{a}__{b}" for a, b in agg.columns]
    module = agg.reset_index()
    module.to_csv(Path(out_dir) / "stage_b1_module_context_effects.csv", index=False)

    cancer_rows = []
    for (model, cancer), g in module.groupby(["model_id", "cancer_type"], sort=True):
        row = {"model_id": model, "cancer_type": cancer, "module_count": len(g)}
        rawg = df[(df.model_id == model) & (df.cancer_type == cancer)]
        row["eligible_n"] = int(rawg.eligible_n.iloc[0])
        row["valid_resamples"] = int(rawg.resample.nunique())
        for metric in METRICS:
            b = g[f"baseline__{metric}__median"]
            a = g[f"actual__{metric}__median"]
            row[f"baseline_vs_actual_module_rank_rho__{metric}"] = spearman(b, a)
            row[f"median_actual_delta__{metric}"] = float(g[f"actual_delta__{metric}__median"].median())
            row[f"median_null_delta__{metric}"] = float(g[f"null_delta__{metric}__median"].median())
            row[f"median_context_specific_delta__{metric}"] = float(g[f"context_specific_delta__{metric}__median"].median())
        row["baseline_cin_vs_cout_rho"] = spearman(g["baseline__cin_pairwise_median_abs__median"], g["baseline__cout_eigengene_median_abs__median"])
        row["actual_cin_vs_cout_rho"] = spearman(g["actual__cin_pairwise_median_abs__median"], g["actual__cout_eigengene_median_abs__median"])
        row["baseline_pc1_vs_cout_rho"] = spearman(g["baseline__cin_pc1_variance_fraction__median"], g["baseline__cout_eigengene_median_abs__median"])
        row["actual_pc1_vs_cout_rho"] = spearman(g["actual__cin_pc1_variance_fraction__median"], g["actual__cout_eigengene_median_abs__median"])
        cancer_rows.append(row)
    cancer_df = pd.DataFrame(cancer_rows).sort_values(["model_id", "cancer_type"])
    cancer_df.to_csv(Path(out_dir) / "stage_b1_cancer_level_diagnostic.csv", index=False)
    return df, module, cancer_df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True); ap.add_argument("--gmt", required=True)
    ap.add_argument("--purity", required=True); ap.add_argument("--leukocyte", required=True)
    ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=1)
    args = ap.parse_args()
    plan = json.loads(Path(args.plan).read_text())
    expected = plan["inputs"]
    checks = {
        "stage_a_profile_cache_sha256": sha256_file(args.cache),
        "absolute_purity_sha256": sha256_file(args.purity),
        "leukocyte_fraction_sha256": sha256_file(args.leukocyte),
        "hallmark_membership_sha256": sha256_file(args.gmt),
    }
    for key, actual in checks.items():
        if actual != expected[key]:
            raise ValueError(f"SHA mismatch for {key}: {actual} != {expected[key]}")

    _init_worker(args.cache, args.gmt, args.purity, args.leukocyte, args.plan)
    cancers = sorted(set(G["cancer_types"]))
    task_list = []
    for model in [m["id"] for m in plan["models"]]:
        covs = _model_covariates(model)
        for cancer in cancers:
            ctx = G["context"]
            mask = ctx.cancer_type.to_numpy() == cancer
            for cov in covs: mask &= np.isfinite(ctx[cov].to_numpy(float))
            if mask.sum() >= plan["fixed_n_design"]["n"]:
                task_list.append((model, cancer))

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "stage_b1_resample_metrics.csv.gz"
    task_meta = []
    with gzip.open(raw_path, "wt", newline="") as gz:
        writer = None
        if args.workers > 1:
            mp = get_context("spawn")
            with mp.Pool(args.workers, initializer=_init_worker, initargs=(args.cache, args.gmt, args.purity, args.leukocyte, args.plan)) as pool:
                iterator = pool.starmap(_task, task_list)
        else:
            iterator = (_task(*t) for t in task_list)
        for result in iterator:
            task_meta.append({k: result[k] for k in ["model_id", "cancer_type", "eligible_n", "valid_resamples"]})
            for row in result["rows"]:
                if writer is None:
                    writer = csv.DictWriter(gz, fieldnames=list(row.keys())); writer.writeheader()
                writer.writerow(row)

    df, module, cancer = summarize(raw_path, out_dir)
    valid = pd.DataFrame(task_meta)
    summary = {
        "status": "DEVELOPMENT_COMPOSITION_ADJUSTED_STATIC_MAP_ONLY",
        "claim_ceiling": plan["claim_ceiling"], "chi_present": False, "cv2_used": False, "composite_score_present": False,
        "fixed_n": plan["fixed_n_design"]["n"], "resamples_per_cancer_model": plan["fixed_n_design"]["resamples_per_cancer_model"],
        "models": sorted(valid.model_id.unique().tolist()), "cancer_model_tasks": int(len(valid)),
        "tasks_by_model": valid.groupby("model_id").size().astype(int).to_dict(),
        "minimum_valid_resamples": int(valid.valid_resamples.min()),
        "raw_resample_rows": int(len(df)), "module_summary_rows": int(len(module)), "cancer_summary_rows": int(len(cancer)),
        "source_sha256": checks,
    }
    (out_dir / "STAGE_B1_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__": main()
