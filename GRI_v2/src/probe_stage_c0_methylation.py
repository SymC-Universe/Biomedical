from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np

TCGA_PATIENT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}", re.I)
TCGA_ROOT_RE = re.compile(r"TCGA[-.][A-Z0-9]{2}[-.][A-Z0-9]{4}[-.][0-9]{2}[A-Z]", re.I)
USER_AGENT = "Cancer-Stability-Atlas/Stage-C0"
CHUNK = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_barcode(value: str) -> str:
    return value.upper().replace(".", "-")


def sample_root(value: str) -> str | None:
    m = TCGA_ROOT_RE.search(value)
    return normalize_barcode(m.group(0)) if m else None


def patient_id(value: str) -> str | None:
    m = TCGA_PATIENT_RE.search(value)
    return normalize_barcode(m.group(0)) if m else None


def is_primary_root(root: str | None) -> bool:
    if not root:
        return False
    parts = root.split("-")
    return len(parts) >= 4 and parts[3][:2] == "01"


def probe_endpoint(url: str) -> dict:
    head_error = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        with urllib.request.urlopen(req, timeout=180) as response:
            headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
            length = headers.get("content-length")
            return {
                "status": "OK_HEAD",
                "http_status": getattr(response, "status", None),
                "content_length": int(length) if length and length.isdigit() else None,
                "content_disposition": headers.get("content-disposition"),
                "content_type": headers.get("content-type"),
                "accept_ranges": headers.get("accept-ranges"),
            }
    except Exception as exc:  # pragma: no cover - network-specific
        head_error = f"{type(exc).__name__}: {exc}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"})
        with urllib.request.urlopen(req, timeout=180) as response:
            headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
            response.read(1)
            content_range = headers.get("content-range")
            total = None
            if content_range and "/" in content_range:
                tail = content_range.rsplit("/", 1)[-1]
                if tail.isdigit():
                    total = int(tail)
            if total is None:
                length = headers.get("content-length")
                if length and length.isdigit() and getattr(response, "status", None) == 200:
                    total = int(length)
            return {
                "status": "OK_RANGE",
                "http_status": getattr(response, "status", None),
                "content_length": total,
                "content_disposition": headers.get("content-disposition"),
                "content_type": headers.get("content-type"),
                "accept_ranges": headers.get("accept-ranges"),
                "content_range": content_range,
                "head_error": head_error,
            }
    except Exception as exc:  # pragma: no cover - network-specific
        return {"status": "ERROR", "error": f"HEAD={head_error}; RANGE={type(exc).__name__}: {exc}"}


def download_resume(url: str, destination: Path, expected_size: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    part = destination.with_suffix(destination.suffix + ".part")
    start = part.stat().st_size if part.exists() else 0
    if start > expected_size:
        raise ValueError(f"Partial file is larger than expected source: {start} > {expected_size}")
    if start == expected_size:
        part.replace(destination)
        return

    headers = {"User-Agent": USER_AGENT}
    if start:
        headers["Range"] = f"bytes={start}-"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=300) as response:
        status = getattr(response, "status", None)
        if start and status != 206:
            start = 0
            mode = "wb"
        else:
            mode = "ab" if start else "wb"
        with part.open(mode) as out:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                out.write(chunk)
    size = part.stat().st_size
    if size != expected_size:
        raise ValueError(f"Downloaded size {size} does not match frozen expected size {expected_size}")
    part.replace(destination)


def inspect_matrix(path: Path, expected_probe_count: int) -> dict:
    probe_counter: Counter[str] = Counter()
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with path.open("rb") as fh:
        header_b = fh.readline()
        sha256.update(header_b)
        md5.update(header_b)
        if not header_b:
            raise ValueError("Methylation matrix is empty")
        header = header_b.decode("utf-8", errors="strict").rstrip("\r\n").split("\t")
        if len(header) < 2:
            raise ValueError("Methylation header has fewer than two columns")
        source_labels = header[1:]
        roots = [sample_root(x) for x in source_labels]
        parsed = sum(r is not None for r in roots)
        if parsed == 0:
            raise ValueError("No TCGA sample roots could be parsed from the methylation header")

        row_count = 0
        blank_probe_ids = 0
        for line in fh:
            sha256.update(line)
            md5.update(line)
            if not line.strip():
                continue
            probe_id = line.split(b"\t", 1)[0].decode("utf-8", errors="strict").strip()
            row_count += 1
            if not probe_id:
                blank_probe_ids += 1
            else:
                probe_counter[probe_id] += 1

    duplicate_probe_ids = sorted([p for p, n in probe_counter.items() if n > 1])
    if row_count != expected_probe_count:
        raise ValueError(f"Probe row count {row_count} does not match frozen expected {expected_probe_count}")
    if blank_probe_ids:
        raise ValueError(f"Found {blank_probe_ids} blank probe identifiers")
    if duplicate_probe_ids:
        raise ValueError(f"Found {len(duplicate_probe_ids)} duplicate probe identifiers")

    primary_roots = [r for r in roots if is_primary_root(r)]
    root_counts = Counter(r for r in primary_roots if r)
    patient_counts = Counter(patient_id(r) for r in primary_roots if r)
    return {
        "header_columns": len(header),
        "methylation_sample_columns": len(source_labels),
        "tcga_sample_roots_parsed": parsed,
        "primary_sample_columns": len(primary_roots),
        "unique_primary_sample_roots": len(root_counts),
        "duplicate_primary_sample_roots": sum(1 for n in root_counts.values() if n > 1),
        "unique_primary_patients": len([p for p in patient_counts if p]),
        "probe_rows": row_count,
        "duplicate_probe_ids": 0,
        "blank_probe_ids": 0,
        "sha256": sha256.hexdigest(),
        "md5": md5.hexdigest(),
        "primary_roots": sorted(root_counts),
        "patient_primary_counts": {str(k): int(v) for k, v in patient_counts.items() if k},
    }


