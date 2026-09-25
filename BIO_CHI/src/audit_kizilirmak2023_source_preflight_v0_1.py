#!/usr/bin/env python3
import hashlib, json, os, re, sys, urllib.request, zipfile
from pathlib import Path

ROOT = Path("BIO_CHI/artifacts/generated/kizilirmak2023_source_preflight_v01")
ROOT.mkdir(parents=True, exist_ok=True)

URLS = {
    "table_s3": [
        "https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10746373/bin/mmc3.xls"
    ],
    "data_s1": [
        "https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc2.zip",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10746373/bin/mmc2.zip"
    ],
    "geo_self": [
        "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247446&targ=self&view=full&form=text"
    ],
    "geo_suppl_index": [
        "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE247nnn/GSE247446/suppl/"
    ]
}

def fetch(candidates, out):
    last = None
    for url in candidates:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-source-audit/0.1"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            Path(out).write_bytes(data)
            return url, data
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
    raise RuntimeError(f"all candidates failed for {out}: {last}")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

report = {
    "schema_version":"0.1",
    "status":"STARTED",
    "scientific_values_opened":False,
    "files":{},
    "geo":{}
}

# Exact published supplements. This workflow inspects identity/schema only.
url, xls = fetch(URLS["table_s3"], ROOT/"mmc3.xls")
report["files"]["table_s3"] = {"url":url,"bytes":len(xls),"sha256":sha256(xls)}
url, zdat = fetch(URLS["data_s1"], ROOT/"mmc2.zip")
report["files"]["data_s1"] = {"url":url,"bytes":len(zdat),"sha256":sha256(zdat)}

with zipfile.ZipFile(ROOT/"mmc2.zip") as z:
    members = []
    for i in z.infolist():
        if i.is_dir():
            continue
        rec = {"name":i.filename,"bytes":i.file_size,"compressed_bytes":i.compress_size}
        if i.filename.lower().endswith(".csv"):
            raw = z.read(i.filename).decode("utf-8","replace").splitlines()
            rec["line_count"] = len(raw)
            rec["column_count"] = len(raw[0].split(",")) if raw else 0
            rec["headerless_numeric_matrix"] = True
        members.append(rec)
    report["files"]["data_s1"]["members"] = members

# Excel schema only. Read no expression rows.
try:
    import xlrd
    book = xlrd.open_workbook(file_contents=xls, on_demand=True)
    sheets = []
    for sname in book.sheet_names():
        sh = book.sheet_by_name(sname)
        header = [str(sh.cell_value(0,c)) for c in range(sh.ncols)] if sh.nrows else []
        gene_id_examples = [str(sh.cell_value(r,0)) for r in range(1,min(sh.nrows,11))] if sh.ncols else []
        target_genes = ["Tnfrsf1a","Rela","Nfkbia","Tnfaip3"]
        target_gene_rows = {}
        if sh.ncols:
            wanted = {g.lower(): g for g in target_genes}
            for r in range(1, sh.nrows):
                gid = str(sh.cell_value(r,0)).strip()
                if gid.lower() in wanted:
                    target_gene_rows[wanted[gid.lower()]] = r + 1
        sheets.append({"name":sname,"nrows":sh.nrows,"ncols":sh.ncols,"header":header,
                       "gene_id_examples":gene_id_examples,"target_gene_rows_1based":target_gene_rows})
    report["files"]["table_s3"]["sheets"] = sheets
except Exception as e:
    report["files"]["table_s3"]["schema_error"] = f"{type(e).__name__}: {e}"

# GEO metadata and supplementary directory listing only.
url, soft = fetch(URLS["geo_self"], ROOT/"GSE247446.soft.txt")
text = soft.decode("utf-8","replace")
report["geo"]["self_url"] = url
report["geo"]["soft_sha256"] = sha256(soft)
report["geo"]["supplementary_file_lines"] = [
    line.strip() for line in text.splitlines()
    if line.startswith("!Series_supplementary_file")
]
report["geo"]["sample_count_declared"] = None
m = re.search(r"!Series_sample_id\s*=\s*(.+)", text)
if m:
    report["geo"]["first_series_sample_line"] = m.group(1)[:500]

try:
    url, idx = fetch(URLS["geo_suppl_index"], ROOT/"GSE247446_suppl_index.html")
    itxt = idx.decode("utf-8","replace")
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', itxt, flags=re.I)
    report["geo"]["suppl_index_url"] = url
    report["geo"]["suppl_index_sha256"] = sha256(idx)
    report["geo"]["suppl_hrefs"] = [h for h in hrefs if not h.startswith("?") and h not in ("../","/")]
except Exception as e:
    report["geo"]["suppl_index_error"] = f"{type(e).__name__}: {e}"

report["status"] = "PASS_SOURCE_MATERIALIZED_SCHEMA_ONLY"
(ROOT/"KIZILIRMAK2023_SOURCE_PREFLIGHT_V01.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

md = [
"# Kizilirmak 2023 source preflight v0.1",
"",
f"**Status:** {report['status']}",
"",
"This preflight materializes the exact published supplements and GEO metadata but does not read expression values or single-cell trajectory values.",
"",
"## Published source identities",
f"- Table S3 SHA256: `{report['files']['table_s3']['sha256']}`",
f"- Data S1 SHA256: `{report['files']['data_s1']['sha256']}`",
"",
"## Table S3 schema"
]
for sh in report["files"]["table_s3"].get("sheets",[]):
    md += [f"- `{sh['name']}`: {sh['nrows']} rows x {sh['ncols']} columns",
           f"  - header: `{sh['header']}`",
           f"  - gene ID examples: `{sh.get('gene_id_examples',[])}`",
           f"  - frozen TNF/NF-kB circuit gene rows: `{sh.get('target_gene_rows_1based',{})}`"]
md += ["","## Data S1 archive members"]
for i in report["files"]["data_s1"]["members"]:
    md.append(f"- `{i['name']}` ({i['bytes']} bytes; {i.get('line_count','?')} lines)")
    if i.get("headerless_numeric_matrix"):
        md.append(f"  - headerless numeric matrix; columns: `{i.get('column_count',0)}`")
md += ["","## GEO supplementary metadata"]
for line in report["geo"].get("supplementary_file_lines",[]):
    md.append(f"- `{line}`")
for h in report["geo"].get("suppl_hrefs",[]):
    md.append(f"- index member: `{h}`")
md += ["","## Scientific state","No chi_GRI value or trajectory endpoint was opened. Next gate is representation/endpoint freeze from this schema."]
(ROOT/"KIZILIRMAK2023_SOURCE_PREFLIGHT_V01_AUDIT.md").write_text("\n".join(md)+"\n", encoding="utf-8")
