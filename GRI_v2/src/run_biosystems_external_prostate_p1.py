#!/usr/bin/env python3
from __future__ import annotations

import argparse, csv, gzip, hashlib, json, math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_network_accel import compute_module_metrics_accelerated

EXPECTED = {
    "rna": "9f94093f3254e1478d37f0b888d8f652e1d7bbf7f6265dd81f15d4d490f8cc92",
    "m450": "90a7a8c12343831524a9711be7e0b3f33f297fe408662fa68c5efa49a7c862d0",
    "epic": "b55bf7b2e427c27e84a331c7f8c07f296dd64c07fa54c74445bb40288777e69f",
    "gmt": "eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596",
}
B = 999


def sha256_file(path: Path, chunk=8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for x in iter(lambda: f.read(chunk), b""):
            h.update(x)
    return h.hexdigest()


def stable_seed(namespace: str, *tokens) -> int:
    s = "|".join([namespace] + [str(x) for x in tokens]).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8], "big") % (2**32)


def bh_fdr(vals):
    p = np.asarray(vals, float)
    out = np.full_like(p, np.nan)
    good = np.flatnonzero(np.isfinite(p))
    if not len(good):
        return out
    v = p[good]
    o = np.argsort(v, kind="mergesort")
    r = v[o]
    q = r * len(r) / np.arange(1, len(r) + 1, dtype=float)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.minimum(q, 1)
    tmp = np.empty_like(q)
    tmp[o] = q
    out[good] = tmp
    return out


def parse_gmt(path: Path):
    mods = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3:
                mods[p[0]] = list(dict.fromkeys(x for x in p[2:] if x))
    if len(mods) != 50:
        raise ValueError(f"expected 50 Hallmarks, got {len(mods)}")
    return mods


def resolve_header(header, participant: str, state: str):
    marker = "_T_" if state == "TUMOR" else "_NT_"
    hits = [h for h in header if participant in str(h) and marker in str(h)]
    if len(hits) != 1:
        raise ValueError(f"{participant} {state}: expected exactly one header hit, got {hits}")
    return hits[0]


def load_c1_support(flags_path: Path, map_path: Path):
    flags = pd.read_csv(flags_path, compression="gzip")
    if len(flags) != 22601 or flags["probe_id"].nunique() != 22601:
        raise ValueError("C1 probe flag universe drift")
    probe_ids = flags["probe_id"].astype(str).to_numpy(object)
    mask = flags["technical_mask_union"].astype(int).to_numpy() == 1
    if int(mask.sum()) != 579:
        raise ValueError(f"C1 technical mask drift: {int(mask.sum())}")

    mp = pd.read_csv(map_path, compression="gzip", dtype=str)
    core = mp[mp["regulatory_stratum"].astype(str).str.contains("PROMOTER_CORE", regex=False)].copy()
    if core["probe_id"].nunique() != 3999:
        raise ValueError(f"PROMOTER_CORE probe count drift: {core['probe_id'].nunique()}")
    gene_map_raw = {}
    for pid, g in core[["probe_id", "gene_symbol"]].itertuples(index=False):
        if not g or str(g).lower() == "nan":
            continue
        gene_map_raw.setdefault(str(pid), []).append(str(g))
    for pid in list(gene_map_raw):
        gene_map_raw[pid] = list(dict.fromkeys(gene_map_raw[pid]))
    return probe_ids, mask, gene_map_raw


