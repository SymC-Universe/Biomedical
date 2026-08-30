# Stage C0.1 sample-identity preregistration

Date: 2026-08-30

Status: **FROZEN AFTER C0 SOURCE/SCHEMA AUDIT AND BEFORE ANY METHYLATION BIOLOGICAL ASSOCIATION**

## Why this sub-stage exists

Stage C0 successfully established the exact frozen PanCanAtlas methylation source and its probe/sample schema, but the header inventory revealed 41 primary TCGA sample roots represented by more than one source column.

The frozen C0 matching key is the TCGA sample root through vial. A one-to-many source mapping at that key is not an unambiguous biological sample identity. Because the C0 plan included `stop_on_unexpected_schema`, the program stops here before Stage C1 and resolves the ambiguity using schema information only.

No methylation beta values, RNA relationships, RPPA relationships, genomic relationships, outcomes, treatment labels, historical GRI quantities, or SymC-preferred patterns are used to define this rule.

Machine-readable contract: `config/stage_c0_1_sample_identity_plan.json`.

## Frozen primary rule

For the primary Stage C1 sample set:

1. retain sample type `01` primary tumors only;
2. parse the TCGA sample root through vial, e.g. `TCGA-XX-YYYY-01A`;
3. admit an exact-root match only when **exactly one** eligible methylation source column maps to that root;
4. if more than one source column maps to the same root, exclude that Stage A sample from the primary Stage C1 set;
5. do not average duplicate-root beta values;
6. do not choose the first, last, lexicographically first, or platform-preferred duplicate;
7. do not select a duplicate using methylation values or agreement with another assay;
8. retain the previously frozen patient-level fallback only when no unique exact-root match exists and the source contains exactly one eligible primary measurement for that patient;
9. do not substitute metastatic, recurrent, or normal samples to recover coverage;
10. retain the existing `n >= 30` per-cancer eligibility gate.

This is intentionally conservative. The cost is at most a small number of primary samples; the benefit is a one-to-one primary sample map with no post-result replicate manipulation.

## Frozen inputs

- Stage A profile cache SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`
- methylation source SHA-256 established at C0: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- methylation source MD5: `5cec086f0b002d17befef76a3241e73b`
- source size: `5,022,150,019` bytes
- C0 summary SHA-256: `b89e5987e50ddec4ec432a511eeb80052c1ce607dafae8c743eae204354c6bcd`

## Allowed operations

C0.1 may read only the methylation matrix header and the Stage A sample identity arrays. It may:

- count full source columns per TCGA sample root;
- list duplicated primary roots and their source labels;
- calculate the Stage A one-to-one coverage remaining after the frozen duplicate-root exclusion;
- report patient-level fallback counts under the unchanged uniqueness rule;
- report per-cancer coverage and `n >= 30` eligibility.

C0.1 may not read methylation beta-value rows for biological analysis and may not calculate any cross-assay or outcome association.

## Required outputs

- `STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json`
- `stage_c0_1_unique_match_coverage.csv`
- `stage_c0_1_duplicate_primary_roots.csv`

## Decision gate

C0.1 passes if:

- the selected Stage A cache matches its frozen SHA-256;
- the selected methylation source has the C0-locked filename/size and the accompanying C0 summary records the exact locked MD5/SHA-256;
- the source header reproduces the C0 schema counts;
- duplicate roots are excluded exactly as frozen;
- every cancer intended for the primary C1 analysis still satisfies `n >= 30` after unique one-to-one matching.

If a cancer falls below `n=30`, it is excluded from the primary C1 cancer set. The threshold is not relaxed.

## What follows C0.1

Only after this sample-identity gate is closed may the project freeze the methylation annotation and feature-reduction protocol. That later freeze must specify the annotation source, genome build, probe-to-gene/regulatory mapping, transcript/multi-mapping rules, promoter/regulatory-region definitions, unmapped-probe handling, modal representation, scalar compression rules, conglomeration-level representation, and construction nulls before any methylation association result is calculated.

## Claim ceiling

C0.1 establishes sample identity and coverage only. It does not establish methylation biology, regulatory causality, substrate inheritance, dynamics, an optimum, a master score, or biological chi.
