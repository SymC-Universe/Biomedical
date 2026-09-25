#!/usr/bin/env python3
import gzip, hashlib, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cfg = json.loads((ROOT / "config" / "SHAFFER2017_GRI_BIOCHI_SOURCE_FREEZE_v0_1.json").read_text())
out = ROOT / "artifacts" / "generated"
out.mkdir(parents=True, exist_ok=True)

def download(url, p):
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(url, timeout=120) as r, open(p, "wb") as f:
        while True:
            b = r.read(1024 * 1024)
            if not b:
                break
            f.write(b)
            h.update(b)
            n += len(b)
    return h.hexdigest(), n

def inspect(path):
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        header = f.readline().rstrip("\n\r").split("\t")
        low = [x.strip('"').lower() for x in header]
        sample_cols = [i for i, x in enumerate(low) if any(k in x for k in ["sample", "condition", "name", "id"])]
        unique = {header[i]: set() for i in sample_cols}
        n = 0
        widths = {}
        for line in f:
            cols = line.rstrip("\n\r").split("\t")
            n += 1
            widths[len(cols)] = widths.get(len(cols), 0) + 1
            for i in sample_cols:
                if i < len(cols) and len(unique[header[i]]) < 500:
                    unique[header[i]].add(cols[i].strip('"'))
    return {
        "header": header,
        "row_count": n,
        "column_width_counts": widths,
        "candidate_sample_columns": {k: sorted(v) for k, v in unique.items()}
    }

records = []
for idx, url in enumerate(cfg["source"]["rna_processed_files"], start=1):
    p = out / ("_shaffer_rna_%d.tsv.gz" % idx)
    sha, size = download(url, p)
    info = inspect(p)
    records.append({"url": url, "sha256": sha, "size_bytes": size, **info})
    p.unlink(missing_ok=True)

joined = " ".join(
    value
    for rec in records
    for vals in rec["candidate_sample_columns"].values()
    for value in vals
).lower()

checks = {
    "all_files_nonempty": all(r["size_bytes"] > 0 for r in records),
    "all_tables_have_rows": all(r["row_count"] > 0 for r in records),
    "untreated_token_present": any(tok in joined for tok in ["nodrug", "no_drug", "untreated"]),
    "week1_token_present": any(tok in joined for tok in ["1week", "week1", "1_week"]),
    "week4_token_present": any(tok in joined for tok in ["4weeks", "4week", "week4", "4_week"]),
    "egfr_token_present": "egfr" in joined,
    "mix_token_present": "mix" in joined
}
status = "PASS_SOURCE_SCHEMA_AND_TIMEPOINT_MAP" if all(checks.values()) else "PARTIAL_SOURCE_SCHEMA_REQUIRES_MAPPING_REVIEW"

result = {
    "schema_version": "0.1",
    "project": "GRI Bio Chi Bridge",
    "gate": "Shaffer 2017 GSE97679 processed RNA source-schema audit",
    "freeze": "BIO_CHI/config/SHAFFER2017_GRI_BIOCHI_SOURCE_FREEZE_v0_1.json",
    "status": status,
    "files": records,
    "checks": checks,
    "molecular_target_statistics_computed": False,
    "gene_effects_opened": False,
    "next_action": "freeze exact development/held-out population-time-replicate carrier roles before B2/B3 analysis"
}
(out / "shaffer2017_source_schema_v0_1.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

md = ["# Shaffer 2017 source-schema audit v0.1", "", "**Status:** " + status, ""]
for i, r in enumerate(records, 1):
    md += [
        "## Processed RNA file %d" % i,
        "- bytes: %d" % r["size_bytes"],
        "- rows: %d" % r["row_count"],
        "- SHA-256: " + r["sha256"],
        "- columns: " + ", ".join(r["header"]),
        ""
    ]
md += ["## Frozen mapping checks", ""]
for k, v in checks.items():
    md.append("- %s: %s" % (k, "PASS" if v else "FAIL"))
md += ["", "No gene-effect or target molecular statistic was computed.", "", result["next_action"], ""]
(out / "SHAFFER2017_SOURCE_SCHEMA_V0_1_AUDIT.md").write_text("\n".join(md), encoding="utf-8")
print(json.dumps(result, indent=2))
