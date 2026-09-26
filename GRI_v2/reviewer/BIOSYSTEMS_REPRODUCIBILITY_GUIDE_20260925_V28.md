# BioSystems Reproducibility Guide V28

**Manuscript ID:** BIOSYS-D-26-00267  
**Guide date:** 25 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Reviewer branch:** `biosystems-v28-biochi-continuation-20260925`  
**Original submission evidence parent:** `biosystems-v27-repro-guide-20260925` @ `ae9d0499e44e211e00c04da208a7bc50e2948893`  
**Status:** REVIEWER ENTRY POINT WITH SEPARATELY FROZEN POST-RESULT BIO CHI CONTINUATION

## Status

The original C1/P1 oncology evidence spine remains unchanged. V28 adds navigation for the closed Kizilirmak context gate, the completed top-down representation phase, one preserved source-transport failure, and one new source-native HOG model qualification. None of these additions retroactively promotes the original TCGA, tumor-normal, or prostate evidence.

The editable manuscript and Supplementary Information remain private authoring artifacts. The public repository carries scientific freezes, code, workflow identities, result pins, failure records, and claim ceilings.

## What happened

The Bio Chi continuation produced two new records after the prior top-down closeout. The Moore et al. E. coli single-cell FRET experiment was frozen but remained scientifically unopened because the automated Dryad route first returned HTTP 403 and then returned a payload that was not a valid MATLAB file. The next independent source-native test used the Jashnsaz et al. HOG signaling Model 3. With network, parameters, final NaCl concentration, initial condition, and basal parameter fixed, six temporal input profiles produced a response family that failed a frozen one-dimensional adequacy rule. The final-state Jacobian spectra were real-only in all six contexts, so a damping-style scalar `chi_bio` was not licensed.

## Why it matters

The continuation strengthens a representation result rather than a numerical boundary claim. Whole-system biological chi can remain identifiable as a relation among context, internal organization, and realized behavior while scalar `chi_bio` is refused. Modal/vector `Chi_bio` is required only when the event needs it. Source and transport failures remain evidence about reproducibility, not scientific negatives.

## V1. Reviewer branch and ancestry

**[CLAIM]** V28 is a navigation and continuation layer above the unchanged v27 submission evidence branch.

**Fixed input identity**

- repository: `SymC-Universe/Biomedical`
- v28 branch: `biosystems-v28-biochi-continuation-20260925`
- v27 parent head: `ae9d0499e44e211e00c04da208a7bc50e2948893`

**Command**

```bash
git fetch origin biosystems-v28-biochi-continuation-20260925 biosystems-v27-repro-guide-20260925
git merge-base --is-ancestor ae9d0499e44e211e00c04da208a7bc50e2948893 origin/biosystems-v28-biochi-continuation-20260925
echo $?
```

**Expected output**

```text
0
```

## V2. Original oncology evidence remains frozen

**[CLAIM]** V28 does not alter the original C1/P1 inferential spine. The full prior claim map and workflow identities remain in the v27 guide and its scientific parent.

**Fixed input identity**

- v27 guide: `GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925.md`
- scientific parent: `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`

**Command**

```bash
git show origin/biosystems-v27-repro-guide-20260925:GRI_v2/reviewer/BIOSYSTEMS_REPRODUCIBILITY_GUIDE_20260925.md | head -40
git show 509c4f3335d9020ea8e910579d6d98cb2fa9e58d:GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md | head -30
```

**Expected output**

The first file identifies v27 as the reviewer entry point and the second resolves the closed v26 scientific record. No V28 result is required to reproduce C1 or P1.

## V3. Kizilirmak context gate

**[CLAIM]** A pre-stimulus global static RNA proxy did not transport as a context-independent determinant of later NF-kB dynamics across TNF-alpha and IL-1beta, while the source-native dynamical phenotypes remained measurable.

**Fixed input identity**

- branch: `gri-biochi-bridge-p0q-20260925`
- primary result pin: `BIO_CHI/config/KIZILIRMAK2023_CONTEXT_GATE_V01_RESULT_PIN.json`
- closure: `BIO_CHI/control/KIZILIRMAK2023_CONTEXT_GATE_CLOSURE_20260925.md`

**Command**

```bash
git fetch origin gri-biochi-bridge-p0q-20260925
git show origin/gri-biochi-bridge-p0q-20260925:BIO_CHI/config/KIZILIRMAK2023_CONTEXT_GATE_V01_RESULT_PIN.json
git show origin/gri-biochi-bridge-p0q-20260925:BIO_CHI/control/KIZILIRMAK2023_CONTEXT_GATE_CLOSURE_20260925.md
```

