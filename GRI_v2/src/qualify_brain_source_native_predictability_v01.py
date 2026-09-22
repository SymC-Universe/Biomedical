from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
import urllib.request
from pathlib import Path

SOURCE_REPO = "grabuffo/State_Dependent_Brain_Stimulation"
SOURCE_COMMIT = "84afcf934c3798b2a40dc8da22d0840e60a4b0f9"
SOURCE_PATH = "data/predictability_salience_to_salience.csv"
EXPECTED_GIT_BLOB_SHA1 = "58e34f8705e30a08954e1c841f13c2e58529634c"
EXPECTED_SIZE = 83196
URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{SOURCE_PATH}"

REQUIRED_COLUMNS = {
    "sub","run_is","r2_cv","r2_cv_std","r2_train","coefficient",
    "coefficient_std","r2_scores","correlation","n_trials","null_r2"
}

def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()

def finite(vals):
    return [v for v in vals if math.isfinite(v)]

def main():
    with urllib.request.urlopen(URL, timeout=60) as r:
        data = r.read()

    size_ok = len(data) == EXPECTED_SIZE
    blob = git_blob_sha1(data)
    blob_ok = blob == EXPECTED_GIT_BLOB_SHA1
    sha256 = hashlib.sha256(data).hexdigest()

    text = data.decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))
    cols = set(rows[0].keys()) if rows else set()
    schema_ok = REQUIRED_COLUMNS.issubset(cols)

    r2 = finite([float(x["r2_cv"]) for x in rows])
    null = finite([float(x["null_r2"]) for x in rows])
    corr = finite([float(x["correlation"]) for x in rows])
    coef = finite([float(x["coefficient"]) for x in rows])
    ntrials = [int(float(x["n_trials"])) for x in rows]
    subjects = sorted({x["sub"] for x in rows})
    sessions = sorted({(x["sub"], x["run_is"]) for x in rows})

    delta = [a-b for a,b in zip(r2, null)]

    out = {
        "schema":"SYMC_BRAIN_SOURCE_NATIVE_PREDICTABILITY_QUALIFICATION_V01",
        "status":"PASS" if (size_ok and blob_ok and schema_ok and len(rows)>0) else "FAIL",
        "epistemic_class":"EXTERNAL_SOURCE_DERIVED_TABLE_QUALIFICATION",
        "source":{
            "repository":SOURCE_REPO,
            "commit":SOURCE_COMMIT,
            "path":SOURCE_PATH,
            "url":URL,
            "expected_git_blob_sha1":EXPECTED_GIT_BLOB_SHA1,
            "observed_git_blob_sha1":blob,
            "size_bytes":len(data),
            "expected_size_bytes":EXPECTED_SIZE,
            "sha256":sha256
        },
        "semantic_checks":{
            "required_columns_present":schema_ok,
            "row_count":len(rows),
            "subject_count":len(subjects),
            "session_count":len(sessions),
            "total_trials_sum":sum(ntrials),
            "min_trials_session":min(ntrials),
            "max_trials_session":max(ntrials)
        },
        "source_native_summary":{
            "median_r2_cv":statistics.median(r2),
            "mean_r2_cv":statistics.fmean(r2),
            "fraction_r2_cv_positive":sum(v>0 for v in r2)/len(r2),
            "median_null_r2":statistics.median(null),
            "mean_null_r2":statistics.fmean(null),
            "fraction_r2_cv_gt_null":sum(a>b for a,b in zip(r2,null))/len(r2),
            "median_delta_r2_vs_null":statistics.median(delta),
            "mean_delta_r2_vs_null":statistics.fmean(delta),
            "median_correlation":statistics.median(corr),
            "mean_correlation":statistics.fmean(corr),
            "fraction_positive_coefficient":sum(v>0 for v in coef)/len(coef)
        },
        "claim_ceiling":(
            "This validates and summarizes the exact source-derived Salience-to-Salience "
            "predictability table at the pinned external commit. It is not an independent "
            "reanalysis of raw SEEG/hdEEG, does not license scalar chi, and does not establish "
            "a SymC increment over the source-native method."
        )
    }

    outdir=Path("joint_information_brain_outputs")
    outdir.mkdir(exist_ok=True)
    (outdir/"brain_source_native_predictability_qualification_v01.json").write_text(
        json.dumps(out,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(out,indent=2,sort_keys=True))
    if out["status"] != "PASS":
        raise SystemExit(2)

if __name__=="__main__":
    main()
