from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, spearmanr, wilcoxon

SOURCE_REPO = "grabuffo/State_Dependent_Brain_Stimulation"
SOURCE_COMMIT = "84afcf934c3798b2a40dc8da22d0840e60a4b0f9"
BASE = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}"

SOURCES = {
    "SEEG": "data/df_results/ieeg_metrics/df_correlations_5MOIs_ieeg.csv",
    "hdEEG": "data/df_results/hd-eeg_metrics/df_correlations_5MOIs_hd-eeg.csv",
}

NETWORK_NAMES = {
    "Default": "DMN",
    "DorsAttn": "DAN",
    "SalVentAttn": "VAN",
    "Cont": "CON",
    "Limbic": "LIM",
    "SomMot": "SMN",
    "Vis": "VIS",
}
ORDERED_NETWORKS = ["DMN", "LIM", "CON", "DAN", "VAN", "SMN", "VIS"]

# Notebook outputs at the pinned source commit, copied prospectively into this
# known-truth validator before executing this reproduction.
EXPECTED = {
    "SEEG": {
        "mean_rho2": {
            "DMN": 0.143669,
            "LIM": 0.164443,
            "CON": 0.171445,
            "DAN": 0.178338,
            "VAN": 0.192850,
            "SMN": 0.190580,
            "VIS": 0.204415,
        },
        "counts": {
            "DMN": 1700,
            "LIM": 950,
            "CON": 625,
            "DAN": 475,
            "VAN": 1650,
            "SMN": 1900,
            "VIS": 600,
        },
        "friedman_chi2": 88.851,
        "friedman_p": 5.247e-17,
        "metric_pairs": 25,
        "median_gradient_rho": 0.821429,
        "mean_gradient_rho": 0.734286,
        "positive_pairs": 25,
        "gradient_wilcoxon_p": 2.980232e-08,
    },
    "hdEEG": {
        "mean_rho2": {
            "DMN": 0.069692,
            "LIM": 0.072444,
            "CON": 0.056306,
            "DAN": 0.072938,
            "VAN": 0.074215,
            "SMN": 0.077248,
            "VIS": 0.061385,
        },
        "counts": {
            "DMN": 1750,
            "LIM": 950,
            "CON": 625,
            "DAN": 475,
            "VAN": 1650,
            "SMN": 1900,
            "VIS": 600,
        },
        "friedman_chi2": 40.2686,
        "friedman_p": 4.034e-07,
        "metric_pairs": 25,
        "median_gradient_rho": -0.035714,
        "mean_gradient_rho": 0.025714,
        "positive_pairs": 12,
        "gradient_wilcoxon_p": 0.531599,
    },
}

OUTDIR = Path("brain_state_known_truth_outputs")
CACHEDIR = OUTDIR / "source_cache"


