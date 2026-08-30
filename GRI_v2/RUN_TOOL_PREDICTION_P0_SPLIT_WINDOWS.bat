@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo GRI v2 P0 - frozen participant split manifest
echo This stage reads the methylation HEADER only.
echo It reads NO methylation beta-value rows and NO predictive target values.
echo It only binds the already-frozen 9,460-person matched identity universe to DISCOVERY / REPLICATION / FINAL_HOLDOUT.
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

echo Running repository contract tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo File pickers will ask for:
echo   1. the completed Stage A hallmark_profile_cache.npz
echo   2. the C0-audited 5.02 GB methylation TSV
echo   3. STAGE_C0_METHYLATION_SOURCE_SUMMARY.json from the completed C0 run
echo.
echo The 5.02 GB file is opened only far enough to read its header line.
echo.
"%PY%" -m src.run_tool_prediction_p0_split_windows
if errorlevel 1 goto :fail

echo.
echo P0 PRE-ELIGIBILITY SPLIT MANIFEST COMPLETE.
echo Return these three compact files from tool_prediction_p0_split_outputs:
echo   P0_SPLIT_MANIFEST_SUMMARY.json
echo   p0_preeligibility_split_manifest.csv
echo   p0_preeligibility_partition_counts.csv
echo.
pause
exit /b 0

:fail
echo.
echo P0 SPLIT MANIFEST STOPPED OR FAILED.
echo No methylation beta-value rows or predictive target values were read by this stage.
echo Copy the exact error text into ChatGPT if the same failure repeats.
pause
exit /b 1
