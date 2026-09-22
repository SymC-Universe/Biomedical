from __future__ import annotations

"""Fetch and freeze GEO MINiML metadata for already-qualified external GRI sources.

Source/provenance only:
- no expression/methylation values are analyzed;
- no GRI feature is computed;
- no cohort is selected as P1;
- no biological outcome is opened.

The output is intended to close sample-identity and source-hash gaps before any
future scientific task is frozen.
"""

import argparse
import hashlib
import json
import tarfile
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SERIES = {
    # Breast primary/metastasis source family
    "GSE58999": {"family": "breast", "modality": "methylation_450k"},
    "GSE57968": {"family": "breast", "modality": "expression_array"},
    # Melanoma MAPKi source family
    "GSE65183": {"family": "melanoma_mapki", "modality": "methylation_450k"},
    "GSE65184": {"family": "melanoma_mapki", "modality": "expression_array"},
    "GSE65185": {"family": "melanoma_mapki", "modality": "rna_seq"},
    # Prostate cross-modality source family
    "GSE262522": {"family": "prostate", "modality": "methylation_450k"},
    "GSE262524": {"family": "prostate", "modality": "methylation_epic"},
    "GSE237995": {"family": "prostate", "modality": "rna_seq"},
}

USER_AGENT = "SymC-GRI-GEO-source-freeze/1.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def geo_bucket(accession: str) -> str:
    if not accession.startswith("GSE") or not accession[3:].isdigit():
        raise ValueError(f"invalid GSE accession: {accession}")
    digits = accession[3:]
    if len(digits) <= 3:
        return "GSEnnn"
    return "GSE" + digits[:-3] + "nnn"


def miniml_url(accession: str) -> str:
    bucket = geo_bucket(accession)
    return (
        f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{accession}/"
        f"miniml/{accession}_family.xml.tgz"
    )


def fetch(url: str, timeout_s: int = 180) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        data = resp.read()
        status = int(getattr(resp, "status", resp.getcode()))
    if status != 200:
        raise RuntimeError(f"{url}: HTTP {status}")
    if not data:
        raise RuntimeError(f"{url}: empty response")
    return data


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first_text(node: ET.Element, child_name: str) -> str | None:
    for child in node:
        if local_name(child.tag) == child_name:
            text = "".join(child.itertext()).strip()
            return text or None
    return None


def texts(node: ET.Element, child_name: str) -> list[str]:
    out: list[str] = []
    for child in node.iter():
        if local_name(child.tag) == child_name:
            text = "".join(child.itertext()).strip()
            if text:
                out.append(text)
    return out


def characteristic_records(node: ET.Element) -> list[dict[str, str | None]]:
    out: list[dict[str, str | None]] = []
    for child in node.iter():
        if local_name(child.tag) != "Characteristics":
            continue
        text = "".join(child.itertext()).strip()
        out.append({
            "tag": child.attrib.get("tag"),
            "value": text or None,
        })
    return out


def relation_records(node: ET.Element) -> list[dict[str, str | None]]:
    out: list[dict[str, str | None]] = []
    for child in node.iter():
        if local_name(child.tag) != "Relation":
            continue
        text = "".join(child.itertext()).strip()
        out.append({
            "type": child.attrib.get("type"),
            "target": text or None,
        })
    return out


def sample_platform_refs(node: ET.Element) -> list[str]:
    refs: list[str] = []
    for child in node.iter():
        if local_name(child.tag) in {"Platform-Ref", "PlatformRef"}:
            ref = child.attrib.get("ref") or child.attrib.get("iid")
            if ref:
                refs.append(ref)
    return sorted(set(refs))


def parse_miniml(xml_path: Path, accession: str) -> dict[str, Any]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    samples: list[dict[str, Any]] = []
    series_nodes: list[ET.Element] = []
    for node in root.iter():
        name = local_name(node.tag)
        if name == "Sample":
            sample_acc = first_text(node, "Accession")
            if not sample_acc:
                continue
            samples.append({
                "gsm": sample_acc,
                "title": first_text(node, "Title"),
                "source": first_text(node, "Source"),
                "type": first_text(node, "Type"),
                "channel_count": first_text(node, "Channel-Count"),
                "characteristics": characteristic_records(node),
                "relations": relation_records(node),
                "platform_refs": sample_platform_refs(node),
                "supplementary_data": texts(node, "Supplementary-Data"),
            })
        elif name == "Series":
            series_nodes.append(node)

    series_meta: dict[str, Any] = {}
    for node in series_nodes:
        acc = first_text(node, "Accession")
        if acc == accession or not series_meta:
            series_meta = {
                "accession": acc,
                "title": first_text(node, "Title"),
                "summary": first_text(node, "Summary"),
                "overall_design": first_text(node, "Overall-Design"),
                "sample_refs": sorted(set(texts(node, "Sample-Ref"))),
                "relations": relation_records(node),
                "supplementary_data": texts(node, "Supplementary-Data"),
            }
            if acc == accession:
                break

    return {
        "series": series_meta,
        "sample_count": len(samples),
        "samples": sorted(samples, key=lambda x: x["gsm"]),
    }


def extract_xml(archive: bytes, accession: str, directory: Path) -> Path:
    archive_path = directory / f"{accession}_family.xml.tgz"
    archive_path.write_bytes(archive)
    with tarfile.open(archive_path, mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile() and m.name.lower().endswith(".xml")]
        if len(members) != 1:
            raise RuntimeError(
                f"{accession}: expected exactly one XML in MINiML archive, found {len(members)}"
            )
        member = members[0]
        tf.extract(member, path=directory, filter="data")
        return directory / member.name


def run(outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    records: dict[str, Any] = {}

    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        for accession, spec in SERIES.items():
            url = miniml_url(accession)
            archive = fetch(url)
            xml_path = extract_xml(archive, accession, temp)
            parsed = parse_miniml(xml_path, accession)
            record = {
                "schema": "GRI_GEO_MINIML_SOURCE_MANIFEST_V01",
                "accession": accession,
                "family": spec["family"],
                "modality": spec["modality"],
                "source_url": url,
                "miniml_archive_sha256": sha256_bytes(archive),
                "miniml_archive_bytes": len(archive),
                "miniml_xml_sha256": hashlib.sha256(xml_path.read_bytes()).hexdigest(),
                "scientific_outcomes_opened": False,
                "gri_features_computed": False,
                "p1_selected": False,
                **parsed,
            }
            target = outdir / f"{accession}_miniml_manifest.json"
            target.write_text(
                json.dumps(record, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            records[accession] = {
                "family": spec["family"],
                "modality": spec["modality"],
                "sample_count": record["sample_count"],
                "miniml_archive_sha256": record["miniml_archive_sha256"],
                "miniml_xml_sha256": record["miniml_xml_sha256"],
                "manifest_file": target.name,
            }

    summary = {
        "schema": "GRI_EXTERNAL_GEO_SOURCE_MANIFEST_SET_V01",
        "status": "COMPLETE_SOURCE_METADATA_ONLY",
        "records": records,
        "scientific_outcomes_opened": False,
        "gri_features_computed": False,
        "p1_selected": False,
        "next_gate": (
            "derive family-specific mechanical identity/crosswalk tables from the frozen "
            "sample metadata before any biological GRI computation"
        ),
    }
    (outdir / "external_geo_source_manifest_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=Path,
        default=ROOT / "external_source_outputs" / "geo_miniml_20260922",
    )
    args = parser.parse_args()
    print(json.dumps(run(args.outdir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
