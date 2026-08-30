@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo GRI v2 P0 - frozen sample eligibility gate
echo.
echo This stage reads methylation beta values ONLY to count finite values per participant.
echo It does NOT read RNA Hallmark target values or predictive outcomes.
echo It does NOT refit partitions, thresholds, or Stage C1 science.
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

echo Running package contract tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo File pickers will ask for exactly two files:
echo   1. the same C0-audited 5.02 GB methylation TSV
echo   2. p0_preeligibility_split_manifest.csv from the split step you just completed
echo.
echo The scan applies the already-frozen 95%% finite-probe eligibility rule.
echo.
"%PY%" -m src.run_tool_prediction_p0_eligibility_windows
if errorlevel 1 goto :fail

echo.
echo P0 SAMPLE ELIGIBILITY COMPLETE.
echo Return these three files from tool_prediction_p0_eligibility_outputs:
echo   P0_ELIGIBILITY_SUMMARY.json
echo   p0_sample_eligibility.csv
echo   p0_partition_eligibility_counts.csv
echo.
pause
exit /b 0

:fail
echo.
echo P0 ELIGIBILITY STOPPED OR FAILED.
echo Copy the exact error text into ChatGPT if the same failure repeats.
pause
exit /b 1
