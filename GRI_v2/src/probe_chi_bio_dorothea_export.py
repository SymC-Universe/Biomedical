from __future__ import annotations

"""Acquire and fingerprint the frozen human DoRothEA sensitivity network.

This is provenance-only B3 machinery. It is intentionally prohibited from
opening SCC25/TCGA expression, scoring TF activity, selecting a TF panel,
reducing state dimension, fitting an operator, or computing G1/G2/Chi_bio.

The exact repository commit and Git blob are already frozen by the A3+B3+C3
architecture decision. This probe turns that repository identity into a
byte-stable human-regulon artifact and a canonical tabular export.
"""

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd
import pyreadr


REPOSITORY = "saezlab/dorothea"
COMMIT = "1461fb75e23e110c2281860526d4333920925282"
SOURCE_PATH = "data/dorothea_hs.rda"
SOURCE_URL = (
    "https://raw.githubusercontent.com/saezlab/dorothea/"
    f"{COMMIT}/{SOURCE_PATH}"
)
EXPECTED_GIT_BLOB_SHA1 = "75c9c0b6f9e9cfc6c34f86e2e0bf0b055ce1d9d9"
EXPECTED_BYTES = 894_668
TRANSIENT_HTTP_STATUS = frozenset({429, 500, 502, 503, 504})
DEFAULT_ATTEMPTS = 4
DEFAULT_BACKOFF_SECONDS = (2.0, 5.0, 10.0)
REQUIRED_COLUMNS = ("tf", "confidence", "target", "mor")
CONFIDENCE_LEVELS = ("A", "B", "C", "D", "E")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def _download_exact_source(
    *,
    attempts: int = DEFAULT_ATTEMPTS,
    backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
    timeout_seconds: float = 90.0,
) -> tuple[bytes, list[dict]]:
    history: list[dict] = []
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(SOURCE_URL, headers={"User-Agent": "GRI-Chi-bio-DoRothEA-provenance/0.1"})
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                status = int(getattr(response, "status", response.getcode()))
                payload = response.read()
            history.append(
                {"attempt": attempt, "status_code": status, "bytes_received": len(payload)}
            )
            if status == 200 and payload:
                return payload, history
            last_error = RuntimeError(f"unexpected HTTP {status} or empty DoRothEA payload")
        except HTTPError as exc:
            history.append(
                {
                    "attempt": attempt,
                    "status_code": int(exc.code),
                    "bytes_received": 0,
                    "error": f"HTTPError: {exc}",
                }
            )
            if int(exc.code) not in TRANSIENT_HTTP_STATUS:
                raise
            last_error = exc
        except (URLError, TimeoutError) as exc:
            history.append(
                {
                    "attempt": attempt,
                    "status_code": None,
                    "bytes_received": 0,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            last_error = exc
        if attempt < attempts:
            time.sleep(backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)])
    raise RuntimeError(f"frozen DoRothEA source unavailable after {attempts} attempts: {last_error}")


def _read_rda(payload: bytes) -> pd.DataFrame:
    if len(payload) != EXPECTED_BYTES:
        raise RuntimeError(f"DoRothEA byte length mismatch: {len(payload)} != {EXPECTED_BYTES}")
    observed_git_sha = _git_blob_sha1(payload)
    if observed_git_sha != EXPECTED_GIT_BLOB_SHA1:
        raise RuntimeError(
            f"DoRothEA Git blob mismatch: {observed_git_sha} != {EXPECTED_GIT_BLOB_SHA1}"
        )

    with tempfile.NamedTemporaryFile(suffix=".rda") as tmp:
        tmp.write(payload)
        tmp.flush()
        objects = pyreadr.read_r(tmp.name)

    if "dorothea_hs" in objects:
        frame = objects["dorothea_hs"]
    elif len(objects) == 1:
        frame = next(iter(objects.values()))
    else:
        raise RuntimeError(f"unexpected objects in dorothea_hs.rda: {sorted(map(str, objects))}")
    if frame is None or frame.empty:
        raise RuntimeError("dorothea_hs.rda produced an empty human regulon")
    return pd.DataFrame(frame)


