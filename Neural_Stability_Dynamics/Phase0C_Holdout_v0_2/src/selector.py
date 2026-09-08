from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.linalg import subspace_angles


def pole_distance(a,b):
    return float(abs(a-b)/max(abs(a),abs(b),1e-12))


def match_indices(vals_a, vals_b):
    a=np.asarray(vals_a,complex); b=np.asarray(vals_b,complex)
    if len(a)==0 or len(b)==0:
        return []
    cost=np.empty((len(a),len(b)),float)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            cost[i,j]=pole_distance(x,y)
    ri,cj=linear_sum_assignment(cost)
    return [(int(i),int(j),float(cost[i,j])) for i,j in zip(ri,cj)]


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


def orthonormal_basis(A):
    A=np.asarray(A,complex)
    if A.ndim!=2 or A.shape[1]==0:
        return None
    Q,R=np.linalg.qr(A)
    d=np.abs(np.diag(R))
    if len(d)==0:
        return None
    tol=max(A.shape)*np.finfo(float).eps*max(float(np.max(d)),1.0)
    r=int(np.sum(d>tol))
    return None if r==0 else Q[:,:r]


def channel_participation(A):
    Q=orthonormal_basis(A)
    if Q is None:
        return None
    lev=np.sum(np.abs(Q)**2,axis=1).real
    s=float(np.sum(lev))
    return None if s<=0 else lev/s


def participation_tv(A,B):
    a=channel_participation(A); b=channel_participation(B)
    if a is None or b is None or len(a)!=len(b):
        return np.nan
    return float(0.5*np.sum(np.abs(a-b)))


def normalized_relational_geometry(vals):
    z=np.asarray(vals,complex)
    if len(z)<2:
        return None
    scale=float(np.median(np.abs(z)))
    if not np.isfinite(scale) or scale<=0:
        return None
    D=np.abs(z[:,None]-z[None,:])/scale
    return D


def relational_geometry_distance(vals_a,vals_b):
    a=np.asarray(vals_a,complex); b=np.asarray(vals_b,complex)
    if len(a)<2 or len(a)!=len(b):
        return np.nan
    Da=normalized_relational_geometry(a); Db=normalized_relational_geometry(b)
    if Da is None or Db is None:
        return np.nan
    den=max(float(np.linalg.norm(Da,'fro')),1e-12)
    return float(np.linalg.norm(Da-Db,'fro')/den)


def gap_ratio(S,q):
    S=np.asarray(S,float)
    if q<=0 or q>=len(S):
        return np.nan
    return float(S[q-1]/max(S[q],1e-15))


def select_observable_order(full_decomp,candidate_orders,common_rules):
    _,S,_=full_decomp
    for q in sorted(candidate_orders):
        if gap_ratio(S,q)>=float(common_rules["singular_gap_threshold"]):
            return int(q)
    return None


def matched_positive(vals_a,shapes_a,vals_b,shapes_b,min_hz,allow_b_superset=False):
    ia=positive_complex_indices(vals_a,min_hz)
    ib=positive_complex_indices(vals_b,min_hz)
    if len(ia)==0 or len(ib)==0:
        return None
    m=match_indices(np.asarray(vals_a)[ia],np.asarray(vals_b)[ib])
    if len(m)!=len(ia):
        return None
    if (not allow_b_superset) and len(ia)!=len(ib):
        return None
    aidx=[int(ia[i]) for i,j,d in m]
    bidx=[int(ib[j]) for i,j,d in m]
    ds=[float(d) for i,j,d in m]
    return {
        "a_idx":aidx,"b_idx":bidx,"distances":ds,
        "a_vals":np.asarray(vals_a)[aidx],"b_vals":np.asarray(vals_b)[bidx],
        "a_shapes":np.asarray(shapes_a)[:,aidx],"b_shapes":np.asarray(shapes_b)[:,bidx]
    }


def crowding_components(vals,threshold):
    vals=np.asarray(vals,complex); n=len(vals)
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    ratios={}
    for i in range(n):
        for j in range(i+1,n):
            ai=max(-vals[i].real,0.0); aj=max(-vals[j].real,0.0)
            r=float(abs(vals[i].imag-vals[j].imag)/max(ai+aj,1e-12))
            ratios[(i,j)]=r
            if r<=float(threshold): union(i,j)
    groups={}
    for i in range(n): groups.setdefault(find(i),[]).append(i)
    clusters=[v for v in groups.values() if len(v)>1]
    singletons=[v[0] for v in groups.values() if len(v)==1]
    return clusters,singletons,ratios


