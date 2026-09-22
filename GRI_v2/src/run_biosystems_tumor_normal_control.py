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

from src import biosystems_tumor_normal_core as core


NA_VALUES = ["", "NA", "N/A", "NaN", "nan", "NULL", "null"]


def normalize_label(x: str) -> str:
    return str(x).strip().strip('"').upper().replace(".", "-")


def parse_gene_symbol(raw: str) -> str:
    return str(raw).strip().strip('"').split("|", 1)[0].strip()


def json_write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", errors="strict") as fh:
        line = fh.readline()
    if not line:
        raise ValueError(f"empty source: {path}")
    return [normalize_label(x) for x in line.rstrip("\r\n").split("\t")]


def unique_header_positions(header: list[str], labels: list[str]) -> dict[str, int]:
    positions: dict[str, list[int]] = {}
    for i, value in enumerate(header):
        positions.setdefault(value, []).append(i)
    out: dict[str, int] = {}
    for raw in labels:
        lab = normalize_label(raw)
        idx = positions.get(lab, [])
        if len(idx) != 1:
            raise ValueError(f"source label {lab} has {len(idx)} header positions")
        out[lab] = idx[0]
    return out


def prepare_selected_samples(pair_manifest: Path, sample_manifest: Path, cfg: dict):
    pairs = pd.read_csv(pair_manifest, dtype=str)
    samples = pd.read_csv(sample_manifest, dtype=str)
    for df in (pairs, samples):
        for col in ["cancer_type", "patient_id"]:
            df[col] = df[col].astype(str).str.upper()
    samples["sample_type"] = samples["sample_type"].astype(str).str.zfill(2)

    primary = set(cfg["primary_paired"]["cancers"])
    secondary = set(cfg["secondary_unpaired_n30"]["cancers"])

    primary_ids = set(
        zip(
            pairs.loc[pairs["cancer_type"].isin(primary), "cancer_type"],
            pairs.loc[pairs["cancer_type"].isin(primary), "patient_id"],
        )
    )
    keep = []
    for row in samples.itertuples(index=False):
        key = (row.cancer_type, row.patient_id)
        ok_primary = row.cancer_type in primary and key in primary_ids
        ok_secondary = row.cancer_type in secondary
        keep.append(bool(ok_primary or ok_secondary))
    selected = samples.loc[np.asarray(keep, dtype=bool)].copy()
    selected = selected.sort_values(["cancer_type", "sample_type", "patient_id"], kind="mergesort").reset_index(drop=True)
    if selected.duplicated(["cancer_type", "patient_id", "sample_type"]).any():
        raise ValueError("selected exact sample manifest is not unique by cancer/patient/sample_type")
    selected["row_index"] = np.arange(len(selected), dtype=int)

    key_index = {
        (r.cancer_type, r.patient_id, r.sample_type): int(r.row_index)
        for r in selected.itertuples(index=False)
    }
    return pairs, samples, selected, key_index


def source_column_binding(path: Path, selected: pd.DataFrame, label_col: str):
    header = read_header(path)
    labels = selected[label_col].astype(str).map(normalize_label).tolist()
    pos_map = unique_header_positions(header, labels)
    binding = []
    for r in selected.itertuples(index=False):
        label = normalize_label(getattr(r, label_col))
        binding.append((pos_map[label], int(r.row_index), label))
    binding.sort()
    return header, binding


