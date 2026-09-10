from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pytest

from src.engine_interface import evaluate_all_layers
from tests.test_engine_regression import _toy, _decomp_gap, _shapes

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "configs" / "development_rules.json").read_text(encoding="utf-8"))


def test_known_bad_scalar_nonstationarity_fails_through_production_interface():
    fits, decomps, orders = _toy(global_scale=1.25)
    out = evaluate_all_layers(fits=fits, decomps=decomps, candidate_orders=orders, rules=RULES)
    assert out["scalar"]["decision"] == "REFUSE_SCALAR_NONSTATIONARY"


def test_known_bad_carrier_rotation_fails_modal_gate_through_production_interface():
    fits, decomps, orders = _toy(rotate=True)
    out = evaluate_all_layers(fits=fits, decomps=decomps, candidate_orders=orders, rules=RULES)
    assert out["modal"]["decision"] == "REFUSE_MODAL_UNSTABLE"


def test_known_bad_structural_reorganization_fails_system_gate_through_production_interface():
    fits, decomps, orders = _toy(structural=True)
    out = evaluate_all_layers(fits=fits, decomps=decomps, candidate_orders=orders, rules=RULES)
    assert out["system"]["decision"] == "REFUSE_SYSTEM_REORGANIZED_OR_UNSTABLE"


def test_known_bad_no_order_is_refused_by_all_layers_through_production_interface():
    orders = [2, 4, 6]; flat = (np.eye(12), np.ones(12), 1)
    decomps = {"full": flat, "first_half": flat, "second_half": flat}; fits = {"full": {}, "first_half": {}, "second_half": {}}
    out = evaluate_all_layers(fits=fits, decomps=decomps, candidate_orders=orders, rules=RULES)
    for layer in ("scalar", "modal", "system"): assert out[layer]["decision"] == "REFUSE_NO_ORDER"


def test_known_bad_edge_order_is_refused_by_all_layers_through_production_interface():
    orders = [2, 4]; decomp = _decomp_gap(4)
    decomps = {"full": decomp, "first_half": decomp, "second_half": decomp}; fits = {"full": {}, "first_half": {}, "second_half": {}}
    out = evaluate_all_layers(fits=fits, decomps=decomps, candidate_orders=orders, rules=RULES)
    for layer in ("scalar", "modal", "system"): assert out[layer]["decision"] == "REFUSE_EDGE_ORDER"


def test_known_bad_unstable_pole_is_refused_by_all_layers_through_production_interface():
    orders=[2,4,6]; decomp=_decomp_gap(4); decomps={"full":decomp,"first_half":decomp,"second_half":decomp}
    vals=np.array([0.1+10j,0.1-10j,-2+20j,-2-20j]); shapes=_shapes([0,1,2,3])
    fits={"full":{},"first_half":{4:(vals,shapes)},"second_half":{4:(vals,shapes)}}
    out=evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=orders,rules=RULES)
    for layer in ("scalar","modal","system"): assert out[layer]["decision"]=="REFUSE_UNSTABLE"


def test_known_bad_no_complex_structure_is_refused_by_all_layers_through_production_interface():
    orders=[2,4,6]; decomp=_decomp_gap(4); decomps={"full":decomp,"first_half":decomp,"second_half":decomp}
    vals=np.array([-0.5+0j,-1.0+0j,-2.0+0j,-3.0+0j]); shapes=_shapes([0,1,2,3])
    fits={"full":{},"first_half":{4:(vals,shapes)},"second_half":{4:(vals,shapes)}}
    out=evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=orders,rules=RULES)
    for layer in ("scalar","modal","system"): assert out[layer]["decision"]=="REFUSE_NO_COMPLEX_STRUCTURE"


def test_unknown_payload_key_fails_closed_at_production_interface():
    fits,decomps,orders=_toy()
    with pytest.raises(ValueError, match="unexpected selector inputs"):
        evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=orders,rules=RULES,arbitrary_side_channel="KNOWN_BAD")