def _common_gate(fits,decomps,candidate_orders,rules):
    common=rules["common"]
    q=select_observable_order(decomps["full"],candidate_orders,common)
    out={"selected_order":q,"common_status":"OK"}
    if q is None:
        out["common_status"]="REFUSE_NO_ORDER"; return out
    if q==max(candidate_orders) and bool(common["refuse_selected_order_at_grid_max"]):
        out["common_status"]="REFUSE_EDGE_ORDER"; return out
    vals,_=fits["full"][q]
    if bool(common["refuse_any_unstable_selected_pole"]) and np.any(np.real(vals)>=0):
        out["common_status"]="REFUSE_UNSTABLE"; return out
    if len(positive_complex_indices(vals,common["complex_frequency_min_hz"]))==0:
        out["common_status"]="REFUSE_NO_COMPLEX_STRUCTURE"; return out
    return out


def _next_order(q,candidate_orders):
    larger=sorted(x for x in candidate_orders if x>q)
    return None if not larger else larger[0]


def evaluate_scalar_layer(fits,decomps,candidate_orders,rules):
    base=_common_gate(fits,decomps,candidate_orders,rules)
    q=base["selected_order"]
    out={**base,"decision":""}
    if base["common_status"]!="OK":
        out["decision"]=base["common_status"]; return out
    nq=_next_order(q,candidate_orders)
    if nq is None:
        out["decision"]="REFUSE_EDGE_ORDER"; return out
    min_hz=float(rules["common"]["complex_frequency_min_hz"])
    a=matched_positive(fits["first_half"][q][0],fits["first_half"][q][1],fits["second_half"][q][0],fits["second_half"][q][1],min_hz)
    b=matched_positive(fits["full"][q][0],fits["full"][q][1],fits["full"][nq][0],fits["full"][nq][1],min_hz,allow_b_superset=True)
    if a is None or b is None:
        out["decision"]="REFUSE_SCALAR_MATCHING"; return out
    out["split_median_pole_distance"]=float(np.median(a["distances"]))
    out["cross_order_median_pole_distance"]=float(np.median(b["distances"]))
    sr=rules["scalar_layer"]
    if out["split_median_pole_distance"]>float(sr["complex_split_median_distance_max"]):
        out["decision"]="REFUSE_SCALAR_NONSTATIONARY"; return out
    if out["cross_order_median_pole_distance"]>float(sr["complex_cross_order_median_distance_max"]):
        out["decision"]="REFUSE_SCALAR_ORDER_UNSTABLE"; return out
    out["decision"]="ADMIT_SCALAR_SPECTRUM"
    return out


def evaluate_modal_layer(fits,decomps,candidate_orders,rules):
    base=_common_gate(fits,decomps,candidate_orders,rules)
    q=base["selected_order"]
    out={**base,"decision":"","mode_claims":[]}
    if base["common_status"]!="OK":
        out["decision"]=base["common_status"]; return out
    nq=_next_order(q,candidate_orders)
    if nq is None:
        out["decision"]="REFUSE_EDGE_ORDER"; return out
    min_hz=float(rules["common"]["complex_frequency_min_hz"])
    split=matched_positive(fits["first_half"][q][0],fits["first_half"][q][1],fits["second_half"][q][0],fits["second_half"][q][1],min_hz)
    cross=matched_positive(fits["full"][q][0],fits["full"][q][1],fits["full"][nq][0],fits["full"][nq][1],min_hz,allow_b_superset=True)
    if split is None or cross is None:
        out["decision"]="REFUSE_MODAL_MATCHING"; return out
    mr=rules["modal_layer"]
    clusters,singletons,_=crowding_components(split["a_vals"],mr["crowding_ratio_subspace_only_le"])
    ok=True
    claims=[]
    for i in singletons:
        sm=mac(split["a_shapes"][:,i],split["b_shapes"][:,i])
        # Match the first-half pole to the selected full-order pole, then use that full pole's cross-order match.
        fullmatch=match_indices([split["a_vals"][i]],cross["a_vals"])
        om=np.nan
        if fullmatch:
            fj=fullmatch[0][1]
            om=mac(cross["a_shapes"][:,fj],cross["b_shapes"][:,fj])
        admit=np.isfinite(sm) and sm>=float(mr["individual_split_MAC_min"]) and np.isfinite(om) and om>=float(mr["individual_cross_order_MAC_min"])
        claims.append({"kind":"INDIVIDUAL","local_index":int(i),"split_MAC":float(sm) if np.isfinite(sm) else np.nan,"cross_order_MAC":float(om) if np.isfinite(om) else np.nan,"admit":bool(admit)})
        ok=ok and admit
    for cl in clusters:
        ss=subspace_similarity(split["a_shapes"][:,cl],split["b_shapes"][:,cl])
        # Map cluster first-half poles to full selected poles, then to next order.
        fm=match_indices(split["a_vals"][cl],cross["a_vals"])
        css=np.nan
        if len(fm)==len(cl):
            full_cols=[j for i,j,d in fm]
            css=subspace_similarity(cross["a_shapes"][:,full_cols],cross["b_shapes"][:,full_cols])
        admit=np.isfinite(ss) and ss>=float(mr["split_subspace_similarity_min"]) and np.isfinite(css) and css>=float(mr["cross_order_subspace_similarity_min"])
        claims.append({"kind":"SUBSPACE","local_indices":";".join(str(int(x)) for x in cl),"split_subspace_similarity":float(ss) if np.isfinite(ss) else np.nan,"cross_order_subspace_similarity":float(css) if np.isfinite(css) else np.nan,"admit":bool(admit)})
        ok=ok and admit
    out["mode_claims"]=claims
    out["decision"]="ADMIT_MODAL_STRUCTURE" if ok and claims else "REFUSE_MODAL_UNSTABLE"
    return out


