# Umeki 2025 EGF-SOS-RAF execution contract v0.1

**Parent freeze:** `BIO_CHI/control/UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_FREEZE_v0_1.md`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC OUTPUT EXTRACTION

## Execution surface

GitHub Actions in `SymC-Universe/Biomedical`.

## Pinned source

`YasushiSako/transfer_entropy_2@3467850de2e45dfc2b7766ba4dce0d7af8839a00`

The analysis downloads only the eight frozen WT dose-series CSVs and verifies their Git blob SHA-1 identities before parsing.

## Required outputs

- `source_manifest.csv`
- `pair_inventory.csv`
- `cell_features.csv`
- `representation_failures.csv`
- `depth_vs_input_cv.json`
- `rank1_representation_cv.json`
- `UMEKI2025_EGF_SOS_RAF_DEPTH_RATE_P0Q_V01_RESULT.json`
- `SHA256SUMS.txt`

## Locked numerical environment

Python 3.11 with pinned NumPy, pandas, SciPy, and scikit-learn versions in the workflow.

## Stop rule

No scientific threshold, time window, feature definition, model term, bootstrap rule, or representation criterion may change after source outcome inspection. Any later alteration becomes a separately frozen post-result sensitivity analysis.
