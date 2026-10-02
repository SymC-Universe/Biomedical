import numpy as np
from nsd_engine.v02_nb23_peak import certified_stationary_peak, certified_switched_peak, switch_boundaries


def test_stationary_peak_certificate_nonconfirmatory_fixture():
    A=np.diag([-0.2,-0.4])
    out=certified_stationary_peak(A,np.eye(2),horizon=2.0,rel_tol=1e-8,max_intervals=10000)
    assert out["scientific_adjudication"]=="NOT_PERFORMED_BY_GITHUB"
    assert out["relative_gap"]<=1e-8
    assert out["lower"]<=1.0+1e-12
    assert out["upper"]>=1.0-1e-12


def test_switched_peak_certificate_partitions_boundaries():
    A0=np.diag([-0.2,-0.4]); A1=np.diag([-0.3,-0.1])
    pts=switch_boundaries(0.75,0.10,2.0)
    assert pts[0]==0.0 and pts[-1]==2.0
    out=certified_switched_peak(A0,A1,np.eye(2),0.75,0.10,horizon=2.0,rel_tol=1e-8,max_intervals=20000)
    assert out["scientific_adjudication"]=="NOT_PERFORMED_BY_GITHUB"
    assert out["relative_gap"]<=1e-8
    assert len(out["switch_partitions"])>=2