def load_methylation(path: Path, selected: pd.DataFrame, expected_rows: int):
    _, binding = source_column_binding(path, selected, "methylation_label")
    positions = [0] + [x[0] for x in binding]
    source_rows_to_selected = np.asarray([x[1] for x in binding], dtype=int)
    out = np.empty((len(selected), int(expected_rows)), dtype=np.float64)
    probe_ids: list[str] = []
    done = 0
    reader = pd.read_csv(
        path,
        sep="\t",
        usecols=positions,
        chunksize=64,
        engine="c",
        low_memory=False,
        na_values=NA_VALUES,
        keep_default_na=True,
    )
    for chunk in reader:
        n = len(chunk)
        ids = chunk.iloc[:, 0].astype(str).str.strip().str.strip('"').tolist()
        vals = chunk.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float).T
        finite = np.isfinite(vals)
        if finite.any():
            mn = float(vals[finite].min())
            mx = float(vals[finite].max())
            if mn < 0 or mx > 1:
                raise ValueError(f"methylation beta outside [0,1] in rows {done}:{done+n}: [{mn},{mx}]")
        out[source_rows_to_selected, done:done+n] = vals
        probe_ids.extend(ids)
        done += n
    if done != int(expected_rows):
        raise ValueError(f"methylation row count {done} != {expected_rows}")
    if len(set(probe_ids)) != len(probe_ids):
        raise ValueError("methylation probe IDs are not unique")
    return out, np.asarray(probe_ids, dtype=str)


def load_rna(path: Path, selected: pd.DataFrame, hallmark_union: set[str], expected_genes: int | None):
    _, binding = source_column_binding(path, selected, "rna_label")
    positions = [0] + [x[0] for x in binding]
    source_rows_to_selected = np.asarray([x[1] for x in binding], dtype=int)
    seen: set[str] = set()
    genes: list[str] = []
    blocks: list[np.ndarray] = []

    reader = pd.read_csv(
        path,
        sep="\t",
        usecols=positions,
        chunksize=64,
        engine="c",
        low_memory=False,
        na_values=NA_VALUES,
        keep_default_na=True,
    )
    for chunk in reader:
        raw_ids = chunk.iloc[:, 0].astype(str).tolist()
        wanted_rows = []
        wanted_genes = []
        for i, raw in enumerate(raw_ids):
            gene = parse_gene_symbol(raw)
            if gene in hallmark_union and gene not in seen:
                seen.add(gene)
                wanted_rows.append(i)
                wanted_genes.append(gene)
        if not wanted_rows:
            continue
        vals = chunk.iloc[wanted_rows, 1:].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
        finite = np.isfinite(vals)
        clipped = np.where(finite, np.maximum(vals, 0.0), np.nan)
        vals = np.where(finite, np.log2(clipped + 1.0), np.nan)
        canonical = np.empty((len(selected), len(wanted_rows)), dtype=np.float64)
        canonical[source_rows_to_selected, :] = vals.T
        blocks.append(canonical)
        genes.extend(wanted_genes)

    if not blocks:
        raise ValueError("no Hallmark-union RNA genes found")
    out = np.column_stack(blocks)
    if expected_genes is not None and out.shape[1] != int(expected_genes):
        raise ValueError(f"Hallmark-union source gene count {out.shape[1]} != frozen expected {expected_genes}")
    if len(set(genes)) != len(genes):
        raise ValueError("RNA Hallmark-union gene symbols are not unique after first-occurrence rule")
    return out, np.asarray(genes, dtype=str)


def cohort_rows_primary(pairs: pd.DataFrame, key_index: dict, cancer: str, sample_type: str):
    pids = sorted(pairs.loc[pairs["cancer_type"].eq(cancer), "patient_id"].astype(str).str.upper().tolist())
    rows = np.asarray([key_index[(cancer, p, sample_type)] for p in pids], dtype=int)
    return pids, rows


def cohort_rows_secondary(samples: pd.DataFrame, key_index: dict, cancer: str, sample_type: str):
    s = samples[(samples["cancer_type"].eq(cancer)) & (samples["sample_type"].eq(sample_type))]
    pids = sorted(s["patient_id"].astype(str).str.upper().tolist())
    rows = np.asarray([key_index[(cancer, p, sample_type)] for p in pids], dtype=int)
    return pids, rows


