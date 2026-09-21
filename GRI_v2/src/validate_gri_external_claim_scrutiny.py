from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "config" / "gri_external_claim_scrutiny_v01.json"

REQUIRED = {f"EC-{i:02d}" for i in range(1,19)}
BANNED_PROMOTION_STATUSES = {"PROVEN","VALIDATED_UNIVERSALLY","CLINICALLY_VALIDATED"}

def validate():
    data=json.loads(LEDGER.read_text())
    assert data["schema"]=="GRI_EXTERNAL_CLAIM_SCRUTINY_V01"
    claims=data["claims"]
    ids={x["id"] for x in claims}
    assert ids==REQUIRED
    assert len(ids)==len(claims)
    assert all(x["status"] not in BANNED_PROMOTION_STATUSES for x in claims)
    by={x["id"]:x for x in claims}
    assert by["EC-15"]["status"]=="NOT_TESTED_AGAINST_STANDARD_TOOLKIT"
    assert by["EC-17"]["status"]=="NOT_ESTABLISHED"
    assert by["EC-18"]["status"]=="ACTIVE_INVESTIGATION"
    assert any("no biological reorganization" in s for s in by["EC-13"]["forbidden"])
    return data

if __name__=="__main__":
    d=validate()
    out=ROOT/"conglomerate_v01_outputs"
    out.mkdir(exist_ok=True)
    (out/"external_claim_scrutiny_validation.json").write_text(
        json.dumps({"status":"PASS","claims":len(d["claims"]),"schema":d["schema"]},indent=2)+"\n"
    )
