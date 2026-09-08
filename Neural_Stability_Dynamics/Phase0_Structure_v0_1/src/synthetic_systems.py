from __future__ import annotations
import numpy as np
from scipy.linalg import expm, qr

def oscillator_block(decay_per_s: float, frequency_hz: float) -> np.ndarray:
    a=float(decay_per_s); b=2*np.pi*float(frequency_hz)
    return np.array([[-a,-b],[b,-a]],dtype=float)

def make_system(modes,n_channels,rng):
    n=2*len(modes); A0=np.zeros((n,n)); k=0
    for m in modes:
        B=oscillator_block(m['decay_per_s'],m['frequency_hz']); A0[k:k+2,k:k+2]=B; k+=2
    Q,_=qr(rng.normal(size=(n,n)))
    A=Q@A0@Q.T
    C=rng.normal(size=(n_channels,n)); C=C/np.maximum(np.linalg.norm(C,axis=0,keepdims=True),1e-12)
    return A,C

def simulate(A,C,dt,n_samples,process_scale,observation_scale,rng):
    F=expm(A*dt); n=A.shape[0]; p=C.shape[0]; x=np.zeros(n); Y=np.empty((n_samples,p))
    burn=max(2000,int(20/dt))
    for _ in range(burn): x=F@x+process_scale*np.sqrt(dt)*rng.normal(size=n)
    for t in range(n_samples):
        x=F@x+process_scale*np.sqrt(dt)*rng.normal(size=n)
        Y[t]=C@x+observation_scale*rng.normal(size=p)
    Y-=Y.mean(axis=0,keepdims=True)
    return Y,F

def continuous_truth(A,C):
    vals,vecs=np.linalg.eig(A); return vals,C@vecs
