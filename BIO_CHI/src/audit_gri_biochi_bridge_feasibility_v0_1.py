#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cfg_path = ROOT / "config" / "GRI_BIOCHI_BRIDGE_FREEZE_v0_1.json"
out_dir = ROOT / "artifacts" / "generated"
out_dir.mkdir(parents=True, exist_ok=True)

cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
records = cfg["candidate_source_records"]
rules = cfg["selection_rule"]

def passes(rec, reqs):
    return all(bool(rec.get(k, False)) for k in reqs)

rows = []
for rec in records:
    row = {
        "id": rec["id"],
        "independence_role": rec["independence_role_for_bridge"],
        "B1_technical": passes(rec, rules["B1_requires"]),
        "B2_technical": passes(rec, rules["B2_requires"]),
        "B3_technical": passes(rec, rules["B3_requires"]),
        "prior_scalar_disposition": rec["prior_scalar_disposition"],
        "prior_modal_disposition": rec["prior_modal_disposition"],
        "prior_biochi_disposition": rec["prior_biochi_disposition"],
    }
    row["B1_external_candidate"] = row["B1_technical"] and row["independence_role"] == "CANDIDATE_PROSPECTIVE"
    row["B2_external_candidate"] = row["B2_technical"] and row["independence_role"] == "CANDIDATE_PROSPECTIVE"
    row["B3_external_candidate"] = row["B3_technical"] and row["independence_role"] == "CANDIDATE_PROSPECTIVE"
    rows.append(row)

b1_ext = [r["id"] for r in rows if r["B1_external_candidate"]]
b2_ext = [r["id"] for r in rows if r["B2_external_candidate"]]
b3_ext = [r["id"] for r in rows if r["B3_external_candidate"]]
b1_dep = [r["id"] for r in rows if r["B1_technical"] and r["independence_role"] != "CANDIDATE_PROSPECTIVE"]

result = {
    "schema_version": "0.1",
    "project": "GRI Bio Chi Bridge",
    "gate": "outcome-blind bridge feasibility audit",
    "freeze": "BIO_CHI/config/GRI_BIOCHI_BRIDGE_FREEZE_v0_1.json",
    "status": "PASS_FEASIBILITY_AUDIT",
    "candidate_records": rows,
    "summary": {
        "B1_external_candidates": b1_ext,
        "B1_dependent_only_candidates": b1_dep,
        "B2_external_candidates": b2_ext,
        "B3_external_candidates": b3_ext,
    },
    "disposition": {
        "B1": "NO_CURRENT_PROSPECTIVE_SCALAR_BRIDGE_CANDIDATE" if not b1_ext else "PROSPECTIVE_CANDIDATE_AVAILABLE",
        "B2": "PROSPECTIVE_SOURCE_MAPPING_REQUIRED" if b2_ext else "NO_CURRENT_PROSPECTIVE_MODAL_BRIDGE_CANDIDATE",
        "B3": "PROSPECTIVE_SOURCE_MAPPING_REQUIRED" if b3_ext else "NO_CURRENT_PROSPECTIVE_RELATIONAL_BRIDGE_CANDIDATE",
    },
    "next_action": "audit Shaffer 2017 and Harmange 2023 carrier/source mappings without opening target molecular outcomes; select only after carrier linkage and assay compatibility are frozen"
}

json_path = out_dir / "gri_biochi_bridge_feasibility_v0_1.json"
json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

md = ["# GRI ↔ Bio Chi bridge feasibility audit v0.1", "", "**Status:** PASS", ""]
md += ["## Scalar bridge B1", ""]
if b1_ext:
    md.append("Prospective candidates: " + ", ".join(b1_ext))
else:
    md.append("No current prospective cancer source satisfies the frozen scalar bridge requirements.")
if b1_dep:
    md.append("Technically evaluable but evidence-dependent only: " + ", ".join(b1_dep))
md += ["", "## Modal bridge B2", "", "Prospective candidates: " + (", ".join(b2_ext) if b2_ext else "none"), "",
       "## Relational bridge B3", "", "Prospective candidates: " + (", ".join(b3_ext) if b3_ext else "none"), "",
       "## Next gate", "",
       "Freeze source/carrier mappings for Shaffer 2017 and Harmange 2023 before selecting the first executable GRI ↔ Bio Chi bridge. No target molecular outcomes are to be opened during that source gate.", ""]
(out_dir / "GRI_BIOCHI_BRIDGE_FEASIBILITY_V0_1_AUDIT.md").write_text("\n".join(md), encoding="utf-8")

print(json.dumps(result, indent=2))
