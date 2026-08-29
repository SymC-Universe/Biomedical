@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1

echo Cancer Stability Atlas Stage A1.1 - fixed-n network calibration
echo This run does NOT compute chi and does NOT use CV/2.
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: Windows Python launcher 'py' was not found.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating local Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto :fail
)

set PY=.venv\Scripts\python.exe
"%PY%" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 goto :fail

set "PICK_CACHE=%TEMP%\csa_a11_cache_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_profile_cache.npz from the completed Stage A1 output" > "%PICK_CACHE%"
if errorlevel 1 goto :fail
set "CACHE="
set /p CACHE=<"%PICK_CACHE%"
del /q "%PICK_CACHE%" >nul 2>nul
if not defined CACHE goto :cancel

set "PICK_GMT=%TEMP%\csa_a11_gmt_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_membership_snapshot.gmt from the same Stage A1 output" > "%PICK_GMT%"
if errorlevel 1 goto :fail
set "GMT="
set /p GMT=<"%PICK_GMT%"
del /q "%PICK_GMT%" >nul 2>nul
if not defined GMT goto :cancel

echo.
echo Running contract tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Running frozen fixed-n calibration...
"%PY%" -m src.run_stage_a1_1 "%CACHE%" "%GMT%" --out stage_a1_1_outputs
if errorlevel 1 goto :fail

echo.
echo STAGE A1.1 COMPLETE.
echo Upload these files from stage_a1_1_outputs:
echo   STAGE_A1_1_SUMMARY.json
echo   stage_a1_1_fixed_n_calibration.csv
echo   stage_a1_1_cancer_level_diagnostic.csv
echo.
pause
exit /b 0

:cancel
echo File selection cancelled.
pause
exit /b 2

:fail
echo.
echo STAGE A1.1 FAILED. Copy the error text above back into ChatGPT.
pause
exit /b 1
