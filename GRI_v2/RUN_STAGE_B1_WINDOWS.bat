@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1

echo Cancer Stability Atlas Stage B1 - composition/context adjustment
echo This run does NOT compute chi, does NOT use CV/2, and does NOT define an optimum.
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
set "PICK1=%TEMP%\csa_b1_cache_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_profile_cache.npz from Stage A1" > "%PICK1%"
set "CACHE="
set /p CACHE=<"%PICK1%"
del /q "%PICK1%" >nul 2>nul
if not defined CACHE goto :cancel
set "PICK2=%TEMP%\csa_b1_gmt_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_membership_snapshot.gmt from Stage A1" > "%PICK2%"
set "GMT="
set /p GMT=<"%PICK2%"
del /q "%PICK2%" >nul 2>nul
if not defined GMT goto :cancel

echo.
echo Running contract tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Running frozen Stage B1. Progress prints after each cancer/model finishes.
echo Keep this window open until STAGE B1 COMPLETE appears.
"%PY%" -m src.run_stage_b1_windows --cache "%CACHE%" --gmt "%GMT%" --purity "sources\TCGA_mastercalls.abs_tables_JSedit.fixed.txt" --leukocyte "sources\TCGA_all_leuk_estimate.masked.20170107.tsv" --plan "config\stage_b1_context_adjustment_plan.json" --out stage_b1_outputs --workers 4
if errorlevel 1 goto :fail

echo.
echo STAGE B1 COMPLETE.
echo Upload from stage_b1_outputs:
echo   STAGE_B1_SUMMARY.json
echo   stage_b1_module_context_effects.csv
echo   stage_b1_cancer_level_diagnostic.csv
echo Keep stage_b1_resample_metrics.csv.gz locally unless ChatGPT asks for it.
echo.
pause
exit /b 0
:cancel
echo File selection cancelled.
pause
exit /b 2
:fail
echo.
echo STAGE B1 FAILED. Copy the error text above back into ChatGPT.
pause
exit /b 1
