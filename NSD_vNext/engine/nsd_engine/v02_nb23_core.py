"""Frozen NSD v0.2 N-B2/N-B3 mechanical primitives."""
import numpy as np
from scipy.linalg import expm


def second_order_matrix(s):
    w1,w2=float(s["omega1"]),float(s["omega2"])
    return np.array([[0,1,0,0],[-w1*w1,-2*s["zeta1"]*w1,s["k12"],s["c12"]],
                     [0,0,0,1],[s["k21"],s["c21"],-w2*w2,-2*s["zeta2"]*w2]],float)


def metric_roots(G):
    G=np.asarray(G,float); d,V=np.linalg.eigh((G+G.T)/2)
    if d.min()<=0: raise RuntimeError("metric not SPD")
    return V@np.diag(np.sqrt(d))@V.T,V@np.diag(1/np.sqrt(d))@V.T


def physical_gain(A,G,t):
    R,Ri=metric_roots(G)
    return float(np.linalg.svd(R@expm(np.asarray(A)*float(t))@Ri,compute_uv=False)[0])
