#!/usr/bin/env python3
import csv, gzip, hashlib, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "SHAFFER2017_GSE97681_SOURCE_METADATA_FREEZE_v0_1.json").read_text())
OUT = ROOT / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

def download(url, path):
    h = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(url, timeout=180) as r, open(path, "wb") as f:
        while True:
            b = r.read(1024 * 1024)
            if not b:
                break
            f.write(b)
            h.update(b)
            total += len(b)
    return h.hexdigest(), total

def audit_tsv_gz(path):
    with gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        lower = [x.strip().lower() for x in header]
        gene_candidates = ["gene_id", "gene", "geneid", "id"]
        sample_candidates = ["sampleid", "sample_id", "sample", "sample name", "samplename"]
        gene_idx = next((lower.index(x) for x in gene_candidates if x in lower), 0 if header else None)
        sample_idx = next((lower.index(x) for x in sample_candidates if x in lower), None)
        schema = "long" if sample_idx is not None else "wide_or_other"
        samples = set()
        genes = set()
        rows = 0
        if sample_idx is None and len(header) > 1:
            samples.update(header[1:])
        for row in reader:
            if not row:
                continue
            rows += 1
            if gene_idx is not None and gene_idx < len(row):
                genes.add(row[gene_idx])
            if sample_idx is not None and sample_idx < len(row):
                samples.add(row[sample_idx])
    return {
        "columns": header,
        "schema_form": schema,
        "row_count": rows,
        "gene_count": len(genes),
        "sample_count": len(samples),
        "sample_ids": sorted(samples),
        "gene_set_sha256": hashlib.sha256(("\n".join(sorted(genes))+"\n").encode()).hexdigest() if genes else None
    }

results = []
base = CFG["source_record"]["processed_files"]
base_url = CFG["access_rule"]["base_url"]
for i, rec in enumerate(base, start=1):
    fn = rec["file"]
    url = base_url + fn
    temp = OUT / ("_gse97681_" + str(i) + ".tsv.gz")
    sha, size = download(url, temp)
    meta = audit_tsv_gz(temp)
    results.append({
        "file": fn,
        "system_role": rec["system_role"],
        "url": url,
        "sha256": sha,
        "size_bytes": size,
        **meta
    })
    temp.unlink(missing_ok=True)

out = {
    "schema_version": "0.1",
    "project": "GRI Bio Chi Bridge",
    "gate": "GSE97681 processed-source metadata-only audit",
    "status": "PASS_METADATA_ONLY" if results else "FAIL_NO_FILES",
    "files": results,
    "target_molecular_values_used_for_inference": False,
    "endpoint_selection_performed": False,
    "next_action": "review source sample identities and define only whether the frozen internal-validation and transfer roles are mechanically supported; do not select B2/B3 endpoints"
}
path = OUT / "shaffer2017_gse97681_source_metadata_v0_1.json"
path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
