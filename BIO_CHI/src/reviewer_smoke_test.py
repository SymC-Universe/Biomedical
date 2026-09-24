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
if q.get("authority") != "SymC GOM v0.8.6 + Bio Chi project-specific three-object nomenclature decision 2026-09-23":
    fail("authority drift")
if q.get("continuation_policy",{}).get("manuscript_private") is not True:
    fail("manuscript privacy drift")
expected = {
    "chi_bio":"biological scalar instance/sublabel of program-wide chi if licensed",
    "Chi_bio":"biological modal/vector representation",
    "Bio_Chi":"biological conglomerate/system stability architecture"
}
if q.get("nomenclature") != expected:
    fail("nomenclature drift")
if q.get("nomenclature_note") != "Exactly three biological objects. Program-wide chi is a parent symbol/class, not a fourth biological object.":
    fail("three-object nomenclature note drift")

# Existing source/provenance limits remain part of the evidence spine.
b = load("BIO_CHI/config/BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json")
if b.get("status") != "PASS_SOURCE_ARCHIVE_IDENTITY_FROZEN":
    fail("Blum archive pin not PASS")
if b.get("frozen_archive",{}).get("sha256") != "8bbd1ead46b5bb6b676bd47a5f415fdd790840a9c726321dc5c209b9c527bc62":
    fail("Blum archive hash drift")
if b.get("archive_contents_opened") is not False:
    fail("Blum source freeze not outcome-blind")

bm = load("BIO_CHI/config/BLUM2019_NATIVE_METHOD_QUALIFICATION_PIN_v0_1.json")
if bm.get("disposition") != "EXACT_NATIVE_METRIC_REPRODUCTION_BLOCKED_METHOD_UNDERSPECIFIED":
    fail("Blum method-limit drift")

g = load("BIO_CHI/config/P0D_GEO_LINEAGE_METADATA_V01_RESULT_PIN.json")
if g.get("status") != "PASS_METADATA_ONLY_SOURCE_LINEAGE_AUDIT":
    fail("GEO lineage pin not PASS")
if g.get("molecular_values_read") is not False or g.get("cell_metadata_rows_read") is not False:
    fail("GEO metadata boundary crossed")

lr = load("BIO_CHI/config/LEE2014_SRP040309_SOURCE_MAP_V01_RESULT_PIN.json")
if lr.get("status") != "PASS_SRA_METADATA_SOURCE_MAP" or lr.get("run_count") != 19:
    fail("Lee run-map drift")
if lr.get("sequence_reads_downloaded") is not False:
    fail("Lee run map downloaded reads")

lm = load("BIO_CHI/config/LEE2014_SRA_SAMPLE_METADATA_V01_RESULT_PIN.json")
if lm.get("status") != "PASS_SRA_SAMPLE_METADATA_MAP":
    fail("Lee metadata pin not PASS")
if lm.get("explicit_reconverted_or_post_withdrawal_rna_samples") != 0:
    fail("Lee recovery-source limitation drift")

bp = load("BIO_CHI/config/P0D_BIOPROJECT_SRA_RECONCILIATION_V02_RESULT_PIN.json")
if bp.get("status") != "PASS_BIOPROJECT_PARENT_CHILD_RECONCILIATION":
    fail("BioProject hierarchy pin not PASS")
if bp.get("shaffer2017",{}).get("run_count") != 155:
    fail("Shaffer SRA run-count drift")
if bp.get("shaffer2017",{}).get("missing_from_child_union") != [] or bp.get("shaffer2017",{}).get("extra_in_child_union") != []:
    fail("Shaffer parent/child run-set drift")
if bp.get("molecular_values_interpreted") is not False:
    fail("BioProject reconciliation crossed outcome boundary")

su = load("BIO_CHI/config/SU2026_NATIVE_METHOD_SOURCE_METADATA_V01_RESULT_PIN.json")
if su.get("status") != "PASS_SU_NATIVE_SOURCE_METADATA":
    fail("Su native-source metadata pin not PASS")
if su.get("expected_m397_rna_gsm_count") != 15 or su.get("missing_gsms") != []:
    fail("Su M397 source membership drift")
if su.get("expression_values_read") is not False or su.get("surprisal_computed") is not False:
    fail("Su source qualification crossed outcome/method boundary")

# Current NF-kB three-object state.
scalar = load("BIO_CHI/config/JARUS_CHI_BIO_SCALAR_P0Q_V01_RESULT_PIN.json")
if scalar.get("status") != "CHI_BIO_P0Q_SUPPORTED_MODEL_SPECIFIC":
    fail("NF-kB chi_bio admission drift")
