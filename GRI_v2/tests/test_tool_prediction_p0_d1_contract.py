from __future__ import annotations

import numpy as np

from src.run_tool_prediction_p0_d1_discovery_source import _fit_pc1, sample_root


def test_pc1_orientation_nonnegative_module_mean():
    X = np.array([[0.0, 0.0], [1.0, 2.0], [2.0, 4.0], [3.0, 6.0]])
    fit = _fit_pc1(X)
    assert fit is not None
    means, loading, explained, method = fit
    scores = (X - means) @ loading
    module_mean = X.mean(axis=1)
    assert np.corrcoef(scores, module_mean)[0, 1] >= 0
    assert explained > 0.99
    assert method == "NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN"


def test_pc1_zero_variance_refuses():
    assert _fit_pc1(np.ones((5, 3))) is None


def test_sample_root_normalizes():
    assert sample_root("x.TCGA.AB.1234.01A.foo") == "TCGA-AB-1234-01A"
