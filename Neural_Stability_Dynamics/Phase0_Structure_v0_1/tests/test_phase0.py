import numpy as np
from src.synthetic_systems import oscillator_block,make_system,simulate
from src.ssi_cov import ssi_cov,continuous_modes
from src.metrics import mac,match_modes

def test_block_poles():
 A=oscillator_block(0.8,7.0); v=np.linalg.eigvals(A); assert np.allclose(v.real,-0.8); assert np.allclose(np.sort(abs(v.imag)/(2*np.pi)),[7,7])
def test_similarity_preserves_eigenvalues():
 rng=np.random.default_rng(1); A,C=make_system([{'decay_per_s':.8,'frequency_hz':7},{'decay_per_s':1.8,'frequency_hz':14}],6,rng); f=np.sort(abs(np.linalg.eigvals(A).imag)/(2*np.pi)); assert np.allclose(f,[7,7,14,14])
def test_mac_scale_invariance():
 v=np.array([1+1j,2-.5j,-1j]); assert np.isclose(mac(v,(3-2j)*v),1.0)
def test_ssi_shapes():
 rng=np.random.default_rng(2); A,C=make_system([{'decay_per_s':.8,'frequency_hz':7},{'decay_per_s':1.8,'frequency_hz':14}],6,rng); Y,_=simulate(A,C,.01,6000,.12,.02,rng); Fh,Ch,S=ssi_cov(Y,4,15); vals,sh=continuous_modes(Fh,Ch,.01); assert Fh.shape==(4,4) and Ch.shape==(6,4) and vals.shape==(4,) and sh.shape==(6,4) and np.isfinite(S[:4]).all()
def test_match_cardinality():
 assert len(match_modes(np.array([-1+2j,-1-2j]),np.array([-1.1+2.1j,-1.1-2.1j])))==2