def _canonicalize(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise RuntimeError(f"DoRothEA human regulon missing columns: {missing}")
    out = frame.loc[:, list(REQUIRED_COLUMNS)].copy()
    for column in ("tf", "confidence", "target"):
        out[column] = out[column].astype(str).str.strip()
        if out[column].eq("").any() or out[column].eq("nan").any():
            raise RuntimeError(f"DoRothEA {column} contains missing/blank identifiers")
    out["confidence"] = out["confidence"].str.upper()
    unexpected = sorted(set(out["confidence"]) - set(CONFIDENCE_LEVELS))
    if unexpected:
        raise RuntimeError(f"unexpected DoRothEA confidence levels: {unexpected}")
    out["mor"] = pd.to_numeric(out["mor"], errors="raise")
    if not out["mor"].map(pd.notna).all():
        raise RuntimeError("DoRothEA mor contains nonfinite/missing values")
    return out.sort_values(["tf", "target", "confidence", "mor"], kind="mergesort").reset_index(drop=True)


def run_probe(output_dir: Path) -> dict:
    payload, attempt_history = _download_exact_source()
    frame = _canonicalize(_read_rda(payload))

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "dorothea_hs.rda"
    raw_path.write_bytes(payload)
    canonical_path = output_dir / "dorothea_hs_canonical.tsv"
    frame.to_csv(canonical_path, sep="\t", index=False, lineterminator="\n")

    mor = pd.to_numeric(frame["mor"], errors="raise")
    pair_groups = frame.groupby(["tf", "target"], dropna=False)
    sign_counts = pair_groups["mor"].apply(
        lambda s: len({-1 if float(x) < 0 else (1 if float(x) > 0 else 0) for x in s})
    )
    confidence_counts = {
        level: int((frame["confidence"] == level).sum()) for level in CONFIDENCE_LEVELS
    }

    result = {
        "status": "PASS_DOROTHEA_EXPORT_PROVENANCE_ONLY",
        "repository": REPOSITORY,
        "repository_commit": COMMIT,
        "source_path": SOURCE_PATH,
        "source_url": SOURCE_URL,
        "expected_git_blob_sha1": EXPECTED_GIT_BLOB_SHA1,
        "observed_git_blob_sha1": _git_blob_sha1(payload),
        "raw_source_file": str(raw_path),
        "raw_source_bytes": len(payload),
        "raw_source_sha256": _sha256_bytes(payload),
        "download_attempt_history": attempt_history,
        "canonical_file": str(canonical_path),
        "canonical_sha256": _sha256(canonical_path),
        "rows": int(frame.shape[0]),
        "columns": list(frame.columns),
        "unique_tf": int(frame["tf"].nunique(dropna=True)),
        "unique_targets": int(frame["target"].nunique(dropna=True)),
        "confidence_edge_counts": confidence_counts,
        "positive_edges": int((mor > 0).sum()),
        "negative_edges": int((mor < 0).sum()),
        "zero_mor_edges": int((mor == 0).sum()),
        "mor_min": float(mor.min()),
        "mor_max": float(mor.max()),
        "exact_duplicate_rows": int(frame.duplicated().sum()),
        "rows_in_duplicated_tf_target_pairs": int(
            frame.duplicated(subset=["tf", "target"], keep=False).sum()
        ),
        "tf_target_pairs_with_multiple_signs": int((sign_counts > 1).sum()),
        "abc_rows": int(frame["confidence"].isin(["A", "B", "C"]).sum()),
        "abc_unique_tf": int(frame.loc[frame["confidence"].isin(["A", "B", "C"]), "tf"].nunique()),
        "abc_unique_targets": int(
            frame.loc[frame["confidence"].isin(["A", "B", "C"]), "target"].nunique()
        ),
        "real_expression_files_opened": False,
        "tf_activity_scored": False,
        "tf_panel_selected": False,
        "state_dimension_selected": False,
        "operator_fit": False,
        "g1_computed": False,
        "g2_computed": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "note": "Exact architecture-frozen DoRothEA human RData bytes are Git-blob verified, then exported canonically for source/representation-sensitivity qualification only.",
    }
    report = output_dir / "dorothea_hs_export_provenance.json"
    report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="development_outputs/chi_bio_regulon_source/dorothea_20260913",
    )
    args = parser.parse_args()
    result = run_probe(Path(args.output_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
