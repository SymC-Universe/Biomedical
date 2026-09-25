#!/usr/bin/env python3
import gzip, hashlib, json, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cfg = json.loads((ROOT / "config" / "SHAFFER2017_GRI_BIOCHI_SOURCE_FREEZE_v0_1.json").read_text())
out = ROOT / "artifacts" / "generated"
out.mkdir(parents=True, exist_ok=True)

def download(url, path):
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(url, timeout=120) as r, open(path, "wb") as f:
        while True:
            b = r.read(1024 * 1024)
            if not b:
                break
            f.write(b)
            h.update(b)
            n += len(b)
    return h.hexdigest(), n

def parse_sample_id(s):
    low = s.lower()
    if "nodrug" in low:
        time = "noDrug"
    elif "1week" in low or "week1" in low:
        time = "week1"
    elif "4week" in low or "week4" in low:
        time = "week4"
    elif "5week" in low or "week5" in low:
        time = "week5"
    else:
        time = "unmapped"

    if "egfrpos" in low or "drugegfr" in low or "nodrugegfr" in low:
        population = "EGFR_high"
    elif "egfrneg" in low:
        population = "EGFR_negative"
    elif "mix" in low:
        population = "mixed"
    else:
        population = "unmapped"

    m = re.search(r'(?:-|)(\d+)$', s)
    replicate = m.group(1) if m else "source_single_or_unparsed"
    return {"sample_id": s, "timepoint": time, "population": population, "replicate_token": replicate}

files = []
gene_sets = []
all_samples = []
for idx, url in enumerate(cfg["source"]["rna_processed_files"], start=1):
    p = out / f"_shaffer_map_{idx}.tsv.gz"
    sha, size = download(url, p)
    genes = set()
    samples = set()
    with gzip.open(p, "rt", encoding="utf-8", errors="replace") as f:
        header = f.readline().rstrip("\n\r").split("\t")
        col = {name:i for i,name in enumerate(header)}
        for line in f:
            parts = line.rstrip("\n\r").split("\t")
            genes.add(parts[col["gene_id"]])
            samples.add(parts[col["sampleID"]])
    mapped = [parse_sample_id(s) for s in sorted(samples)]
    files.append({
        "index": idx,
        "url": url,
        "sha256": sha,
        "size_bytes": size,
        "gene_count": len(genes),
        "sample_count": len(samples),
        "samples": mapped
    })
    gene_sets.append(genes)
    all_samples.extend(mapped)
    p.unlink(missing_ok=True)

common = set.intersection(*gene_sets)
union = set.union(*gene_sets)
only_counts = [len(gs - common) for gs in gene_sets]

result = {
    "schema_version":"0.1",
    "project":"GRI Bio Chi Bridge",
    "gate":"Shaffer 2017 metadata-only common-gene and carrier map audit",
    "status":"PASS_METADATA_MAP",
    "files": files,
    "common_gene_count": len(common),
    "union_gene_count": len(union),
    "genes_outside_common_by_file": only_counts,
    "common_gene_set_sha256": hashlib.sha256(("\n".join(sorted(common))+"\n").encode()).hexdigest(),
    "sample_map": all_samples,
    "all_samples_mapped_timepoint": all(x["timepoint"] != "unmapped" for x in all_samples),
    "all_samples_mapped_population": all(x["population"] != "unmapped" for x in all_samples),
    "counts_or_gene_effects_used_for_scientific_inference": False,
    "next_action":"freeze batch-aware preprocessing and modal-construction candidate after source-native method review"
}
(out/"shaffer2017_common_gene_sample_map_v0_1.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
print(json.dumps(result, indent=2))
