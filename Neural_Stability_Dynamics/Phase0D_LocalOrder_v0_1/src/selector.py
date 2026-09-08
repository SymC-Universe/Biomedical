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
    return np.abs(z[:,None]-z[None,:])/scale


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


def select_observable_order(decomp,candidate_orders,common_rules):
    _,S,_=decomp
    for q in sorted(candidate_orders):
        if gap_ratio(S,q)>=float(common_rules['singular_gap_threshold']):
            return int(q)
    return None


def _next_order(q,candidate_orders):
    larger=sorted(x for x in candidate_orders if x>q)
    return None if not larger else larger[0]


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


def _segment_gate(fits,decomps,segment,candidate_orders,rules):
    common=rules['common']
    q=select_observable_order(decomps[segment],candidate_orders,common)
    out={'selected_order':q,'status':'OK'}
    if q is None:
        out['status']='REFUSE_NO_ORDER'; return out
    if q==max(candidate_orders) and bool(common['refuse_selected_order_at_grid_max']):
        out['status']='REFUSE_EDGE_ORDER'; return out
    vals,_=fits[segment][q]
    if bool(common['refuse_any_unstable_selected_pole']) and np.any(np.real(vals)>=0):
        out['status']='REFUSE_UNSTABLE'; return out
    if len(positive_complex_indices(vals,common['complex_frequency_min_hz']))==0:
        out['status']='REFUSE_NO_COMPLEX_STRUCTURE'; return out
    return out


def segment_orders(decomps,candidate_orders,rules):
    out={}
    for seg in ['full','first_half','second_half']:
        q=select_observable_order(decomps[seg],candidate_orders,rules['common'])
        out[seg]=q
    return out


def _shape_match(vals_a,shapes_a,vals_b,shapes_b,min_hz,allow_b_superset=False):
    ia=positive_complex_indices(vals_a,min_hz)
    ib=positive_complex_indices(vals_b,min_hz)
    if len(ia)==0 or len(ib)==0 or len(ib)<len(ia):
        return None
    if (not allow_b_superset) and len(ia)!=len(ib):
        return None
    M=np.empty((len(ia),len(ib)),float)
    for r,i in enumerate(ia):
        for c,j in enumerate(ib):
            x=mac(np.asarray(shapes_a)[:,i],np.asarray(shapes_b)[:,j])
            M[r,c]=-1.0 if not np.isfinite(x) else x
    rr,cc=linear_sum_assignment(-M)
    if len(rr)!=len(ia):
        return None
    aidx=[int(ia[r]) for r in rr]; bidx=[int(ib[c]) for c in cc]
    return {
        'a_idx':aidx,'b_idx':bidx,'MACs':[float(M[r,c]) for r,c in zip(rr,cc)],
        'a_vals':np.asarray(vals_a)[aidx],'b_vals':np.asarray(vals_b)[bidx],
        'a_shapes':np.asarray(shapes_a)[:,aidx],'b_shapes':np.asarray(shapes_b)[:,bidx]
    }


def _pole_match(vals_a,shapes_a,vals_b,shapes_b,min_hz,allow_b_superset=False):
    ia=positive_complex_indices(vals_a,min_hz); ib=positive_complex_indices(vals_b,min_hz)
    if len(ia)==0 or len(ib)==0 or len(ib)<len(ia): return None
    if (not allow_b_superset) and len(ia)!=len(ib): return None
    m=match_indices(np.asarray(vals_a)[ia],np.asarray(vals_b)[ib])
    if len(m)!=len(ia): return None
    aidx=[int(ia[i]) for i,j,d in m]; bidx=[int(ib[j]) for i,j,d in m]
    return {
        'a_idx':aidx,'b_idx':bidx,'distances':[float(d) for i,j,d in m],
        'a_vals':np.asarray(vals_a)[aidx],'b_vals':np.asarray(vals_b)[bidx],
        'a_shapes':np.asarray(shapes_a)[:,aidx],'b_shapes':np.asarray(shapes_b)[:,bidx]
    }


def _cross_order_pole(fits,segment,q,candidate_orders,min_hz):
    nq=_next_order(q,candidate_orders)
    if nq is None: return None,None
    a=_pole_match(fits[segment][q][0],fits[segment][q][1],fits[segment][nq][0],fits[segment][nq][1],min_hz,allow_b_superset=True)
    return nq,a


