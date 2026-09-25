#!/usr/bin/env python3
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
cfg=json.loads((ROOT/"BIO_CHI/config/BIO_CHI_TOPDOWN_SYSTEM_SELECTION_FREEZE_v0_3.json").read_text())
survivors=[]
for c in cfg["candidates"]:
    mandatory=all(bool(c.get(k)) for k in cfg["mandatory_fields"])
    return_ok=(not bool(c.get("recovery_claimed"))) or bool(c.get("return_target_defined"))
    if mandatory and return_ok:
        vec=tuple(int(bool(c.get(k))) for k in cfg["tie_breakers_in_order"])
        survivors.append((vec,c["id"],c["primary_event"]))
survivors.sort(reverse=True)
if not survivors:
    status="NO_ELIGIBLE_SYSTEM"; selected=None
elif len(survivors)>1 and survivors[0][0]==survivors[1][0]:
    status="SCIENTIFIC_STOP_TIED_SYSTEMS"; selected=None
else:
    status="UNIQUE_SYSTEM_SELECTED"; selected=survivors[0][1]
out={
  "schema_version":"0.3","status":status,"selected_system":selected,
  "eligible_systems":[{"id":sid,"primary_event":event,"tie_vector":list(vec)} for vec,sid,event in survivors],
  "conditional_return_logic_applied":True,"molecular_outcomes_used":False
}
p=ROOT/"BIO_CHI/artifacts/generated/topdown_system_selection_v0_3.json"
p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
if status=="SCIENTIFIC_STOP_TIED_SYSTEMS": raise SystemExit(2)
print("BIO_CHI_TOPDOWN_SYSTEM_SELECTION_V03_DONE")