def read_external_methylation(path: Path, required_probe_order, participant_ids):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f, delimiter="\t"))
    tumor_headers = [resolve_header(header, p, "TUMOR") for p in participant_ids]
    normal_headers = [resolve_header(header, p, "NORMAL") for p in participant_ids]
    wanted_headers = tumor_headers + normal_headers
    pos = {h: header.index(h) for h in wanted_headers}
    target = set(map(str, required_probe_order))
    rows = {}
    row_offset = None
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        next(f)
        for line_no, line in enumerate(f, start=2):
            parts = line.rstrip("\r\n").split("\t")
            if not parts:
                continue
            pid = parts[0].strip().strip('"')
            if pid not in target:
                continue
            if row_offset is None:
                if len(parts) == len(header) + 1:
                    row_offset = 1
                elif len(parts) == len(header):
                    row_offset = 0
                else:
                    raise ValueError(f"unexpected methylation row width {len(parts)} vs header {len(header)}")
            vals = []
            for h in wanted_headers:
                raw = parts[pos[h] + row_offset].strip().strip('"')
                try:
                    vals.append(float(raw))
                except Exception:
                    vals.append(np.nan)
            rows[pid] = vals
    keep = [str(p) for p in required_probe_order if str(p) in rows]
    if len(keep) < 20000:
        raise ValueError(f"external overlap with C1 carrier too small: {len(keep)}")
    x = np.asarray([rows[p] for p in keep], dtype=float).T
    n = len(participant_ids)
    return {
        "probe_ids": np.asarray(keep, dtype=object),
        "tumor": x[:n, :],
        "normal": x[n:, :],
        "tumor_headers": tumor_headers,
        "normal_headers": normal_headers,
    }


def median_ratio_normalize(counts):
    x = np.asarray(counts, float)
    good = np.all(np.isfinite(x) & (x > 0), axis=0)
    if int(good.sum()) < 1000:
        raise ValueError(f"too few positive-across-all genes for median-ratio normalization: {int(good.sum())}")
    log_gm = np.mean(np.log(x[:, good]), axis=0)
    gm = np.exp(log_gm)
    ratios = x[:, good] / gm[None, :]
    sf = np.median(ratios, axis=1)
    if not np.all(np.isfinite(sf) & (sf > 0)):
        raise ValueError("invalid median-ratio size factor")
    return x / sf[:, None], sf, int(good.sum())


def read_external_rna(path: Path, participant_ids, modules):
    df = pd.read_csv(path, compression="gzip", low_memory=False)
    headers = list(df.columns)
    tumor_headers = [resolve_header(headers, p, "TUMOR") for p in participant_ids]
    normal_headers = [resolve_header(headers, p, "NORMAL") for p in participant_ids]
    sample_headers = tumor_headers + normal_headers
    if "Gene" not in df.columns:
        raise ValueError("RNA source missing Gene symbol column")
    counts = df[sample_headers].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float).T
    if not np.isfinite(counts).all() or np.any(counts < 0):
        raise ValueError("RNA raw-count source has invalid selected values")
    norm, sf, n_sf_genes = median_ratio_normalize(counts)
    logx = np.log2(norm + 1.0)
    union = set(g for m in modules.values() for g in m)
    seen = set()
    idx = []
    genes = []
    raw_genes = df["Gene"].astype(str).tolist()
    for i, g in enumerate(raw_genes):
        g = str(g).strip()
        if not g or g.lower() == "nan" or g in seen or g not in union:
            continue
        seen.add(g)
        idx.append(i)
        genes.append(g)
    if len(genes) < 3000:
        raise ValueError(f"Hallmark-union external RNA mapping too small: {len(genes)}")
    hx = logx[:, idx]
    n = len(participant_ids)
    return {
        "genes": np.asarray(genes, dtype=object),
        "tumor": hx[:n, :],
        "normal": hx[n:, :],
        "tumor_headers": tumor_headers,
        "normal_headers": normal_headers,
        "size_factors": sf,
        "size_factor_gene_count": n_sf_genes,
        "hallmark_union_genes": len(genes),
    }


