# Neural Stability Dynamics Phase 0C Untouched Holdout v0.1

This package is already scientifically frozen. Do not edit configuration or thresholds before running it.

## Windows PowerShell
From this extracted folder:

```powershell
python local_runner.py
```

The runner:
1. executes unit/engineering tests;
2. writes a SHA-256 manifest;
3. executes the untouched synthetic holdout;
4. preserves either PASS or FAIL without scientific retuning.

Outputs are written to:

`results/phase0c/`

Upload that entire folder after completion.

## Important
A Phase 0C FAIL is a valid scientific result. Do not rerun with changed thresholds.

No EEG or clinical data are read by this package.
