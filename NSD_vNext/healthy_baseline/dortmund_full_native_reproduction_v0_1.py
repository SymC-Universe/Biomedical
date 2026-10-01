from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Iterable

import mne
import numpy as np
import pandas as pd
import requests

DATASET = "ds005385"
SNAPSHOT = "1.0.3"
S3_ROOT = "https://s3.amazonaws.com/openneuro.org/ds005385"
OCCIPITAL = ("O1", "Oz", "O2")
BANDS = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
}
PIPELINE_ID = "DORTMUND_SOURCE_NATIVE_V01"


def sha256_stream_download(url: str, path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with requests.get(url, stream=True, timeout=(30, 300)) as response:
        response.raise_for_status()
        with path.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                fh.write(chunk)
                h.update(chunk)
                size += len(chunk)
    return h.hexdigest(), size


def band_power(freqs: np.ndarray, psd: np.ndarray, lo: float, hi: float) -> float:
    # Half-open bands match the declared 1-4, 4-8, 8-13, 13-30 partition.
    mask = (freqs >= lo) & (freqs < hi)
    if hi == 30.0:
        mask = (freqs >= lo) & (freqs <= hi)
    if mask.sum() == 0:
        return float("nan")
    return float(np.sum(psd[mask]))


def process_recording(path: Path) -> dict:
    raw = mne.io.read_raw_edf(path, preload=True, verbose="ERROR")
    raw.pick(picks="eeg")
    original_sfreq = float(raw.info["sfreq"])
    raw.notch_filter(freqs=[50.0], verbose="ERROR")
    raw.filter(l_freq=1.0, h_freq=45.0, verbose="ERROR")
    raw.set_eeg_reference(ref_channels="average", projection=False, verbose="ERROR")

    epochs = mne.make_fixed_length_epochs(
        raw,
        duration=2.0,
        overlap=0.0,
        preload=True,
        reject_by_annotation=True,
        verbose="ERROR",
    )
    n_epochs_total = len(epochs)
    epochs.drop_bad(reject={"eeg": 150e-6}, verbose=False)
    n_epochs_clean = len(epochs)
    if n_epochs_clean < 5:
        return {
            "qc_status": "REJECT_LT5_CLEAN_EPOCHS",
            "n_epochs_total": n_epochs_total,
            "n_epochs_clean": n_epochs_clean,
            "sfreq_hz": original_sfreq,
            "n_channels": len(raw.ch_names),
        }

    missing = [ch for ch in OCCIPITAL if ch not in raw.ch_names]
    if missing:
        return {
            "qc_status": "REJECT_MISSING_OCCIPITAL_CHANNEL",
            "missing_channels": missing,
            "n_epochs_total": n_epochs_total,
            "n_epochs_clean": n_epochs_clean,
            "sfreq_hz": original_sfreq,
            "n_channels": len(raw.ch_names),
        }

    spectrum = epochs.compute_psd(
        method="welch",
        fmin=1.0,
        fmax=30.0,
        n_fft=1024,
        n_per_seg=1024,
        n_overlap=0,
        verbose="ERROR",
    )
    epoch_psd, freqs = spectrum.get_data(return_freqs=True)
    # epoch x channel x frequency -> channel x frequency
    mean_psd = np.mean(epoch_psd, axis=0)
    ch_index = {ch: i for i, ch in enumerate(raw.ch_names)}
    occ_psd = np.mean(mean_psd[[ch_index[ch] for ch in OCCIPITAL], :], axis=0)
    global_psd = np.mean(mean_psd, axis=0)

    alpha_occ = band_power(freqs, occ_psd, *BANDS["alpha"])
    total_occ = band_power(freqs, occ_psd, 1.0, 30.0)
    theta_global = band_power(freqs, global_psd, *BANDS["theta"])
    alpha_global = band_power(freqs, global_psd, *BANDS["alpha"])

    alpha_mask = (freqs >= 8.0) & (freqs <= 13.0)
    apf = float(freqs[alpha_mask][np.argmax(occ_psd[alpha_mask])])

    return {
        "qc_status": "PASS",
        "n_epochs_total": n_epochs_total,
        "n_epochs_clean": n_epochs_clean,
        "sfreq_hz": original_sfreq,
        "n_channels": len(raw.ch_names),
        "freq_resolution_hz": float(freqs[1] - freqs[0]),
        "occipital_alpha_relative_power": float(alpha_occ / total_occ),
        "global_theta_alpha_ratio": float(theta_global / alpha_global),
        "occipital_alpha_peak_frequency_hz": apf,
    }


def expected_recordings(row: pd.Series) -> Iterable[tuple[str, str, str]]:
    sessions = ["ses-1"]
    if str(row["session2"]).strip().lower() == "yes":
        sessions.append("ses-2")
    for ses in sessions:
        for eye in ("EyesClosed", "EyesOpen"):
            for acq in ("pre", "post"):
                yield ses, eye, acq


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--age-min", type=int, required=True)
    ap.add_argument("--age-max", type=int, required=True)
    ap.add_argument("--participants", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    work = out / "working_edf"
    work.mkdir(exist_ok=True)

    participants = pd.read_csv(args.participants, sep="\t")
    cohort = participants[
        (participants["age"] >= args.age_min) & (participants["age"] <= args.age_max)
    ].copy()
    cohort = cohort.sort_values("participant_id")

    rows: list[dict] = []
    progress_path = out / f"progress_{args.age_min}_{args.age_max}.json"

    for _, prow in cohort.iterrows():
        sid = str(prow["participant_id"])
        for ses, eye, acq in expected_recordings(prow):
            rel = f"{sid}/{ses}/eeg/{sid}_{ses}_task-{eye}_acq-{acq}_eeg.edf"
            url = f"{S3_ROOT}/{rel}"
            local = work / f"{sid}_{ses}_{eye}_{acq}.edf"
            rec = {
                "pipeline_id": PIPELINE_ID,
                "dataset": DATASET,
                "snapshot": SNAPSHOT,
                "participant_id": sid,
                "sex": str(prow["sex"]),
                "age": int(prow["age"]),
                "session": ses,
                "session_role": "baseline" if ses == "ses-1" else "followup",
                "eye_state": "EC" if eye == "EyesClosed" else "EO",
                "timepoint": acq,
                "source_relative_path": rel,
                "source_url": url,
            }
            try:
                digest, nbytes = sha256_stream_download(url, local)
                rec["source_sha256"] = digest
                rec["source_bytes"] = nbytes
                rec.update(process_recording(local))
            except requests.HTTPError as exc:
                rec["qc_status"] = "SOURCE_HTTP_ERROR"
                rec["error"] = repr(exc)
            except Exception as exc:
                rec["qc_status"] = "IMPLEMENTATION_OR_DATA_ERROR"
                rec["error"] = repr(exc)
            finally:
                if local.exists():
                    local.unlink()

            rows.append(rec)
            pd.DataFrame(rows).to_csv(
                out / f"dortmund_native_{args.age_min}_{args.age_max}.csv", index=False
            )
            progress_path.write_text(
                json.dumps(
                    {
                        "age_min": args.age_min,
                        "age_max": args.age_max,
                        "subjects_total": int(len(cohort)),
                        "last_participant": sid,
                        "recordings_attempted": len(rows),
                        "recordings_pass": sum(r.get("qc_status") == "PASS" for r in rows),
                        "recordings_rejected_lt5": sum(
                            r.get("qc_status") == "REJECT_LT5_CLEAN_EPOCHS" for r in rows
                        ),
                        "recordings_other_failure": sum(
                            r.get("qc_status")
                            not in {"PASS", "REJECT_LT5_CLEAN_EPOCHS"}
                            for r in rows
                        ),
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    summary = {
        "pipeline_id": PIPELINE_ID,
        "task_id": f"DORTMUND_NATIVE_{args.age_min}_{args.age_max}",
        "classification": "INDEPENDENT_HEALTHY_NATIVE_REPRODUCTION_CHUNK",
        "dataset": DATASET,
        "snapshot": SNAPSHOT,
        "age_min": args.age_min,
        "age_max": args.age_max,
        "subject_count": int(len(cohort)),
        "recordings_attempted": len(rows),
        "recordings_pass": sum(r.get("qc_status") == "PASS" for r in rows),
        "recordings_rejected_lt5": sum(
            r.get("qc_status") == "REJECT_LT5_CLEAN_EPOCHS" for r in rows
        ),
        "recordings_other_failure": sum(
            r.get("qc_status") not in {"PASS", "REJECT_LT5_CLEAN_EPOCHS"} for r in rows
        ),
        "runtime": {
            "python": platform.python_version(),
            "mne": mne.__version__,
            "numpy": np.__version__,
            "pandas": pd.__version__,
        },
        "scientific_ceiling": "native healthy source reproduction only; no NSD quantity and no disorder inference",
    }
    (out / f"summary_{args.age_min}_{args.age_max}.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
