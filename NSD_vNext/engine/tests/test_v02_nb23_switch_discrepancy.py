import numpy as np
import pytest

from nsd_engine.v02_nb23_peak import (
    PeakCertificationError,
    certified_switching_discrepancy_max,
    switch_boundaries,
)
from nsd_engine.v02_nb23_switch_reference import dense_switching_discrepancy_reference


def test_switching_discrepancy_exact_zero_anchor():
    A=np.diag([-0.2,-0.5])
    out=certified_switching_discrepancy_max(
        A,A,np.eye(2),0.5,0.1,horizon=2.0
    )
    assert out["lower"]==0.0
    assert out["upper"]==0.0
    assert out["identical_generator_anchor"] is True
    assert out["verdict_namespace"]=="NUMERICAL_ONLY_NO_SCIENTIFIC_VERDICT"


def test_switching_discrepancy_partitions_explicit():
    A0=np.diag([-0.2,-0.5]); A1=np.diag([-0.4,-0.3])
    pts=switch_boundaries(0.5,0.1,2.0)
    out=certified_switching_discrepancy_max(
        A0,A1,np.eye(2),0.5,0.1,horizon=2.0,
        rel_tol=1e-8,max_intervals=5000
    )
    assert out["switch_partitions"]==[
        [float(a),float(b)] for a,b in zip(pts[:-1],pts[1:])
    ]
    assert out["scientific_adjudication"]=="NOT_PERFORMED_BY_GITHUB"


def test_switching_discrepancy_dense_reference_is_enclosed():
    A0=np.diag([-0.2,-0.5]); A1=np.diag([-0.4,-0.3])
    prod=certified_switching_discrepancy_max(
        A0,A1,np.eye(2),0.5,0.1,horizon=2.0,
        rel_tol=1e-8,max_intervals=10000
    )
    ref=dense_switching_discrepancy_reference(
        A0,A1,0.5,0.1,horizon=2.0,samples=20001
    )
    assert prod["lower"]-1e-12 <= ref["maximum"] <= prod["upper"]+1e-12
    assert prod["relative_gap"]<=1e-8
    assert ref["verdict_namespace"]=="NUMERICAL_REFERENCE_ONLY"


def test_switching_discrepancy_budget_exhaustion_fails_closed():
    A0=np.diag([-0.2,-0.5]); A1=np.diag([-0.4,-0.3])
    with pytest.raises(PeakCertificationError):
        certified_switching_discrepancy_max(
            A0,A1,np.eye(2),0.5,0.1,horizon=2.0,
            rel_tol=1e-14,max_intervals=0
        )
