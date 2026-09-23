#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def fail(msg):
    print("BIO_CHI_REVIEWER_SMOKE_FAIL: " + msg, file=sys.stderr)
    raise SystemExit(1)

q = load("BIO_CHI/control/WORK_QUEUE.json")
if q.get("authority") != "SymC GOM v0.8.4": fail("authority drift")
if q.get("continuation_policy",{}).get("manuscript_private") is not True: fail("manuscript privacy drift")
expected = {
 "chi":"program-wide scalar stability class/symbol",
 "chi_bio":"biological scalar instance/sublabel of chi if licensed",
 "Chi_bio":"biological modal/vector representation",
 "Bio_Chi":"biological conglomerate/system stability architecture"
}
if q.get("nomenclature") != expected: fail("nomenclature drift")

b = load("BIO_CHI/config/BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json")
if b.get("status") != "PASS_SOURCE_ARCHIVE_IDENTITY_FROZEN": fail("Blum archive pin not PASS")
if b.get("frozen_archive",{}).get("sha256") != "8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62": fail("Blum archive hash drift")
if b.get("archive_contents_opened") is not False: fail("Blum source freeze not outcome-blind")

bm = load("BIO_CHI/config/BLUM2019_NATIVE_METHOD_QUALIFICATION_PIN_v0_1.json")
if bm.get("disposition") != "EXACT_NATIVE_METRIC_REPRODUCTION_BLOCKED_METHOD_UNDERSPECIFIED": fail("Blum method-limit drift")

g = load("BIO_CHI/config/P0D_GEO_LINEAGE_METADATA_V01_RESULT_PIN.json")
if g.get("status") != "PASS_METADATA_ONLY_SOURCE_LINEAGE_AUDIT": fail("GEO lineage pin not PASS")
if g.get("molecular_values_read") is not False or g.get("cell_metadata_rows_read") is not False: fail("GEO metadata boundary crossed")

lr = load("BIO_CHI/config/LEE2014_SRP040309_SOURCE_MAP_V01_RESULT_PIN.json")
if lr.get("status") != "PASS_SRA_METADATA_SOURCE_MAP" or lr.get("run_count") != 19: fail("Lee run-map drift")
if lr.get("sequence_reads_downloaded") is not False: fail("Lee run map downloaded reads")

lm = load("BIO_CHI/config/LEE2014_SRA_SAMPLE_METADATA_V01_RESULT_PIN.json")
if lm.get("status") != "PASS_SRA_SAMPLE_METADATA_MAP": fail("Lee metadata pin not PASS")
if lm.get("explicit_reconverted_or_post_withdrawal_rna_samples") != 0: fail("Lee recovery-source limitation drift")

bp = load("BIO_CHI/config/P0D_BIOPROJECT_SRA_RECONCILIATION_V02_RESULT_PIN.json")
if bp.get("status") != "PASS_BIOPROJECT_PARENT_CHILD_RECONCILIATION": fail("BioProject hierarchy pin not PASS")
if bp.get("shaffer2017",{}).get("run_count") != 155: fail("Shaffer SRA run-count drift")
if bp.get("shaffer2017",{}).get("missing_from_child_union") != [] or bp.get("shaffer2017",{}).get("extra_in_child_union") != []:
    fail("Shaffer parent/child run-set drift")
if bp.get("molecular_values_interpreted") is not False: fail("BioProject reconciliation crossed outcome boundary")

su = load("BIO_CHI/config/SU2026_NATIVE_METHOD_SOURCE_METADATA_V01_RESULT_PIN.json")
if su.get("status") != "PASS_SU_NATIVE_SOURCE_METADATA": fail("Su native-source metadata pin not PASS")
if su.get("expected_m397_rna_gsm_count") != 15 or su.get("missing_gsms") != []: fail("Su M397 source membership drift")
if su.get("expression_values_read") is not False or su.get("surprisal_computed") is not False:
    fail("Su source qualification crossed outcome/method boundary")

native = q.get("active_native_model_gate",{})
for k in ("chi_bio_constructed","Chi_bio_admitted","Bio_Chi_constructed"):
    if native.get(k) is not False: fail("premature admission flag " + k)

cp = (BIO / "control" / "AUTORUN_CHECKPOINT.md").read_text(encoding="utf-8")
for h in ("Mechanical continuation authority","Scientific stop conditions","Current execution queue"):
    if h not in cp: fail("checkpoint missing " + h)

print("BIO_CHI_REVIEWER_SMOKE_PASS")