def stage_a_coverage(cache_path: Path, matrix_info: dict) -> dict:
    z = np.load(cache_path, allow_pickle=True)
    sample_ids = z["sample_ids"].astype(str)
    patient_ids = z["patient_ids"].astype(str)
    cancer_types = z["cancer_types"].astype(str)
    if not (len(sample_ids) == len(patient_ids) == len(cancer_types)):
        raise ValueError("Stage A cache identity arrays differ in length")

    source_roots = set(matrix_info["primary_roots"])
    patient_counts = matrix_info["patient_primary_counts"]
    unique_source_patients = {p for p, n in patient_counts.items() if int(n) == 1}
    matched = np.zeros(len(sample_ids), dtype=bool)
    exact = 0
    fallback = 0
    for i, (sid, pid) in enumerate(zip(sample_ids, patient_ids)):
        root = sample_root(sid)
        pid_norm = normalize_barcode(pid)
        if root and root in source_roots:
            matched[i] = True
            exact += 1
        elif pid_norm in unique_source_patients:
            matched[i] = True
            fallback += 1

    cancer_rows = []
    for cancer in sorted(set(cancer_types.tolist())):
        mask = cancer_types == cancer
        cancer_rows.append({
            "cancer_type": str(cancer),
            "stage_a_n": int(mask.sum()),
            "methylation_matched_n": int((mask & matched).sum()),
            "passes_n30": bool((mask & matched).sum() >= 30),
        })
    return {
        "stage_a_samples": int(len(sample_ids)),
        "matched_stage_a_samples": int(matched.sum()),
        "exact_sample_root_matches": int(exact),
        "unique_patient_fallback_matches": int(fallback),
        "cancers": len(cancer_rows),
        "cancers_passing_n30": sum(int(r["passes_n30"]) for r in cancer_rows),
        "cancer_coverage": cancer_rows,
    }


def run(plan_path: Path, cache_path: Path | None, out_dir: Path, source_path: Path | None, download: bool) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    src = plan["primary_source"]
    expected_size = int(src["expected_content_length_bytes"])
    expected_probes = int(src["expected_shared_probe_count"])
    expected_md5 = str(src["expected_md5"]).lower()
    url = f"https://api.gdc.cancer.gov/data/{src['gdc_uuid']}"
    out_dir.mkdir(parents=True, exist_ok=True)

    metadata = probe_endpoint(url)
    if metadata.get("content_length") != expected_size:
        raise ValueError(f"Remote content length {metadata.get('content_length')} != frozen expected {expected_size}")
    disposition = metadata.get("content_disposition")
    if disposition and src["file_name"] not in disposition:
        raise ValueError("Remote content-disposition does not identify the frozen source filename")

    summary = {
        "status": "STAGE_C0_METHYLATION_SOURCE_GATE",
        "plan_version": plan["version"],
        "source_file": src["file_name"],
        "gdc_uuid": src["gdc_uuid"],
        "expected_content_length_bytes": expected_size,
        "expected_shared_probe_count": expected_probes,
        "expected_md5": expected_md5,
        "remote_metadata": metadata,
        "biological_association_performed": False,
        "chi_present": False,
        "cv2_used": False,
        "composite_score_present": False,
        "substrate_inheritance_claim": False,
        "claim_ceiling": "source identity, schema, sample coverage, and probe inventory only",
    }

    local = source_path
    if download:
        local = out_dir / src["file_name"] if local is None else local
        if not local.exists():
            download_resume(url, local, expected_size)
    if local is not None and local.exists():
        if local.stat().st_size != expected_size:
            raise ValueError(f"Local file size {local.stat().st_size} != frozen expected {expected_size}")
        matrix = inspect_matrix(local, expected_probes)
        if matrix["md5"].lower() != expected_md5:
            raise ValueError(f"Source MD5 {matrix['md5']} != frozen GDC manifest MD5 {expected_md5}")
        summary["source_sha256"] = matrix["sha256"]
        summary["source_md5"] = matrix["md5"]
        summary["matrix"] = {k: v for k, v in matrix.items() if k not in {"primary_roots", "patient_primary_counts", "sha256", "md5"}}
        if cache_path is not None:
            cache_sha = sha256_file(cache_path)
            expected_cache_sha = plan["frozen_inputs"]["stage_a_profile_cache_sha256"]
            if cache_sha != expected_cache_sha:
                raise ValueError(f"Stage A cache SHA mismatch: {cache_sha} != {expected_cache_sha}")
            coverage = stage_a_coverage(cache_path, matrix)
            summary["stage_a_profile_cache_sha256"] = cache_sha
            summary["coverage"] = {k: v for k, v in coverage.items() if k != "cancer_coverage"}
            coverage_path = out_dir / "stage_c0_methylation_cancer_coverage.csv"
            lines = ["cancer_type,stage_a_n,methylation_matched_n,passes_n30"]
            lines.extend(f"{r['cancer_type']},{r['stage_a_n']},{r['methylation_matched_n']},{str(r['passes_n30']).lower()}" for r in coverage["cancer_coverage"])
            coverage_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    out = out_dir / "STAGE_C0_METHYLATION_SOURCE_SUMMARY.json"
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--cache", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()
    result = run(args.plan, args.cache, args.out, args.source, args.download)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
