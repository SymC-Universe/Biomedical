from __future__ import annotations

"""Read-only discovery probe for chronic SCC25 GEO file listings.

The script records public FTP/HTTP directory listings only. It does not download
large chronic molecular matrices, select features, or compute Chi_bio.
"""

import hashlib
import html.parser
import json
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
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-GRI-source-probe/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), {str(k): str(v) for k, v in response.headers.items()}


def probe() -> dict:
    report: dict = {
        "probe_version": "0.1",
        "purpose": "CHRONIC_GEO_FILE_DISCOVERY_NO_MOLECULAR_ANALYSIS",
        "chi_bio_outcomes_computed": False,
        "feature_selection_performed": False,
        "listings": {},
        "status": "RUNNING",
    }
    passes = 0
    for name, url in LISTINGS.items():
        entry = {"url": url}
        try:
            body, headers = _fetch(url)
            parser = LinkParser()
            parser.feed(body.decode("utf-8", errors="replace"))
            links = [x for x in parser.links if x not in {"../", "/"}]
            entry.update(
                {
                    "status": "PASS",
                    "body_sha256": hashlib.sha256(body).hexdigest(),
                    "body_size_bytes": len(body),
                    "last_modified": headers.get("Last-Modified"),
                    "links": links,
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
