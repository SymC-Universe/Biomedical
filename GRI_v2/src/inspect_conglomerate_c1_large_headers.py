from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

CONFIG_REL = Path("GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json")
OUTPUT_REL = Path("GRI_v2/artifacts/GRI_CONGLOMERATE_C1_LARGE_SOURCE_HEADERS_20260918.json")
RANGE_END = 2 * 1024 * 1024 - 1


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def fetch_prefix(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes=0-{RANGE_END}",
            "User-Agent": "GRI-Conglomerate-C1-Large-Header/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(RANGE_END + 1)
        return data


def line_fields(data: bytes, index: int) -> List[str]:
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    if len(lines) <= index:
        return []
    return lines[index].split("\t")


def summarize(fields: List[str]) -> Dict[str, Any]:
    return {
        "field_count": len(fields),
        "first_fields": fields[:8],
        "last_fields": fields[-8:] if fields else [],
    }


def main() -> None:
    cfg = json.loads((repo_root() / CONFIG_REL).read_text(encoding="utf-8"))
    wanted = {"RNA_PANCAN_FINAL", "METHYLATION_MERGED_27K_450K"}
    rows = []
    for source in cfg["sources"]:
        if source["id"] not in wanted:
            continue
        data = fetch_prefix(source["url"])
        first = line_fields(data, 0)
        second = line_fields(data, 1)
        rows.append({
            "id": source["id"],
            "bytes_requested_max": RANGE_END + 1,
            "bytes_received": len(data),
            "first_line": summarize(first),
            "second_line": summarize(second),
            "prefix_ended_with_newline": data.endswith((b"\n", b"\r")),
        })

    result = {
        "schema": "gri-conglomerate-c1-large-source-header-inspection-v1",
        "date": "2026-09-18",
        "status": "LARGE_HEADER_INSPECTION_COMPLETE",
        "biological_outcome_opened": False,
        "model_fit": False,
        "sources": rows,
    }
    out = repo_root() / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
