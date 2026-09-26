# BioSystems Reproducibility Guide V29

**Manuscript ID:** BIOSYS-D-26-00267  
**Date:** 25 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Reviewer branch:** `biosystems-v29-direct-pmf-recovery-20260925`  
**Immediate parent:** `biosystems-v28-biochi-continuation-20260925` @ `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`  
**Original oncology reviewer route:** `biosystems-v27-repro-guide-20260925` @ `ae9d0499e44e211e00c04da208a7bc50e2948893`

## Status

The original C1/P1 oncology evidence spine is unchanged. V29 adds the first direct experimental biological chi recovery qualification after the V28 source-transport and HOG model continuation. The new source is Meneses et al. (2026), `E. coli` hyperosmotic shock with source-released flagellar-motor, TMRM, and cell-area time series.

The editable manuscript and Supplementary Information remain private. Reviewers can audit the new scientific record from the public branches and pins below without reconstructing the historical repository.

## V1. Ancestry

**[CLAIM]** V29 is a continuation layer above V28 and does not rewrite the original oncology evidence.

**Command**

```bash
git fetch origin \
  biosystems-v29-direct-pmf-recovery-20260925 \
  biosystems-v28-biochi-continuation-20260925 \
  biosystems-v27-repro-guide-20260925

git merge-base --is-ancestor \
  58eb8b4777fae0fb79ab50d38b738dfee556b2a3 \
  origin/biosystems-v29-direct-pmf-recovery-20260925

echo $?
```

**Expected output:** `0`.

For the complete C1/P1, Kizilirmak, top-down biological chi, E. coli source-refusal, and HOG chronology, read the V28 guide:

```text
GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925_V28.md
branch: biosystems-v28-biochi-continuation-20260925
```

## V2. Direct experimental E. coli PMF qualification

**[CLAIM]** The Meneses 2026 source reproduces a directly measured osmotic-shock collapse/recovery event at P0-Q. The whole event is admitted, the minimum supported lower representation is multicoordinate, and scalar `chi_bio` remains unlicensed.

**Fixed identity**

- scientific branch: `bio-chi-ecoli-pmf-recovery-p0q-20260925`
- upstream source: `wadhwalab/2026-Meneses-Osmotic`
- upstream commit: `d14d0caaa07299f13d1b1121d1e4630454fd724b`
- publication DOI: `10.1016/j.bpj.2026.04.014`
- freeze: `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FREEZE.json`
- repaired result pin: `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md`
- repaired workflow run: `36216252676`
- artifact: `10897836350`
- artifact SHA-256: `33e2c253ffb19abe1d3679116df768e08012cc6181cd910a38c3976b4bf77c3f`
- result JSON SHA-256: `e32dcd753fdefb22ed7f20fe3f90d5486969b0139cb72dbeadde00eec35d26f0`

**Command**

```bash
git fetch origin bio-chi-ecoli-pmf-recovery-p0q-20260925

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md
```

**Expected scientific output**

```text
status = EXECUTED_VALID_P0Q
Bio_Chi = DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q

A_dec Spearman rho = 1.0
adaptation plateau Spearman rho = -1.0

rate-depth disposition = FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q

PC1 variance fraction = 0.6620977810898341
maximum standardized 1D residual = 1.1144697154328063
Chi_bio = MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q

chi_bio = NOT_OPENED_NOT_LICENSED
```

The stronger amplitude-versus-rate hypothesis failed. That failure is part of the result, not a defect to be optimized away.

## V3. Source reproduction and preserved implementation failure

**[CLAIM]** The source-reproduction gate passes under the rules frozen before result inspection. The first completed executable artifact nevertheless returned a false-negative whole-event disposition because implementation code added an unfrozen finite-normalized-track-count veto.

**Fixed identity**

- implementation audit: `BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md`
- false-negative run: `36216125834`
- false-negative artifact: `10898060524`
- false-negative artifact SHA-256: `0e6d640aae38c5e2d906b4dbce7a887e89628d9d97176fb6df5cc8141683ea09`

**Command**

```bash
git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md
```

**Expected audit result**

