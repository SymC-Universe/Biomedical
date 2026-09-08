import ast, json
from pathlib import Path
import numpy as np

from src.selector import (
    relational_geometry_distance, subspace_similarity, participation_tv,
    evaluate_scalar_layer, evaluate_modal_layer, evaluate_system_layer,
    select_observable_order
)
from src.synthetic_systems import make_linear_system

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'configs'/'phase0c_design.json').read_text())
RULES=json.loads((ROOT/'configs'/'frozen_rules.json').read_text())


def _shapes(cols):
    A=np.zeros((8,len(cols)),complex)
    for j,c in enumerate(cols): A[c,j]=1
    return A


def _toy(global_scale=1.0, rotate=False, structural=False):
    z1=-1+10j; z2=-2+20j
    first=np.array([z1,z1.conjugate(),z2,z2.conjugate()])
    if structural:
        w1=z1; w2=-1.2+14j
    else:
        w1=global_scale*z1; w2=global_scale*z2
    second=np.array([w1,w1.conjugate(),w2,w2.conjugate()])
    full=first.copy()
    nextv=np.concatenate([full,np.array([-3+0j,-5+0j])])
    qshape=_shapes([0,1,2,3])
    sshape=_shapes([4,5,6,7]) if rotate else qshape.copy()
    nextshape=np.concatenate([qshape,_shapes([4,5])],axis=1)
    fits={
      'full':{4:(full,qshape),6:(nextv,nextshape)},
      'first_half':{4:(first,qshape)},
      'second_half':{4:(second,sshape)}
    }
    S=np.array([100,90,80,70,5,4,3,2],float)
    decomps={'full':(np.eye(8),S,1)}
    return fits,decomps,[2,4,6]


def test_frozen_three_layer_rules_exact():
    assert RULES['common']['singular_gap_threshold']==10.0
    assert RULES['scalar_layer']['complex_split_median_distance_max']==0.03
    assert RULES['modal_layer']['individual_split_MAC_min']==0.95
    assert RULES['system_layer']['split_whole_subspace_similarity_min']==0.98
    assert RULES['system_layer']['split_channel_participation_TV_max']==0.10
    assert RULES['system_layer']['split_relational_pole_geometry_distance_max']==0.05


def test_holdout_v02_is_new_and_unexecuted_by_design():
    assert CFG['seed']==2026090807
    assert CFG['durations_samples']==[10000,20000,28000]
    assert CFG['candidate_orders']==[2,4,6,8,10,12]
    assert CFG['epistemic_status']=='UNTOUCHED_THREE_LAYER_SYNTHETIC_HOLDOUT_DO_NOT_RETUNE'


def test_relational_geometry_is_invariant_to_global_timescale_scaling():
    a=np.array([-1+10j,-2+20j])
    b=1.25*a
    assert relational_geometry_distance(a,b)<1e-12


def test_subspace_and_participation_are_basis_rotation_invariant_inside_same_span():
    A=np.array([[1,0],[0,1],[1,1],[0,0]],complex)
    R=np.array([[1,2],[-2,1]],complex)
    B=A@R
    assert subspace_similarity(A,B)>0.999999999
    assert participation_tv(A,B)<1e-12


def test_observation_reorganization_changes_carrier_geometry():
    A=_shapes([0,1])
    B=_shapes([4,5])
    assert subspace_similarity(A,B)<1e-12
    assert participation_tv(A,B)>0.99


def test_global_timescale_switch_separates_scalar_from_modal_and_system_layers():
    fits,decomps,orders=_toy(global_scale=1.25)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert not s['decision'].startswith('ADMIT_')
    assert m['decision']=='ADMIT_MODAL_STRUCTURE'
    assert g['decision']=='ADMIT_SYSTEM_ORGANIZATION'


def test_observation_switch_preserves_scalar_but_rejects_modal_and_system_layers():
    fits,decomps,orders=_toy(global_scale=1.0,rotate=True)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert s['decision']=='ADMIT_SCALAR_SPECTRUM'
    assert not m['decision'].startswith('ADMIT_')
    assert not g['decision'].startswith('ADMIT_')


def test_structural_switch_preserves_carriers_but_rejects_scalar_and_system_layers():
    fits,decomps,orders=_toy(structural=True)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert not s['decision'].startswith('ADMIT_')
    assert m['decision']=='ADMIT_MODAL_STRUCTURE'
    assert not g['decision'].startswith('ADMIT_')


def test_order_rule_chooses_smallest_qualifying_gap():
    S=np.array([100,90,80,70,5,4,3,2],float)
    assert select_observable_order((np.eye(8),S,1),[2,4,6],RULES['common'])==4


def test_four_mode_family_is_order_eight_truth():
    spec=next(x for x in CFG['systems'] if x['name']=='v02_four_mode')
    A,C=make_linear_system(spec,CFG['n_channels'],np.random.default_rng(9))
    assert A.shape==(8,8)
    assert np.all(np.linalg.eigvals(A).real<0)


def test_layer_challenges_are_scored_only_on_long_record():
    for spec in CFG['systems']:
        if spec.get('role')=='layer_challenge':
            assert spec['score_only_n_samples']==[28000]
            assert spec['switch_sample']==14000


def test_selector_source_has_no_truth_or_clinical_arguments():
    tree=ast.parse((ROOT/'src'/'selector.py').read_text())
    forbidden={'truth','true_vals','true_shapes','diagnosis','phenotype','treatment','chi'}
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            args={a.arg.lower() for a in node.args.args}
            assert not (args & forbidden)


def test_no_clinical_inputs_in_holdout_design():
    txt=(ROOT/'configs'/'phase0c_design.json').read_text().lower()
    for forbidden in ['tdbrain','diagnosis','mdd','adhd','treatment_response','historical desired ordering']:
        assert forbidden not in txt
