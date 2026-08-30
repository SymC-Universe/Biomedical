#!/usr/bin/env python3
"""Acquire and cryptographically inventory frozen Stage C1A annotation sources.

This script is source/provenance only. It never reads methylation beta values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
import urllib.request
from pathlib import Path


def digest_file(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def download_first(urls: list[str], dest: Path) -> str:
    errors: list[str] = []
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GRI-v2-C1A-source-gate/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r, dest.open("wb") as out:
                while True:
                    chunk = r.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
            if dest.stat().st_size <= 0:
                raise RuntimeError("downloaded file is empty")
            return url
        except Exception as exc:  # source-gate diagnostics
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
            if dest.exists():
                dest.unlink()
    raise RuntimeError("all frozen source URLs failed:\n" + "\n".join(errors))


def read_description_from_tar(path: Path) -> dict[str, str]:
    with tarfile.open(path, "r:gz") as tf:
        candidates = [m for m in tf.getmembers() if m.name.endswith("/DESCRIPTION")]
        if len(candidates) != 1:
            raise RuntimeError(f"expected exactly one DESCRIPTION in tarball, got {len(candidates)}")
        fh = tf.extractfile(candidates[0])
        if fh is None:
            raise RuntimeError("could not extract DESCRIPTION")
        text = fh.read().decode("utf-8", errors="strict")
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    ann_cfg = cfg["primary_annotation_source"]
    ann_path = out / ann_cfg["source_filename"]
    resolved = download_first(list(ann_cfg["candidate_urls"]), ann_path)
    desc = read_description_from_tar(ann_path)
    if desc.get("Package") != ann_cfg["package"]:
        raise SystemExit(f"annotation package mismatch: {desc.get('Package')!r}")
    if desc.get("Version") != ann_cfg["package_version"]:
        raise SystemExit(f"annotation version mismatch: {desc.get('Version')!r}")

    chen_cfg = cfg["technical_mask_robustness"]["cross_reactive_component"]
    chen_url = (
        "https://raw.githubusercontent.com/"
        + chen_cfg["repository"]
        + "/"
        + chen_cfg["commit"]
        + "/"
        + chen_cfg["path"]
    )
    chen_path = out / Path(chen_cfg["path"]).name
    download_first([chen_url], chen_path)
    observed_git_blob = git_blob_sha1(chen_path)
    if observed_git_blob != chen_cfg["github_blob_sha1"]:
        raise SystemExit(
            "cross-reactive source Git blob mismatch: "
            f"expected {chen_cfg['github_blob_sha1']} observed {observed_git_blob}"
        )

    first = chen_path.open("r", encoding="utf-8-sig").readline().strip()
    if not first.startswith("TargetID,"):
        raise SystemExit(f"unexpected Chen source header: {first!r}")

    summary = {
        "status": "STAGE_C1A_FROZEN_SOURCES_ACQUIRED",
        "biological_association_performed": False,
        "methylation_beta_values_read": False,
        "annotation": {
            "resolved_url": resolved,
            "filename": ann_path.name,
            "bytes": ann_path.stat().st_size,
            "md5": digest_file(ann_path, "md5"),
            "sha256": digest_file(ann_path, "sha256"),
            "package": desc.get("Package"),
            "version": desc.get("Version"),
            "bioconductor_release_frozen": ann_cfg["bioconductor_release"],
            "lineage": ann_cfg["lineage"],
        },
        "cross_reactive": {
            "resolved_url": chen_url,
            "filename": chen_path.name,
            "bytes": chen_path.stat().st_size,
            "md5": digest_file(chen_path, "md5"),
            "sha256": digest_file(chen_path, "sha256"),
            "git_blob_sha1": observed_git_blob,
            "reference": chen_cfg["reference"],
        },
    }
    (out / "STAGE_C1A_SOURCE_ACQUISITION.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