**Expected output**

The record preserves the clone-G cross-input counterexample, the bounded B-versus-R descriptive survivor, and local scalar refusal. It does not restore the historical static damping interpretation.

## V4. Top-down biological chi representation closeout

**[CLAIM]** The completed top-down phase supports representation adequacy rather than mandatory scalar-first construction.

**Fixed input identity**

- branch: `bio-chi-topdown-pivot-20260924`
- head: `86463567f5fab783689e30ce21d7b061623fff36`
- phase checkpoint: `BIO_CHI/control/TOPDOWN_PHASE_CHECKPOINT_20260925.md`
- representation matrix: `BIO_CHI/control/TOPDOWN_REPRESENTATION_ADEQUACY_MATRIX_20260924.md`

**Command**

```bash
git fetch origin bio-chi-topdown-pivot-20260924
git show 86463567f5fab783689e30ce21d7b061623fff36:BIO_CHI/control/TOPDOWN_PHASE_CHECKPOINT_20260925.md
git show 86463567f5fab783689e30ce21d7b061623fff36:BIO_CHI/control/TOPDOWN_REPRESENTATION_ADEQUACY_MATRIX_20260924.md
```

**Expected output**

The closeout retains mixed or negative Rehman, Marsolier, Shaffer, and Sharma outcomes plus the positive Harmange within-source lineage-memory relation. The whole event is evaluated before lower representation depth.

## V5. E. coli source-transport failure

**[CLAIM]** The E. coli sensory experiment was frozen prospectively at P0-Q but no biological result was opened because the automated source route failed twice at transport/parsing.

**Fixed input identity**

- branch: `bio-chi-ecoli-sensory-p0q-20260925`
- scientific freeze: `BIO_CHI/config/ECOLI2024_SENSORY_TOPDOWN_P0Q_FREEZE_v0_1.json`
- representation specification: `BIO_CHI/control/ECOLI2024_REPRESENTATION_TEST_SPEC_v0_1.md`
- failure checkpoint: `BIO_CHI/control/ECOLI2024_SOURCE_TRANSPORT_BLOCKED_20260925.md`
- workflow run 1: `36212606329`
- workflow run 2: `36212678770`

**Command**

```bash
git fetch origin bio-chi-ecoli-sensory-p0q-20260925
git show origin/bio-chi-ecoli-sensory-p0q-20260925:BIO_CHI/config/ECOLI2024_SENSORY_TOPDOWN_P0Q_FREEZE_v0_1.json
git show origin/bio-chi-ecoli-sensory-p0q-20260925:BIO_CHI/control/ECOLI2024_SOURCE_TRANSPORT_BLOCKED_20260925.md
```

**Expected output**

The checkpoint reports `SOURCE_TRANSPORT_BLOCKED`, with run 1 failing on HTTP 403 and run 2 reaching a non-MATLAB payload. No `chi_bio`, `Chi_bio`, or biological chi outcome is claimed from this source.

## V6. HOG1 input-context model qualification

**[CLAIM]** With the source HOG network and parameterization fixed, six NaCl input kinetics at the same final concentration generated a multicoordinate Hog1 response family. The frozen one-dimensional compression failed and no damping-style scalar carrier was licensed.

**Fixed input identity**

- branch: `bio-chi-hog1-input-context-p0q-20260925`
- freeze: `BIO_CHI/control/HOG1_INPUT_CONTEXT_P0Q_FREEZE_v0_1.md`
- engine: `BIO_CHI/experiments/hog1_input_context_p0q_v01.py`
- result pin: `BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json`
- workflow run: `36212842924`
- artifact: `10896650681`
- artifact digest: `sha256:3e5b8fb3cbfdca78d630e3d1b714c4c11e02de782e2be4f1f35319041c272e70`
- source parameter SHA-256: `47f80b80f740c969170373ad80e94aea68a975e7fd5f0d84d2f5a0cdb39f4443`

**Command**

```bash
git fetch origin bio-chi-hog1-input-context-p0q-20260925
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/control/HOG1_INPUT_CONTEXT_P0Q_FREEZE_v0_1.md
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/experiments/hog1_input_context_p0q_v01.py | sha256sum
```

**Expected output**

The result pin reports:

