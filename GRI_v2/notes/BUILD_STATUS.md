# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The Cancer Stability Atlas / substrate-architecture program remains a development program, not a validated clinical tool. `CV/2` remains historical only. No biological chi coordinate has been admitted, and `chi = 1` is not presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum.

Stages A, A1.1, B1, B2 RPPA, B2 genomic, and B2 static integration are closed. **Stage C0 DNA-methylation source acquisition/audit is now closed as a source-gate PASS. Stage C0.1 sample identity is the active gate.** No methylation biological association has been calculated.

## Stage C0 closure

Canonical audit: `docs/STAGE_C0_METHYLATION_AUDIT_20260830.md`.

The exact frozen PanCanAtlas merged HM27/HM450 source passed the preregistered identity/integrity gates:

- GDC UUID `d82e2c44-89eb-43d9-b6d3-712732bf6a53`;
- exact size `5,022,150,019` bytes;
- exact MD5 `5cec086f0b002d17befef76a3241e73b`;
- local source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- exactly `22,601` probe rows;
- `0` blank probe IDs;
- `0` duplicate probe IDs;
- all `12,039 / 12,039` methylation sample columns have parseable TCGA sample roots;
- frozen Stage A cache SHA-256 matched exactly.

Stage A source-presence coverage is `9,494 / 9,546` tumors (`99.4553%`), and all `32 / 32` cancers pass the existing `n >= 30` gate.

Canonical compact outputs:

- `development_outputs/stage_c0_methylation/STAGE_C0_METHYLATION_SOURCE_SUMMARY.json`
  - SHA-256 `b89e5987e50ddec4ec432a511eeb80052c1ce607dafae8c743eae204354c6bcd`
- `development_outputs/stage_c0_methylation/stage_c0_methylation_cancer_coverage.csv`
  - SHA-256 `5af5209b46a31115aaed3c6681cd442a921d3eb17981843080441cc0a8fe649c`

## Why C1 is not starting yet

The C0 header inventory found `41` primary TCGA sample roots represented by more than one methylation source column. This is a source-schema issue, not a biological result.

Because the frozen C0 contract included `stop_on_unexpected_schema`, the program does not silently average, choose, or deduplicate those columns after seeing the source. Instead Stage C0.1 prospectively freezes a one-to-one sample-identity rule before any methylation beta values are used scientifically.

## Active gate: Stage C0.1 sample identity

Frozen records:

- `config/stage_c0_1_sample_identity_plan.json`
- `docs/STAGE_C0_1_SAMPLE_IDENTITY_PREREGISTRATION_20260830.md`
- `src/run_stage_c0_1_sample_identity.py`
- `src/run_stage_c0_1_windows.py`
- `tests/test_stage_c0_1_sample_identity.py`
- `RUN_STAGE_C0_1_SAMPLE_IDENTITY_WINDOWS.bat`

Primary rule:

1. sample type `01` only;
2. exact Stage A sample root is admitted only if exactly one eligible methylation source column maps to that root;
3. duplicated exact roots are excluded from primary C1;
4. no beta averaging, first/last selection, platform preference, or value-based replicate selection;
5. patient fallback remains allowed only when exactly one eligible primary methylation measurement exists for that patient;
6. the existing `n >= 30` cancer gate is not relaxed.

C0.1 reads only the methylation header for this gate. It does not inspect beta-value rows for biological association.

## Verification

The C0/C0.1 repository state at commit `043caecfeb2d3756dabb29b9d0f5b6346b7fbe03` passed the full GRI v2 suite: `36/36` tests.

The exact C0.1 Windows handoff was then built by GitHub Actions run `33314518877` from commit `35ca555d073142b7accd705b0fdc67051dd251a7` and passed the same full test suite before packaging.

Handoff:

- `CSA_STAGE_C0_1_SAMPLE_IDENTITY_WINDOWS_20260830.zip`
- SHA-256 `9d08b94c4452295522a851501acf7fd341f09b4fd79faca7f180f968f1bce423`

## What follows C0.1

If all intended cancers remain above `n=30`, the next operation is to freeze the methylation annotation and feature-reduction protocol before any cross-assay association. That protocol must specify the exact annotation source/genome build, probe-to-gene/regulatory mapping, transcript and multi-mapping rules, promoter/regulatory-region definitions, unmapped-probe handling, modal representation, any licensed scalar compression, conglomeration/system-level representation, and construction nulls.

The required reporting architecture remains:

- **modal**: mode-resolved/eigenspectrum and participation structure;
- **scalar**: compressed coordinates only where empirically licensed;
- **conglomeration**: module-to-module and whole-system organization across independently measured layers.

The scalar view may not replace the modal or conglomeration views. None of these static methylation quantities is biological chi. Substrate inheritance still requires ordered or temporal evidence.

## Exact user action

1. Download and extract `CSA_STAGE_C0_1_SAMPLE_IDENTITY_WINDOWS_20260830.zip`.
2. Double-click `RUN_STAGE_C0_1_SAMPLE_IDENTITY_WINDOWS.bat`.
3. The Python file pickers will ask for:
   - the completed Stage A `hallmark_profile_cache.npz`;
   - the already-audited 5.02 GB methylation TSV from the completed C0 run;
   - `STAGE_C0_METHYLATION_SOURCE_SUMMARY.json` from C0.
4. At completion, return:
   - `STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json`;
   - `stage_c0_1_unique_match_coverage.csv`;
   - `stage_c0_1_duplicate_primary_roots.csv`.

Keep the 5.02 GB methylation source and the B2 task cache local and unchanged.