if scalar.get("model_specific_chi_bio_admissible") is not True:
    fail("NF-kB chi_bio admissibility flag drift")
if scalar.get("broad_biological_chi_bio_admitted") is not False:
    fail("NF-kB chi_bio scope inflation")

modal = load("BIO_CHI/config/JARUS_CHI_BIO_MODAL_ADMISSION_V01.json")
if modal.get("decision") != "CHI_BIO_MODAL_P0Q_ADMITTED_MODEL_SPECIFIC":
    fail("NF-kB Chi_bio admission drift")
if modal.get("admission",{}).get("Chi_bio_model_specific_admitted") is not True:
    fail("NF-kB Chi_bio flag drift")
if modal.get("admission",{}).get("broad_biological_Chi_bio_admitted") is not False:
    fail("NF-kB Chi_bio scope inflation")

cong = load("BIO_CHI/config/JARUS_BIO_CHI_CONGLOMERATE_ADMISSION_V01.json")
if cong.get("decision") != "BIO_CHI_CONGLOMERATE_P0Q_ADMITTED_MODEL_SPECIFIC":
    fail("NF-kB Bio Chi admission drift")
if cong.get("admission",{}).get("Bio_Chi_model_specific_admitted") is not True:
    fail("NF-kB Bio Chi flag drift")
if cong.get("admission",{}).get("broad_biological_Bio_Chi_admitted") is not False:
    fail("NF-kB Bio Chi scope inflation")

# Independent ERK transport: scalar class survives, complete modal admission is refused.
b3_native = load("BIO_CHI/config/BLUM_B3_NATIVE_REPRODUCTION_V02_RESULT_PIN.json")
if b3_native.get("status") != "PASS_NATIVE_B3_TRAJECTORY_REPRODUCTION":
    fail("B3 native reproduction drift")

b3_gen = load("BIO_CHI/config/BLUM_B3_GENERATOR_TRANSPORT_V02_RESULT_PIN.json")
if b3_gen.get("status") != "PASS_B3_GENERATOR_MODAL_QUALIFICATION":
    fail("B3 generator qualification drift")
if b3_gen.get("scalar_transport_status") != "SCALAR_TRANSPORT_PRESENT":
    fail("B3 scalar transport drift")

b3_rt = load("BIO_CHI/config/BLUM_B3_LOCAL_NONLINEAR_ROUNDTRIP_V01_RESULT_PIN.json")
if b3_rt.get("status") != "FAIL_B3_FULL_MODAL_LOCAL_ROUNDTRIP":
    fail("B3 modal-roundtrip refusal drift")
if b3_rt.get("pair_lane_all_contexts_pass") is not True:
    fail("B3 pair-lane transport drift")
if b3_rt.get("full_modal_lane_all_contexts_pass") is not False:
    fail("B3 full-modal refusal drift")
if b3_rt.get("scientific_disposition",{}).get("ERK_Chi_bio_model_specific_admission") != "REFUSED_UNDER_CURRENT_GATE":
    fail("B3 Chi_bio refusal status drift")
if b3_rt.get("scientific_disposition",{}).get("Bio_Chi_cross_system_transport") != "NOT_OPENED":
    fail("B3 Bio Chi transport scope drift")

native = q.get("active_native_model_gate",{})
for k in ("chi_bio_constructed","Chi_bio_admitted","Bio_Chi_constructed"):
    if native.get(k) is not True:
        fail("current NF-kB admission flag drift " + k)

cross = q.get("cross_system_transport",{})
erk = cross.get("ERK_B3_independent_system",{})
if erk.get("chi_bio_representation_class_transport") != "SUPPORTED_P0Q":
    fail("queue ERK scalar transport drift")
if erk.get("ERK_Chi_bio_admission") != "REFUSED_CURRENT_GATE":
    fail("queue ERK modal refusal drift")
if erk.get("Bio_Chi_transport") != "NOT_OPENED":
    fail("queue ERK Bio Chi scope drift")

cp = (BIO / "control" / "AUTORUN_CHECKPOINT.md").read_text(encoding="utf-8")
for h in ("Mechanical continuation authority","Scientific stop conditions","Current execution queue"):
    if h not in cp:
        fail("checkpoint missing " + h)

print("BIO_CHI_REVIEWER_SMOKE_PASS")
