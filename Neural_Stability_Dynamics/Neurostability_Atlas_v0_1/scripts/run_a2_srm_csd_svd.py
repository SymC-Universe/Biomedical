from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mne
import numpy as np

from src.csd_svd import compare_surfaces, csd_svd_surface

FREEZE = ROOT / "registries" / "A2_SRM_CSD_SVD_PILOT_FREEZE.json"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_channels(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    names = [r["name"] for r in rows]
    bad = [r["name"] for r in rows if str(r.get("status", "")).strip().lower() == "bad"]
    return names, bad, rows


def _load_session(input_root: Path, manifest_index: dict, cfg: dict, subject: str, session: str):
    rec = manifest_index[(subject, session)]
    if not rec.get("verified"):
        raise RuntimeError(f"unverified input for {subject} {session}")
    set_path = input_root / rec["set_path"]
    if _sha256(set_path) != rec["actual_sha256"]:
        raise RuntimeError(f"post-fetch SHA-256 drift for {set_path}")

    base = set_path.name.replace("_eeg.set", "")
    channels_path = set_path.parent / f"{base}_channels.tsv"
    eeg_json_path = set_path.parent / f"{base}_eeg.json"
    if not channels_path.exists() or not eeg_json_path.exists():
        raise RuntimeError(f"missing pinned sidecars for {subject} {session}")

    sidecar = json.loads(eeg_json_path.read_text(encoding="utf-8"))
    source_names, bad_names, channel_rows = _read_channels(channels_path)
    expected = cfg["input_layer"]
    if float(sidecar.get("SamplingFrequency")) != float(expected["declared_sampling_frequency_hz"]):
        raise RuntimeError(f"sampling frequency drift for {subject} {session}")
    if float(sidecar.get("EpochLength")) != float(expected["declared_epoch_length_s"]):
        raise RuntimeError(f"epoch length drift for {subject} {session}")
    if int(sidecar.get("EEGChannelCount")) != int(expected["declared_channels"]):
        raise RuntimeError(f"channel-count sidecar drift for {subject} {session}")

    epochs = mne.read_epochs_eeglab(str(set_path), verbose="ERROR")
    data = epochs.get_data(copy=True)
    sfreq = float(epochs.info["sfreq"])
    ch_names = list(epochs.ch_names)
    if sfreq != float(expected["declared_sampling_frequency_hz"]):
        raise RuntimeError(f"MNE sampling frequency mismatch for {subject} {session}: {sfreq}")
    if ch_names != source_names:
        raise RuntimeError(f"MNE/source channel order mismatch for {subject} {session}")
    if data.shape[1] != int(expected["declared_channels"]):
        raise RuntimeError(f"loaded channel count mismatch for {subject} {session}")
    expected_samples = int(round(sfreq * float(expected["declared_epoch_length_s"])))
    if data.shape[2] != expected_samples:
        raise RuntimeError(
            f"epoch sample-count mismatch for {subject} {session}: "
            f"expected {expected_samples}, observed {data.shape[2]}"
        )
    if data.shape[0] < 4:
        raise RuntimeError(f"fewer than four cleaned epochs for stable split-half mapping: {subject} {session}")
    if not np.all(np.isfinite(data)):
        raise RuntimeError(f"non-finite EEG data for {subject} {session}")

    fcfg = cfg["frequency_grid"]
    full = csd_svd_surface(data, sfreq, fcfg["min_hz"], fcfg["max_hz"])
    split_even = csd_svd_surface(data[0::2], sfreq, fcfg["min_hz"], fcfg["max_hz"])
    split_odd = csd_svd_surface(data[1::2], sfreq, fcfg["min_hz"], fcfg["max_hz"])
    split_cmp = compare_surfaces(split_even, split_odd)

    freqs = full["frequency_hz"]
    if not np.isclose(freqs[0], fcfg["min_hz"], atol=1e-12):
        raise RuntimeError("frozen minimum frequency not represented")
    if not np.isclose(freqs[-1], fcfg["max_hz"], atol=1e-12):
        raise RuntimeError("frozen maximum frequency not represented")
    if len(freqs) > 1 and not np.allclose(np.diff(freqs), fcfg["spacing_hz"], rtol=0, atol=1e-12):
        raise RuntimeError("frozen frequency spacing not represented exactly")

    summary = {
        "subject": subject,
        "session": session,
        "input_set_sha256": rec["actual_sha256"],
        "input_set_md5_source_annex": rec["actual_md5"],
        "input_set_bytes": rec["actual_bytes"],
        "n_epochs": int(data.shape[0]),
        "n_channels": int(data.shape[1]),
        "n_times_per_epoch": int(data.shape[2]),
        "sampling_frequency_hz": sfreq,
        "mne_version": mne.__version__,
        "loaded_data_unit_note": "MNE EEGLAB reader returns EEG in SI volts; source channels.tsv declares uV",
        "source_bad_interpolated_channel_count": len(bad_names),
        "source_bad_interpolated_channels": bad_names,
        "source_channel_order": ch_names,
        "source_software_filters": sidecar.get("SoftwareFilters"),
        "source_reference": sidecar.get("EEGReference"),
        "frequency_bin_count": int(len(freqs)),
        "max_csd_hermitian_relative_error": float(np.max(full["hermitian_relative_error"])),
        "minimum_csd_eigenvalue": float(np.min(full["minimum_eigenvalue"])),
        "split_half": {
            "split_A_zero_based_even_epoch_count": int(len(data[0::2])),
            "split_B_zero_based_odd_epoch_count": int(len(data[1::2])),
            "median_leading_carrier_MAC": split_cmp["median_leading_carrier_MAC"],
            "median_two_dimensional_subspace_similarity": split_cmp["median_two_dimensional_subspace_similarity"],
            "median_participation_total_variation": split_cmp["median_participation_total_variation"],
            "leading_share_curve_correlation": split_cmp["leading_share_curve_correlation"],
            "log_total_cross_spectral_power_curve_correlation": split_cmp["log_total_cross_spectral_power_curve_correlation"],
        },
    }
    return full, split_cmp, summary


def _store_surface(arrays: dict, key: str, surface: dict):
    for name in [
        "frequency_hz",
        "singular_values_first4",
        "singular_shares_first4",
        "u1",
        "u2",
        "participation_u1",
        "trace_power",
        "hermitian_relative_error",
        "minimum_eigenvalue",
    ]:
        arrays[f"{key}__{name}"] = np.asarray(surface[name])


def _store_comparison(arrays: dict, key: str, comp: dict):
    for name in [
        "leading_carrier_MAC_per_frequency",
        "two_dimensional_subspace_similarity_per_frequency",
        "participation_total_variation_per_frequency",
    ]:
        arrays[f"{key}__{name}"] = np.asarray(comp[name])


def build(input_root: Path, manifest_path: Path, arrays_path: Path):
    cfg = json.loads(FREEZE.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "ALL_FROZEN_INPUTS_RETRIEVED_AND_BYTE_VERIFIED":
        raise RuntimeError("input manifest is not byte-verified")
    manifest_index = {(r["subject"], r["session"]): r for r in manifest["records"]}

    arrays = {}
    surfaces = {}
    session_summaries = []
    for subject in cfg["pilot_subjects"]:
        for session in cfg["sessions"]:
            surface, split_cmp, summary = _load_session(
                input_root, manifest_index, cfg, subject, session
            )
            key = f"{subject.replace('-', '_')}__{session.replace('-', '_')}"
            surfaces[(subject, session)] = surface
            _store_surface(arrays, key, surface)
            _store_comparison(arrays, f"{key}__split_half", split_cmp)
            summary["array_key_prefix"] = key
            session_summaries.append(summary)

    pair_summaries = []
    for subject in cfg["pilot_subjects"]:
        a = surfaces[(subject, "ses-t1")]
        b = surfaces[(subject, "ses-t2")]
        t1 = next(x for x in session_summaries if x["subject"] == subject and x["session"] == "ses-t1")
        t2 = next(x for x in session_summaries if x["subject"] == subject and x["session"] == "ses-t2")
        if t1["source_channel_order"] != t2["source_channel_order"]:
            raise RuntimeError(f"paired channel basis differs for {subject}")
        cmp = compare_surfaces(a, b)
        key = f"{subject.replace('-', '_')}__t1_vs_t2"
        _store_comparison(arrays, key, cmp)
        pair_summaries.append({
            "subject": subject,
            "array_key_prefix": key,
            "median_leading_carrier_MAC": cmp["median_leading_carrier_MAC"],
            "median_two_dimensional_subspace_similarity": cmp["median_two_dimensional_subspace_similarity"],
            "median_participation_total_variation": cmp["median_participation_total_variation"],
            "leading_share_curve_correlation": cmp["leading_share_curve_correlation"],
            "log_total_cross_spectral_power_curve_correlation": cmp["log_total_cross_spectral_power_curve_correlation"],
            "bad_interpolated_channels_t1": t1["source_bad_interpolated_channel_count"],
            "bad_interpolated_channels_t2": t2["source_bad_interpolated_channel_count"],
        })

    arrays_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(arrays_path, **arrays)

    return {
        "schema": "neurostability-atlas-a2-srm-csd-svd-result-v0.1",
        "status": "P0_D_ATLAS_COORDINATE_RECONSTRUCTION_NOT_ENGINE_VALIDATION",
        "system_model": "NSD System Model v1.0",
        "source_id": cfg["source_id"],
        "source_snapshot": cfg["source_snapshot"],
        "research_role": cfg["research_role"],
        "pilot_subjects": cfg["pilot_subjects"],
        "input_manifest_sha256": _sha256(manifest_path),
        "method_spec": "A2_SRM_CSD_SVD_METHOD.md",
        "reconstruction_method": "CSD_SVD_OBSERVATIONAL",
        "frequency_grid": cfg["frequency_grid"],
        "arrays_file": str(arrays_path.relative_to(ROOT)),
        "arrays_sha256": _sha256(arrays_path),
        "session_summaries": session_summaries,
        "pair_summaries": pair_summaries,
        "chi": {
            "status": "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE",
            "value": None,
        },
        "elapsed_time": {
            "status": "WITHHELD_PENDING_SOURCE_TIMESTAMP_RECONCILIATION",
            "used_in_analysis": False,
        },
        "engine_selector_eligible": False,
        "nonclaims": [
            "CSD singular vectors are observational spectral principal directions here, not asserted physical eigenmodes.",
            "No peak frequency, damping, pole real part, second-order factorization, or chi value is inferred.",
            "No repeatability threshold or participant exclusion is selected from this pilot.",
            "No age, sex, cognitive score, diagnosis, phenotype, or desired ordering enters reconstruction.",
            "Poor repeatability remains Atlas Limit-Map evidence rather than a reason to replace a frozen participant."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", default="input/srm_a2")
    parser.add_argument("--manifest", default="results/a2_srm/input_manifest.json")
    parser.add_argument("--output", default="results/a2_srm/csd_svd_result.json")
    parser.add_argument("--arrays", default="results/a2_srm/csd_svd_arrays.npz")
    args = parser.parse_args()
    result = build(ROOT / args.input_root, ROOT / args.manifest, ROOT / args.arrays)
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    for row in result["pair_summaries"]:
        print(json.dumps(row, sort_keys=True))
    print("A2 SRM CSD-SVD RECONSTRUCTION COMPLETE. No Engine rule or chi value created.")


if __name__ == "__main__":
    main()
