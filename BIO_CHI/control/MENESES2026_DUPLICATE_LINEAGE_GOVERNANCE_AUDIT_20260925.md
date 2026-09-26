# Meneses duplicate-lineage governance audit

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Authority:** SymC GOM v0.8.6  
**Classification:** GOVERNANCE / EVIDENCE-CLASS CORRECTION

## Finding

The resume-visible continuation created a second freeze at commits `393344f` and `a938bfb` after a prior Meneses direct-experimental lineage had already completed on this same branch.

The earlier canonical chronology is:

- prospective freeze: `3636681325f9337cb7472f05296f4a3dccb5e400`;
- preserved implementation false-negative audit: `ec6e5ad44808119d85de120a408502f62db738a6`;
- repaired primary result pin: `46bde9a7360acf3b32392d0f8142d2438a3e07bc`;
- source-method reconciliation result pin: `9b14bbed4b2c35a7cf009e3239a1594fdc7c153b`;
- scientific closeout: `3f6859319cba00c6e9bfe89a1eb8ca95ea566f09`.

Therefore the later files
`ECOLI2026_PMF_RECOVERY_P0Q_FREEZE_v0_1.md` and
`ECOLI2026_PMF_RECOVERY_EXECUTION_CONTRACT_v0_1.md`
cannot be treated as prospective freezes even though they were written before their own execution. SymC-specific Meneses results already existed in repository history.

## Evidence consequence

Any execution descending from the later duplicate freeze is reclassified as:

`POST_RESULT_ROBUSTNESS_REANALYSIS`

It may test robustness, implementation differences, or alternate representation criteria. It cannot add an independent P0-Q confirmation count and cannot supersede the earlier canonical Meneses result merely because it is newer.

## Canonical Meneses conclusion retained

The prior closed lineage remains the primary record:

- biological chi: `DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q`;
- `Chi_bio`: `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q`, source-method robust;
- `chi_bio`: `NOT_OPENED_NOT_LICENSED`;
- stronger rate-depth dissociation rule: failed and preserved.

## Root cause

The duplicated freeze arose from conversation/UI timeout continuity: the repository had advanced further than the visible conversational checkpoint. This is an operations synchronization failure, not a scientific contradiction.

## Repair

1. retain all duplicate commits and workflow outputs as provenance;
2. do not delete or rewrite their timestamps;
3. reclassify their evidence level explicitly;
4. use the earlier closeout as the Meneses primary scientific record;
5. proceed to a genuinely new perturbation-path transport question rather than repeating the dose-response compression attack.
