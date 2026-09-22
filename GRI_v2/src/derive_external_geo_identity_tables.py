from __future__ import annotations

"""Derive mechanical crosswalks from frozen GEO MINiML metadata.

This module never opens molecular values or GRI outcomes. It converts source
metadata into explicit identity tables and refuses ambiguous/conflicting
metadata rather than resolving it silently.
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_manifest(directory: Path, accession: str) -> dict[str, Any]:
    return json.loads(
        (directory / f"{accession}_miniml_manifest.json").read_text(encoding="utf-8")
    )


def characteristics(sample: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in sample.get("characteristics", []):
        tag = (item.get("tag") or "").strip().lower()
        value = (item.get("value") or "").strip()
        if tag:
            if tag in out and out[tag] != value:
                raise ValueError(
                    f"{sample.get('gsm')}: duplicate characteristic tag {tag!r}"
                )
            out[tag] = value
    return out


def canonical_breast_state(value: str) -> str:
    v = value.strip().lower()
    if v == "primary tumor":
        return "PRIMARY"
    if v in {"lymph node metastasis", "regional metastasis"}:
        return "METASTASIS"
    raise ValueError(f"unrecognized breast state: {value!r}")


def breast_crosswalk(directory: Path) -> dict[str, Any]:
    expr = load_manifest(directory, "GSE57968")
    meth = load_manifest(directory, "GSE58999")

    methylation_by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for s in meth["samples"]:
        ch = characteristics(s)
        patient = ch.get("unique patient id")
        state = ch.get("sample type")
        if not patient or not state:
            raise ValueError(f"{s['gsm']}: missing methylation patient/state")
        key = (patient, canonical_breast_state(state))
        methylation_by_key[key].append(s)

    rows: list[dict[str, Any]] = []
    used_meth: set[str] = set()
    for s in expr["samples"]:
        ch = characteristics(s)
        patient = ch.get("patient id")
        state = ch.get("tissue subtype")
        if not patient or not state:
            raise ValueError(f"{s['gsm']}: missing expression patient/state")
        key = (patient, canonical_breast_state(state))
        candidates = methylation_by_key.get(key, [])
        if len(candidates) != 1:
            raise ValueError(
                f"{s['gsm']}: expected one methylation match for {key}, found {len(candidates)}"
            )
        m = candidates[0]
        used_meth.add(m["gsm"])
        rows.append({
            "patient_id": patient,
            "state": key[1],
            "expression_gsm": s["gsm"],
            "expression_title": s.get("title"),
            "methylation_gsm": m["gsm"],
            "methylation_title": m.get("title"),
            "identity_basis": "EXACT_PATIENT_ID_PLUS_SOURCE_STATE_CHARACTERISTICS",
            "grI_outcome_opened": False,
        })

    extra_meth = [s for s in meth["samples"] if s["gsm"] not in used_meth]
    if len(rows) != 72 or len(extra_meth) != 16:
        raise ValueError(
            f"breast source structure changed: matched={len(rows)}, extra_methylation={len(extra_meth)}"
        )

    pair_counts = defaultdict(set)
    for row in rows:
        pair_counts[row["patient_id"]].add(row["state"])
    complete_pairs = sorted(
        patient for patient, states in pair_counts.items()
        if states == {"PRIMARY", "METASTASIS"}
    )
    if len(complete_pairs) != 36:
        raise ValueError(f"expected 36 complete expression patient pairs, got {len(complete_pairs)}")

    return {
        "schema": "GRI_BREAST_EXTERNAL_PRODUCTION_CROSSWALK_V01",
        "status": "PASS",
        "matched_expression_samples": len(rows),
        "matched_expression_patients": len(complete_pairs),
        "methylation_only_samples": len(extra_meth),
        "methylation_only_gsms": sorted(s["gsm"] for s in extra_meth),
        "rows": sorted(rows, key=lambda x: (x["patient_id"], x["state"])),
        "scientific_outcomes_opened": False,
        "p1_selected": False,
    }


def prostate_crosswalk(directory: Path) -> dict[str, Any]:
    rna = load_manifest(directory, "GSE237995")
    m450 = load_manifest(directory, "GSE262522")
    mepic = load_manifest(directory, "GSE262524")

    meth_by_title: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for platform, manifest in (("450K", m450), ("EPIC", mepic)):
        for s in manifest["samples"]:
            meth_by_title[s["title"]].append((platform, s))

    rows: list[dict[str, Any]] = []
    for s in rna["samples"]:
        matches = meth_by_title.get(s["title"], [])
        if len(matches) != 1:
            raise ValueError(
                f"{s['gsm']}: expected one exact-title methylation match, found {len(matches)}"
            )
        platform, m = matches[0]
        rows.append({
            "identity_key": s["title"],
            "rna_gsm": s["gsm"],
            "methylation_gsm": m["gsm"],
            "methylation_platform": platform,
            "identity_basis": "EXACT_GEO_TITLE",
            "gri_outcome_opened": False,
        })

    if len(rows) != 121:
        raise ValueError(f"expected 121 prostate crosswalk rows, got {len(rows)}")
    if sum(r["methylation_platform"] == "450K" for r in rows) != 68:
        raise ValueError("450K partition changed")
    if sum(r["methylation_platform"] == "EPIC" for r in rows) != 53:
        raise ValueError("EPIC partition changed")

    return {
        "schema": "GRI_PROSTATE_EXTERNAL_PRODUCTION_CROSSWALK_V01",
        "status": "PASS",
        "matched_rows": len(rows),
        "platform_counts": {"450K": 68, "EPIC": 53},
        "rows": sorted(rows, key=lambda x: x["identity_key"]),
        "scientific_outcomes_opened": False,
        "p1_selected": False,
    }


_PT_RE = re.compile(
    r"^Pt(?P<patient>\d+)-(?P<state>baseline\d*|DP\d+|DD-DP\d+|DDP\d+)"
    r"(?P<replicate>-\d+|\.replicate)?$",
    re.I,
)
_DESC_PATIENT_RE = re.compile(r"\bPatient\s+(?P<patient>\d+)\b", re.I)
_DESC_BIOPSY_RE = re.compile(r"\b(?P<biopsy>\d+)(?:st|nd|rd|th)\s+biopsy\b", re.I)


def normalize_melanoma_state(raw: str) -> str:
    v = raw.upper()
    if v.startswith("BASELINE"):
        return "BASELINE"
    v = v.replace("DD-DP", "DDP")
    return v


def melanoma_title_record(
    sample: dict[str, Any],
    *,
    modality: str,
) -> dict[str, Any]:
    title = sample.get("title") or ""
    description = sample.get("description") or ""
    ch = characteristics(sample)
    match = _PT_RE.match(title)

    record: dict[str, Any] = {
        "gsm": sample["gsm"],
        "modality": modality,
        "raw_title": title,
        "description": description,
        "mapki_sensitivity": ch.get("mapki sensitivity"),
        "mapki_treatment": ch.get("mapki treatment"),
        "source_class": "HUMAN_PATIENT" if match else "CELL_MODEL",
        "identity_status": "SOURCE_METADATA_RETAINED",
        "gri_outcome_opened": False,
    }

    if not match:
        record.update({
            "patient_id_from_title": None,
            "state_from_title": None,
            "replicate_label": None,
            "patient_id_from_description": None,
            "biopsy_order_from_description": None,
            "identity_anomaly": None,
        })
        return record

    patient_title = int(match.group("patient"))
    state = normalize_melanoma_state(match.group("state"))
    replicate = match.group("replicate")
    desc_patient_match = _DESC_PATIENT_RE.search(description)
    desc_biopsy_match = _DESC_BIOPSY_RE.search(description)
    patient_desc = int(desc_patient_match.group("patient")) if desc_patient_match else None
    biopsy_desc = int(desc_biopsy_match.group("biopsy")) if desc_biopsy_match else None

    anomaly = None
    if patient_desc is not None and patient_desc != patient_title:
        anomaly = "TITLE_DESCRIPTION_PATIENT_CONFLICT"

    record.update({
        "patient_id_from_title": patient_title,
        "state_from_title": state,
        "replicate_label": replicate,
        "patient_id_from_description": patient_desc,
        "biopsy_order_from_description": biopsy_desc,
        "identity_anomaly": anomaly,
    })
    return record


def melanoma_manifest(directory: Path) -> dict[str, Any]:
    manifests = [
        ("methylation_450k", load_manifest(directory, "GSE65183")),
        ("expression_array", load_manifest(directory, "GSE65184")),
        ("rna_seq", load_manifest(directory, "GSE65185")),
    ]
    rows: list[dict[str, Any]] = []
    for modality, manifest in manifests:
        rows.extend(
            melanoma_title_record(s, modality=modality)
            for s in manifest["samples"]
        )

    if len(rows) != 218:
        raise ValueError(f"expected 218 melanoma source samples, got {len(rows)}")

    anomalies = [r for r in rows if r["identity_anomaly"]]
    human = [r for r in rows if r["source_class"] == "HUMAN_PATIENT"]
    cell = [r for r in rows if r["source_class"] == "CELL_MODEL"]

    return {
        "schema": "GRI_MELANOMA_MAPKI_SOURCE_SAMPLE_MANIFEST_V01",
        "status": "SOURCE_MANIFEST_COMPLETE_WITH_ANOMALIES" if anomalies else "PASS",
        "rows_total": len(rows),
        "human_rows": len(human),
        "cell_model_rows": len(cell),
        "identity_anomaly_count": len(anomalies),
        "identity_anomalies": anomalies,
        "rows": sorted(rows, key=lambda x: (x["modality"], x["gsm"])),
        "scientific_outcomes_opened": False,
        "p1_selected": False,
        "anomaly_rule": (
            "title/description conflicts are quarantined and may not be silently "
            "resolved from title alone"
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def run(source_dir: Path, outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)

    breast = breast_crosswalk(source_dir)
    prostate = prostate_crosswalk(source_dir)
    melanoma = melanoma_manifest(source_dir)

    (outdir / "breast_crosswalk.json").write_text(
        json.dumps(breast, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(
        outdir / "breast_crosswalk.csv",
        breast["rows"],
        [
            "patient_id", "state", "expression_gsm", "expression_title",
            "methylation_gsm", "methylation_title", "identity_basis",
            "grI_outcome_opened",
        ],
    )

    (outdir / "prostate_crosswalk.json").write_text(
        json.dumps(prostate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(
        outdir / "prostate_crosswalk.csv",
        prostate["rows"],
        [
            "identity_key", "rna_gsm", "methylation_gsm",
            "methylation_platform", "identity_basis", "gri_outcome_opened",
        ],
    )

    (outdir / "melanoma_source_manifest.json").write_text(
        json.dumps(melanoma, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(
        outdir / "melanoma_source_manifest.csv",
        melanoma["rows"],
        [
            "gsm", "modality", "raw_title", "description",
            "mapki_sensitivity", "mapki_treatment", "source_class",
            "patient_id_from_title", "state_from_title", "replicate_label",
            "patient_id_from_description", "biopsy_order_from_description",
            "identity_anomaly", "identity_status", "gri_outcome_opened",
        ],
    )

    summary = {
        "schema": "GRI_EXTERNAL_IDENTITY_DERIVATION_V01",
        "status": "COMPLETE_SOURCE_IDENTITY_ONLY",
        "breast": {
            "matched_expression_samples": breast["matched_expression_samples"],
            "matched_expression_patients": breast["matched_expression_patients"],
            "methylation_only_samples": breast["methylation_only_samples"],
        },
        "prostate": {
            "matched_rows": prostate["matched_rows"],
            "platform_counts": prostate["platform_counts"],
        },
        "melanoma": {
            "rows_total": melanoma["rows_total"],
            "human_rows": melanoma["human_rows"],
            "cell_model_rows": melanoma["cell_model_rows"],
            "identity_anomaly_count": melanoma["identity_anomaly_count"],
            "status": melanoma["status"],
        },
        "scientific_outcomes_opened": False,
        "gri_features_computed": False,
        "p1_selected": False,
    }
    (outdir / "external_identity_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=ROOT / "external_source_outputs" / "geo_miniml_20260922",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=ROOT / "external_source_outputs" / "identity_20260922",
    )
    args = parser.parse_args()
    print(json.dumps(run(args.source_dir, args.outdir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