def symmetric_probe_rules(beta_t, beta_n):
    ft = np.isfinite(beta_t).sum(axis=0) / beta_t.shape[0] >= 0.95
    fn = np.isfinite(beta_n).sum(axis=0) / beta_n.shape[0] >= 0.95
    keep = ft & fn
    with np.errstate(all="ignore"):
        mt = np.nanmedian(beta_t, axis=0)
        mn = np.nanmedian(beta_n, axis=0)
    if not np.isfinite(mt[keep]).all() or not np.isfinite(mn[keep]).all():
        raise ValueError("retained external probe median nonfinite")
    bt = np.asarray(beta_t[:, keep], float).copy()
    bn = np.asarray(beta_n[:, keep], float).copy()
    mt2, mn2 = mt[keep], mn[keep]
    bad = ~np.isfinite(bt)
    if bad.any():
        bt[bad] = np.broadcast_to(mt2, bt.shape)[bad]
    bad = ~np.isfinite(bn)
    if bad.any():
        bn[bad] = np.broadcast_to(mn2, bn.shape)[bad]
    return keep, bt, bn


def spectral_concentration_centered(xc):
    n, p = xc.shape
    g = (xc @ xc.T) / float(p)
    vals = np.linalg.eigvalsh(g)[::-1]
    scale = float(np.sum(np.abs(vals)))
    tol = 1e-10 * scale
    if np.any(vals < -tol):
        raise ValueError("negative modal eigenvalue")
    vals = np.where(vals < 0, 0, vals)[: n - 1]
    if vals.sum() <= 0:
        return np.nan
    q = vals / vals.sum()
    nz = q > 0
    h = float(-np.sum(q[nz] * np.log(q[nz])))
    return float(1 - h / math.log(float(n - 1)))


def centered(x):
    x = np.asarray(x, float)
    return x - x.mean(axis=0, keepdims=True)


def permute_columns_fy(xc, seed):
    rng = np.random.default_rng(seed)
    n, p = xc.shape
    idx = np.broadcast_to(np.arange(n, dtype=np.int16)[:, None], (n, p)).copy()
    cols = np.arange(p)
    for i in range(n - 1, 0, -1):
        j = rng.integers(0, i + 1, size=p)
        tmp = idx[i, :].copy()
        idx[i, :] = idx[j, cols]
        idx[j, cols] = tmp
    return xc[idx, cols[None, :]]


def h1_nulls(beta, namespace, lane, track, workers=4):
    xc = centered(beta)
    obs = spectral_concentration_centered(xc)
    def one(rep):
        xp = permute_columns_fy(xc, stable_seed(namespace, lane, track, "H1", rep))
        return spectral_concentration_centered(xp)
    vals = np.empty(B, float)
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        fut = {ex.submit(one, r): r for r in range(B)}
        for f in as_completed(fut):
            vals[fut[f]] = f.result()
    return obs, vals


def cka_centered(xc, yc):
    kx = xc @ xc.T
    ky = yc @ yc.T
    n = xc.shape[0]
    h = np.eye(n) - np.ones((n, n)) / n
    kx = h @ kx @ h
    ky = h @ ky @ h
    den = float(np.linalg.norm(kx, "fro") * np.linalg.norm(ky, "fro"))
    return float(np.sum(kx * ky) / den) if den > 0 else np.nan


def h2_test(beta, expr, namespace, lane, track):
    mx = centered(beta)
    rx = centered(expr)
    obs = cka_centered(mx, rx)
    vals = []
    for rep in range(B):
        perm = np.random.default_rng(stable_seed(namespace, lane, track, "H2", rep)).permutation(beta.shape[0])
        vals.append(cka_centered(mx[perm, :], rx))
    return obs, np.asarray(vals, float)


def rank_cols(x):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    for j in range(x.shape[1]):
        out[:, j] = pd.Series(x[:, j]).rank(method="average").to_numpy(float)
    return out


def same_stat_ranked(a, b):
    ac = a - a.mean(axis=0, keepdims=True)
    bc = b - b.mean(axis=0, keepdims=True)
    den = np.sqrt(np.sum(ac * ac, axis=0) * np.sum(bc * bc, axis=0))
    r = np.divide(np.sum(ac * bc, axis=0), den, out=np.full(ac.shape[1], np.nan), where=den > 0)
    return float(np.nanmedian(np.abs(r)))


