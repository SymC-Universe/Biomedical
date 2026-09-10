from pathlib import Path
import csv, json, shutil, subprocess, sys, tempfile
import numpy as np
import pytest

from src.contracts import selector_payload
from src.engine_interface import evaluate_all_layers
from src.integrity import build_manifest_text, verify_manifest
from src.semantic_validation import compare_summary

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "configs" / "development_rules.json").read_text())
ORDERS = [2,4,6,8,10]


def _shapes(cols):
    A=np.zeros((8,len(cols)),complex)
    for j,c in enumerate(cols): A[c,j]=1
    return A


def _decomp_gap(q,n=12):
    S=np.linspace(120,30,n)
    S[q:]=np.linspace(4,1,n-q)
    return np.eye(n),S,1


def _toy_ok():
    z1=-1+10j; z2=-2+20j
    first=np.array([z1,z1.conjugate(),z2,z2.conjugate()])
    second=first.copy(); qshape=_shapes([0,1,2,3])
    extra=np.array([-3+0j,-5+0j]); nxt=np.concatenate([first,extra])
    nxtshape=np.concatenate([qshape,_shapes([4,5])],axis=1)
    fits={
      'full':{},
      'first_half':{4:(first,qshape),6:(nxt,nxtshape)},
      'second_half':{4:(second,qshape),6:(nxt,nxtshape)}
    }
    decomps={'full':_decomp_gap(4),'first_half':_decomp_gap(4),'second_half':_decomp_gap(4)}
    return fits,decomps


def test_production_input_contract_accepts_only_structural_payload():
    fits,decomps=_toy_ok()
    p=selector_payload(fits=fits,decomps=decomps,candidate_orders=ORDERS,rules=RULES)
    assert set(p)=={'fits','decomps','candidate_orders','rules'}


@pytest.mark.parametrize('bad_key', ['diagnosis','phenotype','treatment','outcome','truth','chi','labels'])
def test_production_input_contract_fails_on_known_bad_scientific_input(bad_key):
    fits,decomps=_toy_ok()
    with pytest.raises(ValueError):
        evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=ORDERS,rules=RULES,**{bad_key:'KNOWN_BAD'})


def test_production_engine_interface_runs_without_forbidden_inputs():
    fits,decomps=_toy_ok()
    out=evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=ORDERS,rules=RULES)
    assert out['scalar']['decision']=='ADMIT_SCALAR_SPECTRUM'
    assert out['modal']['decision']=='ADMIT_MODAL_STRUCTURE'
    assert out['system']['decision']=='ADMIT_SYSTEM_ORGANIZATION'


def test_confirmatory_runner_is_fail_closed_before_p1_ready_record():
    proc=subprocess.run([sys.executable,'local_runner.py'],cwd=ROOT,capture_output=True,text=True)
    assert proc.returncode!=0
    assert 'CONFIRMATORY EXECUTION BLOCKED' in proc.stdout


def test_manifest_verifier_detects_known_bad_mutation(tmp_path):
    root=tmp_path/'pkg'; root.mkdir(); (root/'a.txt').write_text('good')
    manifest=root/'FREEZE_MANIFEST.sha256'
    manifest.write_text(build_manifest_text(root))
    ok,problems=verify_manifest(root,manifest)
    assert ok and not problems
    (root/'a.txt').write_text('bad')
    ok,problems=verify_manifest(root,manifest)
    assert not ok
    assert any(x.startswith('HASH_MISMATCH:a.txt') for x in problems)


def test_manifest_verifier_detects_unfrozen_added_file(tmp_path):
    root=tmp_path/'pkg'; root.mkdir(); (root/'a.txt').write_text('good')
    manifest=root/'FREEZE_MANIFEST.sha256'; manifest.write_text(build_manifest_text(root))
    (root/'b.txt').write_text('surprise')
    ok,problems=verify_manifest(root,manifest)
    assert not ok and 'UNFROZEN_FILE:b.txt' in problems


def _write_semantic_fixture(base, summary_override=None):
    base.mkdir(parents=True,exist_ok=True)
    fields=['trial_id','role','expected_system','scalar_decision','modal_decision','system_decision']
    rows=[
        {'trial_id':'a','role':'stationary_truth','expected_system':'ADMIT','scalar_decision':'ADMIT_SCALAR_SPECTRUM','modal_decision':'ADMIT_MODAL_STRUCTURE','system_decision':'ADMIT_SYSTEM_ORGANIZATION'},
        {'trial_id':'b','role':'stationary_truth','expected_system':'ADMIT','scalar_decision':'REFUSE_SCALAR_NONSTATIONARY','modal_decision':'ADMIT_MODAL_STRUCTURE','system_decision':'REFUSE_SYSTEM_REORGANIZED_OR_UNSTABLE'},
    ]
    with (base/'layer_decisions.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    (base/'failures.json').write_text('[]')
    metrics={'stationary_trial_count':2,'stationary_scalar_admission_rate':0.5,'stationary_modal_admission_rate':1.0,'stationary_system_trial_count':2,'stationary_system_admission_rate':0.5,'failed_fits':0}
    if summary_override: metrics.update(summary_override)
    (base/'summary.json').write_text(json.dumps({'metrics':metrics}))


def test_semantic_validator_recomputes_core_meaning(tmp_path):
    d=tmp_path/'r'; _write_semantic_fixture(d)
    ok,problems=compare_summary(d)
    assert ok and not problems


def test_semantic_validator_fails_on_known_bad_summary_mutation(tmp_path):
    d=tmp_path/'r'; _write_semantic_fixture(d,{'stationary_scalar_admission_rate':1.0})
    ok,problems=compare_summary(d)
    assert not ok
    assert any('stationary_scalar_admission_rate' in p for p in problems)


def test_no_freeze_manifest_or_p1_ready_record_exists_in_p0_package():
    assert not (ROOT/'FREEZE_MANIFEST.sha256').exists()
    assert not (ROOT/'P1_READY.json').exists()
    hold=json.loads((ROOT/'configs/P1_DESIGN_HOLD.json').read_text())
    assert hold['scientific_holdout_executed'] is False
    assert hold['scientific_holdout_seed'] is None


def test_layer_c_unresolved_geometry_is_partial_not_full_admission():
    from tests.test_engine_regression import _toy
    fits,decomps,orders=_toy(single=True)
    out=evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=orders,rules=RULES)['system']
    assert out['carrier_status']=='ADMIT'
    assert out['participation_status']=='ADMIT'
    assert out['geometry_status']=='UNRESOLVED'
    assert out['decision']=='PARTIAL_SYSTEM_ORGANIZATION_GEOMETRY_UNRESOLVED'


def test_unequal_local_order_is_visible_open_channel_and_refused():
    fits,decomps=_toy_ok()
    decomps['second_half']=_decomp_gap(6)
    z=np.array([-1+10j,-1-10j,-2+20j,-2-20j,-3+25j,-3-25j])
    sh=_shapes([0,1,2,3,4,5])
    z8=np.concatenate([z,[-4+0j,-5+0j]])
    sh8=np.concatenate([sh,_shapes([6,7])],axis=1)
    fits['second_half'][6]=(z,sh); fits['second_half'][8]=(z8,sh8)
    out=evaluate_all_layers(fits=fits,decomps=decomps,candidate_orders=ORDERS,rules=RULES)
    for layer in ['scalar','modal','system']:
        assert out[layer]['decision'].startswith('REFUSE_')
        assert out[layer]['order_transition_status']=='ORDER_CHANGED_SHARED_MODE_TRACKING_UNRESOLVED'
