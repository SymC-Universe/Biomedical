# BioSystems Reproducibility Guide V29

**Manuscript ID:** BIOSYS-D-26-00267  
**Guide date:** 26 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Reviewer branch:** `biosystems-v29-biochi-path-transport-20260926`  
**V28 parent:** `biosystems-v28-biochi-continuation-20260925` @ `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`  
**Original scientific parent:** `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`  
**Status:** REVIEWER ENTRY POINT / ORIGINAL C1-P1 SPINE UNCHANGED / BIOLOGICAL CHI CONTINUATION SEPARATELY FROZEN

## Purpose

V29 is the shortest reviewer route through the current submission evidence and its separately frozen biological-chi continuation. It does not reopen or modify the original TCGA C1, tumor-normal, external-prostate P1, or their adversarial controls. Those claims remain bound to the V26 scientific parent and the V28 reviewer layer.

V29 adds four governance/scientific items after V28: the canonical direct-experimental Meneses *E. coli* recovery qualification, explicit demotion of a timeout-generated duplicate lineage, a genuinely new same-system perturbation-path transport gate, and a post-result path-signal diagnostic that has no promotion rights.

The editable manuscript and Supplementary Information remain private authoring artifacts. Public GitHub carries the freezes, executable code, workflows, result pins, failures, audits, and claim ceilings needed for reviewer verification.

## Five-minute route

1. Verify V29 descends from V28 and that the original C1/P1 scientific parent is unchanged.
2. Use the V28 guide for the original oncology claim map, Kizilirmak context gate, top-down Bio Chi closeout, Moore source-transport refusal, and HOG model qualification.
3. Verify the canonical Meneses direct-experimental result and its source-method reconciliation.
4. Verify the timeout-duplicate governance audit so the same system is not double-counted.
5. Verify the new Meneses path-transport gate and, separately, the post-result diagnostic.
6. Run the master smoke test at the end of this guide.

## V1. Reviewer lineage

**[CLAIM]** V29 is a navigation/continuation layer above V28. It does not replace the original C1/P1 scientific parent.

**Fixed identity**

- V29 reviewer branch: `biosystems-v29-biochi-path-transport-20260926`
- V28 head: `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`
- original scientific parent: `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

**Command**

```bash
git fetch origin biosystems-v29-biochi-path-transport-20260926 biosystems-v28-biochi-continuation-20260925
git merge-base --is-ancestor 58eb8b4777fae0fb79ab50d38b738dfee556b2a3 origin/biosystems-v29-biochi-path-transport-20260926
echo $?
```

**Expected output**

```text
0
```

## V2. Original oncology evidence remains frozen

**[CLAIM]** V29 adds no new evidence to the original TCGA C1/P1 inferential spine.

**Fixed identity**

- V28 guide: `GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925_V28.md`
- original scientific parent: `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

**Command**

```bash
git show origin/biosystems-v28-biochi-continuation-20260925:GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925_V28.md | head -35
git show 509c4f3335d9020ea8e910579d6d98cb2fa9e58d:GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md | head -25
```

**Expected output**

The V28 file identifies the prior reviewer route and the V26 file resolves the closed original scientific record. No Meneses result is required to reproduce C1 or P1.

## V3. Context, representation, and refusal lineage inherited from V28

**[CLAIM]** The biological-chi continuation remains representation-first and preserves refusal rather than forcing a scalar.

**Fixed identity**

Use V28 for:

- Kizilirmak NF-kB context gate: `gri-biochi-bridge-p0q-20260925`
- top-down biological-chi closeout: `bio-chi-topdown-pivot-20260924` @ `86463567f5fab783689e30ce21d7b061623fff36`
- Moore *E. coli* sensory source refusal: `bio-chi-ecoli-sensory-p0q-20260925`
- HOG input-context model qualification: `bio-chi-hog1-input-context-p0q-20260925`

**Expected disposition**

The continuation distinguishes scalar `chi_bio`, modal/vector `Chi_bio`, and whole-system biological chi. Scalar refusal remains valid evidence. No universal biological `chi=1` boundary is claimed.

## V4. Canonical Meneses direct-experimental recovery qualification

**[CLAIM]** A direct experimental *E. coli* osmotic-shock source reproduces a whole perturbation/recovery relation that requires multicoordinate organization under the frozen P0-Q representation test, while scalar `chi_bio` remains unlicensed.

**Fixed identity**

- branch: `bio-chi-ecoli-pmf-recovery-p0q-20260925`
- primary result pin: `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`
- closeout: `BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md`
- source-method reconciliation: `BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`
- upstream source: `wadhwalab/2026-Meneses-Osmotic@d14d0caaa07299f13d1b1121d1e4630454fd724b`
- corrected publication DOI: `10.1016/j.bpj.2026.04.014`

Primary repaired workflow:

- run `36216252676`
- artifact `10897836350`
- digest `sha256:33e2c253ffb19abe1d3679116df768e08012cc6181cd910a38c3976b4bf77c3f`

Source-method reconciliation:

- run `36216368561`
- artifact `10897991063`
- digest `sha256:0534f1173b51a4d4fc4459bdb28a800a7759968f96119434d5f7ea35c1308dc9`

**Command**

```bash
git fetch origin bio-chi-ecoli-pmf-recovery-p0q-20260925
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md
```

**Expected primary record**

```text
EXECUTED_VALID_P0Q
DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q
MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q
FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q
NOT_OPENED_NOT_LICENSED
```

Key frozen representation values are PC1 variance fraction `0.6620977811` and maximum absolute standardized one-dimensional residual `1.1144697154`; one-dimensional adequacy fails. The post-result source-method reconciliation again fails one-dimensional adequacy and cannot promote the primary evidence.

## V5. Timeout-continuity duplicate is not independent evidence

**[CLAIM]** A later resume-visible Meneses freeze was created after the canonical Meneses result already existed in repository history. It is therefore post-result robustness, not an independent prospective confirmation.

**Fixed identity**

- governance audit: `BIO_CHI/control/MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md`
- source-normalization audit: `BIO_CHI/control/MENESES2026_DUPLICATE_REANALYSIS_SOURCE_METHOD_AUDIT_20260925.md`

**Command**

```bash
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md
git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_DUPLICATE_REANALYSIS_SOURCE_METHOD_AUDIT_20260925.md
```

**Expected output**

The governance record contains `POST_RESULT_ROBUSTNESS_REANALYSIS` and identifies `TIMEOUT_CONTINUITY_DUPLICATION + SOURCE_NORMALIZATION_MISMATCH` as the operational root cause. No duplicate result is counted as a second biological confirmation.

## V6. New same-system perturbation-path transport gate

**[CLAIM]** In the same direct *E. coli* motor system, perturbation-path identity is detectable from a frozen four-coordinate recovery representation at a concentration omitted from training, whereas collapse depth alone does not satisfy the frozen detection rule.

**Fixed identity**

- branch: `bio-chi-meneses-path-transport-p0q-20260926`
- prospective freeze: `BIO_CHI/control/MENESES2026_PATH_TRANSPORT_P0Q_FREEZE_v0_1.md`
- engine: `BIO_CHI/experiments/meneses2026_path_transport_p0q_v01.py`
- result pin: `BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json`
- closeout: `BIO_CHI/control/MENESES2026_PATH_TRANSPORT_CLOSURE_20260926.md`
- workflow run: `36284374387`
- workflow head: `79a098f777a27bb18bcb2c8fb26b69e301ab0e57`
- artifact: `10919776838`
- artifact digest: `sha256:71dbba045f674852ae8862cef89013297cbdcd2c16c440e55feea2386c1d35d5`
- result JSON SHA-256: `f06476bb9daa7fc3f8dcefd8e5eee15ea7d72fead44394b41bae111af8b5a108`

The frozen representation is:

```text
R = [A_dec, log(tau_dec), log(tau_inc), G_rec]
```

Four source-defined paths are represented at 200, 300, 400, and 500 mM: sucrose, sorbitol, sodium/buffer context, and clockwise motor rotation. All `143/143` source-facing fits are eligible; frozen fit failures are zero.

**Command**

```bash
git fetch origin bio-chi-meneses-path-transport-p0q-20260926
git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/control/MENESES2026_PATH_TRANSPORT_P0Q_FREEZE_v0_1.md
git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json
git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/control/MENESES2026_PATH_TRANSPORT_CLOSURE_20260926.md
```

**Expected primary result**

```text
full-vector balanced accuracy = 0.3846366627
full-vector null 97.5 percentile = 0.3272412031
upper-tail permutation p = 0.0009995002
primary = PATH_REORGANIZATION_DETECTED_P0Q

depth-only balanced accuracy = 0.2967254785
depth-only null 97.5 percentile = 0.3026513906
depth-only frozen detection = false
```

Held-out balanced accuracies are `0.2500`, `0.4875`, `0.51875`, and `0.2875` for 200, 300, 400, and 500 mM. The heterogeneity is part of the result.

The full-minus-depth accuracy increment is `0.0879111842`, below the prospectively frozen `0.10` threshold for the strongest secondary label. Because the freeze did not name the realized case in which the full vector detects, depth does not, and the increment is below `0.10`, the secondary disposition remains exactly:

```text
SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10
```

No post-result relabel repairs that taxonomy gap.

## V7. Post-result path-signal diagnostic

**[CLAIM]** A separately frozen post-result diagnostic localizes the already-detected path signal but has no promotion rights and does not alter V6.

**Fixed identity**