def meth_pc1(m):
    m = np.asarray(m, float)
    xc = m - m.mean(0, keepdims=True)
    if np.allclose(xc, 0):
        raise ValueError("zero meth Hallmark")
    u, s, vt = np.linalg.svd(xc, full_matrices=False)
    eig = u[:, 0] * s[0]
    load = vt[0].copy()
    mean = m.mean(1)
    if np.std(eig, ddof=1) > 0 and np.std(mean, ddof=1) > 0:
        if float(np.corrcoef(eig, mean)[0, 1]) < 0:
            eig = -eig
    else:
        j = int(np.argmax(np.abs(load)))
        if load[j] < 0:
            eig = -eig
    return eig


def rna_pc1(raw):
    x = np.asarray(raw, float)
    fin = np.isfinite(x)
    cnt = fin.sum(0)
    sd = np.nanstd(x, axis=0, ddof=1)
    valid = (cnt >= max(20, int(math.ceil(0.95 * x.shape[0])))) & np.isfinite(sd) & (sd > 0)
    if int(valid.sum()) < 15:
        raise ValueError("RNA Hallmark <15 genes")
    y = x[:, valid]
    mu = np.nanmean(y, 0)
    ss = np.nanstd(y, 0, ddof=1)
    z = (y - mu) / ss
    z = np.where(np.isfinite(z), z, 0)
    u, s, _ = np.linalg.svd(z, full_matrices=False)
    eig = u[:, 0] * s[0]
    mean = z.mean(1)
    if np.std(eig, ddof=1) > 0 and np.std(mean, ddof=1) > 0 and float(np.corrcoef(eig, mean)[0, 1]) < 0:
        eig = -eig
    return eig, int(valid.sum())


def build_gene_map(retained_probe_ids, core_raw):
    local = {str(p): i for i, p in enumerate(retained_probe_ids)}
    gm = {}
    for pid, genes in core_raw.items():
        i = local.get(str(pid))
        if i is None:
            continue
        for g in genes:
            gm.setdefault(g, []).append(i)
    return {g: np.asarray(sorted(set(v)), int) for g, v in gm.items()}


def hallmark_mats(beta, expr, probe_ids, core_raw, modules, genes):
    gm = build_gene_map(probe_ids, core_raw)
    gi = {str(g): i for i, g in enumerate(genes)}
    ms, rs, common = {}, {}, []
    for h in sorted(modules):
        mm = []
        usedm = []
        probes = set()
        for gene in modules[h]:
            loc = gm.get(gene)
            if loc is None or len(loc) == 0:
                continue
            mm.append(np.median(beta[:, loc], axis=1))
            usedm.append(gene)
            probes.update(map(int, loc))
        if len(usedm) < 10 or len(probes) < 10:
            continue
        rg = [g for g in modules[h] if g in gi]
        if not rg:
            continue
        rr = expr[:, [gi[g] for g in rg]]
        try:
            me = meth_pc1(np.column_stack(mm))
            re, _ = rna_pc1(rr)
        except Exception:
            continue
        ms[h] = me
        rs[h] = re
    common = sorted(set(ms) & set(rs))
    if len(common) < 25:
        raise ValueError(f"common Hallmark support below 25: {len(common)}")
    return common, np.column_stack([ms[h] for h in common]), np.column_stack([rs[h] for h in common])


def h3_tests(beta, expr, probe_ids, core_raw, modules, genes, namespace, lane, track):
    common, ms, rs = hallmark_mats(beta, expr, probe_ids, core_raw, modules, genes)
    mr = rank_cols(ms)
    rr = rank_cols(rs)
    obs = same_stat_ranked(mr, rr)
    pnull = np.empty(B, float)
    lnull = np.empty(B, float)
    for rep in range(B):
        rng = np.random.default_rng(stable_seed(namespace, lane, track, "H3A", rep))
        perm = rng.permutation(beta.shape[0])
        pnull[rep] = same_stat_ranked(mr[perm, :], rr)
        rng2 = np.random.default_rng(stable_seed(namespace, lane, track, "H3B", rep))
        lp = rng2.permutation(len(common))
        lnull[rep] = same_stat_ranked(mr[:, lp], rr)
    return obs, pnull, lnull, len(common)