def _cross_order_shape(fits,segment,q,candidate_orders,min_hz):
    nq=_next_order(q,candidate_orders)
    if nq is None: return None,None
    a=_shape_match(fits[segment][q][0],fits[segment][q][1],fits[segment][nq][0],fits[segment][nq][1],min_hz,allow_b_superset=True)
    return nq,a


def _base_local(fits,decomps,candidate_orders,rules):
    gf=_segment_gate(fits,decomps,'first_half',candidate_orders,rules)
    gs=_segment_gate(fits,decomps,'second_half',candidate_orders,rules)
    qfull=select_observable_order(decomps['full'],candidate_orders,rules['common'])
    out={'full_selected_order':qfull,'first_selected_order':gf['selected_order'],'second_selected_order':gs['selected_order']}
    if gf['status']!='OK': out['local_status']=gf['status']; return out
    if gs['status']!='OK': out['local_status']=gs['status']; return out
    out['local_status']='OK'
    return out


def evaluate_scalar_layer(fits,decomps,candidate_orders,rules):
    out=_base_local(fits,decomps,candidate_orders,rules); out['decision']=''
    if out['local_status']!='OK': out['decision']=out['local_status']; return out
    q1=int(out['first_selected_order']); q2=int(out['second_selected_order'])
    if q1!=q2:
        out['decision']='REFUSE_SCALAR_ORDER_CHANGE'; return out
    min_hz=float(rules['common']['complex_frequency_min_hz'])
    split=_pole_match(fits['first_half'][q1][0],fits['first_half'][q1][1],fits['second_half'][q2][0],fits['second_half'][q2][1],min_hz)
    n1,c1=_cross_order_pole(fits,'first_half',q1,candidate_orders,min_hz)
    n2,c2=_cross_order_pole(fits,'second_half',q2,candidate_orders,min_hz)
    if split is None or c1 is None or c2 is None:
        out['decision']='REFUSE_SCALAR_MATCHING'; return out
    out['split_median_pole_distance']=float(np.median(split['distances']))
    out['first_cross_order_median_pole_distance']=float(np.median(c1['distances']))
    out['second_cross_order_median_pole_distance']=float(np.median(c2['distances']))
    sr=rules['scalar_layer']
    if out['split_median_pole_distance']>float(sr['complex_split_median_distance_max']):
        out['decision']='REFUSE_SCALAR_NONSTATIONARY'; return out
    if max(out['first_cross_order_median_pole_distance'],out['second_cross_order_median_pole_distance'])>float(sr['complex_cross_order_median_distance_max']):
        out['decision']='REFUSE_SCALAR_ORDER_UNSTABLE'; return out
    out['decision']='ADMIT_SCALAR_SPECTRUM'; return out


def _modal_compare_pair(vals_a,shapes_a,vals_b,shapes_b,min_hz,mr,allow_b_superset=False):
    mm=_shape_match(vals_a,shapes_a,vals_b,shapes_b,min_hz,allow_b_superset=allow_b_superset)
    if mm is None: return None
    clusters,singletons,_=crowding_components(mm['a_vals'],mr['crowding_ratio_subspace_only_le'])
    claims=[]; ok=True
    for i in singletons:
        mv=mac(mm['a_shapes'][:,i],mm['b_shapes'][:,i])
        admit=np.isfinite(mv) and mv>=float(mr['individual_split_MAC_min'])
        claims.append({'kind':'INDIVIDUAL','local_index':int(i),'similarity':float(mv) if np.isfinite(mv) else np.nan,'admit':bool(admit)})
        ok=ok and admit
    for cl in clusters:
        ss=subspace_similarity(mm['a_shapes'][:,cl],mm['b_shapes'][:,cl])
        admit=np.isfinite(ss) and ss>=float(mr['split_subspace_similarity_min'])
        claims.append({'kind':'SUBSPACE','local_indices':';'.join(map(str,cl)),'similarity':float(ss) if np.isfinite(ss) else np.nan,'admit':bool(admit)})
        ok=ok and admit
    return {'match':mm,'claims':claims,'ok':bool(ok and claims)}


