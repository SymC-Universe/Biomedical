#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html.parser
import io
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

GEO_ACCESSIONS = ["GSE145356", "GSE164716", "GSE237228", "GSE97682", "GSE255671"]
HASH_LIMIT_BYTES = 100 * 1024 * 1024
USER_AGENT = "BioChiSourceFreeze/0.1 (+reviewer-reproducibility)"

class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
    def handle_starttag(self, tag: str, attrs):
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.hrefs.append(value)


def request(url: str, method: str = "GET"):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method=method)
    return urllib.request.urlopen(req, timeout=180)


def get_bytes(url: str) -> tuple[bytes, dict]:
    with request(url, "GET") as r:
        data = r.read()
        meta = {
            "resolved_url": r.geturl(),
            "content_type": r.headers.get("Content-Type"),
            "content_length_header": r.headers.get("Content-Length"),
            "last_modified": r.headers.get("Last-Modified"),
            "etag": r.headers.get("ETag"),
        }
    return data, meta


def head(url: str) -> dict:
    try:
        with request(url, "HEAD") as r:
            return {
                "resolved_url": r.geturl(),
                "content_type": r.headers.get("Content-Type"),
                "content_length_header": r.headers.get("Content-Length"),
                "last_modified": r.headers.get("Last-Modified"),
                "etag": r.headers.get("ETag"),
            }
    except Exception as exc:
        return {"head_error": f"{type(exc).__name__}: {exc}"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def probe_size(url: str) -> tuple[int | None, dict]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            meta = {
                "probe_status": getattr(r, "status", None),
                "probe_content_range": r.headers.get("Content-Range"),
                "probe_content_length": r.headers.get("Content-Length"),
            }
            cr = r.headers.get("Content-Range")
            if cr and "/" in cr:
                total = cr.rsplit("/", 1)[1]
                if total.isdigit():
                    return int(total), meta
            cl = r.headers.get("Content-Length")
            if cl and cl.isdigit() and getattr(r, "status", None) == 200:
                return int(cl), meta
            return None, meta
    except Exception as exc:
        return None, {"probe_error": f"{type(exc).__name__}: {exc}"}


def geo_bucket(gse: str) -> str:
    m = re.fullmatch(r"GSE(\d+)", gse)
    if not m:
        raise ValueError(gse)
    digits = m.group(1)
    return f"GSE{digits[:-3]}nnn"


def geo_root(gse: str) -> str:
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{geo_bucket(gse)}/{gse}/"


def list_directory(url: str) -> tuple[list[str], str]:
    raw, _ = get_bytes(url)
    text = raw.decode("utf-8", errors="replace")
    parser = LinkParser()
    parser.feed(text)
    names: list[str] = []
    for href in parser.hrefs:
        parsed = urllib.parse.urlparse(href)
        path = parsed.path
        name = path.rstrip("/").split("/")[-1]
        if not name or name in {"..", "."}:
            continue
        if href.startswith("?") or href.startswith("#"):
            continue
        names.append(urllib.parse.unquote(name))
    return sorted(set(names)), sha256(raw)


def freeze_file(url: str) -> dict:
    meta = head(url)
    size = None
    try:
        if meta.get("content_length_header"):
            size = int(meta["content_length_header"])
    except Exception:
        size = None
    record = {"url": url, **meta, "content_length_bytes": size}
    if size is None:
        size, probe_meta = probe_size(url)
        record.update(probe_meta)
        record["content_length_bytes"] = size
    if size is None:
        record.update({
            "sha256": None,
            "hash_status": "DEFERRED_UNKNOWN_SIZE",
            "hash_limit_bytes": HASH_LIMIT_BYTES,
            "content_interpreted": False,
        })
        return record
    if size > HASH_LIMIT_BYTES:
        record.update({
            "sha256": None,
            "hash_status": "DEFERRED_LARGE_FILE",
            "hash_limit_bytes": HASH_LIMIT_BYTES,
            "content_interpreted": False,
        })
        return record
    try:
        data, get_meta = get_bytes(url)
        record.update(get_meta)
        record["content_length_bytes"] = len(data)
        record["sha256"] = sha256(data)
        record["hash_status"] = "FROZEN"
        record["content_interpreted"] = False
    except Exception as exc:
        record["sha256"] = None
        record["hash_status"] = "ERROR"
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["content_interpreted"] = False
    return record


def freeze_geo(gse: str) -> dict:
    root = geo_root(gse)
    result = {"accession": gse, "root": root, "directories": {}, "failures": []}
    for dirname in ("suppl", "matrix", "soft"):
        durl = urllib.parse.urljoin(root, dirname + "/")
        try:
            names, listing_sha = list_directory(durl)
        except Exception as exc:
            result["directories"][dirname] = {
                "url": durl,
                "status": "UNAVAILABLE",
                "error": f"{type(exc).__name__}: {exc}",
            }
            continue
        entries = []
        for name in names:
            # Keep only files in these flat GEO directories; nested links are not expected here.
            furl = urllib.parse.urljoin(durl, urllib.parse.quote(name))
            rec = freeze_file(furl)
            rec["name"] = name
            entries.append(rec)
            if rec.get("hash_status") == "ERROR":
                result["failures"].append(f"{dirname}/{name}: {rec.get('error')}")
        result["directories"][dirname] = {
            "url": durl,
            "status": "ENUMERATED",
            "listing_sha256": listing_sha,
            "file_count": len(entries),
            "files": entries,
        }
    return result


def freeze_jarus_code() -> dict:
    url = "https://doi.org/10.1371/journal.pone.0286416.s015"
    data, meta = get_bytes(url)
    rec = {
        "id": "jarus_nfkb_s1_code",
        "doi_asset": url,
        "size_bytes": len(data),
        "sha256": sha256(data),
        "content_interpreted": False,
        **meta,
    }
    if not zipfile.is_zipfile(io.BytesIO(data)):
        rec["archive_status"] = "NOT_ZIP"
        return rec
    members = []
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            payload = zf.read(info.filename)
            members.append({
                "path": info.filename,
                "size_bytes": len(payload),
                "sha256": sha256(payload),
            })
    rec["archive_status"] = "ZIP_OK"
    rec["member_count"] = len(members)
    rec["members"] = members
    return rec


def main() -> None:
    failures: list[str] = []
    geos = []
    for gse in GEO_ACCESSIONS:
        try:
            frozen = freeze_geo(gse)
            geos.append(frozen)
            failures.extend([f"{gse}: {x}" for x in frozen.get("failures", [])])
        except Exception as exc:
            geos.append({"accession": gse, "fatal_error": f"{type(exc).__name__}: {exc}"})
            failures.append(f"{gse}: fatal {type(exc).__name__}: {exc}")
    try:
        jarus = freeze_jarus_code()
        if jarus.get("archive_status") != "ZIP_OK":
            failures.append("Jaruszewicz S1 Code did not resolve to a ZIP archive")
    except Exception as exc:
        jarus = {"fatal_error": f"{type(exc).__name__}: {exc}"}
        failures.append(f"Jaruszewicz S1 Code: {type(exc).__name__}: {exc}")

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_type": "outcome_blind_source_file_freeze",
        "molecular_values_interpreted": False,
        "hash_limit_bytes": HASH_LIMIT_BYTES,
        "geo": geos,
        "jarus_nfkb_s1_code": jarus,
        "failures": failures,
    }
    out = OUT / "external_source_freeze_v0_1.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "generated": str(out.relative_to(ROOT)),
        "geo_count": len(geos),
        "jarus_archive_status": jarus.get("archive_status"),
        "failure_count": len(failures),
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit("BIO_CHI_EXTERNAL_SOURCE_FREEZE_PARTIAL")
    print("BIO_CHI_EXTERNAL_SOURCE_FREEZE_PASS")

if __name__ == "__main__":
    main()
