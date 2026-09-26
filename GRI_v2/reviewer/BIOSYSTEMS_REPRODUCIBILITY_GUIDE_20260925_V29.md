# BioSystems Reproducibility Guide V29

**Manuscript ID:** BIOSYS-D-26-00267  
**Guide date:** 25 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Reviewer branch:** `biosystems-v29-biochi-meneses-20260925`  
**Original oncology scientific parent:** `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`  
**Prior reviewer navigation parent:** `biosystems-v28-biochi-continuation-20260925` @ `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`  
**Status:** REVIEWER ENTRY POINT / NO RETROACTIVE PROMOTION OF C1 OR P1

## Status

V29 adds navigation for the canonical Meneses 2026 direct-experimental biological chi qualification, the same-system perturbation-path transport test, the depth-conditioned follow-up, and a timeout-continuity governance correction. The TCGA C1/P1 inferential spine is unchanged. HOG remains a source-native model qualification; Meneses is a direct experimental P0-Q continuation outside oncology.

The editable manuscript and Supplementary Information remain private authoring artifacts. Public GitHub records contain the scientific freezes, source identities, code, workflow provenance, result pins, failures, implementation audits, and claim ceilings required to audit the statements added in V29.

## V1. V29 ancestry

**[CLAIM]** V29 is a navigation layer above the unchanged oncology evidence spine.

**Fixed input identity**

- branch: `biosystems-v29-biochi-meneses-20260925`
- V28 parent: `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`
- oncology scientific parent: `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

**Command**

```bash
git fetch origin biosystems-v29-biochi-meneses-20260925
git merge-base --is-ancestor 58eb8b4777fae0fb79ab50d38b738dfee556b2a3 origin/biosystems-v29-biochi-meneses-20260925
echo $?
```

**Expected output**

```text
0
```

## V2. Original oncology evidence remains frozen

**[CLAIM]** No Meneses, HOG, Kizilirmak, Harmange, or Su continuation result changes the original C1/P1 evidence class.

**Fixed input identity**

- v27 reviewer guide: `GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925.md`
- scientific parent: `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

**Command**

```bash
git show 509c4f3335d9020ea8e910579d6d98cb2fa9e58d:GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md | head -30
```

**Expected output**

The closed original oncology evidence chronology resolves without requiring any later biological-chi branch.

## V3. HOG input-context qualification

**[CLAIM]** A fixed HOG network and parameterization required multicoordinate response organization when only input kinetics changed; no stable complex pair licensed scalar `chi_bio`.

**Fixed input identity**

- branch: `bio-chi-hog1-input-context-p0q-20260925`
- result pin: `BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json`
- workflow run: `36212842924`
- artifact: `10896650681`
- artifact digest: `sha256:3e5b8fb3cbfdca78d630e3d1b714c4c11e02de782e2be4f1f35319041c272e70`

**Command**

```bash
git fetch origin bio-chi-hog1-input-context-p0q-20260925
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json
```

**Expected output**

- PC1 variance fraction `0.8082785568519034`
- maximum standardized 1D residual `0.9757894172146091`
- `MULTICOORDINATE_RESPONSE_ORGANIZATION_REQUIRED_P0Q`
- `NOT_LICENSED_NO_STABLE_COMPLEX_PAIR_ACROSS_ALL_CONTEXTS`

## V4. Canonical Meneses prospective freeze

**[CLAIM]** The direct Meneses result has a prospective source freeze that predates its outcome-bearing workflow and is distinct from a later timeout-generated duplicate freeze.

**Fixed input identity**

- branch: `bio-chi-ecoli-pmf-recovery-p0q-20260925`
- canonical freeze commit: `3636681325f9337cb7472f05296f4a3dccb5e400`
- freeze: `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FREEZE.json`
- upstream source: `wadhwalab/2026-Meneses-Osmotic` @ `d14d0caaa07299f13d1b1121d1e4630454fd724b`

**Command**

```bash
git fetch origin bio-chi-ecoli-pmf-recovery-p0q-20260925
git show 3636681325f9337cb7472f05296f4a3dccb5e400:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FREEZE.json | head -40
```

**Expected output**

The freeze identifies 200, 300, 400, and 500 mM sucrose shock, immediate motor traces, sustained adaptation, TMRM, cell area, the multicoordinate representation test, the stronger rate-depth rule, and scalar refusal rules before the canonical outcome.

## V5. Meneses source reproduction and direct whole event

