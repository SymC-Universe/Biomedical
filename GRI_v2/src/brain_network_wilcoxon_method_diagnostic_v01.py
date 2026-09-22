from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import spearmanr, wilcoxon

SOURCE_REPO = "grabuffo/State_Dependent_Brain_Stimulation"
SOURCE_COMMIT = "84afcf934c3798b2a40dc8da22d0840e60a4b0f9"
BASE = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}"
SOURCES = {
    "SEEG": "data/df_results/ieeg_metrics/df_correlations_5MOIs_ieeg.csv",
    "hdEEG": "data/df_results/hd-eeg_metrics/df_correlations_5MOIs_hd-eeg.csv",
}
SOURCE_NOTEBOOK_P = {"SEEG": 2.980232e-08, "hdEEG": 0.531599}
NETWORK_NAMES = {
    "Default": "DMN", "DorsAttn": "DAN", "SalVentAttn": "VAN",
    "Cont": "CON", "Limbic": "LIM", "SomMot": "SMN", "Vis": "VIS",
}
ORDERED = ["DMN", "LIM", "CON", "DAN", "VAN", "SMN", "VIS"]


def gradients_for(url: str):
    with urllib.request.urlopen(url, timeout=120) as response:
        df = pd.read_csv(response)
    df = df.loc[(df["Radius_pre"] == 100) & (df["Radius_post"] == 100)].copy()
    df["Network"] = df["Network"].map(NETWORK_NAMES)
    df = df.dropna(subset=["Network"])
    df["Network"] = pd.Categorical(df["Network"], categories=ORDERED, ordered=True)
    df["Explained_Variance"] = df["Correlation"] ** 2
    pair = (
        df.groupby(["Metric_pre", "Metric_post", "Network"], observed=True)["Explained_Variance"]
        .mean().unstack("Network").reindex(columns=ORDERED).dropna().reset_index()
    )
    vals = []
    for _, row in pair.iterrows():
        vals.append(float(spearmanr(np.arange(1, 8), row[ORDERED].to_numpy(float)).statistic))
    return np.asarray(vals, dtype=float)


def method_result(x, method):
    try:
        r = wilcoxon(x, alternative="greater", zero_method="wilcox", method=method)
        return {"statistic": float(r.statistic), "pvalue": float(r.pvalue), "error": None}
    except Exception as exc:
        return {"statistic": None, "pvalue": None, "error": f"{type(exc).__name__}: {exc}"}


def main():
    result = {
        "schema": "SYMC_BRAIN_NETWORK_WILCOXON_METHOD_DIAGNOSTIC_V01",
        "source_commit": SOURCE_COMMIT,
        "scipy_version": scipy.__version__,
        "purpose": "Adjudicate source-notebook versus current-runtime Wilcoxon p-value drift without altering biological results.",
        "modalities": {},
    }
    for modality, rel in SOURCES.items():
        x = gradients_for(f"{BASE}/{rel}")
        methods = {m: method_result(x, m) for m in ["auto", "exact", "approx"]}
        rec = {
            "n": int(len(x)),
            "n_positive": int((x > 0).sum()),
            "n_zero": int((x == 0).sum()),
            "n_unique": int(len(np.unique(x))),
            "median": float(np.median(x)),
            "mean": float(np.mean(x)),
            "source_notebook_pvalue": SOURCE_NOTEBOOK_P[modality],
            "runtime_methods": methods,
        }
        if modality == "SEEG" and rec["n_positive"] == rec["n"] and rec["n_zero"] == 0:
            rec["all_positive_sign_assignment_probability"] = float(2.0 ** (-rec["n"]))
        result["modalities"][modality] = rec

    out=Path("brain_state_known_truth_outputs")
    out.mkdir(exist_ok=True)
    (out/"brain_network_wilcoxon_method_diagnostic_v01.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
