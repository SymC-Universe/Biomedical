import numpy as np
from nsd_engine.v02_nb1_generators import CTruth, c_matrices, simulate_c, coarse_from_fine


def test_v02_generator_and_sampling_contract():
    truth=CTruth(0.8,8.0,0.24,0.05)
    a=simulate_c(truth,4012295144428264894,seconds=1.0)
    b=simulate_c(truth,4012295144428264894,seconds=1.0)
    assert np.array_equal(a,b)
    _,P,Qc,_,Qd=c_matrices(truth)
    assert all(np.linalg.eigvalsh((M+M.T)/2).min() >= -1e-9 for M in (P,Qc,Qd))
    fine=np.arange(23040,dtype=float)
    assert np.array_equal(coarse_from_fine(fine),fine[::2])
