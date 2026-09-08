# Neural Stability Dynamics - Phase 0 Structure Calibration v0.1

## Purpose
This package starts from underlying dynamical structure rather than from a desired scalar.

Primary question: **Can an output-only system-identification method recover known modal structure from synthetic multichannel time series?**

Primary recovery objects are continuous-time poles/eigenvalues and observable mode shapes. Model order is held fixed to truth in this first engineering calibration. A damping ratio is reported only as a secondary descriptor for a successfully matched stable complex pole.

## Scientific firewall
No diagnosis labels, TDBRAIN participant tables, treatment outcomes, or historical desired ordering are used anywhere in Phase 0. Passing Phase 0 does not validate an EEG biomarker or psychiatric interpretation.

## Quick start on Windows PowerShell
```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install numpy scipy pytest
python local_runner.py
```
If `py -3.14` is unavailable, use the Python command that launches your installed 3.14 environment.

Outputs appear under `results/phase0_structure/`. Review `RUN_LOG.txt`, `WORKING_STATE.json`, `trial_results.csv`, `summary.json`, `CONFIG_SHA256.txt`, and `CODE_MANIFEST.sha256`.

This version deliberately does **not** read TDBRAIN, select model order, claim a system-level chi, average modal damping values, join diagnosis labels, or tune to disease separation.
