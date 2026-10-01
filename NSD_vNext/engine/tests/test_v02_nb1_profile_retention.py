import types
import numpy as np

import nsd_engine.v02_nb1_profile as prof


class _Fit:
    parameters={
        "damping_ratio":0.4,
        "latent_fraction":0.5,
        "natural_frequency_hz":8.0,
        "g":0.1,
    }
    negative_log_likelihood=10.0
    success=True
    bic=25.0
    raw_parameters=(0.1,0.2,0.3,0.4)
    attempted_start_count=3
    converged_start_count=3
    optimizer_message="ok"
    legacy_attempted_start_count=2
    legacy_converged_start_count=2
    legacy_best_negative_log_likelihood=10.1
    legacy_best_success=True
    legacy_best_raw_parameters=(0.1,0.2,0.3,0.5)
    winning_start_origin="fixture"
    recurrence_seed_status="SEED_READY"
    recurrence_seed_ready=True
    recurrence_seed_start_nll=10.2
    recurrence_seed_condition_number=2.0


def test_optimize_chi_retains_every_start_and_bound_evidence(monkeypatch):
    starts=[
        ("a",np.array([0.0,0.0,0.0])),
        ("b",np.array([1.0,1.0,1.0])),
    ]
    monkeypatch.setattr(prof,"starts",lambda *args,**kwargs:starts)
    calls=[]
    def fake_minimize(fun,start,method,bounds,options):
        calls.append(np.asarray(start,float))
        if len(calls)==1:
            return types.SimpleNamespace(
                fun=12.0,x=np.array([0.2,0.3,0.4]),success=True,status=0,
                message="ok",nit=3,nfev=7
            )
        return types.SimpleNamespace(
            fun=11.0,x=np.array([8.0,0.1,0.2]),success=False,status=1,
            message="iteration cap",nit=80,nfev=91
        )
    monkeypatch.setattr(prof,"minimize",fake_minimize)
    out=prof.optimize_chi(np.ones(8),120.0,_Fit(),0.4)
    assert out["winning_start"]=="b"
    assert out["nuisance_bound_hit"] is True
    assert len(out["optimizer_runs"])==2
    assert out["optimizer_runs"][0]["success"] is True
    assert out["optimizer_runs"][1]["success"] is False
    assert out["optimizer_runs"][1]["status"]==1
    assert out["optimizer_runs"][1]["nuisance_bound_hit"] is True


def test_profile_retains_endpoints_and_reproduction_evidence(monkeypatch):
    monkeypatch.setattr(prof,"standardize",lambda x:np.asarray(x,float))
    monkeypatch.setattr(prof,"fit_continuous_lineage_candidate_rs",lambda *a,**k:_Fit())

    def fake_opt(std,fs,fit,chi,previous=None):
        return {
            "chi":float(chi),
            "status":"FINITE",
            "nll":10.0+(float(chi)-0.4)**2,
            "nuisance_raw":[0.1,0.2,0.3],
            "winning_start":"fixture",
            "nuisance_bound_hit":False,
            "optimizer_runs":[{
                "origin":"fixture","initial_raw":[0,0,0],"finite":True,
                "success":True,"status":0,"message":"ok","nll":10.0,
                "nit":1,"nfev":1,"terminal_raw":[0.1,0.2,0.3],
                "nuisance_bound_hit":False,
            }],
        }
    monkeypatch.setattr(prof,"optimize_chi",fake_opt)

    def fake_scalar(fun,bounds,method,options):
        x=0.4
        value=fun(x)
        return types.SimpleNamespace(
            x=x,fun=value,success=True,status=0,message="ok",nit=4,nfev=5
        )
    monkeypatch.setattr(prof,"minimize_scalar",fake_scalar)

    out=prof.profile_evidence(np.linspace(-1.0,1.0,64),120.0)
    kinds={x["kind"] for x in out["endpoint_candidates"]}
    assert kinds=={"left_endpoint","right_endpoint"}
    assert out["fitted_profile_reproduced"] is True
    assert out["unique_lowest_candidate"] is True
    assert out["lowest_candidate_interior"] is True
    assert out["refined_candidates"][0]["scalar_evaluations"]
    assert out["scientific_adjudication"]=="NOT_PERFORMED_BY_ENGINE"
