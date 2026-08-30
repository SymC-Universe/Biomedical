# Stage C0 DNA-methylation source audit

Date: 2026-08-30

Status: **PASS SOURCE GATE; C1 BIOLOGICAL ANALYSIS BLOCKED PENDING PRE-ASSOCIATION SAMPLE-IDENTITY AND ANNOTATION FREEZE**

## Frozen contract audited

- `config/stage_c0_methylation_source_plan.json`
- `docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md`

Stage C0 was explicitly limited to source identity, integrity, schema, probe inventory, and sample coverage. It did not admit methylation-RNA, methylation-protein, methylation-genomic, clinical, treatment, dynamical, historical-GRI, or preferred-SymC association testing.

## Source identity and integrity

The locally acquired source matches the frozen source exactly:

- file: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`
- expected / remote content length: `5,022,150,019` bytes
- expected / observed MD5: `5cec086f0b002d17befef76a3241e73b`
- observed SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`

The GDC HEAD request returned HTTP 400, but the preregistered fallback one-byte range request succeeded with HTTP 206 and `Content-Range: 0-0/5022150019`. This is a transport detail, not a source failure, because the exact expected size was independently recovered and the complete local file subsequently matched the frozen MD5.

The Stage A cache also matches the frozen input:

- observed / expected SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`

## Probe inventory

The matrix contains exactly the frozen publication-era shared-probe inventory:

- probe rows: `22,601`
- blank probe IDs: `0`
- duplicate probe IDs: `0`

This passes the source-gate feature-integrity rules.

## Sample schema

Header inventory:

- methylation sample columns: `12,039`
- TCGA sample roots parsed: `12,039 / 12,039`
- primary-tumor sample columns: `10,317`
- unique primary sample roots: `10,271`
- unique primary patients: `10,268`
- primary sample roots represented by more than one source column: `41`

The 41 duplicated primary sample roots are a source-schema fact discovered at C0. They do **not** invalidate source identity or probe integrity, but they prevent immediate C1 association because the frozen matching key is the TCGA sample root through vial and a one-to-many root is not an unambiguous primary mapping.

No methylation beta values were inspected to decide how to handle these roots.

## Stage A coverage

- frozen Stage A tumors: `9,546`
- matched by the C0 presence/fallback inventory: `9,494`
- coverage: `99.4553%`
- exact sample-root presence matches: `9,493`
- unique-patient fallback matches: `1`
- cancers evaluated: `32`
- cancers passing frozen `n >= 30`: `32 / 32`

Only seven cancers have unmatched Stage A cases in the source-presence inventory:

| Cancer | Stage A n | Matched n | Unmatched |
| --- | ---: | ---: | ---: |
| GBM | 154 | 126 | 28 |
| BRCA | 1083 | 1067 | 16 |
| COAD | 441 | 439 | 2 |
| LUAD | 510 | 508 | 2 |
| READ | 156 | 154 | 2 |
| KIRC | 515 | 514 | 1 |
| LUSC | 486 | 485 | 1 |

All other cancers have complete Stage A presence coverage, and the smallest matched cancer remains CHOL at `n=36`, above the frozen `n=30` threshold.

## Epistemic decision

C0 passes its intended source gate. It establishes that the exact frozen PanCanAtlas merged methylation matrix is locally available, cryptographically identified, structurally parseable, contains the expected 22,601 unique probes, and has sufficient primary-tumor coverage in all 32 cancers.

C0 does **not** authorize biological association yet because the schema inventory exposed 41 duplicated primary sample roots. Under the preregistered `stop_on_unexpected_schema` rule, the program stops before C1 and freezes a separate sample-identity resolution contract.

The pre-C1 primary rule is deliberately conservative: a Stage A sample-root match is admitted only when exactly one eligible primary methylation source column maps to that root. Duplicate-root samples are excluded from the primary C1 sample set; they are not averaged, selected by order, selected by platform, or selected by their methylation values. The pre-existing patient-level fallback remains allowed only when exactly one eligible primary source measurement exists for that patient.

This resolution is frozen in `config/stage_c0_1_sample_identity_plan.json` and `docs/STAGE_C0_1_SAMPLE_IDENTITY_PREREGISTRATION_20260830.md` before any methylation biological association is calculated.

## Claim ceiling

C0 supports only source identity, integrity, schema, probe inventory, and sample coverage.

It does not establish:

- regulatory causality;
- methylation-RNA or methylation-protein coupling;
- substrate inheritance;
- temporal ordering;
- damping, recovery, criticality, or a phase/state transition;
- treatment response or clinical utility;
- an optimum;
- a master stability score;
- biological chi.

## Canonical compact outputs

- `development_outputs/stage_c0_methylation/STAGE_C0_METHYLATION_SOURCE_SUMMARY.json`
  - SHA-256 `b89e5987e50ddec4ec432a511eeb80052c1ce607dafae8c743eae204354c6bcd`
- `development_outputs/stage_c0_methylation/stage_c0_methylation_cancer_coverage.csv`
  - SHA-256 `5af5209b46a31115aaed3c6681cd442a921d3eb17981843080441cc0a8fe649c`

The approximately 5.02 GB source remains local and is identified by MD5 and SHA-256 rather than committed to GitHub.