**[CLAIM]** The canonical Meneses source inventories and orthogonal summaries reproduce, and the direct collapse/recovery whole event is admitted at literature-open P0-Q.

**Fixed input identity**

- result pin: `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md`
- repaired run: `36216252676`
- artifact: `10897836350`
- artifact digest: `sha256:33e2c253ffb19abe1d3679116df768e08012cc6181cd910a38c3976b4bf77c3f`

**Command**

```bash
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json
```

**Expected output**

- immediate trace counts `8,10,8,12`
- sustained-adaptation counts `8,8,8,4`
- source TMRM and cell-area summary reproduction passes
- biological chi = `DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q`

## V6. Meneses representation and failed stronger rate-depth claim

**[CLAIM]** The direct experimental event requires multicoordinate representation under the frozen criterion; the stronger rate-stable/depth-variable rule fails.

**Command**

```bash
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json | grep -E 'pc1_variance|reconstruction|rate_depth|Chi_bio|chi_bio' -A4
```

**Expected output**

Primary lane:

- PC1 variance fraction `0.6620977810898341`
- maximum standardized 1D residual `1.1144697154328063`
- `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q`
- `FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q`
- scalar `chi_bio` = `NOT_OPENED_NOT_LICENSED`

## V7. Source-method reconciliation

**[CLAIM]** The multicoordinate conclusion survives the manuscript-facing source fit method and is not an artifact of the older four-parameter immediate fit.

**Fixed input identity**

- freeze: `BIO_CHI/control/MENESES2026_SOURCE_METHOD_RECONCILIATION_FREEZE_20260925.md`
- result pin: `BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`
- run: `36216368561`
- artifact: `10897991063`
- digest: `sha256:0534f1173b51a4d4fc4459bdb28a800a7759968f96119434d5f7ea35c1308dc9`

**Command**

```bash
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json
```

**Expected output**

- PC1 variance fraction `0.7719879506509367`
- maximum standardized 1D residual `1.2036796471330158`
- `SOURCE_METHOD_ROBUST_AT_P0Q`
- stronger rate-depth rule fails in both lanes

## V8. Preserved implementation failures and timeout governance

**[CLAIM]** Mechanical failures are retained without being converted into scientific evidence.

**Fixed input identity**

- `BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md`
- `BIO_CHI/control/MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md`
- `BIO_CHI/control/MENESES2026_DUPLICATE_REANALYSIS_SOURCE_METHOD_AUDIT_20260925.md`

**Command**

```bash
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md | grep -E 'false negative|finite-normalized|freeze' -i
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md | grep POST_RESULT_ROBUSTNESS_REANALYSIS
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_DUPLICATE_REANALYSIS_SOURCE_METHOD_AUDIT_20260925.md | grep 'F_0-1'
```

**Expected output**

The first implementation's non-frozen TMRM finite-track veto is identified as a false-negative implementation gate; the timeout duplicate is reclassified as post-result; and the duplicate TMRM denominator mismatch is documented rather than used to revise the canonical result.

## V9. Same-system perturbation-path transport

**[CLAIM]** At matched nominal concentrations, the frozen four-coordinate motor response organization does not transport unchanged from canonical sucrose/CCW to sorbitol, sodium-buffer, or clockwise-locked contexts.

**Fixed input identity**

- branch: `bio-chi-ecoli-path-transport-p0q-20260925`
- freeze: `BIO_CHI/control/MENESES2026_PATH_TRANSPORT_P0Q_FREEZE_v0_1.md`
- result pin: `BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/MENESES2026_PATH_TRANSPORT_CLOSURE_20260925.md`
- run: `36218586127`
- artifact: `10897189701`
- digest: `sha256:3e127309661dd7e75aed175e3a63390a1c62e2760eec5e2220ac630108424d45`

**Command**

```bash
git fetch origin bio-chi-ecoli-path-transport-p0q-20260925
git show origin/bio-chi-ecoli-path-transport-p0q-20260925:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json
```

**Expected output**

| comparison | D_path | Holm p | max standardized median difference | disposition |
| --- | ---: | ---: | ---: | --- |
| sorbitol vs sucrose | 2.10317 | 0.00029997 | 1.63825 | `PATH_DEPENDENT_REORGANIZATION_P0Q` |
| sodium-buffer vs sucrose | 1.44792 | 0.0194981 | 1.25237 | `PATH_DEPENDENT_REORGANIZATION_P0Q` |
| clockwise vs sucrose | 2.18054 | 0.00029997 | 1.48348 | `PATH_DEPENDENT_REORGANIZATION_P0Q` |