def evaluate_modal_layer(fits,decomps,candidate_orders,rules):
    out=_base_local(fits,decomps,candidate_orders,rules); out['decision']=''; out['mode_claims']=[]
    if out['local_status']!='OK': out['decision']=out['local_status']; return out
    q1=int(out['first_selected_order']); q2=int(out['second_selected_order'])
    if q1!=q2:
        out['decision']='REFUSE_MODAL_ORDER_CHANGE'; return out
    min_hz=float(rules['common']['complex_frequency_min_hz']); mr=rules['modal_layer']
    split=_modal_compare_pair(fits['first_half'][q1][0],fits['first_half'][q1][1],fits['second_half'][q2][0],fits['second_half'][q2][1],min_hz,mr)
    n1,c1=_cross_order_shape(fits,'first_half',q1,candidate_orders,min_hz)
    n2,c2=_cross_order_shape(fits,'second_half',q2,candidate_orders,min_hz)
    if split is None or c1 is None or c2 is None:
        out['decision']='REFUSE_MODAL_MATCHING'; return out
    # Cross-order stability is carrier based, independent of pole proximity.
    def cross_ok(cm):
        clusters,singletons,_=crowding_components(cm['a_vals'],mr['crowding_ratio_subspace_only_le'])
        ok=True
        for i in singletons:
            v=mac(cm['a_shapes'][:,i],cm['b_shapes'][:,i]); ok=ok and np.isfinite(v) and v>=float(mr['individual_cross_order_MAC_min'])
        for cl in clusters:
            v=subspace_similarity(cm['a_shapes'][:,cl],cm['b_shapes'][:,cl]); ok=ok and np.isfinite(v) and v>=float(mr['cross_order_subspace_similarity_min'])
        return bool(ok)
    out['mode_claims']=split['claims']
    out['split_carrier_ok']=split['ok']; out['first_cross_order_carrier_ok']=cross_ok(c1); out['second_cross_order_carrier_ok']=cross_ok(c2)
    out['decision']='ADMIT_MODAL_STRUCTURE' if out['split_carrier_ok'] and out['first_cross_order_carrier_ok'] and out['second_cross_order_carrier_ok'] else 'REFUSE_MODAL_UNSTABLE'
    return out


def cluster_objects(vals,shapes,crowd_threshold):
    vals=np.asarray(vals,complex); shapes=np.asarray(shapes,complex)
    clusters,singletons,_=crowding_components(vals,crowd_threshold)
    groups=[[i] for i in singletons]+[list(c) for c in clusters]
    groups=sorted(groups,key=lambda g: float(np.mean(vals[g].imag)))
    return [{'indices':g,'centroid':complex(np.mean(vals[g])),'basis':shapes[:,g],'size':len(g)} for g in groups]


def cluster_relational_compare(vals_a,shapes_a,vals_b,shapes_b,crowd_threshold):
    A=cluster_objects(vals_a,shapes_a,crowd_threshold); B=cluster_objects(vals_b,shapes_b,crowd_threshold)
    if len(A)!=len(B): return {'status':'CLUSTER_COUNT_CHANGED','distance':np.nan,'ok':False}
    if sorted(x['size'] for x in A)!=sorted(x['size'] for x in B): return {'status':'CLUSTER_SIGNATURE_CHANGED','distance':np.nan,'ok':False}
    if len(A)==0: return {'status':'NO_CLUSTERS','distance':np.nan,'ok':False}
    M=np.empty((len(A),len(B)),float)
    for i,a in enumerate(A):
        for j,b in enumerate(B): M[i,j]=subspace_similarity(a['basis'],b['basis'])
    rr,cc=linear_sum_assignment(-M)
    if len(rr)!=len(A): return {'status':'CLUSTER_MATCH_FAILED','distance':np.nan,'ok':False}
    if any(A[i]['size']!=B[j]['size'] for i,j in zip(rr,cc)):
        return {'status':'CLUSTER_SIZE_MATCH_FAILED','distance':np.nan,'ok':False}
    ca=np.asarray([A[i]['centroid'] for i in rr],complex); cb=np.asarray([B[j]['centroid'] for i,j in zip(rr,cc)],complex)
    if len(ca)<2:
        return {'status':'UNRESOLVED_INSUFFICIENT_RESOLVED_CLUSTERS','distance':np.nan,'ok':True}
    d=relational_geometry_distance(ca,cb)
    return {'status':'RESOLVED','distance':float(d),'ok':np.isfinite(d)}


def _system_pair(vals_a,shapes_a,vals_b,shapes_b,min_hz,sr,mr,allow_b_superset=False):
    mm=_shape_match(vals_a,shapes_a,vals_b,shapes_b,min_hz,allow_b_superset=allow_b_superset)
    if mm is None: return None
    A=mm['a_shapes']; B=mm['b_shapes']
    sub=subspace_similarity(A,B); tv=participation_tv(A,B)
    rg=cluster_relational_compare(mm['a_vals'],A,mm['b_vals'],B,mr['crowding_ratio_subspace_only_le'])
    carrier_ok=np.isfinite(sub) and sub>=float(sr['split_whole_subspace_similarity_min']) and np.isfinite(tv) and tv<=float(sr['split_channel_participation_TV_max'])
    geometry_ok=bool(rg['ok']) and (rg['status']!='RESOLVED' or rg['distance']<=float(sr['split_relational_pole_geometry_distance_max']))
    return {'subspace_similarity':sub,'participation_TV':tv,'relational':rg,'carrier_ok':bool(carrier_ok),'geometry_ok':bool(geometry_ok),'match':mm}