- immediate bead trace counts reproduce exactly: `8, 10, 8, 12`;
- sustained bead trace counts reproduce exactly: `8, 8, 8, 4`;
- all frozen TMRM and cell-area population summaries reproduce within tolerance;
- raw orthogonal-assay source-track counts are 40 per condition;
- finite-normalized TMRM contributing-track counts are `39, 40, 39, 39, 38` from control through 500 mM;
- the finite-normalized count was never a frozen admission criterion and is retained only as a diagnostic.

The erroneous run remains in the record. It was not deleted or relabeled as scientific evidence.

## V4. Source-method reconciliation

**[CLAIM]** The multicoordinate recovery conclusion is robust to the authors' manuscript-facing sucrose fitting method.

The primary frozen execution used the general four-parameter immediate fit lane present in the source repository. A source audit then identified the manuscript-facing `sucrose_shock_analysis.ipynb` lane, which fixes collapse amplitude from pre/post windows and constrains collapse `tau > 0`. A post-result reconciliation was frozen before that sensitivity output was extracted.

**Fixed identity**

- reconciliation freeze: `BIO_CHI/control/MENESES2026_SOURCE_METHOD_RECONCILIATION_FREEZE_20260925.md`
- engine: `BIO_CHI/experiments/meneses2026_source_method_reconciliation_v01.py`
- result pin: `BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`
- run: `36216368561`
- artifact: `10897991063`
- artifact SHA-256: `0534f1173b51a4d4fc4459bdb28a800a7759968f96119434d5f7ea35c1308dc9`
- result JSON SHA-256: `b96def0062b759727533748abb04d070cd79fef547db69fb9376c6a8e4e4346d`

**Command**

```bash
git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json
```

**Expected output**

```text
rate-depth disposition =
  FROZEN_RATE_DEPTH_RULE_NOT_MET_POSTRESULT_RECONCILIATION

PC1 variance fraction = 0.7719879506509367
maximum standardized 1D residual = 1.2036796471330158

Chi_bio =
  MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_POSTRESULT

comparison =
  SOURCE_METHOD_ROBUST_AT_P0Q

chi_bio =
  NOT_OPENED_NOT_LICENSED
```

The reconciliation is post-result and cannot promote the primary P0-Q evidence. It demonstrates source-method robustness of the representation conclusion only.

## V5. What the direct experiment changes

The Meneses result supplies the direct experimental layer that the preceding HOG qualification lacked. It does **not** produce a privileged numerical `chi_bio`.

The current hierarchy is:

- **biological chi / biological chi:** admitted for this source as the directly measured relation among osmotic perturbation, energetic/physical reorganization, and realized recovery;
- **`Chi_bio`:** multicoordinate recovery architecture required under both source-fit lanes;
- **`chi_bio`:** not opened because the source time constants are empirical response summaries rather than independently licensed mechanistic modal carriers.

The frozen rate-depth simplification also fails. Collapse depth and sustained plateau are strongly dose ordered, but the rate coordinates do not jointly satisfy the frozen stability rule. The result therefore adds friction to an amplitude-only interpretation instead of rescuing one.

## V6. V29 master smoke test

```bash
set -e

git fetch origin \
  biosystems-v29-direct-pmf-recovery-20260925 \
  biosystems-v28-biochi-continuation-20260925 \
  bio-chi-ecoli-pmf-recovery-p0q-20260925

git merge-base --is-ancestor \
  58eb8b4777fae0fb79ab50d38b738dfee556b2a3 \
  origin/biosystems-v29-direct-pmf-recovery-20260925

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json \
  | grep -q DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json \
  | grep -q MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json \
  | grep -q FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md \
  | grep -q FALSE-NEGATIVE

git show \
  origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:\
BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json \
  | grep -q SOURCE_METHOD_ROBUST_AT_P0Q

echo V29_SMOKE_TEST_PASS
```

**Expected output**

```text
V29_SMOKE_TEST_PASS
```

## What happens next

The next biological chi experiment should test whether this **multicoordinate recovery architecture transports** across a different perturbation path or a different directly measured biological system. Another scalar-first exercise is now low information because this experiment already demonstrates a directly reproducible whole-system relation while refusing one-dimensional compression and an unlicensed scalar.

## What the user needs to do

Nothing is required at this checkpoint. The scientific records are pinned publicly; the manuscript and Supplementary Information remain private authoring artifacts.
