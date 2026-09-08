# Neural Stability Dynamics Phase 0D v0.1

This package is the **untouched prospective synthetic holdout** that follows the archived Phase 0C v0.2 FAIL/FAIL/FAIL result and its post-hoc failure-boundary audit.

Phase 0D does not rescue or rescore Phase 0C. It tests a new estimator architecture on a new seed and new synthetic systems.

## Why Phase 0D exists

Phase 0C showed that the full nonstationary record could select a mixture order larger than the order of either local regime. The frozen Phase 0C evaluator then imposed that full-record order on both halves, contaminating the intended scalar/modal/system dissociation tests. Phase 0C also demanded raw pairwise pole geometry inside crowded/near-degenerate modal clusters even though individual modes there were already declared non-identifiable.

Phase 0D fixes those architectural problems **before** this holdout is executed:

1. full, first-half, and second-half observable orders are selected independently;
2. full-record mixture order is diagnostic only;
3. modal carriers are aligned by MAC/subspace rather than by pole proximity;
4. whole-system relational geometry is evaluated between resolved modal clusters;
5. single or crowded unresolved geometry is explicitly `UNRESOLVED`, not converted into a scalar or a false failure;
6. scalar, modal, and system layers remain separately scored.

## Local execution

Run only:

```powershell
python local_runner.py
```

The runner first executes engineering tests, writes the code/config/rules manifest, and only then executes the untouched Phase 0D holdout.

When complete, preserve and send the entire:

`results\\phase0d_v01`

Do not change thresholds after seeing the result.
