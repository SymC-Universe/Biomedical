import numpy as np
from nsd_engine.v02_nb23_targets import spectral_abscissa, physical_response_curve, integrated_burden, evidence_namespace


def test_v02_nb23_target_fixture():
    A=np.diag([-0.2,-0.4]); G=np.eye(2); x0=np.array([1.0,1.0]); t=np.linspace(0.0,2.0,21)
    r=physical_response_curve(A,G,x0,t)
    assert spectral_abscissa(A)==-0.2
    assert integrated_burden(t,r)>0.0
    assert evidence_namespace()=="RAW_TARGET_EVIDENCE_ONLY"
