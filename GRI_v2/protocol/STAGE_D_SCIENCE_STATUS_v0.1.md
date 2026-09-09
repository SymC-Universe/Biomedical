# GRI Stage D Science Status v0.1

Date: 2026-09-08
Branch: `gri-stage-d-perturbation-recovery`

## Current project status

Stage D has been prospectively opened but no Stage-D biological outcome has been interpreted.

Frozen:
- purpose and claim ceiling;
- D1-D4 dataset roles;
- substrate-inheritance evidence ladder translation;
- scalar/modal/conglomeration separation;
- relationship R and uncertainty U requirement;
- recovery/persistence primary endpoint family;
- CKA analytic floor and spectral ceiling definitions;
- no-master-score rule;
- no-stage-as-pseudotime rule;
- nonlinear-detector requirement before biological outcome interpretation;
- execution order and compute-backend roles.

Not yet frozen because metadata/design must be inspected first:
- exact assay files within each GEO accession;
- final sample/condition mapping;
- exact feature universes/annotations;
- exact scaling and imputation;
- exact D1/D2 matched controls;
- D2 trajectory model support rules;
- nonlinear kernel/bandwidth implementation;
- empirical-null replicate counts for every new test;
- multiplicity families;
- capacity-matched comparator replicates;
- context-depth mappings.

## Immediate next computational step

Run metadata-only D0 inventory and return its artifact. No numeric methylation, RNA, or contact matrix should be opened before the D0.3 analysis freeze.

## What can advance without user input

- GitHub protocol/config/test/workflow hardening;
- metadata-only preflight CI;
- exact provenance templates;
- design-audit code that does not inspect biological outcome matrices;
- mechanical fixes to any failing preflight.

## Exact next user action

If GitHub metadata preflight succeeds, no user action is needed until its artifact is reviewed.
If GitHub cannot complete the live NCBI inventory, run the three-cell Kaggle Phase-A metadata procedure in `GRI_v2/kaggle/STAGE_D_KAGGLE_RUNBOOK.md` and return `STAGE_D_D0_METADATA_RETURN.zip`.

## Success condition for current gate

D0 metadata gate closes only when every frozen accession has:
- authoritative metadata retrieved;
- sample counts recorded;
- raw sample metadata exported;
- supplementary filenames/URLs inventoried;
- ambiguities explicitly marked rather than guessed;
- an audit confirming that no numeric biological matrix was opened.
