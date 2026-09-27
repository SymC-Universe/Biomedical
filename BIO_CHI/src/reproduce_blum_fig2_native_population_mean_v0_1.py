#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
import pathlib
import statistics
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
CFG = BIO / "config" / "BLUM2019_FIG2_NATIVE_MEAN_REPRODUCTION_FREEZE_v0_1.json"
PIN = BIO / "config" / "BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json"
OUT = BIO / "artifacts" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "blum2019_fig2_native_population_mean_v0_1.json"
UA = "BioChiReviewerReproducibility/0.1"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def finite_float(value: str, label: str) -> float:
    x = float(value)
    if not math.isfinite(x):
        raise SystemExit(f"BLUM_FIG2_NONFINITE_{label} value={value!r}")
    return x


def read_csv_bytes(payload: bytes):
    text = payload.decode("utf-8-sig", errors="strict")
    return list(csv.DictReader(io.StringIO(text)))


def read_csv_gz_bytes(payload: bytes):
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as gz:
        text = gz.read().decode("utf-8-sig", errors="strict")
    return list(csv.DictReader(io.StringIO(text)))


def main() -> None:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pin = json.loads(PIN.read_text(encoding="utf-8"))

    req = urllib.request.Request(
        pin["selected_file"]["download_url"],
        headers={"User-Agent": UA, "Accept": "application/zip,*/*;q=0.5"},
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        archive = response.read()

    observed_sha = sha256(archive)
    if observed_sha != cfg["source_sha256"]:
        raise SystemExit(
            f"BLUM_FIG2_SOURCE_HASH_MISMATCH expected={cfg['source_sha256']} observed={observed_sha}"
        )

    duration_results = {}
    total_rows = 0
    total_cells = 0

    with zipfile.ZipFile(io.BytesIO(archive), "r") as zf:
        names = set(zf.namelist())

        for duration_key, members in cfg["source_members"].items():
            duration = int(duration_key)
            for required in (members["ekar"], members["grouping"]):
                if required not in names:
                    raise SystemExit(f"BLUM_FIG2_MISSING_MEMBER {required}")

            grouping_payload = zf.read(members["grouping"])
            grouping_rows = read_csv_bytes(grouping_payload)
            group_map = {}
            for row in grouping_rows:
                idx = str(row["group.idx"]).strip()
                label = str(row["group"]).strip()
                if idx in group_map and group_map[idx] != label:
                    raise SystemExit(f"BLUM_FIG2_GROUP_COLLISION duration={duration} group.idx={idx}")
                group_map[idx] = label

            ekar_payload = zf.read(members["ekar"])
            ekar_rows = read_csv_gz_bytes(ekar_payload)
            total_rows += len(ekar_rows)

            cells = defaultdict(list)
            seen = set()
            for row in ekar_rows:
                gidx = str(row["group.idx"]).strip()
                if gidx not in group_map:
                    raise SystemExit(f"BLUM_FIG2_UNKNOWN_GROUP duration={duration} group.idx={gidx}")
                fov = str(row["fov"]).strip()
                track_id = str(row["id"]).strip()
                t = finite_float(row["realtime"], "REALTIME")
                y = finite_float(row["intensity_ekar"], "INTENSITY_EKAR")
                key = (gidx, fov, track_id)
                obs_key = key + (t,)
                if obs_key in seen:
                    raise SystemExit(
                        f"BLUM_FIG2_DUPLICATE_OBSERVATION duration={duration} group.idx={gidx} fov={fov} id={track_id} realtime={t}"
                    )
                seen.add(obs_key)
                cells[key].append((t, y))

            normalized_by_group_time = defaultdict(list)
            baseline_support = []
            group_cell_keys = defaultdict(set)

            for key, observations in cells.items():
                gidx, fov, track_id = key
                baseline = [y for t, y in observations if 0.0 <= t <= 40.0]
                if not baseline:
                    raise SystemExit(
                        f"BLUM_FIG2_NO_BASELINE duration={duration} group.idx={gidx} fov={fov} id={track_id}"
                    )
                baseline_mean = statistics.fmean(baseline)
                if (not math.isfinite(baseline_mean)) or baseline_mean == 0.0:
                    raise SystemExit(
                        f"BLUM_FIG2_BAD_BASELINE duration={duration} group.idx={gidx} fov={fov} id={track_id} mean={baseline_mean}"
                    )
                baseline_support.append(len(baseline))
                group_cell_keys[gidx].add(key)
                for t, y in observations:
                    normalized_by_group_time[(gidx, t)].append(y / baseline_mean)

            total_cells += len(cells)
            groups_out = []
            for gidx in sorted(group_map, key=lambda x: (float(x) if x.replace(".", "", 1).isdigit() else math.inf, x)):
                times = sorted(t for (gg, t) in normalized_by_group_time if gg == gidx)
                trajectory = []
                for t in times:
                    vals = normalized_by_group_time[(gidx, t)]
                    trajectory.append(
                        {
                            "realtime_min": t,
                            "population_mean_normalized_ekar": statistics.fmean(vals),
                            "n_cells_observed": len(vals),
                        }
                    )
                groups_out.append(
                    {
                        "group_idx": gidx,
                        "group": group_map[gidx],
                        "unique_cells": len(group_cell_keys[gidx]),
                        "timepoint_count": len(times),
                        "trajectory": trajectory,
                    }
                )

            duration_results[str(duration)] = {
                "pulse_duration_min": duration,
                "ekar_member": members["ekar"],
                "grouping_member": members["grouping"],
                "ekar_member_sha256": sha256(ekar_payload),
                "grouping_member_sha256": sha256(grouping_payload),
                "row_count": len(ekar_rows),
                "unique_cell_count": len(cells),
                "group_count": len(groups_out),
                "baseline_observations_per_cell_min": min(baseline_support),
                "baseline_observations_per_cell_max": max(baseline_support),
                "groups": groups_out,
            }

    result = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "gate": cfg["gate"],
        "archive_sha256": observed_sha,
        "publication_native_normalization": cfg["publication_native_rule"],
        "selection_rule": cfg["prospective_selection_rule"],
        "execution_rules": cfg["execution_rules"],
        "biological_data_rows_read": True,
        "raw_row_level_values_emitted": False,
        "interpolation_used": False,
        "smoothing_used": False,
        "imputation_used": False,
        "symc_metric_computed": False,
        "chi_bio_constructed": False,
        "Chi_bio_admitted": False,
        "Bio_Chi_constructed": False,
        "total_source_rows": total_rows,
        "total_unique_cell_tracks_across_duration_files": total_cells,
        "durations": duration_results,
        "status": "PASS_NATIVE_FIG2_POPULATION_MEAN_REPRODUCTION",
    }
    OUT_FILE.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    compact = {
        "output": str(OUT_FILE.relative_to(ROOT)),
        "status": result["status"],
        "archive_sha256": observed_sha,
        "total_source_rows": total_rows,
        "total_unique_cell_tracks_across_duration_files": total_cells,
        "durations": {
            k: {
                "row_count": v["row_count"],
                "unique_cell_count": v["unique_cell_count"],
                "group_count": v["group_count"],
                "baseline_observations_per_cell_min": v["baseline_observations_per_cell_min"],
                "baseline_observations_per_cell_max": v["baseline_observations_per_cell_max"],
                "groups": [
                    {
                        "group_idx": g["group_idx"],
                        "group": g["group"],
                        "unique_cells": g["unique_cells"],
                        "timepoint_count": g["timepoint_count"],
                    }
                    for g in v["groups"]
                ],
            }
            for k, v in duration_results.items()
        },
        "symc_metric_computed": False,
    }
    print(json.dumps(compact, indent=2))
    print("BIO_CHI_BLUM_FIG2_NATIVE_MEAN_REPRODUCTION_PASS")


if __name__ == "__main__":
    main()
