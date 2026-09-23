#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, csv, gzip, hashlib, itertools, json, lzma, math, re
from pathlib import Path

import numpy as np
import pandas as pd

C1_SHA = "589365b92797f6e0ea479b75437c44ed86327cfc86b3e7caf7df01b4be2bcdd9"
METH_SHA = "65ee8783e9d47f568a94a35944719c1aae1df0c693150dd2bcdba44b876c55ad"
RNA_SHA = "1cbd6826074498a57025124da0a2857f1248338b21aaf1e3034cea48c7f68397"
GTF_SHA = "4e8afc75f90821668b0a8f45a33c31a792b4b4f754621d76ad9e50b0492a3a89"
NS = "BIOSYSTEMS_HCI005_DECITABINE_INTERVENTION_V01"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def stable_seed(*tokens) -> int:
    s = "|".join([NS] + [str(x) for x in tokens]).encode()
    return int.from_bytes(hashlib.sha256(s).digest()[:8], "big") % (2**32)

def spearman(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    good = np.isfinite(x) & np.isfinite(y)
    if int(good.sum()) < 10:
        return float("nan")
    xr = pd.Series(x[good]).rank(method="average").to_numpy(float)
    yr = pd.Series(y[good]).rank(method="average").to_numpy(float)
    if np.std(xr) == 0 or np.std(yr) == 0:
        return float("nan")
    return float(np.corrcoef(xr, yr)[0, 1])

def load_c1_support(probe_path: Path, support_path: Path):
    if sha256_file(probe_path) != C1_SHA:
        raise SystemExit("C1_PROBE_SHA_MISMATCH")
    probe_ids = [x.strip() for x in probe_path.read_text().splitlines() if x.strip()]
    if len(probe_ids) != 22601 or len(set(probe_ids)) != 22601:
        raise SystemExit("C1_PROBE_CARRIER_DRIFT")
    raw = lzma.decompress(base64.b64decode(support_path.read_bytes()))
    lines = raw.decode("utf-8").splitlines()
    if not lines or lines[0] != "CORE" or "MASK" not in lines:
        raise SystemExit("SUPPORT_SCHEMA_DRIFT")
    k = lines.index("MASK")
    core = {}
    for line in lines[1:k]:
        if not line:
            continue
        pid, genes = line.split("\t", 1)
        core[pid] = [g for g in genes.split(";") if g]
    return probe_ids, core, hashlib.sha256(support_path.read_bytes()).hexdigest(), hashlib.sha256(raw).hexdigest()

def gencode_map(path: Path):
    if sha256_file(path) != GTF_SHA:
        raise SystemExit("GENCODE_V33_SHA_MISMATCH")
    pat_id = re.compile(r'gene_id "([^"]+)"')
    pat_name = re.compile(r'gene_name "([^"]+)"')
    out = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line or line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 9 or p[2] != "gene":
                continue
            mi = pat_id.search(p[8]); mn = pat_name.search(p[8])
            if mi and mn:
                out[mi.group(1).split(".")[0]] = mn.group(1)
    if len(out) < 50000:
        raise SystemExit(f"GENCODE_MAP_TOO_SMALL {len(out)}")
    return out

def read_methylation(path: Path, gsms: list[str], required: list[str]):
    if sha256_file(path) != METH_SHA:
        raise SystemExit("METHYLATION_SHA_MISMATCH")
    target = set(required)
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as f:
        header = None
        idx = None
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                header = next(csv.reader([next(f).rstrip("\r\n")], delimiter="\t", quotechar='"'))
                pos = {h: i for i, h in enumerate(header)}
                miss = [g for g in gsms if g not in pos]
                if miss:
                    raise SystemExit(f"METH_GSM_MISSING {miss}")
                idx = [pos[g] for g in gsms]
                break
        if header is None:
            raise SystemExit("METH_TABLE_HEADER_NOT_FOUND")
        for line in f:
            if line.startswith("!series_matrix_table_end"):
                break
            parts = next(csv.reader([line.rstrip("\r\n")], delimiter="\t", quotechar='"'))
            if not parts:
                continue
            pid = parts[0]
            if pid not in target:
                continue
            vals = []
            for j in idx:
                try:
                    vals.append(float(parts[j]))
                except Exception:
                    vals.append(np.nan)
            rows[pid] = vals
    keep = [p for p in required if p in rows]
    x = np.asarray([rows[p] for p in keep], float).T
    finite = np.all(np.isfinite(x), axis=0)
    keep = np.asarray(keep, dtype=object)[finite]
    x = x[:, finite]
    if len(keep) < 15000:
        raise SystemExit(f"LOW_FINITE_C1_SUPPORT {len(keep)}")
    return keep, x

def read_rna(path: Path, columns: list[str], gene_map: dict[str, str]):
    if sha256_file(path) != RNA_SHA:
        raise SystemExit("RNA_SHA_MISMATCH")
    df = pd.read_csv(path, sep="\t", compression="gzip", low_memory=False)
    if "gene/TE" not in df.columns:
        raise SystemExit("RNA_ID_COLUMN_MISSING")
    miss = [c for c in columns if c not in df.columns]
    if miss:
        raise SystemExit(f"RNA_SAMPLE_COLUMN_MISSING {miss}")
    ids = df["gene/TE"].astype(str).str.split(".", n=1, regex=False).str[0]
    syms = ids.map(gene_map)
    vals = df[columns].apply(pd.to_numeric, errors="coerce")
    tmp = vals.copy()
    tmp.insert(0, "symbol", syms)
    tmp = tmp.loc[tmp["symbol"].notna() & (tmp["symbol"].astype(str) != "")]
    # Raw count data are additive: sum Ensembl rows mapping to the same symbol.
    agg = tmp.groupby("symbol", sort=True)[columns].sum(min_count=1)
    x = agg.to_numpy(float).T  # samples x symbols
    if not np.all(np.isfinite(x) & (x >= 0)):
        raise SystemExit("RNA_INVALID_COUNTS")
    positive = np.all(x > 0, axis=0)
    if int(positive.sum()) < 5000:
        raise SystemExit(f"TOO_FEW_SIZE_FACTOR_GENES {int(positive.sum())}")
    log_gm = np.mean(np.log(x[:, positive]), axis=0)
    gm = np.exp(log_gm)
    sf = np.median(x[:, positive] / gm[None, :], axis=1)
    if not np.all(np.isfinite(sf) & (sf > 0)):
        raise SystemExit("INVALID_SIZE_FACTORS")
    norm = x / sf[:, None]
    logx = np.log2(norm + 1.0)
    return agg.index.to_numpy(dtype=object), logx, sf, int(positive.sum())

def group_delta(mat, dec_idx):
    dec_idx = np.asarray(sorted(dec_idx), int)
    all_idx = np.arange(mat.shape[0])
    veh_idx = np.asarray([i for i in all_idx if i not in set(dec_idx.tolist())], int)
    return np.mean(mat[dec_idx], axis=0) - np.mean(mat[veh_idx], axis=0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", type=Path, required=True)
    ap.add_argument("--methylation", type=Path, required=True)
    ap.add_argument("--rna", type=Path, required=True)
    ap.add_argument("--gencode", type=Path, required=True)
    ap.add_argument("--c1-probes", type=Path, required=True)
    ap.add_argument("--support", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(a.freeze.read_text())
    probes, core, support_sha, support_raw_sha = load_c1_support(a.c1_probes, a.support)
    gm = gencode_map(a.gencode)

    reps = cfg["replicate_map"]
    meth_gsms = [r["methylation_gsm"] for r in reps]
    rna_cols = [r["rna_column"] for r in reps]
    observed_dec = tuple(i for i, r in enumerate(reps) if r["group"] == "Decitabine")
    if observed_dec != (4,5,6,7):
        raise SystemExit(f"GROUP_ORDER_DRIFT {observed_dec}")

    pids, meth = read_methylation(a.methylation, meth_gsms, probes)
    rna_genes, rna, size_factors, sf_gene_count = read_rna(a.rna, rna_cols, gm)

    # Build per-sample promoter-gene methylation matrix.
    pidx = {str(p): i for i, p in enumerate(pids)}
    gene_to_probe = {}
    for pid, genes in core.items():
        j = pidx.get(pid)
        if j is None:
            continue
        for g in genes:
            gene_to_probe.setdefault(g, []).append(j)

    ridx = {str(g): i for i, g in enumerate(rna_genes)}
    common = sorted(set(gene_to_probe) & set(ridx))
    if len(common) < 2500:
        raise SystemExit(f"LOW_PROMOTER_RNA_OVERLAP {len(common)}")
    meth_gene = np.column_stack([
        np.median(meth[:, np.asarray(sorted(set(gene_to_probe[g])), int)], axis=1)
        for g in common
    ])
    rna_gene = np.column_stack([rna[:, ridx[g]] for g in common])

    # Observed global manipulation on the C1 carrier.
    meth_probe_delta = group_delta(meth, observed_dec)
    global_meth = float(np.median(meth_probe_delta))
    meth_gene_delta = group_delta(meth_gene, observed_dec)
    rna_gene_delta = group_delta(rna_gene, observed_dec)
    obs_rho = spearman(meth_gene_delta, rna_gene_delta)

    assignments = list(itertools.combinations(range(8), 4))
    global_null = []
    rho_treatment_null = []
    for dec in assignments:
        global_null.append(float(np.median(group_delta(meth, dec))))
        md = group_delta(meth_gene, dec)
        rd = group_delta(rna_gene, dec)
        rho_treatment_null.append(spearman(md, rd))
    global_null = np.asarray(global_null, float)
    rho_treatment_null = np.asarray(rho_treatment_null, float)
    p_global = float(np.mean(global_null <= global_meth + 1e-15))
    p_treatment = float(np.mean(rho_treatment_null <= obs_rho + 1e-15))

    # Identity null destroys gene matching while preserving each marginal intervention effect vector.
    B = 9999
    null_identity = np.empty(B, float)
    for b in range(B):
        rng = np.random.default_rng(stable_seed("GENE_IDENTITY", b))
        null_identity[b] = spearman(meth_gene_delta, rna_gene_delta[rng.permutation(len(common))])
    p_identity = float((1 + np.sum(null_identity <= obs_rho)) / (B + 1))

    manip_pass = bool(global_meth < 0 and p_global <= 0.05)
    coupling_pass = bool(
        manip_pass and obs_rho < 0 and p_identity <= 0.05 and p_treatment <= 0.05
    )
    status = "INTERVENTION_CONSISTENT_COUPLING_SUPPORTED" if coupling_pass else "INTERVENTION_COUPLING_NOT_SUPPORTED"

    pd.DataFrame({
        "gene": common,
        "promoter_methylation_delta_dec_minus_vehicle": meth_gene_delta,
        "rna_delta_dec_minus_vehicle": rna_gene_delta,
    }).to_csv(a.out / "HCI005_DECITABINE_GENE_DELTAS_V01.csv", index=False)

    out = {
        "schema_version":"0.1",
        "status":status,
        "source_sha256":{
            "methylation":sha256_file(a.methylation),
            "rna":sha256_file(a.rna),
            "gencode_v33":sha256_file(a.gencode),
            "c1_probe_carrier":sha256_file(a.c1_probes),
            "support_payload":support_sha,
            "support_decoded":support_raw_sha,
        },
        "retained_c1_probe_count":int(len(pids)),
        "rna_symbol_count":int(len(rna_genes)),
        "rna_size_factor_gene_count":sf_gene_count,
        "analysis_gene_count":int(len(common)),
        "size_factors":size_factors.tolist(),
        "global_c1_methylation_delta_dec_minus_vehicle":global_meth,
        "global_methylation_exact_p_lower":p_global,
        "global_methylation_assignment_count":len(assignments),
        "methylation_manipulation_support":manip_pass,
        "gene_matched_spearman_rho":obs_rho,
        "gene_identity_permutation_p_lower":p_identity,
        "gene_identity_B":B,
        "treatment_assignment_exact_p_lower":p_treatment,
        "treatment_assignment_count":len(assignments),
        "coupling_support":coupling_pass,
        "claim_ceiling":cfg["claim_ceiling"],
    }
    (a.out / "HCI005_DECITABINE_INTERVENTION_RESULT_V01.json").write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