def evaluate_system_layer(fits,decomps,candidate_orders,rules):
    out=_base_local(fits,decomps,candidate_orders,rules); out['decision']=''
    if out['local_status']!='OK': out['decision']=out['local_status']; return out
    q1=int(out['first_selected_order']); q2=int(out['second_selected_order'])
    if q1!=q2:
        out['decision']='REFUSE_SYSTEM_ORDER_CHANGE'; return out
    min_hz=float(rules['common']['complex_frequency_min_hz']); sr=rules['system_layer']; mr=rules['modal_layer']
    i1=positive_complex_indices(fits['first_half'][q1][0],min_hz); i2=positive_complex_indices(fits['second_half'][q2][0],min_hz)
    if min(len(i1),len(i2))<int(sr['minimum_positive_complex_modes_for_carrier']):
        out['decision']='REFUSE_SYSTEM_INSUFFICIENT_RELATIONAL_MODES'; return out
    split=_system_pair(fits['first_half'][q1][0],fits['first_half'][q1][1],fits['second_half'][q2][0],fits['second_half'][q2][1],min_hz,sr,mr)
    n1,c1=_cross_order_shape(fits,'first_half',q1,candidate_orders,min_hz)
    n2,c2=_cross_order_shape(fits,'second_half',q2,candidate_orders,min_hz)
    if split is None or c1 is None or c2 is None:
        out['decision']='REFUSE_SYSTEM_MATCHING'; return out
    # For cross-order checks use matched selected-mode subsets only.
    def from_match(cm):
        A=cm['a_shapes']; B=cm['b_shapes']
        sub=subspace_similarity(A,B); tv=participation_tv(A,B)
        rg=cluster_relational_compare(cm['a_vals'],A,cm['b_vals'],B,mr['crowding_ratio_subspace_only_le'])
        carrier=np.isfinite(sub) and sub>=float(sr['cross_order_whole_subspace_similarity_min']) and np.isfinite(tv) and tv<=float(sr['cross_order_channel_participation_TV_max'])
        geom=bool(rg['ok']) and (rg['status']!='RESOLVED' or rg['distance']<=float(sr['cross_order_relational_pole_geometry_distance_max']))
        return {'subspace_similarity':sub,'participation_TV':tv,'relational':rg,'carrier_ok':bool(carrier),'geometry_ok':bool(geom)}
    co1=from_match(c1); co2=from_match(c2)
    out['split_whole_subspace_similarity']=split['subspace_similarity']
    out['split_channel_participation_TV']=split['participation_TV']
    out['split_relational_geometry_status']=split['relational']['status']
    out['split_relational_pole_geometry_distance']=split['relational']['distance']
    out['first_cross_order_whole_subspace_similarity']=co1['subspace_similarity']
    out['second_cross_order_whole_subspace_similarity']=co2['subspace_similarity']
    out['first_cross_order_channel_participation_TV']=co1['participation_TV']
    out['second_cross_order_channel_participation_TV']=co2['participation_TV']
    out['first_cross_order_relational_geometry_status']=co1['relational']['status']
    out['second_cross_order_relational_geometry_status']=co2['relational']['status']
    out['first_cross_order_relational_pole_geometry_distance']=co1['relational']['distance']
    out['second_cross_order_relational_pole_geometry_distance']=co2['relational']['distance']
    ok=split['carrier_ok'] and split['geometry_ok'] and co1['carrier_ok'] and co1['geometry_ok'] and co2['carrier_ok'] and co2['geometry_ok']
    if ok:
        unresolved=any(x['relational']['status'].startswith('UNRESOLVED') for x in [split,co1,co2])
        out['decision']='ADMIT_SYSTEM_ORGANIZATION_GEOMETRY_UNRESOLVED' if unresolved else 'ADMIT_SYSTEM_ORGANIZATION'
    else:
        out['decision']='REFUSE_SYSTEM_REORGANIZED_OR_UNSTABLE'
    return out
