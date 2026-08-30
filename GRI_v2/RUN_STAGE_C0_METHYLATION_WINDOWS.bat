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

:select_cache
set "PICK1=%TEMP%\csa_c0_cache_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select the completed Stage A hallmark_profile_cache.npz" > "%PICK1%"
set "CACHE="
set /p CACHE=<"%PICK1%"
del /q "%PICK1%" >nul 2>nul
if not defined CACHE goto :cancel

if not exist "%CACHE%" (
  echo.
  echo SELECTED CACHE PATH DOES NOT EXIST:
  echo   %CACHE%
  echo Please select the actual existing completed Stage A hallmark_profile_cache.npz.
  echo.
  goto :select_cache
)

echo.
echo Verifying selected Stage A cache BEFORE methylation acquisition...
"%PY%" -m src.validate_stage_c0_cache "%CACHE%"
if errorlevel 1 (
  echo.
  echo The selected file is missing or is not the frozen completed Stage A cache.
  echo Please choose the correct hallmark_profile_cache.npz.
  echo.
  goto :select_cache
)

if not exist "large_sources" mkdir "large_sources"
if not exist "stage_c0_methylation_outputs" mkdir "stage_c0_methylation_outputs"

echo.
echo Running repository contract tests before acquisition...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Starting frozen Stage C0 source acquisition/audit.
echo Expected source size: 5,022,150,019 bytes.
echo Any valid existing source file or .part data in large_sources will be reused.
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
echo Do not delete the source file or .part file in large_sources; valid acquired data will be reused.
echo Copy the exact error text into ChatGPT if the same failure repeats.
pause
exit /b 1