def download(url: str, target: Path) -> dict:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
        status = getattr(response, "status", 200)
    target.write_bytes(data)
    return {
        "url": url,
        "http_status": int(status),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def analyze(path: Path, modality: str) -> dict:
    df = pd.read_csv(path)
    df = df.loc[(df["Radius_pre"] == 100) & (df["Radius_post"] == 100)].copy()
    df["Explained_Variance"] = df["Correlation"] ** 2
    df["Network"] = df["Network"].map(NETWORK_NAMES)
    df = df.dropna(subset=["Network"])
    df["Network"] = pd.Categorical(df["Network"], categories=ORDERED_NETWORKS, ordered=True)

    network_summary = (
        df.groupby("Network", observed=True)["Explained_Variance"]
        .agg(["mean", "count"])
        .reindex(ORDERED_NETWORKS)
    )

    pair_means = (
        df.groupby(["Metric_pre", "Metric_post", "Network"], observed=True)["Explained_Variance"]
        .mean()
        .unstack("Network")
        .reindex(columns=ORDERED_NETWORKS)
        .dropna()
        .reset_index()
    )

    friedman = friedmanchisquare(
        *[pair_means[n].to_numpy(dtype=float) for n in ORDERED_NETWORKS]
    )

    gradients = []
    for _, row in pair_means.iterrows():
        values = row[ORDERED_NETWORKS].to_numpy(dtype=float)
        if modality == "SEEG":
            res = spearmanr(np.arange(1, len(ORDERED_NETWORKS) + 1), values, alternative="greater")
        else:
            res = spearmanr(np.arange(1, len(ORDERED_NETWORKS) + 1), values)
        gradients.append(float(res.statistic))

    gradients = np.asarray(gradients, dtype=float)
    grad_test = wilcoxon(gradients, alternative="greater")

    return {
        "rows_at_radius_100": int(len(df)),
        "mean_rho2": {n: float(network_summary.loc[n, "mean"]) for n in ORDERED_NETWORKS},
        "counts": {n: int(network_summary.loc[n, "count"]) for n in ORDERED_NETWORKS},
        "friedman_chi2": float(friedman.statistic),
        "friedman_p": float(friedman.pvalue),
        "metric_pairs": int(len(pair_means)),
        "median_gradient_rho": float(np.median(gradients)),
        "mean_gradient_rho": float(np.mean(gradients)),
        "positive_pairs": int((gradients > 0).sum()),
        "gradient_wilcoxon_p": float(grad_test.pvalue),
    }


def close(a: float, b: float, tol: float) -> bool:
    return bool(abs(a - b) <= tol)


def validate(result: dict, expected: dict) -> dict:
    checks = {}
    for n in ORDERED_NETWORKS:
        checks[f"mean_rho2_{n}"] = close(result["mean_rho2"][n], expected["mean_rho2"][n], 5e-6)
        checks[f"count_{n}"] = result["counts"][n] == expected["counts"][n]

    checks["friedman_chi2"] = close(result["friedman_chi2"], expected["friedman_chi2"], 5e-4)
    checks["friedman_p"] = bool(np.isclose(result["friedman_p"], expected["friedman_p"], rtol=5e-3, atol=1e-20))
    checks["metric_pairs"] = result["metric_pairs"] == expected["metric_pairs"]
    checks["median_gradient_rho"] = close(result["median_gradient_rho"], expected["median_gradient_rho"], 5e-6)
    checks["mean_gradient_rho"] = close(result["mean_gradient_rho"], expected["mean_gradient_rho"], 5e-6)
    checks["positive_pairs"] = result["positive_pairs"] == expected["positive_pairs"]
    checks["gradient_wilcoxon_p"] = bool(np.isclose(
        result["gradient_wilcoxon_p"], expected["gradient_wilcoxon_p"], rtol=5e-5, atol=1e-12
    ))
    return {
        "checks": checks,
        "all_pass": bool(all(checks.values())),
    }


def main() -> None:
    OUTDIR.mkdir(exist_ok=True)
    final = {
        "schema": "SYMC_BRAIN_STATE_KNOWN_TRUTH_SOURCE_REPRODUCTION_V01",
        "epistemic_class": "SOURCE_NATIVE_REPRODUCTION",
        "source_repo": SOURCE_REPO,
        "source_commit": SOURCE_COMMIT,
        "claim_ceiling": (
            "Reproduces source-native network-dependence summaries from pinned derived "
            "tables. It does not establish scalar chi, capital Chi, or SymC incremental value."
        ),
        "modalities": {},
    }

    overall = True
    for modality, relpath in SOURCES.items():
        local = CACHEDIR / f"{modality}.csv"
        identity = download(f"{BASE}/{relpath}", local)
        result = analyze(local, modality)
        validation = validate(result, EXPECTED[modality])
        overall = overall and validation["all_pass"]
        final["modalities"][modality] = {
            "source": identity,
            "result": result,
            "validation": validation,
        }

    final["status"] = "PASS" if overall else "FAIL"
    (OUTDIR / "brain_network_dependence_source_reproduction_v01.json").write_text(
        json.dumps(final, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(final, indent=2, sort_keys=True))

    if not overall:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