```text
status = EXECUTED_VALID_SOURCE_NATIVE_MODEL_QUALIFICATION
PC1 variance fraction = 0.8082785568519034
maximum standardized 1D reconstruction residual = 0.9757894172146091
one-dimensional adequacy = false
Chi_bio = MULTICOORDINATE_RESPONSE_ORGANIZATION_REQUIRED_P0Q
chi_bio = NOT_LICENSED_NO_STABLE_COMPLEX_PAIR_ACROSS_ALL_CONTEXTS
```

The model qualification is not experimental biological validation.

## V7. HOG1 source and numerical reproduction

**[CLAIM]** The executable HOG1 result is derived from the source-released Model 3 equations and source parameter object, without outcome-dependent retuning.

**Fixed input identity**

- upstream repository: `neuertlab/Jashnsaz_STARProtocols_2021`
- `get_models.m` blob: `a31de158ff7474648c0d48a2994eaa25b10cc610`
- `Get_ODE.m` blob: `1ede4299ec77dc8cfffeec8381b7ae2ccf4b205b`
- `get_simData.m` blob: `8a2a99b8a1193fc35a86437c251b17d8e82cad03`
- parameter object blob: `7b152c6aa33018970dcd689244864fcb595f1f52`

**Command**

```bash
python BIO_CHI/experiments/hog1_input_context_p0q_v01.py
cat BIO_CHI/experiments/hog1_results/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT.json
```

**Expected output**

The six contexts are `step`, `root2`, `linear`, `quadratic`, `quintic`, and `heptic`. The final concentration is 0.3 M. The result must reproduce the pinned representation disposition and scalar refusal in V6.

## V8. Claim ceiling and refusal audit

**[CLAIM]** Failures and refusals are preserved without being converted into support.

**Fixed input identity**

Use the V3 through V7 records.

**Command**

```bash
for b in   gri-biochi-bridge-p0q-20260925   bio-chi-topdown-pivot-20260924   bio-chi-ecoli-sensory-p0q-20260925   bio-chi-hog1-input-context-p0q-20260925
do
  git fetch origin "$b"
done

git show origin/bio-chi-ecoli-sensory-p0q-20260925:BIO_CHI/control/ECOLI2024_SOURCE_TRANSPORT_BLOCKED_20260925.md | grep SOURCE_TRANSPORT_BLOCKED
git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json | grep NOT_LICENSED_NO_STABLE_COMPLEX_PAIR
```

**Expected output**

Both refusal strings are present. The E. coli branch remains scientifically unopened. The HOG1 branch retains multicoordinate `Chi_bio` and refuses scalar `chi_bio`.

## V9. Master smoke test

**[CLAIM]** A reviewer can verify the continuation without downloading a large raw-data collection or running historical scripts.

**Command**

```bash
set -e
git fetch origin   biosystems-v28-biochi-continuation-20260925   biosystems-v27-repro-guide-20260925   bio-chi-topdown-pivot-20260924   gri-biochi-bridge-p0q-20260925   bio-chi-ecoli-sensory-p0q-20260925   bio-chi-hog1-input-context-p0q-20260925

git merge-base --is-ancestor ae9d0499e44e211e00c04da208a7bc50e2948893 origin/biosystems-v28-biochi-continuation-20260925

git show origin/bio-chi-ecoli-sensory-p0q-20260925:BIO_CHI/control/ECOLI2024_SOURCE_TRANSPORT_BLOCKED_20260925.md | grep -q SOURCE_TRANSPORT_BLOCKED

git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json | grep -q MULTICOORDINATE_RESPONSE_ORGANIZATION_REQUIRED_P0Q

git show origin/bio-chi-hog1-input-context-p0q-20260925:BIO_CHI/config/HOG1_INPUT_CONTEXT_P0Q_V01_RESULT_PIN.json | grep -q NOT_LICENSED_NO_STABLE_COMPLEX_PAIR_ACROSS_ALL_CONTEXTS

echo "V28_SMOKE_TEST_PASS"
```

**Expected output**

```text
V28_SMOKE_TEST_PASS
```

## What happens next

The next Bio Chi experiment should preferentially use a directly retrievable source with an explicit perturbation, measurable recovery or reorganization, and target-observable power. The current result does not justify inventing a scalar. A future scalar route should open only when an independently licensed same-mode dynamical carrier exists.

## What the user needs to do

Nothing is required to preserve or reproduce the records above. The working manuscript and supplement remain private; the public GitHub record is sufficient for reviewer audit of the scientific lineage.
