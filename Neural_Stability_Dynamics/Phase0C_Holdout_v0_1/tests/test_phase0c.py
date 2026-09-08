import ast, json
from pathlib import Path
import numpy as np

from src.selector import (
    gap_ratio, select_observable_order,
    crowding_clusters, mac, subspace_similarity
)
from src.synthetic_systems import make_linear_system

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/"configs"/"phase0c_design.json").read_text())
RULES=json.loads((ROOT/"configs"/"frozen_rules.json").read_text())

def test_frozen_thresholds_exact():
    assert RULES["singular_gap_threshold"]==10.0
    assert RULES["complex_split_median_distance_max"]==0.03
    assert RULES["complex_cross_order_median_distance_max"]==0.02
    assert RULES["individual_split_MAC_min"]==0.95
    assert RULES["crowding_ratio_subspace_only_le"]==1.0
    assert RULES["split_subspace_similarity_min"]==0.99

def test_order_rule_chooses_smallest_qualifying_gap():
    S=np.array([100,80,40,20,1.0,0.8,0.7,0.6,0.5,0.4,0.3],float)
    fake=(np.eye(len(S)),S,1)
    q=select_observable_order(fake,[2,4,6,8,10],RULES)
    assert q==4

def test_no_order_when_gap_below_threshold():
    S=np.array([10,9,8,7,6,5,4,3,2,1.5,1.2],float)
    fake=(np.eye(len(S)),S,1)
    assert select_observable_order(fake,[2,4,6,8,10],RULES) is None

def test_crowding_rule_marks_overlapping_pair():
    vals=np.array([-0.7+10j,-0.7-10j,-0.7+10.8j,-0.7-10.8j],complex)
    clusters,_=crowding_clusters(vals,0.25,1.0)
    assert len(clusters)==1 and len(clusters[0])==2

def test_mac_scale_invariance():
    a=np.array([1+1j,2-1j,3],complex)
    assert mac(a,7j*a)>0.999999999

def test_subspace_basis_invariance():
    rng=np.random.default_rng(4)
    A=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2))
    R=np.array([[1,2],[-2,1]],complex)
    assert subspace_similarity(A,A@R)>0.999999999

def test_selector_source_has_no_truth_argument():
    tree=ast.parse((ROOT/"src"/"selector.py").read_text())
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            args=[a.arg.lower() for a in node.args.args]
            assert "truth" not in args and "true_vals" not in args and "true_shapes" not in args

def test_holdout_seed_and_parameters_differ_from_phase0b():
    assert CFG["seed"]==2026090803
    assert CFG["durations_samples"]==[9000,18000,24000]
    assert CFG["candidate_orders"]==[2,4,6,8,10]

def test_three_mode_family_is_order_six_truth():
    spec=next(x for x in CFG["systems"] if x["name"]=="holdout_three_mode")
    A,C=make_linear_system(spec,CFG["n_channels"],np.random.default_rng(8))
    assert A.shape==(6,6)
    assert np.all(np.linalg.eigvals(A).real<0)

def test_fixed_switch_occurs_inside_shortest_holdout():
    spec=next(x for x in CFG["systems"] if x["name"]=="holdout_switch_fixed")
    assert 0 < spec["switch_sample"] < min(CFG["durations_samples"])

def test_no_clinical_inputs_in_holdout_design():
    txt=(ROOT/"configs"/"phase0c_design.json").read_text().lower()
    for forbidden in ["tdbrain","diagnosis","mdd","adhd","treatment_response"]:
        assert forbidden not in txt
    assert set(RULES["forbidden_selector_inputs"]) >= {"truth","chi","diagnosis","phenotype","treatment"}
