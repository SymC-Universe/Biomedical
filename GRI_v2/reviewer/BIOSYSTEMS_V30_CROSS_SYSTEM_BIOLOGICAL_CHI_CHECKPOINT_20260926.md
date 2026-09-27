# BioSystems V30 cross-system biological chi checkpoint

**Date:** 26 September 2026  
**Status:** CLOSED FOR THIS ITERATION  
**Authority:** SymC GOM v0.8.6  
**Reviewer guide:** `GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260926_V30.md`

## Submission spine

The original C1/P1 oncology evidence spine remains unchanged. V30 is a research-integrated continuation above V29. V29 is preserved as the lean pre-Stentor submission fallback.

## New cross-system result

The canonical Stentor gate used the source-controlled Ramdas et al. behavioral object at `tejasramdas/stentor_habituation@8704c114555af3477a1dd7471beedde205fed263`.

A prospective replicate-unit amendment was made before SymC-specific outcome inspection after source code showed that controlled cells were pooled from multiple experimental folders. The primary unit is therefore the source-run median, not the individual cell.

The 1,200 controlled cells mapped to 171 source-run units across 12 stimulation-interval by recovery-interval conditions.

The frozen four-coordinate representation was:
`[H1_depth, Recovery, H2_depth, AUC_shift]`.

Under leave-one-recovery-interval-out validation:
- full-vector balanced accuracy = 0.4639841;
- stratified null 97.5th percentile = 0.4177844;
- 2,000-permutation upper-tail p = 0.0014993;
- primary disposition = `CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q`.

Recovery alone was also positive:
- balanced accuracy = 0.4561351;
- null 97.5th percentile = 0.4140139;
- upper-tail p = 0.0009995;
- secondary disposition = `PATH_INFORMATION_NOT_SEPARATED_FROM_RECOVERY_ONLY_P0Q`.

The independent 12-condition representation-adequacy test refused one dimension:
- PC1 variance fraction = 0.7346072;
- maximum standardized one-dimensional residual = 1.1628776;
- `Chi_bio = MULTICOORDINATE_CONDITION_REPRESENTATION_REQUIRED_P0Q`.

Scalar `chi_bio` remains `NOT_OPENED_NOT_LICENSED`.

## Cross-system meaning

Meneses E. coli and Stentor both support bounded path/context-sensitive whole-event organization. The minimal informative representation is not identical: in Stentor, recovery alone carries stimulation-frequency information even though the total 12-condition architecture is multicoordinate. The commonality is therefore relational organization, not common mechanism, common numerical coordinates, or a universal scalar.

## Canonical Stentor identities

Branch: `bio-chi-stentor-cross-system-p0q-20260926`  
Run: `36285086980`  
Workflow head: `56533470bca936e370758a3f12e9890a3eca4769`  
Artifact: `10920058447`  
Artifact digest: `sha256:d10818d9549deb2f9df2e9dadd296861f5c5cd1714e0513669631e82fe5e2931`  
Result JSON SHA-256: `246f129ddc8e8623bc99115311425fc8c3f38aba72fef8b3aa0a35a6cce2adb9`

Earlier Stentor workflow runs are noncanonical and are documented in `BIO_CHI/control/STENTOR2026_EXECUTION_LINEAGE_AUDIT_20260926.md`.

## What happens next and why

The next high-value experiment should move to a third direct biological system, preferably one with a source-native dynamical model or modal carrier. This tests whether the relational architecture continues to transport while giving scalar `chi_bio` a fair opportunity to be independently licensed rather than invented from summary coordinates.

## What the user needs to do

Nothing at this checkpoint. Public science is pinned in GitHub; editable manuscript and Supplementary Information remain private.