- freeze: `BIO_CHI/control/MENESES2026_PATH_SIGNAL_DIAGNOSTIC_FREEZE_20260926.md`
- engine: `BIO_CHI/experiments/meneses2026_path_signal_diagnostic_v01.py`
- result pin: `BIO_CHI/config/MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01_RESULT_PIN.json`
- workflow run: `36284508053`
- workflow head: `fad31e203762c7e47fb569d9e175fe51670fe804`
- artifact: `10919484871`
- artifact digest: `sha256:0ee429b118b24cba6a2276aae3ba6bac8627ae52f23b4e737903eba461dea0e8`
- result JSON SHA-256: `1fd8104c7f50acc50be0b94ac449e5777a2195dd8b50e571c2ce1516d96b7040`

**Command**

```bash
git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/config/MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01_RESULT_PIN.json
```

**Expected diagnostic pattern**

Single-coordinate frozen diagnostic detection:

```text
A_dec         false
log_tau_dec   true
log_tau_inc   true
G_rec         true
```

All four leave-one-coordinate-out three-feature representations remain detectable. Thus no single coordinate is uniquely required to retain the post-result aggregate path signal.

After Benjamini-Hochberg adjustment across six pairwise path tests, detectable contrasts are:

```text
sucrose vs sorbitol              q = 0.005994
sucrose vs clockwise             q = 0.029970
sorbitol vs sodium/buffer        q = 0.005994
sorbitol vs clockwise            q = 0.025974
```

Non-detected pairwise contrasts are sucrose vs sodium/buffer context (`q = 0.53946`) and sodium/buffer context vs clockwise (`q = 0.09710`). This selective pattern is explanatory post-result evidence only.

## V8. Representation hierarchy after V29

The current evidence does not license one universal biological scalar.

| Object | Current V29 disposition |
| --- | --- |
| scalar `chi_bio` | Refused/not opened where no independently identified modal carrier exists; the Meneses sigmoid/exponential timescales are response summaries, not a mechanistic second-order scalar carrier |
| modal/vector `Chi_bio` | Required or informative when multicoordinate dynamics are needed; Meneses direct recovery refuses one-dimensional compression; HOG similarly requires multicoordinate organization at model-qualification level |
| whole-system biological chi | Supported only at bounded source/event scope where the frozen whole-event relation reproduces; Meneses direct recovery and its path-transport gate are P0-Q examples, not universal laws |

The relationship among these levels is itself the research target. Lower-dimensional representations do not automatically inherit whole-system meaning, and a whole-system relation does not imply that a scalar must exist.

## V9. Master smoke test

**[CLAIM]** A reviewer can verify the current continuation from GitHub without reconstructing historical repository state manually or downloading all third-party source data.

**Command**

```bash
set -e

git fetch origin \
  biosystems-v29-biochi-path-transport-20260926 \
  biosystems-v28-biochi-continuation-20260925 \
  bio-chi-ecoli-pmf-recovery-p0q-20260925 \
  bio-chi-meneses-path-transport-p0q-20260926

git merge-base --is-ancestor 58eb8b4777fae0fb79ab50d38b738dfee556b2a3 origin/biosystems-v29-biochi-path-transport-20260926

git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json | grep -q DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q

git show origin/bio-chi-ecoli-pmf-recovery-p0q-20260925:BIO_CHI/control/MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md | grep -q POST_RESULT_ROBUSTNESS_REANALYSIS

git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json | grep -q PATH_REORGANIZATION_DETECTED_P0Q

git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json | grep -q SECONDARY_RULE_UNDERSPECIFIED_FULL_ONLY_LT_0_10

git show origin/bio-chi-meneses-path-transport-p0q-20260926:BIO_CHI/config/MENESES2026_PATH_SIGNAL_DIAGNOSTIC_V01_RESULT_PIN.json | grep -q POST_RESULT_NO_PROMOTION

echo "V29_SMOKE_TEST_PASS"
```

**Expected output**

```text
V29_SMOKE_TEST_PASS
```

## What happens next and why

The same-system Meneses source has now answered both the direct recovery-representation question and a perturbation-path transport question. Continuing to mine the same data would yield diminishing independent evidence. The next high-value Bio Chi experiment is a cross-system transport test using another directly measured biological perturbation/recovery source with explicit path or context variation and an accessible native dynamical carrier. The goal is to ask whether path-sensitive multicoordinate recovery organization transports, reorganizes, or refuses classification outside *E. coli*.

## What the user needs to do

Nothing is required to reproduce or preserve the current lineage. Public scientific records and reviewer navigation are in GitHub; editable manuscript and Supplementary Information remain private authoring artifacts.

**Guide disposition:** V29 is the current reviewer entry point for the BioSystems submission package and its separately frozen biological-chi continuation. It creates no new scientific result by itself.