def upper_p(obs, null):
    v = np.asarray(null, float)
    v = v[np.isfinite(v)]
    return float((1 + np.sum(v >= obs)) / (len(v) + 1))


def endpoint_row(name, obs, null):
    med = float(np.median(null))
    effect = float(obs - med)
    return {
        "endpoint": name,
        "observed": float(obs),
        "null_median": med,
        "null_mean": float(np.mean(null)),
        "null_sd": float(np.std(null, ddof=1)),
        "effect": effect,
        "p_upper": upper_p(obs, null),
    }


def run_architecture_lane(beta_t, beta_n, probe_ids_all, mask_all, rna_t, genes, core_raw, modules, namespace, lane, workers):
    common_keep, bt, bn = symmetric_probe_rules(beta_t, beta_n)
    pids = probe_ids_all[common_keep]
    mask = mask_all[common_keep]
    out = {}
    null_store = {}
    for track, keep in {
        "PRIMARY_PUBLICATION": np.ones(len(pids), dtype=bool),
        "MASKED_TECHNICAL": ~mask,
    }.items():
        b = bt[:, keep]
        p = pids[keep]
        h1obs, h1null = h1_nulls(b, namespace, lane, track, workers=workers)
        h2obs, h2null = h2_test(b, rna_t, namespace, lane, track)
        h3obs, h3null, h3bnull, nh = h3_tests(b, rna_t, p, core_raw, modules, genes, namespace, lane, track)
        rows = [
            endpoint_row("H1", h1obs, h1null),
            endpoint_row("H2", h2obs, h2null),
            endpoint_row("H3a", h3obs, h3null),
        ]
        q = bh_fdr([x["p_upper"] for x in rows])
        for x, qq in zip(rows, q):
            x["bh_q"] = float(qq)
            x["passes_q05"] = bool(x["effect"] > 0 and qq < 0.05)
            x["track"] = track
            x["lane"] = lane
            x["n"] = int(b.shape[0])
            x["probe_count"] = int(b.shape[1])
            x["common_hallmarks"] = int(nh)
        h3b = endpoint_row("H3b_descriptive", h3obs, h3bnull)
        h3b.update(track=track, lane=lane, n=int(b.shape[0]), probe_count=int(b.shape[1]), common_hallmarks=int(nh))
        out[track] = rows + [h3b]
        null_store[track] = {
            "H1": h1null,
            "H2": h2null,
            "H3a": h3null,
            "H3b": h3bnull,
        }
    return out, null_store, {"common_probe_count": int(common_keep.sum()), "masked_removed": int(mask.sum())}


def stage_a_summary(expr, genes, modules):
    ms = compute_module_metrics_accelerated(
        expr, genes, modules,
        minimum_mapped_genes=15,
        minimum_gene_finite_fraction=0.95,
        minimum_gene_finite_samples=20,
        minimum_pairwise_overlap_fraction=0.80,
        minimum_pairwise_overlap_samples=20,
    )
    if not ms:
        raise ValueError("no evaluable Hallmarks in external Stage A")
    return {
        "cin_pairwise": float(np.nanmedian([z.cin_pairwise_median_abs for z in ms])),
        "cin_pc1": float(np.nanmedian([z.cin_pc1_variance_fraction for z in ms])),
        "cout": float(np.nanmedian([z.cout_eigengene_median_abs for z in ms])),
        "evaluable_hallmarks": len(ms),
    }


