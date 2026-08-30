# Reviewer entry point: GRI v2 / Cancer Stability Atlas

**Repository state:** active development, not a validated clinical tool  
**Active branch:** `gri-v2`  
**Current computational gate:** Stage B2 genomic decomposition, 306 frozen tasks; partial results are not interpreted

This directory is the reviewer-facing navigation layer for the GRI v2 / Cancer Stability Atlas program. It does not replace the scientific source files. It points to the exact configs, code, audits, outputs, and provenance records that support each stage.

## Read this first

The historical GRI scalar construction is retained as provenance, not as the target model. In the active program:

- `CV/2` is a historical descriptive comparator, not chi;
- no valid biological chi coordinate has been admitted;
- static RNA, genomic, protein, composition, and future methylation measurements remain separate coordinates unless later model competition justifies a reduction;
- no value of `chi = 1` is presumed to be a cancer optimum, healthy state, therapeutic target, or maximum-organization point;
- null and failed branches are retained rather than rewritten as support.

Canonical scientific guardrails:

- `../docs/EPISTEMIC_CONSTITUTION.md`
- `../docs/CHI_ADMISSION_RULES.md`
- `../docs/TOOL_OBJECTIVE.md`

Canonical live status:

- `../notes/BUILD_STATUS.md`

## Current evidence ladder

| Stage | Status | What it establishes | Primary reviewer record |
| --- | --- | --- | --- |
| Historical scalar closure | Closed, descriptive only | Reconstructs and audits the historical `CV/2` branch; it is not promoted as chi | milestone registry and archived audit provenance |
| Stage A1 | Closed development layer | Static Hallmark RNA network measurement map | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Stage A1.1 | Closed calibration | Fixed-`n=30`, 100-resample construction calibration for finite-sample effects | `../docs/STAGE_A1_1_AUDIT_20260829.md` |
| Stage B1 | Closed | Independent purity/leukocyte context decomposition | `../docs/STAGE_B1_AUDIT_20260829.md` |
| Stage B2 source audit | Closed | Pre-association source coverage and provenance | `../docs/STAGE_B2_SOURCE_AUDIT_20260829.md` |
| Stage B2 preregistration | Frozen before target association results | Genomic/protein coordinate rules, nulls, and integration rules | `../docs/STAGE_B2_PREREGISTRATION_20260829.md` |
| Stage B2 RPPA | Closed | Orthogonal static RNA/protein coupling layer under a block-permutation construction null | `../docs/STAGE_B2_RPPA_AUDIT_20260829.md` |
| Stage B2 genomic | In progress | Five genomic coordinates tested against the frozen RNA map, including incremental information beyond B1 context | `../config/stage_b2_integration_plan.json` plus current code/tests; final audit pending |
| Genome-wide methylation extension | Deferred behind independent gate | No result claim yet | current status in `../README.md` and `../notes/BUILD_STATUS.md` |
| Dynamic biological chi | Not admitted | Requires genuine same-coordinate dynamic rates and admission tests | `../docs/CHI_ADMISSION_RULES.md` |

## Three reviewer routes

### 1. Scientific logic, approximately 10 minutes

Read in this order:

1. `../README.md`
2. `../docs/TOOL_OBJECTIVE.md`
3. `../docs/EPISTEMIC_CONSTITUTION.md`
4. `CLAIM_EVIDENCE_MAP.md`

This route answers what is being claimed, what is explicitly not being claimed, and which stages are closed versus pending.

### 2. Result audit, approximately 30 minutes

For any stage cited in a manuscript:

1. read its dated audit under `../docs/`;
2. inspect the corresponding frozen plan under `../config/`;
3. inspect compact committed results under `../development_outputs/`;
4. verify larger external artifacts and hashes in `../artifacts/MILESTONE_ARTIFACTS.md`;
5. inspect the stage implementation under `../src/` and its contract/regression tests under `../tests/`.

### 3. Reproduction / forensic review

Start with:

- `../requirements.txt`
- `../WORKFLOW.md`
- `../src/`
- `../tests/`
- `../artifacts/MILESTONE_ARTIFACTS.md`
- `REVIEWER_MANIFEST.json`

Large source datasets are intentionally not duplicated into Git history when that would be impractical. Their identity, role, and hashes are recorded in source/provenance files and the milestone registry.

## Repository layout

| Location | Reviewer meaning |
| --- | --- |
| `../docs/` | dated scientific audits, objectives, and epistemic rules |
| `../config/` | frozen or preregistered analysis contracts |
| `../src/` | analysis implementations |
| `../tests/` | contract and regression tests |
| `../development_outputs/` | compact committed result summaries |
| `../artifacts/` | hashes and provenance for larger milestone artifacts |
| `../inputs/` | compact source identity/provenance records, not giant raw data copies |
| `../notes/BUILD_STATUS.md` | canonical current handoff and next gate |
| `../WORKFLOW.md` | repository and data-management rules |

## Submission snapshots

A manuscript or data submission should never ask a reviewer to rely on the moving `gri-v2` branch alone. At submission time, the exact evidentiary state will be frozen to an immutable tag/release and accompanied by a submission-specific index containing:

- exact commit and tag;
- paper/data-release title and version;
- included and excluded scientific stages;
- claim-to-evidence map;
- figure/table source map;
- result and artifact SHA-256 hashes;
- test/CI record;
- source-data access and provenance notes;
- explicit null, failed, deferred, and non-claim ledger.

See `SUBMISSION_RELEASE_CHECKLIST.md`.

## Important status warning

The current Stage B2 genomic computation contains 306 frozen tasks. Until all 306 tasks and their expected resamples are complete and independently audited, no partial genomic pattern is a project result and no reviewer-facing claim should be built from an interim checkpoint.
