#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, urllib.request, urllib.parse
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SHARMA2010_OSF_SOURCE_DISCOVERY_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"sharma2010_osf_source_discovery_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/vnd.api+json"})
    with urllib.request.urlopen(req,timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))

def page_all(url):
    out=[]
    while url:
        j=get_json(url)
        out.extend(j.get("data",[]))
        nxt=(j.get("links") or {}).get("next")
        url=nxt
    return out

def related_href(rel):
    if not rel: return None
    links=rel.get("links") or {}
    related=links.get("related")
    if isinstance(related,str): return related
    if isinstance(related,dict): return related.get("href")
    return None

def walk_files(url,path_prefix=""):
    items=page_all(url)
    out=[]
    for it in items:
        a=it.get("attributes") or {}
        kind=a.get("kind")
        name=a.get("name") or it.get("id")
        path=f"{path_prefix}/{name}".lstrip("/")
        rec={
          "id":it.get("id"),"kind":kind,"name":name,"path":path,
          "size":a.get("size"),"date_created":a.get("date_created"),"date_modified":a.get("date_modified"),
          "extra":a.get("extra"),"links":it.get("links"),"relationships":it.get("relationships")
        }
        if kind=="folder":
            files_url=related_href((it.get("relationships") or {}).get("files"))
            if files_url:
                rec["children"]=walk_files(files_url,path)
            else:
                rec["children"]=[]
        out.append(rec)
    return out

def flatten(nodes):
    out=[]
    for n in nodes:
        out.append({k:v for k,v in n.items() if k!="children"})
        if n.get("children"): out.extend(flatten(n["children"]))
    return out

def discover_node(node_id, label):
    providers=page_all(f"https://api.osf.io/v2/nodes/{node_id}/files/")
    trees=[]
    for p in providers:
        a=p.get("attributes") or {}
        provider_name=a.get("name") or p.get("id")
        href=f"https://api.osf.io/v2/nodes/{node_id}/files/{p.get('id')}/"
        try:
            tree=walk_files(href,f"{label}/{provider_name}")
        except Exception:
            rel=(p.get("relationships") or {}).get("files")
            fallback=related_href(rel)
            tree=walk_files(fallback,f"{label}/{provider_name}") if fallback else []
        trees.append({"node_id":node_id,"node_label":label,"provider_id":p.get("id"),"provider_name":provider_name,"tree":tree})
    return trees

def collect_nodes(root_id):
    seen=set()
    out=[]
    stack=[root_id]
    while stack:
        nid=stack.pop()
        if nid in seen: continue
        seen.add(nid)
        n=get_json(f"https://api.osf.io/v2/nodes/{nid}/")
        attrs=(n.get("data") or {}).get("attributes",{})
        label=attrs.get("title") or nid
        out.append({"id":nid,"title":label,"category":attrs.get("category")})
        try:
            children=page_all(f"https://api.osf.io/v2/nodes/{nid}/children/")
            for ch in children:
                cid=ch.get("id")
                if cid and cid not in seen: stack.append(cid)
        except Exception:
            pass
    return out

def main():
    cfg=json.loads(CFG.read_text())
    node=cfg["replication_source"]["osf_node"]
    root=get_json(f"https://api.osf.io/v2/nodes/{node}/")
    nodes=collect_nodes(node)
    alltrees=[]
    for n in nodes:
        alltrees.extend(discover_node(n["id"],n["title"]))
    flat=[]
    for p in alltrees: flat.extend(flatten(p["tree"]))
    keys=[k.lower() for k in cfg["keywords"]]
    hits=[]
    for f in flat:
        name=(f.get("path") or "").lower()
        matched=[k for k in keys if k in name]
        if matched:
            hits.append({"path":f.get("path"),"kind":f.get("kind"),"size":f.get("size"),"matched_keywords":matched,"links":f.get("links"),"extra":f.get("extra")})
    result={
      "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "status":"PASS_OSF_SOURCE_DISCOVERY",
      "node":{
        "id":node,
        "title":(root.get("data") or {}).get("attributes",{}).get("title"),
        "description":(root.get("data") or {}).get("attributes",{}).get("description"),
        "date_modified":(root.get("data") or {}).get("attributes",{}).get("date_modified")
      },
      "node_count":len(nodes),"provider_count":len(alltrees),"file_folder_count":len(flat),
      "nodes":nodes,"providers":alltrees,"keyword_hits":hits,
      "experimental_values_opened":False
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
      "status":result["status"],"node":result["node"],"node_count":len(nodes),"provider_count":len(alltrees),"file_folder_count":len(flat),
      "keyword_hits":[{"path":x["path"],"kind":x["kind"],"size":x["size"],"matched_keywords":x["matched_keywords"]} for x in hits],
      "experimental_values_opened":False
    },indent=2))
    print("BIO_CHI_SHARMA_OSF_SOURCE_DISCOVERY_PASS")

if __name__=="__main__": main()