def rna_tn_test(rna_t, rna_n, genes, modules, namespace):
    obs_t = stage_a_summary(rna_t, genes, modules)
    obs_n = stage_a_summary(rna_n, genes, modules)
    metrics = ["cin_pairwise", "cin_pc1", "cout"]
    observed = {m: obs_t[m] - obs_n[m] for m in metrics}
    nulls = {m: np.empty(B, float) for m in metrics}
    def one(rep):
        rng = np.random.default_rng(stable_seed(namespace, "RNA_TN", rep))
        swap = rng.integers(0, 2, size=rna_t.shape[0]).astype(bool)
        a = rna_t.copy()
        b = rna_n.copy()
        a[swap, :] = rna_n[swap, :]
        b[swap, :] = rna_t[swap, :]
        ta = stage_a_summary(a, genes, modules)
        tb = stage_a_summary(b, genes, modules)
        return {m: ta[m] - tb[m] for m in metrics}
    with ThreadPoolExecutor(max_workers=4) as ex:
        fut = {ex.submit(one, r): r for r in range(B)}
        for f in as_completed(fut):
            rep = fut[f]
            z = f.result()
            for m in metrics:
                nulls[m][rep] = z[m]
    rows = []
    for m in metrics:
        p = float((1 + np.sum(nulls[m] <= observed[m])) / (B + 1))
        rows.append({"metric": m, "tumor": obs_t[m], "adjacent": obs_n[m], "tumor_minus_adjacent": observed[m], "p_lower": p})
    q = bh_fdr([x["p_lower"] for x in rows])
    for x, qq in zip(rows, q):
        x["bh_q"] = float(qq)
        x["passes_directional_q05"] = bool(x["tumor_minus_adjacent"] < 0 and qq < 0.05)
    return rows, nulls


def flatten_endpoint_rows(result):
    rows = []
    for track in result:
        rows.extend(result[track])
    return rows


def pass_map(result):
    p = result["PRIMARY_PUBLICATION"]
    return {x["endpoint"]: bool(x.get("passes_q05", False)) for x in p if x["endpoint"] in {"H1", "H2", "H3a"}}


def primary_class(result):
    pm = pass_map(result)
    n = sum(pm.values())
    if n == 3:
        return "P1_FULL_TRANSPORT"
    if n > 0:
        return "P1_PARTIAL_TRANSPORT"
    return "P1_NO_TRANSPORT"


