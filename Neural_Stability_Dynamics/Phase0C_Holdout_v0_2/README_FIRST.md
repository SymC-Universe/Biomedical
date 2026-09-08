# Neural Stability Dynamics Phase 0C v0.2
## Untouched Three-Layer Synthetic Holdout

This package is scientifically frozen. Do not edit configuration, code, or thresholds before running it.

Phase 0C v0.1 was superseded before execution. Do not run the old v0.1 package for scientific scoring.

## Your local step
From this extracted folder in PowerShell, run exactly:

```powershell
python local_runner.py
```

The runner will:
1. run engineering/unit tests;
2. regenerate the code/config/rules SHA-256 manifest;
3. execute the untouched v0.2 synthetic holdout;
4. preserve separate scalar, modal, and system PASS/FAIL outcomes without retuning.

Results are written to:

`results/phase0c_v02/`

After it finishes, upload everything in that folder. You do not need to choose which output files matter.

No EEG, clinical labels, or treatment outcomes are read by this package.
