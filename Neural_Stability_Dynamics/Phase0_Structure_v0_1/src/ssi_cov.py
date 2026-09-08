from __future__ import annotations
import numpy as np

def output_covariances(Y,max_lag):
    n,p=Y.shape; out=[]
    for lag in range(1,max_lag+1): out.append((Y[lag:].T@Y[:-lag])/(n-lag))
    return out

def ssi_cov(Y,order,block_rows):
    Y=np.asarray(Y,float)
    if Y.ndim!=2: raise ValueError('Y must be samples x channels')
    n,p=Y.shape
    if order<=0 or order>=p*block_rows: raise ValueError('invalid model order')
    if n<20*block_rows: raise ValueError('not enough samples')
    covs=output_covariances(Y,2*block_rows)
    H=np.empty((p*block_rows,p*block_rows))
    for i in range(block_rows):
        for j in range(block_rows): H[i*p:(i+1)*p,j*p:(j+1)*p]=covs[i+j]
    U,S,_=np.linalg.svd(H,full_matrices=False)
    O=U[:,:order]@np.diag(np.sqrt(np.maximum(S[:order],0)))
    C_hat=O[:p,:]; F_hat=np.linalg.pinv(O[:-p,:])@O[p:,:]
    return F_hat,C_hat,S

def continuous_modes(F_hat,C_hat,dt):
    vals_d,vecs=np.linalg.eig(F_hat)
    vals_c=np.log(vals_d.astype(complex))/dt
    return vals_c,C_hat@vecs