def evaluate_system_layer(fits,decomps,candidate_orders,rules):
    base=_common_gate(fits,decomps,candidate_orders,rules)
    q=base["selected_order"]
    out={**base,"decision":""}
    if base["common_status"]!="OK":
        out["decision"]=base["common_status"]; return out
    nq=_next_order(q,candidate_orders)
    if nq is None:
        out["decision"]="REFUSE_EDGE_ORDER"; return out
    min_hz=float(rules["common"]["complex_frequency_min_hz"])
    split=matched_positive(fits["first_half"][q][0],fits["first_half"][q][1],fits["second_half"][q][0],fits["second_half"][q][1],min_hz)
    cross=matched_positive(fits["full"][q][0],fits["full"][q][1],fits["full"][nq][0],fits["full"][nq][1],min_hz,allow_b_superset=True)
    if split is None or cross is None:
        out["decision"]="REFUSE_SYSTEM_MATCHING"; return out
    sr=rules["system_layer"]
    if len(split["a_vals"])<int(sr["minimum_positive_complex_modes"]):
        out["decision"]="REFUSE_SYSTEM_INSUFFICIENT_RELATIONAL_MODES"; return out
    out["split_whole_subspace_similarity"]=subspace_similarity(split["a_shapes"],split["b_shapes"])
    out["split_channel_participation_TV"]=participation_tv(split["a_shapes"],split["b_shapes"])
    out["split_relational_pole_geometry_distance"]=relational_geometry_distance(split["a_vals"],split["b_vals"])
    out["cross_order_whole_subspace_similarity"]=subspace_similarity(cross["a_shapes"],cross["b_shapes"])
    out["cross_order_channel_participation_TV"]=participation_tv(cross["a_shapes"],cross["b_shapes"])
    out["cross_order_relational_pole_geometry_distance"]=relational_geometry_distance(cross["a_vals"],cross["b_vals"])
    checks=[
        np.isfinite(out["split_whole_subspace_similarity"]) and out["split_whole_subspace_similarity"]>=float(sr["split_whole_subspace_similarity_min"]),
        np.isfinite(out["cross_order_whole_subspace_similarity"]) and out["cross_order_whole_subspace_similarity"]>=float(sr["cross_order_whole_subspace_similarity_min"]),
        np.isfinite(out["split_channel_participation_TV"]) and out["split_channel_participation_TV"]<=float(sr["split_channel_participation_TV_max"]),
        np.isfinite(out["cross_order_channel_participation_TV"]) and out["cross_order_channel_participation_TV"]<=float(sr["cross_order_channel_participation_TV_max"]),
        np.isfinite(out["split_relational_pole_geometry_distance"]) and out["split_relational_pole_geometry_distance"]<=float(sr["split_relational_pole_geometry_distance_max"]),
        np.isfinite(out["cross_order_relational_pole_geometry_distance"]) and out["cross_order_relational_pole_geometry_distance"]<=float(sr["cross_order_relational_pole_geometry_distance_max"]),
    ]
    out["decision"]="ADMIT_SYSTEM_ORGANIZATION" if all(checks) else "REFUSE_SYSTEM_REORGANIZED_OR_UNSTABLE"
    return out
