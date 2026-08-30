# Reviewer entry point: GRI v2 / Cancer Stability Atlas

**Repository state:** active development, not a validated clinical tool  
**Active branch:** `gri-v2`  
**Current scientific gate:** Stage C0 DNA-methylation source acquisition/audit; Stage B2 static computation and integration are closed

This directory is the reviewer-facing navigation layer. It points to the exact preregistrations, code, tests, outputs, audits, and provenance records supporting each stage.

## Read this first

The historical GRI scalar construction is provenance, not the target model. In the active program:

- `CV/2` is a historical descriptive comparator, not chi;
- no valid biological chi coordinate has been admitted;
- static RNA, genomic, protein, composition, and methylation measurements remain separate coordinates unless later model competition justifies reduction;
- no value of `chi = 1` is presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum;
- null and failed branches are retained;
- modal structure, scalar summaries, and conglomeration/system organization are complementary views, not interchangeable replacements.

Canonical guardrails:

- `../docs/EPISTEMIC_CONSTITUTION.md`
- `../docs/CHI_ADMISSION_RULES.md`
- `../docs/TOOL_OBJECTIVE.md`

Canonical live handoff:

- `../notes/BUILD_STATUS.md`

## Evidence ladder

| Stage | Status | What it establishes | Primary reviewer record |
| --- | --- | --- | --- |
| Historical scalar closure | Closed, not promoted | Historical `CV/2` branch is reconstructable but not biological chi | milestone registry and active-program summary |
| Stage A1 | Closed development layer | Static Hallmark RNA network map | `../docs/STAGE_A1_AUDIT_20260829.md` |
| Stage A1.1 | Closed calibration | Fixed-`n=30`, 100-resample construction calibration | `../docs/STAGE_A1_1_AUDIT_20260829.md` |
| Stage B1 | Closed | Independent purity/leukocyte context decomposition | `../docs/STAGE_B1_AUDIT_20260829.md` |
| Stage B2 source audit | Closed | Pre-association source coverage and provenance | `../docs/STAGE_B2_SOURCE_AUDIT_20260829.md` |
| Stage B2 preregistration | Frozen historical contract | Genomic/protein coordinate rules, nulls, and integration rules | `../docs/STAGE_B2_PREREGISTRATION_20260829.md` |
| Stage B2 RPPA | Closed | Orthogonal static RNA/protein coupling above block-permutation floor | `../docs/STAGE_B2_RPPA_AUDIT_20260829.md` |
| Stage B2 genomic | Closed | Small distributed genomic decomposition effects with strong Hallmark-topology preservation | `../docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` |
| Stage B2 static integration | Closed | Layered RNA/composition/genomic/protein static architecture, no master score | `../docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md` |
| Stage C0 methylation source gate | **Frozen; local source audit next** | Exact source identity, platform representation, matching rules, and allowed source/schema operations are fixed before methylation association | `../docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md` |
| Stage C1 methylation biology | Not started | Annotation/feature reduction and modal + scalar + conglomeration association design must be frozen after C0 and before association | prospective |
| Ordered/temporal substrate test | Not started | Required before any substrate-inheritance promotion | prospective |
| Dynamic biological chi | Not admitted | Requires genuine same-coordinate dynamic rates and separate admission tests | `../docs/CHI_ADMISSION_RULES.md` |

## Stage C0 reviewer route

C0 is deliberately separated from biological interpretation. Review these in order:

1. `../config/stage_c0_methylation_source_plan.json`
2. `../docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md`
3. `../src/probe_stage_c0_methylation.py`
4. `../tests/test_stage_c0_methylation_contract.py`
5. GitHub Actions run `33292691811`

The pre-acquisition run passed the full GRI v2 suite, confirmed the frozen GDC endpoint reports exactly `5,022,150,019` bytes, and performed no biological association.

Tested Windows handoff:

- `CSA_STAGE_C0_METHYLATION_WINDOWS_20260830.zip`
- SHA-256 `69dcaa00e96c9668c97b1b20047d121db3f61533f6e6f5bb55e41f22a11916eb`

A successful C0 local run may establish only source identity, hashes, schema, 22,601-probe inventory, TCGA sample identity, and primary-tumor coverage. It cannot establish methylation-RNA coupling, a regulatory mechanism, substrate inheritance, dynamics, criticality, an optimum, treatment response, or biological chi.

## Three general reviewer routes

### 1. Scientific logic

Read:

1. `../README.md`
2. `../docs/TOOL_OBJECTIVE.md`
3. `../docs/EPISTEMIC_CONSTITUTION.md`
4. `CLAIM_EVIDENCE_MAP.md`

### 2. Result audit

For a cited stage:

1. read its dated audit/preregistration under `../docs/`;
2. inspect the frozen plan under `../config/`;
3. inspect compact committed results under `../development_outputs/` when results exist;
4. verify larger artifacts/hashes under `../artifacts/`;
5. inspect the implementation under `../src/` and contract/regression tests under `../tests/`.

### 3. Reproduction / forensic review

Start with:

- `../requirements.txt`
- `../WORKFLOW.md`
- `../src/`
- `../tests/`
- `../artifacts/MILESTONE_ARTIFACTS.md`
- `REVIEWER_MANIFEST.json`

Large datasets are intentionally not duplicated into Git history. Their identities, roles, sizes, and cryptographic hashes are recorded. The 306 B2 task-cache gzip files remain local forensic/restart artifacts and are individually hash-registered in the task-status ledger.

## Repository layout

| Location | Reviewer meaning |
| --- | --- |
| `../docs/` | dated audits, preregistrations, objectives, epistemic rules |
| `../config/` | frozen/preregistered analysis contracts |
| `../src/` | implementations |
| `../tests/` | contract/regression tests |
| `../development_outputs/` | compact committed results |
| `../artifacts/` | hashes/provenance for larger milestones |
| `../inputs/` | compact source identity/provenance records |
| `../notes/BUILD_STATUS.md` | canonical current handoff |
| `../WORKFLOW.md` | repository/data-management rules |

## Submission snapshots

A paper or data submission will not ask reviewers to rely on the moving `gri-v2` branch. The evidentiary state will be frozen to an immutable tag/release with:

- exact commit and tag;
- included/excluded scientific stages;
- claim-to-evidence map;
- figure/table source map;
- result/artifact hashes;
- test/CI record;
- source-data provenance;
- explicit null, failed, deferred, and non-claim ledger.

See `SUBMISSION_RELEASE_CHECKLIST.md`.
