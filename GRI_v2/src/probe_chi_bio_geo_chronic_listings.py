from __future__ import annotations

"""Read-only discovery probe for chronic SCC25 GEO file listings.

The script records public FTP/HTTP directory listings and file metadata via HEAD
requests. It does not download chronic molecular matrices, select features, or
compute Chi_bio.
"""

import hashlib
import html.parser
import json
import urllib.parse
import urllib.request
from pathlib import Path


LISTINGS = {
    "GSE98812_RNA_SUPPL": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/suppl/",
    "GSE98812_RNA_MATRIX": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98812/matrix/",
    "GSE98813_METHYLATION_SUPPL": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/suppl/",
    "GSE98813_METHYLATION_MATRIX": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE98nnn/GSE98813/matrix/",
}


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def _fetch(url: str, timeout: int = 60) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-GRI-source-probe/0.2"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), {str(k): str(v) for k, v in response.headers.items()}


def _head(url: str, timeout: int = 60) -> dict[str, str | int | None]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "SymC-GRI-source-probe/0.2"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        headers = {str(k): str(v) for k, v in response.headers.items()}
    length = headers.get("Content-Length")
    return {
        "content_length_bytes": int(length) if length is not None else None,
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
        "content_type": headers.get("Content-Type"),
    }


def _is_geo_file_link(base_url: str, href: str) -> bool:
    target = urllib.parse.urljoin(base_url, href)
    parsed = urllib.parse.urlparse(target)
    return parsed.hostname == "ftp.ncbi.nlm.nih.gov" and not target.endswith("/")


def probe() -> dict:
    report: dict = {
        "probe_version": "0.2",
        "purpose": "CHRONIC_GEO_FILE_DISCOVERY_AND_SIZE_PREFLIGHT_NO_MOLECULAR_ANALYSIS",
        "chi_bio_outcomes_computed": False,
        "feature_selection_performed": False,
        "chronic_molecular_files_downloaded": False,
        "listings": {},
        "status": "RUNNING",
    }
    passes = 0
    for name, url in LISTINGS.items():
        entry: dict = {"url": url}
        try:
            body, headers = _fetch(url)
            parser = LinkParser()
            parser.feed(body.decode("utf-8", errors="replace"))
            links = [x for x in parser.links if x not in {"../", "/"}]
            files = []
            for href in links:
                if not _is_geo_file_link(url, href):
                    continue
                file_url = urllib.parse.urljoin(url, href)
                file_entry = {"href": href, "url": file_url}
                try:
                    file_entry.update(_head(file_url))
                    file_entry["head_status"] = "PASS"
                except Exception as exc:
                    file_entry.update(
                        {
                            "head_status": "FAIL",
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        }
                    )
                files.append(file_entry)
            entry.update(
                {
                    "status": "PASS",
                    "body_sha256": hashlib.sha256(body).hexdigest(),
                    "body_size_bytes": len(body),
                    "last_modified": headers.get("Last-Modified"),
                    "links": links,
                    "geo_file_metadata": files,
                }
            )
            passes += 1
        except Exception as exc:
            entry.update(
                {
                    "status": "FAIL",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        report["listings"][name] = entry
    report["status"] = "PASS_AT_LEAST_ONE_LISTING" if passes else "FAIL_ALL_LISTINGS"
    return report


def main() -> int:
    report = probe()
    out = Path("development_outputs/chi_bio_geo_source_probe/GRI_CHI_BIO_CHRONIC_GEO_LISTINGS.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