def feature_carriers(meth: np.ndarray, rna: np.ndarray, tumor_rows: np.ndarray, normal_rows: np.ndarray,
                     technical_mask: np.ndarray, cfg: dict):
    fr = cfg["feature_rules"]
    mt = meth[tumor_rows, :]
    mn = meth[normal_rows, :]
    mft = np.isfinite(mt).mean(axis=0)
    mfn = np.isfinite(mn).mean(axis=0)
    with np.errstate(all="ignore"):
        med_t = np.nanmedian(mt, axis=0)
        med_n = np.nanmedian(mn, axis=0)
    shared_meth = (
        (mft >= float(fr["methylation_finite_fraction_min"]))
        & (mfn >= float(fr["methylation_finite_fraction_min"]))
        & np.isfinite(med_t)
        & np.isfinite(med_n)
    )

    rt = rna[tumor_rows, :]
    rn = rna[normal_rows, :]
    rft = np.isfinite(rt).mean(axis=0)
    rfn = np.isfinite(rn).mean(axis=0)
    with np.errstate(all="ignore"):
        sdt = np.nanstd(rt, axis=0, ddof=1)
        sdn = np.nanstd(rn, axis=0, ddof=1)
    shared_rna = (
        (rft >= float(fr["rna_finite_fraction_min"]))
        & (rfn >= float(fr["rna_finite_fraction_min"]))
        & np.isfinite(sdt)
        & np.isfinite(sdn)
        & (sdt > 0)
        & (sdn > 0)
    )
    tracks = {
        "PRIMARY_PUBLICATION": shared_meth,
        "MASKED_TECHNICAL": shared_meth & (~technical_mask),
    }
    return tracks, shared_rna, med_t, med_n


def build_gene_map(map_df: pd.DataFrame, probe_index: dict[str, int], track_mask: np.ndarray,
                   promoter_groups: set[str]):
    source_idx = np.flatnonzero(track_mask)
    global_to_local = np.full(len(track_mask), -1, dtype=int)
    global_to_local[source_idx] = np.arange(len(source_idx), dtype=int)
    g = map_df[map_df["refgene_group"].isin(promoter_groups)].copy()
    out: dict[str, np.ndarray] = {}
    for gene, gg in g.groupby("gene_symbol", sort=False):
        loc = []
        for pid in dict.fromkeys(gg["probe_id"].astype(str).tolist()):
            j = probe_index.get(pid)
            if j is not None and track_mask[j]:
                loc.append(int(global_to_local[j]))
        if loc:
            out[str(gene)] = np.asarray(sorted(set(loc)), dtype=int)
    return out


def build_hallmark_scores(beta_draw: np.ndarray, rna_draw: np.ndarray, gene_map: dict[str, np.ndarray],
                          modules: dict[str, list[str]], rna_gene_index: dict[str, int], cfg: dict):
    fr = cfg["feature_rules"]
    meth_scores: dict[str, np.ndarray] = {}
    rna_scores: dict[str, np.ndarray] = {}
    meta: dict[str, dict] = {}
    for hall in sorted(modules):
        mats = []
        used_genes = []
        used_probes: set[int] = set()
        for gene in modules[hall]:
            loc = gene_map.get(gene)
            if loc is None or len(loc) == 0:
                continue
            mats.append(np.median(beta_draw[:, loc], axis=1))
            used_genes.append(gene)
            used_probes.update(map(int, loc.tolist()))
        if (
            len(used_genes) < int(fr["methylation_minimum_hallmark_genes"])
            or len(used_probes) < int(fr["methylation_minimum_hallmark_probes"])
        ):
            continue
        rgenes = [g for g in modules[hall] if g in rna_gene_index]
        if not rgenes:
            continue
        raw = rna_draw[:, [rna_gene_index[g] for g in rgenes]]
        try:
            me, _ = core.methylation_pc1(np.column_stack(mats))
            re, n_rna, imp = core.rna_hallmark_pc1(
                raw,
                minimum_genes=int(fr["rna_minimum_hallmark_genes"]),
                finite_fraction=float(fr["rna_finite_fraction_min"]),
                minimum_finite=int(fr["rna_minimum_finite"]),
            )
        except ValueError:
            continue
        meth_scores[hall] = me
        rna_scores[hall] = re
        meta[hall] = {
            "methylation_genes": len(used_genes),
            "methylation_probes": len(used_probes),
            "rna_genes": int(n_rna),
            "rna_pc1_imputed_fraction": float(imp),
        }
    return meth_scores, rna_scores, meta


