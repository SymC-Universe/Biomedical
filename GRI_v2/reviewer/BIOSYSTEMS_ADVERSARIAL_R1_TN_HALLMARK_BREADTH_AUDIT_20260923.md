# BioSystems adversarial Round 1 - tumor-normal RNA Hallmark breadth audit

**Date:** 23 September 2026
**Status:** CLOSED / POST-HOC ADVERSARIAL SENSITIVITY
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`

## Purpose

Round-1 review raised the possibility that the strong tumor-normal RNA reduction is driven primarily by a small immune/inflammatory Hallmark subset rather than a broad shift in RNA module organization.

This audit uses the already frozen TN-A1 and TN-P20 module-level outputs. It does not change the TN design and is explicitly post-hoc because Hallmark breadth was not a primary preregistered endpoint.

## Result

Across the 50 Hallmarks, cancer-median tumor-minus-normal direction is:

### TN-A1 n=30 primary
- `C_in,pair`: 49/50 Hallmarks lower in tumor;
- `C_in,PC1`: 47/50 lower in tumor;
- `C_out`: 50/50 lower in tumor.

### TN-P20 paired sensitivity
- `C_in,pair`: 48/50 Hallmarks lower in tumor;
- `C_in,PC1`: 48/50 lower in tumor;
- `C_out`: 50/50 lower in tumor.

## Interpretation

The pan-cancer direction is not concentrated in a small immune/inflammatory Hallmark subset. It is broad across the frozen Hallmark library.

This observation does **not** remove tissue-composition confounding:
- Hallmarks themselves can carry composition information;
- adjacent normal and tumor can differ in multiple cell populations simultaneously;
- the audit is post-hoc and descriptive;
- no immune-module exclusion threshold was frozen before the tumor-normal outcome.

The correct use is therefore:

> The tumor-normal RNA shift is broad across Hallmark modules and is not explained by a small subset of immune/inflammatory modules alone; however, broad tissue-composition differences remain a viable alternative contributor until a symmetric composition control is available.

## Claim ceiling

This audit cannot convert the tumor-normal result into a tumor-cell-intrinsic mechanism and cannot substitute for a symmetric composition sensitivity.