def conflict(primary_result, sensitivity_result):
    p0 = {x["endpoint"]: x for x in primary_result["PRIMARY_PUBLICATION"] if x["endpoint"] in {"H1","H2","H3a"}}
    s0 = {x["endpoint"]: x for x in sensitivity_result["PRIMARY_PUBLICATION"] if x["endpoint"] in {"H1","H2","H3a"}}
    issues = []
    for e in ["H1","H2","H3a"]:
        if np.sign(p0[e]["effect"]) != np.sign(s0[e]["effect"]):
            issues.append(f"{e}:effect_sign")
        if bool(p0[e]["passes_q05"]) != bool(s0[e]["passes_q05"]):
            issues.append(f"{e}:q05_status")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--rna", required=True, type=Path)
    ap.add_argument("--m450", required=True, type=Path)
    ap.add_argument("--epic", required=True, type=Path)
    ap.add_argument("--gmt", required=True, type=Path)
    ap.add_argument("--c1-flags", required=True, type=Path)
    ap.add_argument("--c1-map", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(a.config.read_text())
    ns = cfg["seed_namespace"]

    for label, path in [("rna",a.rna),("m450",a.m450),("epic",a.epic),("gmt",a.gmt)]:
        got = sha256_file(path)
        if got != EXPECTED[label]:
            raise ValueError(f"{label} SHA mismatch {got} != {EXPECTED[label]}")
        print(label, path.stat().st_size, got, flush=True)

    modules = parse_gmt(a.gmt)
    c1_probe_ids, c1_mask, core_raw = load_c1_support(a.c1_flags, a.c1_map)

    primary_parts = cfg["primary_450k"]["selected_participants"]
    full32_parts = cfg["primary_450k"]["complete_pair_pool"]
    epic_parts = cfg["epic_sensitivity"]["participants"]

    m30 = read_external_methylation(a.m450, c1_probe_ids, primary_parts)
    r30 = read_external_rna(a.rna, primary_parts, modules)
    primary, primary_nulls, primary_diag = run_architecture_lane(
        m30["tumor"], m30["normal"], c1_probe_ids, c1_mask, r30["tumor"], r30["genes"],
        core_raw, modules, ns, "PRIMARY_450K_N30", a.workers
    )

    m32 = read_external_methylation(a.m450, c1_probe_ids, full32_parts)
    r32 = read_external_rna(a.rna, full32_parts, modules)
    full32, full32_nulls, full32_diag = run_architecture_lane(
        m32["tumor"], m32["normal"], c1_probe_ids, c1_mask, r32["tumor"], r32["genes"],
        core_raw, modules, ns, "SENSITIVITY_450K_N32", a.workers
    )

    me = read_external_methylation(a.epic, c1_probe_ids, epic_parts)
    re = read_external_rna(a.rna, epic_parts, modules)
    epic, epic_nulls, epic_diag = run_architecture_lane(
        me["tumor"], me["normal"], c1_probe_ids, c1_mask, re["tumor"], re["genes"],
        core_raw, modules, ns, "SENSITIVITY_EPIC_N26", a.workers
    )

    rna_tn_rows, rna_tn_nulls = rna_tn_test(r30["tumor"], r30["normal"], r30["genes"], modules, ns)

    primary_outcome = primary_class(primary)
    tech_issues = conflict(primary, {"PRIMARY_PUBLICATION": primary["MASKED_TECHNICAL"]})
    full32_issues = conflict(primary, full32)
    epic_issues = conflict(primary, epic)
    final_outcome = primary_outcome
    if tech_issues or full32_issues or epic_issues:
        final_outcome = "P1_REPRESENTATION_DEPENDENT"

    pd.DataFrame(flatten_endpoint_rows(primary)).to_csv(a.out/"P1_PRIMARY_450K_N30_ENDPOINTS.csv", index=False)
    pd.DataFrame(flatten_endpoint_rows(full32)).to_csv(a.out/"P1_SENSITIVITY_450K_N32_ENDPOINTS.csv", index=False)
    pd.DataFrame(flatten_endpoint_rows(epic)).to_csv(a.out/"P1_SENSITIVITY_EPIC_N26_ENDPOINTS.csv", index=False)
    pd.DataFrame(rna_tn_rows).to_csv(a.out/"P1_SECONDARY_RNA_TUMOR_NORMAL.csv", index=False)

    np.savez_compressed(
        a.out/"P1_PRIMARY_NULL_DISTRIBUTIONS.npz",
        **{f"{tr}_{e}": arr for tr,z in primary_nulls.items() for e,arr in z.items()}
    )

    summary = {
        "schema":"gri-biosystems-external-prostate-p1-v1",
        "status":"COMPLETE",
        "molecular_outcome_opened":True,
        "primary_outcome_before_sensitivity_adjudication":primary_outcome,
        "final_outcome":final_outcome,
        "primary_endpoints":primary["PRIMARY_PUBLICATION"],
        "technical_track":primary["MASKED_TECHNICAL"],
        "primary_diagnostics":primary_diag,
        "full32_diagnostics":full32_diag,
        "epic_diagnostics":epic_diag,
        "sensitivity_conflicts":{
            "masked_technical":tech_issues,
            "full_n32":full32_issues,
            "epic_n26":epic_issues,
        },
        "secondary_rna_tumor_normal":rna_tn_rows,
        "rna_normalization":{
            "primary_size_factor_genes":r30["size_factor_gene_count"],
            "primary_hallmark_union_genes":r30["hallmark_union_genes"],
            "full32_size_factor_genes":r32["size_factor_gene_count"],
            "epic_size_factor_genes":re["size_factor_gene_count"],
        },
        "source_sha256":EXPECTED,
        "seed_namespace":ns,
        "B":B,
        "claim_ceiling":"independent external static architecture transport; no biological chi, causal direction, recovery, clinical utility, or universal boundary",
    }
    (a.out/"P1_RUN_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