This is a finer representation result and does not contradict the source's gross phenotype robustness claim.

## V10. Depth-conditioned follow-up

**[CLAIM]** The matched-dose path result does not justify the stronger claim that path identity independently predicts the complete recovery vector after collapse depth is modeled.

**Fixed input identity**

- branch: `bio-chi-ecoli-depth-conditioned-p0q-20260925`
- freeze: `BIO_CHI/control/MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_FREEZE_v0_1.md`
- result pin: `BIO_CHI/config/MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/MENESES2026_DEPTH_CONDITIONED_PATH_CLOSURE_20260925.md`
- run: `36218707913`
- artifact: `10898495701`
- digest: `sha256:3e403e16c8107117a38b6a688d44e2e2df762622836512a61654bc99cd44a620`

**Command**

```bash
git fetch origin bio-chi-ecoli-depth-conditioned-p0q-20260925
git show origin/bio-chi-ecoli-depth-conditioned-p0q-20260925:BIO_CHI/config/MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01_RESULT_PIN.json
```

**Expected output**

- valid cells `143`
- fit failures `0`
- depth-only MSE `1.386650105058987`
- depth-plus-path MSE `1.3992070288026903`
- fractional improvement `-0.009055582008677782`
- bootstrap 95% interval `[-0.4202077600861875, 0.11030784776222519]`
- disposition `DEPTH_CONDITIONING_UNRESOLVED_P0Q`

The coordinate-level `log_tau_dec` improvement of 25.3% remains descriptive only and cannot override the aggregate frozen rule.

## V11. Scalar refusal audit

**[CLAIM]** Neither the HOG nor Meneses continuation creates a scalar biological stability coordinate merely because fitted time constants exist.

**Command**

```bash
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json | grep -E 'chi_bio|complex_pair'
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json | grep -A4 'chi_bio'
git show origin/bio-chi-ecoli-path-transport-p0q-20260925:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json | grep 'chi_bio'
```

**Expected output**

HOG refuses scalar admission because no stable complex pair exists across contexts. Meneses refuses scalar admission because source fit taus are empirical response summaries rather than an independently licensed modal carrier.

## V12. V29 smoke test

**[CLAIM]** A reviewer can verify the new biological-chi continuation from a small set of branch records without reconstructing historical repository archaeology.

**Command**

```bash
set -e

git fetch origin \
  biosystems-v29-biochi-meneses-20260925 \
  bio-chi-hog1-input-context-p0q-20260925 \
  bio-chi-ecoli-pmf-recovery-p0q-20260925 \
  bio-chi-ecoli-path-transport-p0q-20260925 \
  bio-chi-ecoli-depth-conditioned-p0q-20260925

git merge-base --is-ancestor 58eb8b4777fae0fb79ab50d38b738dfee556b2a3 origin/biosystems-v29-biochi-meneses-20260925

git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json | grep -q DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q

git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json | grep -q MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q

git show origin/bio-chi-ecoli-path-transport-p0q-20260925:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json | grep -q MULTICOORDINATE_MOTOR_ARCHITECTURE_CONTEXT_DEPENDENT_ACROSS_TESTED_PATHS_P0Q

git show origin/bio-chi-ecoli-depth-conditioned-p0q-20260925:BIO_CHI/config/MENESES2026_DEPTH_CONDITIONED_PATH_P0Q_V01_RESULT_PIN.json | grep -q DEPTH_CONDITIONING_UNRESOLVED_P0Q

echo V29_SMOKE_TEST_PASS
```

**Expected output**

```text
V29_SMOKE_TEST_PASS
```

## Claim ceiling

The V29 additions do not establish a universal biological chi value, a universal `chi_bio=1` boundary, a pan-cancer dynamical law, or a general substrate-inheritance law. Meneses provides one direct experimental bacterial perturbation/recovery system. It supports a whole-event biological chi relation and multicoordinate representation at P0-Q, demonstrates matched-nominal-dose path-associated response reorganization, and leaves the independent path contribution unresolved after collapse-depth conditioning.

## What happens next and why

The Meneses sequence is closed for this iteration. Repeatedly mining the same dataset would convert an independent signal into post-result optimization. The next high-value experiment should move to an independent biological system with a directly measured perturbation magnitude and at least one separable recovery-rate coordinate. That design can freeze the depth-versus-rate question prospectively before outcome inspection.