@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo Cancer Stability Atlas Stage C0.1 - unique sample identity gate
echo This stage reads the methylation HEADER only.
echo It performs NO methylation biological association and reads NO beta-value rows for analysis.
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
"%PY%" -m src.run_stage_c0_1_windows
if errorlevel 1 goto :fail

echo.
echo STAGE C0.1 SAMPLE IDENTITY GATE COMPLETE.
echo Return these three compact files from stage_c0_1_sample_identity_outputs:
echo   STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json
echo   stage_c0_1_unique_match_coverage.csv
echo   stage_c0_1_duplicate_primary_roots.csv
echo.
pause
exit /b 0

:fail
echo.
echo STAGE C0.1 STOPPED OR FAILED.
echo No methylation beta-value association was run.
echo Copy the exact error text into ChatGPT if the same failure repeats.
pause
exit /b 1
