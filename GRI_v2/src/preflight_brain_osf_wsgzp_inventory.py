from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests

NODE = "wsgzp"
API = f"https://api.osf.io/v2/nodes/{NODE}/files/"
KEYWORDS = (
    "seeg", "eeg", "metric", "moi", "preprocess", "stim", "trial",
    "predict", "radius", "deriv", "csv", "pickle", "pkl"
)
MAX_PAGES_PER_LIST = 100
TIMEOUT = 45


def get_json(url: str) -> dict:
    r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "SymC-GRI-source-preflight/1.0"})
    r.raise_for_status()
    return r.json()


def list_pages(url: str):
    seen = set()
    pages = 0
    while url:
        if url in seen:
            raise RuntimeError(f"pagination loop at {url}")
        seen.add(url)
        pages += 1
        if pages > MAX_PAGES_PER_LIST:
            raise RuntimeError("pagination ceiling exceeded")
        payload = get_json(url)
        for item in payload.get("data", []):
            yield item
        url = payload.get("links", {}).get("next")


def compact_file(item: dict, parent_path: str = "") -> dict:
    attrs = item.get("attributes", {})
    links = item.get("links", {})
    name = attrs.get("name")
    kind = attrs.get("kind")
    materialized = attrs.get("materialized_path") or attrs.get("path") or ""
    path = materialized if materialized else f"{parent_path}/{name}".replace("//", "/")
    return {
        "id": item.get("id"),
        "name": name,
        "kind": kind,
        "path": path,
        "size": attrs.get("size"),
        "date_modified": attrs.get("date_modified"),
        "download": links.get("download"),
        "files": links.get("move") if False else None,
        "_relationships": item.get("relationships", {}),
        "_links": links,
    }


def child_url(item: dict) -> str | None:
    rel = item.get("relationships", {}).get("files", {})
    links = rel.get("links", {})
    related = links.get("related", {})
    if isinstance(related, dict):
        return related.get("href")
    if isinstance(related, str):
        return related
    # OSF file API commonly exposes folder listing through links["new_folder"]
    # only for mutation; if no relationship is present we do not invent a path.
    return None


def main():
    providers = list(list_pages(API))
    provider_summary = []
    roots = []
    for p in providers:
        attrs = p.get("attributes", {})
        rel = p.get("relationships", {})
        files_rel = rel.get("files", {}).get("links", {}).get("related", {})
        href = files_rel.get("href") if isinstance(files_rel, dict) else files_rel
        provider_summary.append({
            "id": p.get("id"),
            "name": attrs.get("name"),
            "node": NODE,
            "root_files_url": href,
        })
        if href:
            roots.append((p.get("id"), href))

    all_entries = []
    queue = list(roots)
    visited_lists = set()
    while queue:
        provider_id, url = queue.pop(0)
        if not url or url in visited_lists:
            continue
        visited_lists.add(url)
        for item in list_pages(url):
            rec = compact_file(item)
            rec["provider_id"] = provider_id
            rel = rec.pop("_relationships", {})
            links = rec.pop("_links", {})
            all_entries.append(rec)
            kind = rec.get("kind")
            if kind == "folder":
                files_rel = item.get("relationships", {}).get("files", {}).get("links", {}).get("related", {})
                href = files_rel.get("href") if isinstance(files_rel, dict) else files_rel
                if href:
                    queue.append((provider_id, href))

    relevant = []
    for rec in all_entries:
        hay = f"{rec.get('name','')} {rec.get('path','')}".lower()
        if any(k in hay for k in KEYWORDS):
            relevant.append(rec)

    result = {
        "schema": "GRI_BRAIN_OSF_WSGZP_INVENTORY_PREFLIGHT_V01",
        "status": "PASS" if provider_summary else "FAIL_NO_PROVIDER",
        "node": NODE,
        "api": API,
        "providers": provider_summary,
        "n_list_endpoints_visited": len(visited_lists),
        "n_entries": len(all_entries),
        "n_keyword_relevant_entries": len(relevant),
        "relevant_entries": relevant,
        "all_entries": all_entries if len(all_entries) <= 500 else None,
        "all_entries_omitted_if_large": len(all_entries) > 500,
        "scientific_outcomes_opened": False,
        "purpose": (
            "Resolve whether the upstream OSF node exposes a raw/processed source "
            "with explicit spatial-radius provenance sufficient for exact source-native reproduction."
        ),
    }

    out = Path("brain_source_qualification_outputs")
    out.mkdir(exist_ok=True)
    (out / "osf_wsgzp_inventory_preflight_v01.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
