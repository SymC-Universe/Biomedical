# E. coli PMF recovery execution contract v0.1

**Parent freeze:** `BIO_CHI/control/ECOLI2026_PMF_RECOVERY_P0Q_FREEZE_v0_1.md`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC OUTPUT EXTRACTION

## Retrieval

All analysis inputs are pulled from the pinned upstream commit
`wadhwalab/2026-Meneses-Osmotic@d14d0caaa07299f13d1b1121d1e4630454fd724b`.

The workflow records SHA-256 for every downloaded Parquet file before analysis.

## Reversible-shock source files

- `data/time-series/bead/sucrose_200mM.parquet`
- `data/time-series/bead/sucrose_300mM.parquet`
- `data/time-series/bead/sucrose_400mM.parquet`
- `data/time-series/bead/sucrose_500mM.parquet`

## Sustained-adaptation source files

- `data/time-series/bead/adaption_200mM.parquet`
- `data/time-series/bead/adaption_300mM.parquet`
- `data/time-series/bead/adaption_400mM.parquet`
- `data/time-series/bead/adaption_500mM.parquet`

## Independent-observable source files

TMRM and cell-area `control.parquet` plus 200, 300, 400, and 500 mM files.

## Locked software

Python 3.11 with pinned NumPy, pandas, SciPy, scikit-learn, and pyarrow in the GitHub Actions workflow.

## Output contract

The execution must emit:

- `source_manifest.csv`
- `motor_reversible_cell_features.csv`
- `motor_reversible_fit_failures.csv`
- `motor_adaptation_cell_features.csv`
- `motor_adaptation_fit_failures.csv`
- `representation_cv.json`
- `tmrm_recomputed_summary.csv`
- `cell_area_recomputed_summary.csv`
- `ECOLI2026_PMF_RECOVERY_P0Q_V01_RESULT.json`
- `SHA256SUMS.txt`

No result is promoted unless the source hashes, cell counts, fit counts, and representation disposition are all present.