def choose_members(rng: np.random.Generator, pids: list[str], n: int) -> list[str]:
    if len(pids) < int(n):
        raise ValueError(f"cohort n={len(pids)} below required {n}")
    if len(pids) == int(n):
        return list(pids)
    idx = np.sort(rng.choice(len(pids), size=int(n), replace=False))
    return [pids[int(i)] for i in idx]


def draw_memberships(mode: str, cancer: str, tumor_pids: list[str], normal_pids: list[str],
                     cfg: dict):
    block = cfg["primary_paired"] if mode == "PRIMARY_PAIRED" else cfg["secondary_unpaired_n30"]
    n = int(block["fixed_n"])
    reps = int(block["resamples"])
    ns = cfg["seed_namespace"]
    rows = []
    for rep in range(reps):
        if mode == "PRIMARY_PAIRED":
            if tumor_pids != normal_pids:
                raise ValueError(f"{cancer}: primary paired patient lists differ")
            rng = np.random.default_rng(core.stable_seed(ns, mode, cancer, rep, "paired_membership"))
            tp = choose_members(rng, tumor_pids, n)
            npids = list(tp)
        else:
            rt = np.random.default_rng(core.stable_seed(ns, mode, cancer, rep, "tumor_membership"))
            rn = np.random.default_rng(core.stable_seed(ns, mode, cancer, rep, "normal_membership"))
            tp = choose_members(rt, tumor_pids, n)
            npids = choose_members(rn, normal_pids, n)
        rows.append((rep, tp, npids))
    return rows


def summarize_group(g: pd.DataFrame, expected_draws: int):
    endpoints = ["tn_h2_headroom_diff", "tn_h3a_excess_diff"]
    row = {
        "mode": str(g["mode"].iloc[0]),
        "cancer_type": str(g["cancer_type"].iloc[0]),
        "track": str(g["track"].iloc[0]),
        "draws_total": int(len(g)),
    }
    for ep in endpoints:
        vals = pd.to_numeric(g[ep], errors="coerce").to_numpy(float)
        good = vals[np.isfinite(vals)]
        row[f"{ep}_valid_draws"] = int(len(good))
        if len(good) == expected_draws:
            row[f"{ep}_median"] = float(np.median(good))
            row[f"{ep}_q05"] = float(np.quantile(good, 0.05))
            row[f"{ep}_q95"] = float(np.quantile(good, 0.95))
        else:
            row[f"{ep}_median"] = np.nan
            row[f"{ep}_q05"] = np.nan
            row[f"{ep}_q95"] = np.nan
    return row


