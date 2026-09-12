# GRI post-FINAL capacity-control provenance discrepancy

**Date:** 2026-09-11  
**Status:** MATERIAL PROVENANCE / DESCRIPTION DISCREPANCY  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A  
**Scientific result changed:** NO

## Discrepancy

The 8 September 2026 rebuilt main manuscript states that a dimensionality-matched post-FINAL capacity-control analysis "is therefore frozen separately as an adversarial extension." The supplement likewise says a post-FINAL dimensionality-matched capacity-control protocol is "retained separately as adversarial follow-up." However, the exact runnable freeze artifact, configuration, hash, timestamp, or source-of-record package has not been recovered in either the current GitHub repository audit or the current File Library provenance search.

The same supplement elsewhere uses weaker wording that such a post-FINAL equal-dimensional control **can test** whether Hallmark-structured features outperform a capacity-matched non-Hallmark representation. That wording is consistent with an intended control whose executable freeze has not yet been verified.

## Searches completed

### GitHub

- code search: `equal-dimensional control` -> no current GRI runnable freeze recovered;
- code search: `capacity matched` -> no current GRI runnable freeze recovered;
- code search: `POST_FINAL` -> no current GRI runnable freeze recovered;
- commit search: `equal-dimensional` -> no matching commit;
- commit search: `capacity matched` -> no matching commit.

### File Library

Searches for:

- `equal-dimensional` + `post-FINAL` + GRI comparator;
- `capacity-matched` + Hallmark methylation freeze;
- `same-capacity non-Hallmark methylation control`;
- `dimensionality-matched` + `P0` + `FINAL_HOLDOUT`;
- `non-Hallmark methylation PCs` + frozen;
- `post-FINAL capacity-control protocol`;

recovered the September 8 manuscript/supplement and reviewer/audit commentary, but no distinct executable/config/freeze package.

## Current admissible statement

Until the source-of-record freeze is recovered, the project may state only:

> A post-FINAL dimensionality-matched capacity control was planned/identified as an adversarial follow-up, but the exact historical executable freeze has not yet been provenance-verified in the recovered project record.

Do **not** state as established fact that the exact executable control is currently recovered and frozen.

## Scientific consequence

This does not invalidate the internal FINAL_HOLDOUT result. The admissible result remains:

- the 45-Hallmark methylation plus two-covariate model outperformed the two-covariate baseline in 17/18 primary-evaluable cancers;
- this establishes additional held-out methylation information beyond the two measured covariates in the tested internal TCGA partitions;
- it does not isolate Hallmark organization as the unique source of the gain;
- it does not constitute capacity-matched superiority over a non-Hallmark representation.

## Protocol classification

`PROVENANCE_STATE = REFERENCED_BUT_NOT_RECOVERED`

`HISTORICAL_FREEZE_STATUS = UNVERIFIED`

`CURRENT_CLAIM_EFFECT = CLAIM_CEILING_UNCHANGED`

`REMEDIATION_CLASS = SOURCE_OF_RECORD_RECOVERY_OR_AUTHORITATIVE_TEXT_CORRECTION`

This is not a scientific failure and does not justify inventing or reconstructing a historical freeze after the fact.

## Allowed next actions

1. Continue exact provenance recovery from local archives and historical commits/files.
2. If an artifact is recovered, verify timestamp/commit/hash/content and confirm it predates inspection of its own result.
3. If unrecoverable, explicitly close the historical freeze as unavailable.
4. A newly designed capacity-matched control remains scientifically useful but must be labeled NEW POST-FINAL P0-Q and frozen prospectively relative to its own result.
5. Before submission, authoritative manuscript wording that says the analysis **is frozen separately** must either be supported by a recovered source-of-record artifact or revised to the weaker, accurate planned/retained-follow-up wording under user-authorized manuscript editing.

## Stop rule

Do not execute a newly invented control under the identity of the missing historical freeze. Do not upgrade the original FINAL_HOLDOUT status with any post-FINAL analysis.