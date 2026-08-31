@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo GRI v2 P0 D1 - DISCOVERY-only methylation source preprocessing
echo.
echo This run is intentionally one-sided:
echo   - reads methylation beta values ONLY for eligible DISCOVERY participants in the 19 frozen evaluable cancers
echo   - fits probe eligibility, discovery medians, TSS200 gene scores, and methylation Hallmark PC1s ONLY in DISCOVERY
echo   - reads NO RNA expression target values
echo   - reads NO REPLICATION or FINAL_HOLDOUT methylation values
echo   - changes NO P0 threshold, partition, or Stage C1 science
echo.
where py >nul 2>nul
if errorlevel 1 (echo ERROR: Windows Python launcher 'py' was not found.& pause& exit /b 1)
if not exist ".venv\Scripts\python.exe" (
  echo Creating local Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto :fail
)
set PY=.venv\Scripts\python.exe
"%PY%" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 goto :fail

echo Verifying package integrity...
"%PY%" verify_package.py
if errorlevel 1 goto :fail

echo Running pre-data regression tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Two file pickers will appear:
echo   1. the same C0-audited 5.02 GB methylation TSV
echo   2. the exact Hallmark membership snapshot .gmt used in Stage A
echo.
echo The Stage A RNA cache is NOT requested in D1 because RNA predictive targets remain unopened here.
echo.
"%PY%" -m src.run_tool_prediction_p0_d1_windows
if errorlevel 1 goto :fail

echo.
echo D1 COMPLETE.
echo Upload P0_D1_DISCOVERY_SOURCE_PREPROCESS_RESULTS.zip to ChatGPT.
echo.
pause
exit /b 0

:fail
echo.
echo P0 D1 STOPPED OR FAILED.
echo Preserve the exact error text. No scientific threshold should be changed to make the run pass.
pause
exit /b 1
