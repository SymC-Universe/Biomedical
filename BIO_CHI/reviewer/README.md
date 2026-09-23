# Bio Chi reviewer entry point

This directory is the reviewer-facing navigation layer for the Bio Chi investigation.

## What this repository is designed to let a reviewer do

A reviewer should be able to answer, from GitHub alone whenever redistribution permits:

- What was asked?
- What was frozen before outcomes were opened?
- Which source files/datasets were used?
- How were source identities verified?
- What code produced each result?
- Which nulls and comparators were used?
- What failed or refused classification?
- Which claims are supported and which are not?
- How can the result be rerun?
- Which exact commit/workflow/artifact generated a reported value?

## Current evidence level

**P0-D exploratory / function + limit mapping.**

No biological scalar χ_bio is admitted. No universal Bio Chi law is established. No causal Stability Inheritance claim is established.

## Navigation

- `../README.md` — scientific status and project map.
- `../control/AUTORUN_CHECKPOINT.md` — durable execution state.
- `../control/WORK_QUEUE.json` — machine-readable queue.
- `../artifacts/DATASET_ELIGIBILITY_MATRIX_v0_1.md` — testbed selection evidence.
- `../config/P0D_TESTBED_REGISTRY_v0_1.json` — machine-readable testbed registry.
- `../../GRI_v2/docs/CHI_BIO_NOMENCLATURE_AND_JOINT_TARGET_20260922.md` — naming/representation contract.
- `../../GRI_v2/docs/CHI_BIO_P0D_INVESTIGATION_CHARTER_20260922.md` — scientific charter.

## Manuscript privacy

Working manuscript text is intentionally not public during active investigation. The public repository contains the complete scientific/reproducibility spine rather than an unpublished narrative draft. A submission/release snapshot will be exported only when authorized.

Private working-manuscript location:
`/Atlas - Chi Bio/Private Working Manuscripts`

## Reviewer reproducibility policy

Every promoted result will receive a compact provenance record containing:
- source identifier + cryptographic hash where available;
- code/config commit;
- environment identity;
- workflow run ID;
- artifact ID/digest;
- endpoint and null definition;
- uncertainty/multiplicity rule;
- status: exploratory, qualification, confirmation, refusal, or failure;
- exact claim ceiling.

No favorable result may erase an unfavorable result from the same frozen program.
