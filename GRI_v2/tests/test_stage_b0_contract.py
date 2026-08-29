import json
from pathlib import Path
import tempfile

from src.probe_stage_b0_sources import scan_barcodes


def test_plan_keeps_primary_context_independent_of_rna():
    p = json.loads((Path(__file__).parents[1] / "config" / "stage_b0_source_plan.json").read_text())
    assert p["constraints"]["chi_allowed"] is False
    assert p["constraints"]["cv2_used"] is False
    assert p["constraints"]["stage_a_results_may_not_select_sources"] is True
    primary = [s for s in p["sources"] if s["role"] == "PRIMARY_B1_CONTEXT"]
    assert {s["id"] for s in primary} == {"absolute_purity_ploidy", "leukocyte_fraction"}
    assert all(s["circularity"] == "INDEPENDENT_OF_STAGE_A_RNA" for s in primary)


def test_barcode_scanner_counts_patient_and_primary_sample():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.tsv"
        p.write_text("id\tvalue\nTCGA-AA-1234-01A\t0.5\nTCGA-AA-1234-01B\t0.6\nTCGA-BB-5678-11A\t0.2\n")
        d = scan_barcodes(p)
        assert d["unique_tcga_patients_detected"] == 2
        assert d["unique_tcga_sample_barcodes_detected"] == 3
        assert d["unique_primary_tumor_sample_barcodes_detected"] == 2
