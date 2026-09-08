from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.linalg import subspace_angles

def _pole_dist(a,b):
    return abs(a-b)/max(abs(a),abs(b),1e-12)

def _match(vals_a, vals_b):
    a=np.asarray(vals_a,complex); b=np.asarray(vals_b,complex)
    if len(a)==0 or len(b)==0:
        return []
    cost=np.empty((len(a),len(b)))
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            cost[i,j]=_pole_dist(x,y)
    ri,cj=linear_sum_assignment(cost)
    return [(int(i),int(j),float(cost[i,j])) for i,j in zip(ri,cj)]

def complex_indices(vals,min_hz):
    vals=np.asarray(vals,complex)
    return np.where(np.abs(vals.imag)/(2*np.pi)>=float(min_hz))[0]

def positive_complex_indices(vals,min_hz):
    vals=np.asarray(vals,complex)
    return np.where(vals.imag/(2*np.pi)>=float(min_hz))[0]

def mac(a,b):
    a=np.asarray(a,complex).ravel(); b=np.asarray(b,complex).ravel()
    den=np.vdot(a,a).real*np.vdot(b,b).real
    return np.nan if den<=0 else float(abs(np.vdot(a,b))**2/den)

def subspace_similarity(A,B):
    A=np.asarray(A,complex); B=np.asarray(B,complex)
    if A.ndim!=2 or B.ndim!=2 or A.shape[0]!=B.shape[0] or min(A.shape[1],B.shape[1])==0:
        return np.nan
    ang=subspace_angles(A,B)
    return float(np.mean(np.cos(ang)**2))

def gap_ratio(S,q):
    S=np.asarray(S,float)
    if q<=0 or q>=len(S):
        return np.nan
    return float(S[q-1]/max(S[q],1e-15))

def select_observable_order(full_decomp,candidate_orders,rules):
    _,S,_=full_decomp
    for q in sorted(candidate_orders):
        if gap_ratio(S,q)>=float(rules["singular_gap_threshold"]):
            return int(q)
    return None

def set_distance(vals_a,vals_b,min_hz,positive_only=False):
    pick=positive_complex_indices if positive_only else complex_indices
    ia=pick(vals_a,min_hz); ib=pick(vals_b,min_hz)
    m=_match(np.asarray(vals_a)[ia],np.asarray(vals_b)[ib])
    if not m:
        return np.nan,[]
    ds=np.array([x[2] for x in m],float)
    return float(np.median(ds)),m

def split_shape_metrics(vals_full,shapes_full,vals_first,shapes_first,vals_second,shapes_second,min_hz):
    fi=positive_complex_indices(vals_full,min_hz)
    a=positive_complex_indices(vals_first,min_hz)
    b=positive_complex_indices(vals_second,min_hz)
    mf=_match(np.asarray(vals_full)[fi],np.asarray(vals_first)[a])
    ms=_match(np.asarray(vals_full)[fi],np.asarray(vals_second)[b])
    mapf={i:(j,d) for i,j,d in mf}; maps={i:(j,d) for i,j,d in ms}
    rows=[]
    for local_i,global_i in enumerate(fi):
        if local_i not in mapf or local_i not in maps:
            continue
        jf,df=mapf[local_i]; js,ds=maps[local_i]
        rows.append({
            "full_index":int(global_i),
            "split_pole_distance":float(max(df,ds)),
            "split_shape_MAC":float(min(
                mac(shapes_full[:,global_i],shapes_first[:,a[jf]]),
                mac(shapes_full[:,global_i],shapes_second[:,b[js]])
            ))
        })
    return rows

def order_mode_persistence(vals_q,shapes_q,vals_next,shapes_next,min_hz):
    iq=positive_complex_indices(vals_q,min_hz)
    jn=positive_complex_indices(vals_next,min_hz)
    m=_match(np.asarray(vals_q)[iq],np.asarray(vals_next)[jn])
    out={}
    for i,j,d in m:
        out[int(iq[i])]={"order_pole_distance":float(d),"order_shape_MAC":float(mac(shapes_q[:,iq[i]],shapes_next[:,jn[j]]))}
    return out

def crowding_clusters(vals,min_hz,threshold):
    vals=np.asarray(vals,complex)
    idx=list(positive_complex_indices(vals,min_hz))
    parent={i:i for i in idx}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    pair_ratio={}
    for ai,i in enumerate(idx):
        for j in idx[ai+1:]:
            alpha_i=max(-vals[i].real,0.0); alpha_j=max(-vals[j].real,0.0)
            ratio=abs(vals[i].imag-vals[j].imag)/max(alpha_i+alpha_j,1e-12)
            pair_ratio[(i,j)]=float(ratio)
            if ratio<=float(threshold):
                union(i,j)
    groups={}
    for i in idx:
        groups.setdefault(find(i),[]).append(i)
    clusters=[sorted(v) for v in groups.values() if len(v)>1]
    return clusters,pair_ratio

def cluster_split_subspace(cluster,vals_full,shapes_full,vals_half,shapes_half,min_hz):
    hidx=positive_complex_indices(vals_half,min_hz)
    m=_match(np.asarray(vals_full)[cluster],np.asarray(vals_half)[hidx])
    if len(m)<len(cluster):
        return np.nan
    cols_full=[]; cols_half=[]
    for i,j,d in m:
        cols_full.append(cluster[i]); cols_half.append(hidx[j])
    return subspace_similarity(shapes_full[:,cols_full],shapes_half[:,cols_half])

def evaluate_model(fits,decomps,candidate_orders,rules):
    q=select_observable_order(decomps["full"],candidate_orders,rules)
    base={"selected_order":q,"decision":None}
    if q is None:
        base["decision"]="REFUSE_NO_ORDER"; return base
    if q==max(candidate_orders) and bool(rules["refuse_selected_order_at_grid_max"]):
        base["decision"]="REFUSE_EDGE_ORDER"; return base
    vals,shapes=fits["full"][q]
    if bool(rules["refuse_any_unstable_selected_pole"]) and np.any(np.real(vals)>=0):
        base["decision"]="REFUSE_UNSTABLE"; return base
    min_hz=float(rules["complex_frequency_min_hz"])
    if len(positive_complex_indices(vals,min_hz))==0:
        base["decision"]="REFUSE_NO_COMPLEX_STRUCTURE"; return base
    dsplit,_=set_distance(fits["first_half"][q][0],fits["second_half"][q][0],min_hz,positive_only=True)
    base["complex_split_median_distance"]=dsplit
    if (not np.isfinite(dsplit)) or dsplit>float(rules["complex_split_median_distance_max"]):
        base["decision"]="REFUSE_NONSTATIONARY"; return base
    nextq=sorted([x for x in candidate_orders if x>q])[0]
    dorder,_=set_distance(vals,fits["full"][nextq][0],min_hz,positive_only=True)
    base["complex_cross_order_median_distance"]=dorder
    if (not np.isfinite(dorder)) or dorder>float(rules["complex_cross_order_median_distance_max"]):
        base["decision"]="REFUSE_ORDER_UNSTABLE"; return base
    base["decision"]="ADMIT_MODEL"
    return base
