# Reproducing the Bio Chi investigation

This page is the reviewer-facing "how" entry point.

## 1. Clone and checkout

```bash
git clone https://github.com/SymC-Universe/Biomedical.git
cd Biomedical
git checkout chi-bio-recovery-p0d-20260922
```

For a published result, use the exact release tag/commit recorded beside that result rather than the moving branch.

## 2. Validate the governance and privacy contract

```bash
python BIO_CHI/src/validate_control.py
```

Expected output:

```text
BIO_CHI_CONTROL_PASS
```

This checks the canonical χ / χ_bio / Χ_bio / Bio Chi hierarchy, the durable queue, continuation rules, testbed IDs, required reviewer files, and the public working-manuscript firewall.

## 3. Verify source endpoints

```bash
python BIO_CHI/src/preflight_sources.py
```

The script:
- reads `BIO_CHI/config/SOURCE_MANIFEST_v0_1.json`;
- verifies declared public source endpoints;
- records content length/HTTP metadata when supplied;
- does **not** inspect biological target outcomes;
- writes `BIO_CHI/artifacts/generated/source_preflight_v0_1.json`.

GitHub Actions also executes this preflight and stores the JSON as artifact `BIO_CHI_SOURCE_PREFLIGHT_V01`.

## 4. Inspect testbed selection

Human-readable:
- `BIO_CHI/artifacts/DATASET_ELIGIBILITY_MATRIX_v0_1.md`
- `BIO_CHI/artifacts/SOURCE_QUALIFICATION_LEDGER_v0_1.md`
- `BIO_CHI/artifacts/LITERATURE_SEARCH_LEDGER_v0_1.md`

Machine-readable:
- `BIO_CHI/config/P0D_TESTBED_REGISTRY_v0_1.json`

Testbeds are selected by design quality, source accessibility, native biological validity, and falsifiability, not by whether their published result resembles SymC.

## 5. Manuscript

There is intentionally no working manuscript in the public repository.

The public GitHub repository is the reproducibility and evidence source of record. Working manuscript text remains private until an authorized submission/release snapshot is created.

## 6. Future promoted results

Every promoted result will add:
- frozen config/preregistration;
- exact source manifest and hashes;
- executable analysis code;
- tests/known-bad controls;
- environment lock;
- workflow run and artifact digest;
- compact machine-readable results;
- figure/table generator;
- claim/evidence and non-claim record.

A reviewer should therefore be able to move from a manuscript claim to the exact computation without asking the author to email scripts.
