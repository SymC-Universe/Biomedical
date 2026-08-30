@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1

echo Cancer Stability Atlas Stage B2a - genomic decomposition
echo Frozen design: 5 genomic coordinates, n=30, 100 resamples per eligible cancer-coordinate task.
echo This run does NOT compute chi, does NOT use CV/2, and does NOT define an optimum.
echo The run is checkpointed. If Windows closes or the run stops, launch this same file again and select the same Stage A cache.
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

set "PICK1=%TEMP%\csa_b2_cache_%RANDOM%_%RANDOM%.txt"
"%PY%" scripts_select_file.py "Select hallmark_profile_cache.npz from completed Stage A1" > "%PICK1%"
set "CACHE="
set /p CACHE=<"%PICK1%"
del /q "%PICK1%" >nul 2>nul
if not defined CACHE goto :cancel

echo.
echo Running B2 contract and execution tests...
"%PY%" -m pytest -q
if errorlevel 1 goto :fail

echo.
echo Running frozen Stage B2a genomic analysis.
echo Progress prints after each completed cancer-coordinate task.
echo There are 306 eligible tasks in the full frozen run.
echo Completed task files are hash-checked and reused automatically after any restart.
echo.
"%PY%" -m src.run_stage_b2_genomic_resume --cache "%CACHE%" --gmt "inputs\hallmark_membership_snapshot.gmt" --absolute "sources\ABSOLUTE_scores.tsv" --seg "sources\seg_based_scores.tsv" --b1-context "inputs\stage_b1_context_matched.csv" --plan "config\stage_b2_integration_plan.json" --out stage_b2_genomic_outputs --workers 4
if errorlevel 1 goto :fail

echo.
echo STAGE B2A GENOMIC COMPLETE.
echo Upload these four files from stage_b2_genomic_outputs back into ChatGPT:
echo   STAGE_B2_GENOMIC_SUMMARY.json
echo   stage_b2_genomic_module_effects.csv
echo   stage_b2_genomic_cancer_diagnostic.csv
echo   stage_b2_genomic_task_status.csv
echo.
echo Keep the _task_cache folder locally. It is the restartable raw audit record.
echo.
pause
exit /b 0

:cancel
echo File selection cancelled.
pause
exit /b 2

:fail
echo.
echo STAGE B2A STOPPED OR FAILED.
echo Your completed task checkpoints remain in stage_b2_genomic_outputs\_task_cache.
echo Launch RUN_STAGE_B2_GENOMIC_WINDOWS.bat again to resume from completed tasks.
echo If the same error repeats, copy the error text into ChatGPT.
pause
exit /b 1
