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
RULES=json.loads((ROOT/'configs'/'development_rules.json').read_text())
ORDERS=[2,4,6,8,10]


def _shapes(cols):
    A=np.zeros((8,len(cols)),complex)
    for j,c in enumerate(cols): A[c,j]=1
    return A


def _decomp_gap(q,n=12):
    S=np.linspace(120,30,n)
    S[q:]=np.linspace(4,1,n-q)
    return np.eye(n),S,1


def _toy(global_scale=1.0, rotate=False, structural=False, crowding=False, single=False):
    if single:
        first=np.array([-1+10j,-1-10j])
        second=first.copy(); q=2
        A=_shapes([0,1]); B=A.copy(); nxt=np.concatenate([first,[-3+0j,-5+0j]])
        fits={
            'full':{},
            'first_half':{2:(first,A),4:(nxt,np.concatenate([A,_shapes([2,3])],axis=1))},
            'second_half':{2:(second,B),4:(nxt,np.concatenate([B,_shapes([2,3])],axis=1))}
        }
        decomps={'full':_decomp_gap(4),'first_half':_decomp_gap(2),'second_half':_decomp_gap(2)}
        return fits,decomps,[2,4,6]

    z1=-1+10j; z2=-2+20j
    first=np.array([z1,z1.conjugate(),z2,z2.conjugate()])
    if crowding:
        first=np.array([-1+10j,-1-10j,-1+20j,-1-20j])
        second=np.array([-1+14j,-1-14j,-1+15j,-1-15j])
    elif structural:
        w1=z1; w2=-1.2+14j
        second=np.array([w1,w1.conjugate(),w2,w2.conjugate()])
    else:
        w1=global_scale*z1; w2=global_scale*z2
        second=np.array([w1,w1.conjugate(),w2,w2.conjugate()])
    qshape=_shapes([0,1,2,3])
    sshape=_shapes([4,5,6,7]) if rotate else qshape.copy()
    extra=np.array([-3+0j,-5+0j])
    fnext=np.concatenate([first,extra]); snext=np.concatenate([second,extra])
    fnextshape=np.concatenate([qshape,_shapes([4,5])],axis=1)
    snextshape=np.concatenate([sshape,_shapes([4,5])],axis=1)
    fits={
      'full':{},
      'first_half':{4:(first,qshape),6:(fnext,fnextshape)},
      'second_half':{4:(second,sshape),6:(snext,snextshape)}
    }
    decomps={'full':_decomp_gap(8),'first_half':_decomp_gap(4),'second_half':_decomp_gap(4)}
    return fits,decomps,ORDERS


def test_development_rules_preserve_local_order_and_carrier_matching_for_regression():
    assert RULES['common']['singular_gap_threshold']==10.0
    assert 'independently' in RULES['common']['order_policy']
    assert RULES['scalar_layer']['complex_split_median_distance_max']==0.03
    assert RULES['modal_layer']['individual_split_MAC_min']==0.95
    assert 'MAC/subspace' in RULES['modal_layer']['matching_policy']
    assert RULES['system_layer']['minimum_positive_complex_modes_for_carrier']==1
    assert RULES['system_layer']['single_or_crowded_cluster_geometry_policy']=='UNRESOLVED_NOT_FAILURE'
    assert RULES['status']=='P0_CALIBRATION_ONLY_NOT_P1_FROZEN'


def test_full_record_order_inflation_is_not_imposed_on_halves():
    fits,decomps,orders=_toy(global_scale=1.18)
    assert select_observable_order(decomps['full'],orders,RULES['common'])==8
    assert select_observable_order(decomps['first_half'],orders,RULES['common'])==4
    assert select_observable_order(decomps['second_half'],orders,RULES['common'])==4
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    assert s['full_selected_order']==8
    assert s['first_selected_order']==4 and s['second_selected_order']==4


def test_global_timescale_switch_separates_layers_under_local_order():
    fits,decomps,orders=_toy(global_scale=1.25)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert not s['decision'].startswith('ADMIT_')
    assert m['decision']=='ADMIT_MODAL_STRUCTURE'
    assert g['decision'].startswith('ADMIT_SYSTEM_ORGANIZATION')


def test_observation_switch_preserves_scalar_rejects_carrier_and_system():
    fits,decomps,orders=_toy(global_scale=1.0,rotate=True)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert s['decision']=='ADMIT_SCALAR_SPECTRUM'
    assert not m['decision'].startswith('ADMIT_')
    assert not g['decision'].startswith('ADMIT_')


def test_structural_switch_preserves_carriers_but_rejects_scalar_and_system():
    fits,decomps,orders=_toy(structural=True)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert not s['decision'].startswith('ADMIT_')
    assert m['decision']=='ADMIT_MODAL_STRUCTURE'
    assert not g['decision'].startswith('ADMIT_')


def test_crowding_transition_preserves_carriers_but_changes_system_cluster_structure():
    fits,decomps,orders=_toy(crowding=True)
    s=evaluate_scalar_layer(fits,decomps,orders,RULES)
    m=evaluate_modal_layer(fits,decomps,orders,RULES)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert not s['decision'].startswith('ADMIT_')
    assert m['decision']=='ADMIT_MODAL_STRUCTURE'
    assert not g['decision'].startswith('ADMIT_')


def test_single_complex_mode_can_admit_system_with_geometry_unresolved():
    fits,decomps,orders=_toy(single=True)
    g=evaluate_system_layer(fits,decomps,orders,RULES)
    assert g['decision']=='PARTIAL_SYSTEM_ORGANIZATION_GEOMETRY_UNRESOLVED'
    assert g['geometry_status']=='UNRESOLVED'
    assert g['carrier_status']=='ADMIT'
    assert g['participation_status']=='ADMIT'
    assert g['split_relational_geometry_status'].startswith('UNRESOLVED')


def test_relational_geometry_is_invariant_to_global_timescale_scaling():
    a=np.array([-1+10j,-2+20j]); b=1.25*a
    assert relational_geometry_distance(a,b)<1e-12


def test_subspace_and_participation_are_basis_rotation_invariant_inside_same_span():
    A=np.array([[1,0],[0,1],[1,1],[0,0]],complex); R=np.array([[1,2],[-2,1]],complex); B=A@R
    assert subspace_similarity(A,B)>0.999999999
    assert participation_tv(A,B)<1e-12


def test_order_rule_chooses_smallest_qualifying_gap():
    assert select_observable_order(_decomp_gap(4),[2,4,6,8],RULES['common'])==4


def test_selector_source_has_no_truth_or_clinical_arguments():
    tree=ast.parse((ROOT/'src'/'selector.py').read_text())
    forbidden={'truth','true_vals','true_shapes','diagnosis','phenotype','treatment','chi'}
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            args={a.arg.lower() for a in node.args.args}
            assert not (args & forbidden)
