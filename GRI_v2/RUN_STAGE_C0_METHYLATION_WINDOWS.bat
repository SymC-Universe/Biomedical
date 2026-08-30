@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo Cancer Stability Atlas Stage C0 - DNA methylation source gate
echo This stage downloads and audits the frozen 5.02 GB PanCanAtlas merged HM27/HM450 matrix.
echo It performs NO biological association, NO chi calculation, and NO feature selection from outcomes.
echo The download is resumable. Re-launch this same file after an interruption.
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

set "PICK1=%TEMP%\csa_c0_cache_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_profile_cache.npz from completed Stage A1" > "%PICK1%"
set "CACHE="
set /p CACHE=<"%PICK1%"
del /q "%PICK1%" >nul 2>nul
if not defined CACHE goto :cancel

if not exist "large_sources" mkdir "large_sources"
if not exist "stage_c0_methylation_outputs" mkdir "stage_c0_methylation_outputs"

echo.
echo Running repository contract tests before acquisition...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Starting frozen Stage C0 source acquisition/audit.
echo Expected source size: 5,022,150,019 bytes.
echo Existing .part data will be reused if the GDC endpoint honors byte ranges.
echo.
"%PY%" -m src.probe_stage_c0_methylation --plan "config\stage_c0_methylation_source_plan.json" --cache "%CACHE%" --out "stage_c0_methylation_outputs" --source "large_sources\jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv" --download
if errorlevel 1 goto :fail

echo.
echo STAGE C0 METHYLATION SOURCE GATE COMPLETE.
echo Return these two compact files from stage_c0_methylation_outputs:
echo   STAGE_C0_METHYLATION_SOURCE_SUMMARY.json
echo   stage_c0_methylation_cancer_coverage.csv
echo.
echo Keep the 5.02 GB methylation matrix in large_sources. Do not upload it to ChatGPT or commit it to GitHub.
echo.
pause
exit /b 0

:cancel
echo File selection cancelled.
pause
exit /b 2

:fail
echo.
echo STAGE C0 STOPPED OR FAILED.
echo Do not delete the .part file in large_sources; a valid partial download can be resumed.
echo Copy the exact error text into ChatGPT if the same failure repeats.
pause
exit /b 1