def primary_inference(summary: pd.DataFrame, cfg: dict):
    primary = summary[
        summary["mode"].eq("PRIMARY_PAIRED") & summary["track"].eq("PRIMARY_PUBLICATION")
    ].copy()
    expected_cancers = list(cfg["primary_paired"]["cancers"])
    if sorted(primary["cancer_type"].tolist()) != sorted(expected_cancers):
        raise ValueError("primary cancer summary set drift")
    endpoint_fields = [
        ("TN_H2_HEADROOM", "tn_h2_headroom_diff_median"),
        ("TN_H3A_PATIENT_NULL_EXCESS", "tn_h3a_excess_diff_median"),
    ]
    rows = []
    pvals = []
    for name, field in endpoint_fields:
        vals = pd.to_numeric(primary[field], errors="coerce").to_numpy(float)
        fully = bool(np.isfinite(vals).all())
        if fully:
            pos, neg, ties, p = core.exact_sign_test_two_sided(vals)
            med = float(np.median(vals))
            status = "EVALUABLE"
        else:
            pos = neg = ties = 0
            p = float("nan")
            med = float("nan")
            status = "INDETERMINATE_SUPPORT"
        rows.append({
            "endpoint": name,
            "status": status,
            "cancers_expected": len(expected_cancers),
            "cancers_evaluable": int(np.isfinite(vals).sum()),
            "positive_cancers": int(pos),
            "negative_cancers": int(neg),
            "ties": int(ties),
            "pan_cancer_median_tumor_minus_normal": med,
            "exact_two_sided_sign_p": p,
        })
        pvals.append(p)
    q = core.bh_fdr(pvals)
    for row, qq in zip(rows, q):
        row["bh_q_two_primary_endpoints"] = float(qq) if np.isfinite(qq) else np.nan
        if row["status"] != "EVALUABLE":
            row["disposition"] = "INDETERMINATE_SUPPORT"
        elif float(qq) < float(cfg["inference"]["alpha"]):
            if row["pan_cancer_median_tumor_minus_normal"] > 0:
                row["disposition"] = "TUMOR_ASSOCIATED_STRENGTHENING_OR_REORGANIZATION"
            elif row["pan_cancer_median_tumor_minus_normal"] < 0:
                row["disposition"] = "TUMOR_ASSOCIATED_WEAKENING_OR_DISORGANIZATION"
            else:
                row["disposition"] = "NO_DIRECTIONAL_DIFFERENCE"
        else:
            row["disposition"] = "PAN_CANCER_DIRECTIONAL_SPECIFICITY_NOT_SUPPORTED"
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--pair-manifest", required=True)
    ap.add_argument("--sample-manifest", required=True)
    ap.add_argument("--rna-source", required=True)
    ap.add_argument("--methylation-source", required=True)
    ap.add_argument("--gmt", required=True)
    ap.add_argument("--probe-flags", required=True)
    ap.add_argument("--probe-map", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rna_path = Path(args.rna_source)
    meth_path = Path(args.methylation_source)
    gmt_path = Path(args.gmt)
    flags_path = Path(args.probe_flags)
    map_path = Path(args.probe_map)

    observed_hashes = {
        "rna": core.sha256_file(rna_path),
        "methylation": core.sha256_file(meth_path),
        "hallmark": core.sha256_file(gmt_path),
        "probe_flags": core.sha256_file(flags_path),
        "probe_map": core.sha256_file(map_path),
    }
    expected = cfg["source_bindings"]
    if observed_hashes["rna"] != expected["rna"]["sha256"]:
        raise SystemExit("RNA source hash mismatch")
    if observed_hashes["methylation"] != expected["methylation"]["sha256"]:
        raise SystemExit("methylation source hash mismatch")
    if observed_hashes["hallmark"] != expected["hallmark"]["raw_sha256"]:
        raise SystemExit("Hallmark GMT hash mismatch")
    if observed_hashes["probe_flags"] != expected["annotation"]["probe_flags_sha256"]:
        raise SystemExit("probe-flags hash mismatch")
    if observed_hashes["probe_map"] != expected["annotation"]["probe_gene_region_map_sha256"]:
        raise SystemExit("probe-map hash mismatch")

    modules = core.parse_gmt(gmt_path)
    hallmark_union = set()
    for genes in modules.values():
        hallmark_union.update(genes)

    pairs, samples, selected, key_index = prepare_selected_samples(
        Path(args.pair_manifest), Path(args.sample_manifest), cfg
    )

    meth, probe_ids = load_methylation(
        meth_path, selected, int(expected["methylation"]["expected_probe_rows"])
    )
    rna, rna_genes = load_rna(
        rna_path, selected, hallmark_union, cfg["feature_rules"].get("expected_hallmark_union_source_genes")
    )

    flags = pd.read_csv(flags_path, compression="gzip")
    if not np.array_equal(flags["probe_id"].astype(str).to_numpy(), probe_ids):
        raise ValueError("probe flag/source row order mismatch")
    technical_mask = pd.to_numeric(flags["technical_mask_union"], errors="raise").astype(bool).to_numpy()
    map_df = pd.read_csv(map_path, compression="gzip", dtype=str).fillna("")
    probe_index = {p: i for i, p in enumerate(probe_ids.tolist())}
    rna_gene_index = {g: i for i, g in enumerate(rna_genes.tolist())}

    draw_rows = []
    carrier_rows = []

    modes = [
        ("PRIMARY_PAIRED", cfg["primary_paired"]["cancers"]),
        ("SECONDARY_UNPAIRED_N30", cfg["secondary_unpaired_n30"]["cancers"]),
    ]
    for mode, cancers in modes:
        for cancer in cancers:
            if mode == "PRIMARY_PAIRED":
                tumor_pids, tumor_cohort = cohort_rows_primary(pairs, key_index, cancer, "01")
                normal_pids, normal_cohort = cohort_rows_primary(pairs, key_index, cancer, "11")
            else:
                tumor_pids, tumor_cohort = cohort_rows_secondary(samples, key_index, cancer, "01")
                normal_pids, normal_cohort = cohort_rows_secondary(samples, key_index, cancer, "11")

            tracks, shared_rna, med_t, med_n = feature_carriers(
                meth, rna, tumor_cohort, normal_cohort, technical_mask, cfg
            )
            carrier_rows.append({
                "mode": mode,
                "cancer_type": cancer,
                "tumor_source_cohort_n": len(tumor_pids),
                "normal_source_cohort_n": len(normal_pids),
                "shared_rna_h2_genes": int(shared_rna.sum()),
                "shared_methylation_primary_probes": int(tracks["PRIMARY_PUBLICATION"].sum()),
                "shared_methylation_masked_probes": int(tracks["MASKED_TECHNICAL"].sum()),
            })

            memberships = draw_memberships(mode, cancer, tumor_pids, normal_pids, cfg)
            for track, track_mask in tracks.items():
                if int(track_mask.sum()) < 2:
                    raise ValueError(f"{mode}/{cancer}/{track}: fewer than two methylation probes")
                source_idx = np.flatnonzero(track_mask)
                gene_map = build_gene_map(
                    map_df,
                    probe_index,
                    track_mask,
                    set(cfg["feature_rules"]["promoter_core_groups"]),
                )

                for rep, tpids, npids in memberships:
                    trows = np.asarray([key_index[(cancer, p, "01")] for p in tpids], dtype=int)
                    nrows = np.asarray([key_index[(cancer, p, "11")] for p in npids], dtype=int)
                    n = len(trows)
                    if len(nrows) != n:
                        raise ValueError("tumor/normal draw size mismatch")

                    bt = core.median_impute(meth[np.ix_(trows, source_idx)], med_t[source_idx])
                    bn = core.median_impute(meth[np.ix_(nrows, source_idx)], med_n[source_idx])
                    rt_h2 = rna[np.ix_(trows, np.flatnonzero(shared_rna))]
                    rn_h2 = rna[np.ix_(nrows, np.flatnonzero(shared_rna))]
                    xrt = core.center_rna_missing(rt_h2)
                    xrn = core.center_rna_missing(rn_h2)
                    xmt = bt - bt.mean(axis=0, keepdims=True)
                    xmn = bn - bn.mean(axis=0, keepdims=True)

                    kmt = core.centered_kernel(xmt)
                    kmn = core.centered_kernel(xmn)
                    krt = core.centered_kernel(xrt)
                    krn = core.centered_kernel(xrn)
                    h2_t = core.cka_kernels(kmt, krt)
                    h2_n = core.cka_kernels(kmn, krn)
                    bnull = int(cfg["nulls"]["permutations"])
                    pt = core.permutation_matrix(cfg["seed_namespace"], cancer, f"{mode}:{track}:TUMOR", rep, "H2", n, bnull)
                    pn = core.permutation_matrix(cfg["seed_namespace"], cancer, f"{mode}:{track}:NORMAL", rep, "H2", n, bnull)
                    h2null_t = core.cka_row_perm_nulls(kmt, krt, pt)
                    h2null_n = core.cka_row_perm_nulls(kmn, krn, pn)
                    h2med_t = float(np.nanmedian(h2null_t))
                    h2med_n = float(np.nanmedian(h2null_n))
                    h2head_t = core.h2_headroom(h2_t, h2med_t)
                    h2head_n = core.h2_headroom(h2_n, h2med_n)

                    rtd = rna[trows, :]
                    rnd = rna[nrows, :]
                    mts, rts, _ = build_hallmark_scores(bt, rtd, gene_map, modules, rna_gene_index, cfg)
                    mns, rns, _ = build_hallmark_scores(bn, rnd, gene_map, modules, rna_gene_index, cfg)
                    common = sorted(set(mts) & set(rts) & set(mns) & set(rns))
                    min_common = int(cfg["feature_rules"]["minimum_common_hallmarks"])
                    if len(common) >= min_common:
                        mtm = np.column_stack([mts[h] for h in common])
                        rtm = np.column_stack([rts[h] for h in common])
                        mnm = np.column_stack([mns[h] for h in common])
                        rnm = np.column_stack([rns[h] for h in common])
                        h3_t = core.same_hallmark_fast(mtm, rtm)
                        h3_n = core.same_hallmark_fast(mnm, rnm)
                        h3pt = core.permutation_matrix(cfg["seed_namespace"], cancer, f"{mode}:{track}:TUMOR", rep, "H3A", n, bnull)
                        h3pn = core.permutation_matrix(cfg["seed_namespace"], cancer, f"{mode}:{track}:NORMAL", rep, "H3A", n, bnull)
                        h3null_t = core.same_hallmark_patient_nulls(mtm, rtm, h3pt)
                        h3null_n = core.same_hallmark_patient_nulls(mnm, rnm, h3pn)
                        h3ex_t = h3_t - float(np.nanmedian(h3null_t))
                        h3ex_n = h3_n - float(np.nanmedian(h3null_n))
                    else:
                        h3_t = h3_n = h3ex_t = h3ex_n = np.nan

                    draw_rows.append({
                        "mode": mode,
                        "cancer_type": cancer,
                        "track": track,
                        "resample": int(rep),
                        "n_tumor": int(n),
                        "n_normal": int(n),
                        "methylation_features": int(track_mask.sum()),
                        "rna_h2_features": int(shared_rna.sum()),
                        "h3_common_hallmarks": int(len(common)),
                        "h2_tumor_observed": float(h2_t),
                        "h2_tumor_null_median_B199": h2med_t,
                        "h2_tumor_null_mean_B199": float(np.nanmean(h2null_t)),
                        "h2_tumor_headroom": float(h2head_t),
                        "h2_normal_observed": float(h2_n),
                        "h2_normal_null_median_B199": h2med_n,
                        "h2_normal_null_mean_B199": float(np.nanmean(h2null_n)),
                        "h2_normal_headroom": float(h2head_n),
                        "tn_h2_headroom_diff": float(h2head_t - h2head_n),
                        "h3a_tumor_observed": float(h3_t) if np.isfinite(h3_t) else np.nan,
                        "h3a_tumor_excess_patient_null": float(h3ex_t) if np.isfinite(h3ex_t) else np.nan,
                        "h3a_normal_observed": float(h3_n) if np.isfinite(h3_n) else np.nan,
                        "h3a_normal_excess_patient_null": float(h3ex_n) if np.isfinite(h3ex_n) else np.nan,
                        "tn_h3a_excess_diff": float(h3ex_t - h3ex_n) if np.isfinite(h3ex_t) and np.isfinite(h3ex_n) else np.nan,
                        "tumor_participants": "|".join(tpids),
                        "normal_participants": "|".join(npids),
                    })

    draws = pd.DataFrame(draw_rows)
    carriers = pd.DataFrame(carrier_rows)
    draws.to_csv(outdir / "TUMOR_NORMAL_DRAW_RESULTS.csv.gz", index=False, compression="gzip")
    carriers.to_csv(outdir / "TUMOR_NORMAL_FEATURE_CARRIERS.csv", index=False)

    summary_rows = []
    for (mode, cancer, track), g in draws.groupby(["mode", "cancer_type", "track"], sort=True):
        expected_draws = (
            int(cfg["primary_paired"]["resamples"])
            if mode == "PRIMARY_PAIRED"
            else int(cfg["secondary_unpaired_n30"]["resamples"])
        )
        summary_rows.append(summarize_group(g, expected_draws))
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(outdir / "TUMOR_NORMAL_CANCER_SUMMARY.csv", index=False)

    inference = primary_inference(summary, cfg)
    inference.to_csv(outdir / "TUMOR_NORMAL_GLOBAL_INFERENCE.csv", index=False)

    primary_summary = summary[
        summary["mode"].eq("PRIMARY_PAIRED") & summary["track"].eq("PRIMARY_PUBLICATION")
    ][["cancer_type", "tn_h2_headroom_diff_median", "tn_h3a_excess_diff_median"]].copy()
    masked_summary = summary[
        summary["mode"].eq("PRIMARY_PAIRED") & summary["track"].eq("MASKED_TECHNICAL")
    ][["cancer_type", "tn_h2_headroom_diff_median", "tn_h3a_excess_diff_median"]].copy()
    dep = primary_summary.merge(masked_summary, on="cancer_type", suffixes=("_primary", "_masked"), validate="one_to_one")
    for ep in ["tn_h2_headroom_diff", "tn_h3a_excess_diff"]:
        a = pd.to_numeric(dep[f"{ep}_median_primary"], errors="coerce").to_numpy(float)
        b = pd.to_numeric(dep[f"{ep}_median_masked"], errors="coerce").to_numpy(float)
        dep[f"{ep}_sign_reversal"] = np.isfinite(a) & np.isfinite(b) & (np.sign(a) != np.sign(b)) & (a != 0) & (b != 0)
    dep.to_csv(outdir / "TUMOR_NORMAL_TECHNICAL_MASK_DEPENDENCE.csv", index=False)

    run_summary = {
        "schema": "gri-biosystems-tumor-normal-result-v1",
        "status": "COMPLETE" if len(draws) else "NO_RESULTS",
        "claim_ceiling": "tumor-versus-solid-tissue-normal architectural specificity only; no causality, diagnosis, prognosis, treatment response, biological chi, or external confirmation",
        "source_hashes": observed_hashes,
        "selected_sample_rows": int(len(selected)),
        "rna_hallmark_union_source_genes": int(len(rna_genes)),
        "methylation_probe_rows": int(len(probe_ids)),
        "primary_cancers": list(cfg["primary_paired"]["cancers"]),
        "secondary_cancers": list(cfg["secondary_unpaired_n30"]["cancers"]),
        "draw_result_rows": int(len(draws)),
        "primary_inference": inference.to_dict(orient="records"),
        "normal_architecture_allowed": True,
        "secondary_cannot_rescue_primary": True,
        "biological_chi_used": False,
        "external_confirmation_claimed": False,
    }
    json_write(outdir / "TUMOR_NORMAL_RUN_SUMMARY.json", run_summary)

    hash_rows = []
    for p in sorted(outdir.iterdir()):
        if p.is_file() and p.name != "TUMOR_NORMAL_OUTPUT_SHA256.json":
            hash_rows.append({"filename": p.name, "sha256": core.sha256_file(p), "bytes": p.stat().st_size})
    json_write(outdir / "TUMOR_NORMAL_OUTPUT_SHA256.json", {"files": hash_rows})
    print(json.dumps(run_summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
