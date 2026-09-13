from __future__ import annotations

"""Acquire and canonically fingerprint the frozen CollecTRI human source.

This is provenance-only P0-D machinery. It is deliberately prohibited from
loading SCC25/TCGA expression, estimating TF activity, choosing a regulon panel,
fitting an operator, or computing G1/G2/Chi_bio.

The source URL and human-format transformation below reproduce the relevant
`decoupler==2.2.0` CollecTRI wrapper semantics at tag commit
7e8e957cbbb2230079cdd3c13a0ac114a67b9655. The direct source is used so a
transient Zenodo gateway timeout does not force repeated installation/provider
round trips or silently change source identity.
"""

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import time

import pandas as pd
import requests


SOURCE_URL = "https://zenodo.org/records/8192729/files/CollecTRI_regulons.csv?download=1"
DECOUPLER_VERSION_SEMANTICS = "2.2.0"
DECOUPLER_TAG_COMMIT = "7e8e957cbbb2230079cdd3c13a0ac114a67b9655"
DECOUPLER_COLLECTRI_SOURCE_BLOB = "48bfd3388c34e58312e60c772190218658289b78"
TRANSIENT_HTTP_STATUS = frozenset({429, 500, 502, 503, 504})
DEFAULT_ATTEMPTS = 4
DEFAULT_BACKOFF_SECONDS = (2.0, 5.0, 10.0)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _download_exact_source(
    *,
    url: str = SOURCE_URL,
    attempts: int = DEFAULT_ATTEMPTS,
    backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
    timeout_seconds: float = 90.0,
) -> tuple[bytes, list[dict]]:
    if attempts <= 0:
        raise ValueError("attempts must be positive")
    if not backoff_seconds and attempts > 1:
        raise ValueError("backoff_seconds must be nonempty when multiple attempts are allowed")
    history: list[dict] = []
    last_error: Exception | None = None
    session = requests.Session()
    session.headers.update({"User-Agent": "GRI-Chi-bio-provenance-probe/0.2"})

    for attempt in range(1, attempts + 1):
        try:
            response = session.get(url, timeout=timeout_seconds)
            history.append(
                {
                    "attempt": attempt,
                    "status_code": int(response.status_code),
                    "bytes_received": int(len(response.content)),
                }
            )
            if response.status_code == 200:
                if not response.content:
                    raise RuntimeError("Zenodo returned HTTP 200 with an empty CollecTRI payload")
                return response.content, history
            if response.status_code not in TRANSIENT_HTTP_STATUS:
                response.raise_for_status()
            last_error = requests.HTTPError(
                f"transient HTTP {response.status_code} from frozen CollecTRI source"
            )
        except requests.RequestException as exc:
            last_error = exc
            if not history or history[-1].get("attempt") != attempt:
                history.append(
                    {
                        "attempt": attempt,
                        "status_code": None,
                        "bytes_received": 0,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        if attempt < attempts:
            delay = backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)]
            time.sleep(float(delay))

    raise RuntimeError(
        f"frozen CollecTRI source unavailable after {attempts} bounded attempts: {last_error}"
    )


