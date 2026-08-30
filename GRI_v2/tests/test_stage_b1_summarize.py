from pathlib import Path

import pandas as pd

from src.summarize_stage_b1 import METRICS, summarize


def test_summarize_uses_resample_column_not_dataframe_method(tmp_path: Path):
    rows = []
    for r in range(3):
        for module in ["M1", "M2", "M3"]:
            row = {"model_id": "PURITY", "cancer_type": "TEST", "eligible_n": 40, "resample": r, "module": module}
            for i, metric in enumerate(METRICS):
                b = 0.1 + 0.01 * i + 0.001 * r
                a = b - 0.002
                n = b - 0.001
                row[f"baseline__{metric}"] = b
                row[f"actual__{metric}"] = a
                row[f"null__{metric}"] = n
                row[f"actual_delta__{metric}"] = a - b
                row[f"null_delta__{metric}"] = n - b
                row[f"context_specific_delta__{metric}"] = a - n
            rows.append(row)
    raw = tmp_path / "raw.csv.gz"
    pd.DataFrame(rows).to_csv(raw, index=False, compression="gzip")
    _, module, cancer = summarize(raw, tmp_path)
    assert len(module) == 3
    assert len(cancer) == 1
    assert int(cancer.iloc[0]["valid_resamples"]) == 3
