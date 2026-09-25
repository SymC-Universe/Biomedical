#!/usr/bin/env python3
import hashlib, json, re, urllib.request, zipfile
from pathlib import Path
import xlrd

ROOT=Path("BIO_CHI/artifacts/generated/kizilirmak2023_il1b_preflight_v01")
ROOT.mkdir(parents=True,exist_ok=True)
TABLE_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc3.xls"
DYN_URL="https://ars.els-cdn.com/content/image/1-s2.0-S2589004223026500-mmc2.zip"
TABLE_SHA="f76c8eaf685d192f2340d178aac62f8263004077276d3e64f96ba41faab408f4"
DYN_SHA="9ee2914095e9676b92806c33e46929965c6b4c7535f74a00d4462152678ba7b8"

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 GRI-BioChi-IL1B-preflight/0.1"})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read()
def sha(b): return hashlib.sha256(b).hexdigest()

tb=get(TABLE_URL); db=get(DYN_URL)
if sha(tb)!=TABLE_SHA: raise RuntimeError("Table S3 SHA mismatch")
if sha(db)!=DYN_SHA: raise RuntimeError("Data S1 SHA mismatch")
(ROOT/"mmc3.xls").write_bytes(tb); (ROOT/"mmc2.zip").write_bytes(db)

book=xlrd.open_workbook(file_contents=tb,on_demand=True)
sh=book.sheet_by_name("Sheet1")
targets=["Il1rap","Rela","Nfkbia","Tnfaip3"]
rows={}
for r in range(1,sh.nrows):
    gid=str(sh.cell_value(r,0)).strip()
    if gid in targets:
        rows[gid]=r+1

with zipfile.ZipFile(ROOT/"mmc2.zip") as z:
    members=[]
    for i in z.infolist():
        if i.is_dir(): continue
        if re.search(r"IL1|IL-1|Fig5",i.filename,re.I):
            rec={"name":i.filename,"bytes":i.file_size}
            if i.filename.lower().endswith(".csv"):
                raw=z.read(i.filename).decode("utf-8","replace").splitlines()
                rec["line_count"]=len(raw)
                rec["column_count"]=len(raw[0].split(",")) if raw else 0
                rec["headerless_numeric_matrix"]=True
            members.append(rec)

out={
  "schema_version":"0.1",
  "status":"PASS" if set(rows)==set(targets) and members else "REFUSE",
  "scientific_values_opened":False,
  "target_gene_rows_1based":rows,
  "matching_data_s1_members":members,
  "source_hashes":{"table_s3":sha(tb),"data_s1":sha(db)}
}
(ROOT/"KIZILIRMAK2023_IL1B_PREFLIGHT_V01.json").write_text(json.dumps(out,indent=2),encoding="utf-8")

lines=["# Kizilirmak IL-1beta transport source preflight v0.1","",f"**Status:** {out['status']}","",
       "No transcriptomic or trajectory values were read for this preflight.","","## Frozen circuit rows"]
for g,r in rows.items(): lines.append(f"- {g}: row {r}")
lines += ["","## IL-1beta / Figure 5 source members"]
for m in members:
    lines.append(f"- {m['name']} ({m['line_count']} rows x {m['column_count']} columns)" if "line_count" in m else f"- {m['name']}")
(ROOT/"KIZILIRMAK2023_IL1B_PREFLIGHT_V01_AUDIT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
