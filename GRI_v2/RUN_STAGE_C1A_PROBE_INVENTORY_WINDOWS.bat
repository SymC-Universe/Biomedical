@echo off
setlocal
cd /d "%~dp0"
echo.
echo Stage C1A frozen annotation/probe inventory
echo ------------------------------------------
echo This gate reuses the already-audited methylation TSV.
echo It streams the file for SHA-256 and probe IDs only.
echo No methylation beta-value biological association is performed.
echo.
python -m src.run_stage_c1a_windows
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo STAGE C1A STOPPED OR FAILED.
  echo Keep all source and output files unchanged and send this console output to ChatGPT.
  pause
  exit /b %RC%
)
echo STAGE C1A PROBE INVENTORY COMPLETE.
echo Return:
echo   stage_c1a_probe_inventory_outputs\STAGE_C1A_PROBE_INVENTORY_SUMMARY.json
echo   stage_c1a_probe_inventory_outputs\stage_c1a_regulatory_stratum_counts.csv
echo Keep the generated .csv.gz mapping and flags files locally for the later C1 run.
pause
