import json
from pathlib import Path

import numpy as np

from src.coordinate_registry import ChiCandidate, REQUIRED_CHI_GATES, classify_as_chi
from src.module_network import compute_module_metrics


def test_cv2_is_explicitly_rejected_as_chi_even_if_all_gates_are_marked():
    candidate = ChiCandidate.from_gates("CV/2", "CV", "constant_two", REQUIRED_CHI_GATES)
    assert classify_as_chi(candidate) == "REJECT_HISTORICAL_CV2_IS_NOT_CHI"


def test_incomplete_candidate_cannot_be_chi():
    candidate = ChiCandidate.from_gates("candidate", "recovery_rate", "response_rate", {"G1", "G2", "G3"})
    assert classify_as_chi(candidate).startswith("REJECT_MISSING_CHI_GATES:")


def test_coherent_module_has_high_internal_and_low_external_coupling():
    rng = np.random.default_rng(7)
    n = 100
    latent = rng.normal(size=n)
    module = np.column_stack([latent + rng.normal(scale=0.15, size=n) for _ in range(5)])
    background = rng.normal(size=(n, 8))
    x = np.column_stack([module, background])
    genes = [f"M{i}" for i in range(5)] + [f"B{i}" for i in range(8)]
    out = compute_module_metrics(x, genes, {"TEST": [f"M{i}" for i in range(5)]}, minimum_mapped_genes=3)
    m = out[0]
    assert m.cin_pairwise_median_abs > 0.9
    assert m.cin_pc1_variance_fraction > 0.9
    assert m.cout_eigengene_median_abs < 0.2


def test_stage_a1_forbids_chi_cv2_and_composite_score():
    root = Path(__file__).resolve().parents[1]
    d = json.loads((root / "config" / "stage_a1_plan.json").read_text())
    assert d["chi_allowed"] is False
    assert "historical comparator only" in d["cv2_policy"]
    assert d["composite_score_allowed"] is False
    assert d["module_policy"]["historical_gri_modules_allowed_in_primary"] is False