def _apply_decoupler_220_human_semantics(raw: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the human branch of decoupler 2.2.0 `op.collectri`.

    No organism translation is required because the frozen source is the human
    export. Complexes remain included, matching remove_complexes=False.
    """

    required = {"source", "target", "weight", "resources", "references"}
    missing = required - set(raw.columns)
    if missing:
        raise RuntimeError(f"raw CollecTRI source missing required columns: {sorted(missing)}")

    out = raw.copy()
    resources: list[object] = []
    for value in out["resources"]:
        if pd.isna(value):
            resources.append(value)
            continue
        text = str(value)
        parts = text.replace("CollecTRI", "").split(";")
        resources.append(
            ";".join(sorted([part.replace("_", "") for part in parts if part != ""]))
        )
    out["resources"] = resources
    out["references"] = out["references"].str.replace("CollecTRI:", "", regex=False)
    out = out.dropna()
    out["weight"] = pd.to_numeric(out["weight"], errors="raise")
    out = out.drop_duplicates(["source", "target"]).reset_index(drop=True)
    return out


def _canonicalize(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"source", "target", "weight"}
    missing = required - set(frame.columns)
    if missing:
        raise RuntimeError(f"CollecTRI export missing required columns: {sorted(missing)}")
    out = frame.copy()
    sort_cols = ["source", "target", "weight"] + [
        c for c in out.columns if c not in {"source", "target", "weight"}
    ]
    return out.sort_values(sort_cols, kind="mergesort", na_position="last").reset_index(drop=True)


def run_probe(output_dir: Path) -> dict:
    payload, attempt_history = _download_exact_source()
    raw_frame = pd.read_csv(BytesIO(payload))
    frame = _apply_decoupler_220_human_semantics(raw_frame)
    if frame.empty:
        raise RuntimeError("frozen CollecTRI human source produced an empty processed export")
    canonical = _canonicalize(frame)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "CollecTRI_regulons_source.csv"
    raw_path.write_bytes(payload)
    tsv = output_dir / "collectri_human_canonical.tsv"
    canonical.to_csv(tsv, sep="\t", index=False, lineterminator="\n")

    weights = pd.to_numeric(canonical["weight"], errors="coerce")
    if weights.isna().any():
        raise RuntimeError("CollecTRI weight column contains nonnumeric values")

    duplicated_exact = int(canonical.duplicated().sum())
    duplicated_pair = int(canonical.duplicated(subset=["source", "target"], keep=False).sum())
    pair_sign_counts = (
        canonical.assign(_sign=weights.map(lambda x: -1 if x < 0 else (1 if x > 0 else 0)))
        .groupby(["source", "target"], dropna=False)["_sign"]
        .nunique()
    )
    contradictory_signed_pairs = int((pair_sign_counts > 1).sum())

    result = {
        "status": "PASS_COLLECTRI_EXPORT_PROVENANCE_ONLY",
        "source_url": SOURCE_URL,
        "source_record": "Zenodo 8192729 / CollecTRI_regulons.csv",
        "raw_source_file": str(raw_path),
        "raw_source_sha256": _sha256_bytes(payload),
        "raw_source_bytes": int(len(payload)),
        "download_attempt_history": attempt_history,
        "transformation_semantics": "decoupler 2.2.0 human collectri, remove_complexes=False",
        "decoupler_version_semantics": DECOUPLER_VERSION_SEMANTICS,
        "decoupler_tag_commit": DECOUPLER_TAG_COMMIT,
        "decoupler_collectri_source_blob": DECOUPLER_COLLECTRI_SOURCE_BLOB,
        "output_file": str(tsv),
        "canonical_sha256": _sha256(tsv),
        "rows": int(canonical.shape[0]),
        "columns": list(canonical.columns),
        "unique_sources_tf": int(canonical["source"].nunique(dropna=True)),
        "unique_targets": int(canonical["target"].nunique(dropna=True)),
        "positive_edges": int((weights > 0).sum()),
        "negative_edges": int((weights < 0).sum()),
        "zero_weight_edges": int((weights == 0).sum()),
        "exact_duplicate_rows_after_provider_semantics": duplicated_exact,
        "rows_in_duplicated_source_target_pairs_after_provider_semantics": duplicated_pair,
        "source_target_pairs_with_multiple_signs_after_provider_semantics": contradictory_signed_pairs,
        "real_expression_files_opened": False,
        "tf_activity_scored": False,
        "state_dimension_selected": False,
        "regulon_panel_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "note": "Exact raw Zenodo bytes and canonical transformed bytes are both hashed. This probe reproduces the pinned decoupler 2.2.0 human transformation but does not select the source for G1 or score any expression data.",
    }
    report = output_dir / "collectri_human_export_provenance.json"
    report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="development_outputs/chi_bio_regulon_source/collectri_20260913",
    )
    args = parser.parse_args()
    result = run_probe(Path(args.output_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
