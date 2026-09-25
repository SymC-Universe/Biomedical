# Kizilirmak 2023 source-preflight correction checkpoint

**Date:** 25 September 2026
**Branch:** `gri-biochi-bridge-p0q-20260925`
**Task:** `GRI_BIOCHI_KIZILIRMAK_C_D_20260925`
**Failure class:** mechanical schema-inspection defect; limited value exposure; no endpoint/result analysis.

## What happened

The extended schema preflight treated the first row of the headerless Data S1 CSV files as if it were a header. This caused the first time-point NCI values to be serialized into the schema artifact.

## Root cause

The source CSV files are numeric matrices with no header row. The preflight assumed a header existed because it used the first line to infer CSV geometry.

## Scientific effect

The C+D scientific design, the A/B carrier structure, and the no-retuning rule were already frozen before this exposure. No peak counts, oscillatory fractions, AUCs, clone-level dynamic summaries, chi_GRI values, or relationships between RNA and dynamics were computed or inspected.

The exposed first time-point values therefore do not determine any frozen analysis choice. They are preserved as a procedural contamination record rather than hidden or relabeled.

## Repair

Future preflight runs record only matrix row/column counts for headerless dynamic CSV files and do not serialize numeric row contents. The full C+D execution remains prospective with respect to all target summaries.

## Disposition

`PASS_WITH_RECORDED_LIMITED_PREFLIGHT_EXPOSURE`

This is not a scientific failure and does not license any retuning.
