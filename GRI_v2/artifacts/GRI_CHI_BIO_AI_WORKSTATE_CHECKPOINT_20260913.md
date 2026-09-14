# GRI Chi_bio durable work-state checkpoint

**Checkpoint date:** 2026-09-13  
**TASK_ID:** `GRI_CHI_BIO_ADMISSION_PROGRAM_20260912`  
**Branch:** `gri-v071-protocol-integration-20260910-chi-bio`  
**Draft PR:** `#4 GRI: establish Chi_bio admission-or-falsification program`  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**SCIENTIFIC_STATE_CHANGED:** YES by explicit user approval of A3+B3+C3; `Chi_bio` remains `NOT_ADMITTED`.

## APPROVED SCIENTIFIC ARCHITECTURE

The approved family remains:

- G1 normalized regulatory-interaction theoretical primary;
- S1 transcriptomic regulatory state;
- methylation/substrate external/contextual rather than naively concatenated;
- L3 paired local + embedded scope;
- G2 discrete transition-operator temporal comparator;
- G4 attraction/diffusion stochastic alternative.

The user subsequently approved the recommended next architecture bundle:

- **A3:** `r=2` and `r=3` are co-equal robustness representations; no rank winner; material disagreement returns `REPRESENTATION_DEPENDENT_NO_TRANSFER`;
- **B3:** an externally sourced signed-regulon universe plus a prospectively fixed low-dimensional rule; CollecTRI leads provenance qualification, DoRothEA remains a representation sensitivity;
- **C3:** withhold normalized empirical G1 until restoration is independently resolved.

Architecture freeze:

`config/gri_Chi_bio_ABC_architecture_freeze_20260913_v0_1.json`

The freeze is guarded by `src/chi_bio_abc_architecture_contract.py` and dedicated regression tests. It is intentionally **not** a full empirical-execution freeze.

## HARDENED G1 DISPOSITION

- `R = beta I`: exact unity route retained;
- symmetric production Jacobian + SPD restoration: generalized exact route retained;
- general directed heterogeneous restoration: naive normalized unity route rejected by known counterexamples;
- two targeted source passes did not locate transcriptome-wide SCC25 turnover sufficient to justify a general restoration operator.

Therefore C3 is active: no normalized empirical G1 is authorized.

## G2 WORK PUSHED AFTER A3 APPROVAL

1. Extended the empirical freeze contract to support A3 without privileging either rank.
2. Added an A3-specific empirical freeze template that remains incomplete and therefore refuses real execution.
3. Updated source preflight so a complete A3 freeze must validate before local molecular files can be opened.
4. Exposed a hidden operator-model issue: `x_next = T x + B u + c` shares one `T`, so additive treatment forcing cannot itself demonstrate treatment-induced operator reorganization.
5. Implemented the pre-outcome treatment-interaction mechanics:

   ```text
   x_next = T0 x + u DeltaT x + B u + c
   T_PBS = T0
   T_CTX = T0 + DeltaT
   ```

6. Added synthetic known-truth tests for treatment-dependent operator recovery, rank deficiency and non-normal diagnostics.
7. Added a 500-replicate-per-cell CI calibration across r=2/r=3, stable/near-boundary/above-boundary/non-normal truth systems and a fixed synthetic noise grid. This calibration cannot read SCC25/TCGA data and cannot select empirical thresholds or a rank winner.
8. Added leave-one-transition-out stability diagnostics. These are explicitly deterministic sensitivity diagnostics, not iid/bootstrap biological uncertainty.
9. Prepared pre-outcome decision packets for RNA normalization, feature-universe construction and the shared pretreatment day-0 convention.
10. Added a computational execution plan covering SCC25, B3 regulon qualification and later TCGA transport.

## IMPORTANT SYNTHETIC NUMERICAL FINDING

The first synthetic calibration regression expected essentially machine-exact spectral recovery whenever the tiny sequential design was formally full rank. CI exposed that assumption as too strong: full-rank sequential trajectories can still be ill-conditioned, producing small but visible spectral perturbations even with zero injected noise.

The regression was repaired **without hiding the signal**:

- the calibration retains the actual condition-number and recovery-error distributions;
- independent random-design known-truth tests still verify exact algebraic implementation;
- the sequential calibration now requires finite diagnostics and correct mathematical unit-circle side rather than inventing an arbitrary numerical-error cutoff;
- this finding strengthens the requirement for a separately frozen conditioning/model-stability refusal rule before real data.

No real-data result was involved.

## CURRENT PRE-OUTCOME RECOMMENDATIONS, NOT YET FROZEN

### D. G2 operator model

Recommended:

```text
D2 treatment-interaction operator = primary candidate
D1 shared-T + additive input = restricted/null comparator
D3 separate-arm T = stress sensitivity only if identifiable
```

### E. RNA normalization

Current leading first-pass candidate is a transparent fixed library-size/log-CPM-like transform that is exactly reproducible from the frozen public processed count table. A DESeq2 VST remains an important methodological sensitivity only if the tximport/count-construction compatibility can be qualified without reconstructing missing source objects. Raw SRA reprocessing is escalation only.

### F. Feature universe

Leading architecture:

```text
fixed GENCODE-compatible gene semantics
INTERSECT
prospectively fixed PBS-control-only detectability rule
```

No exact detectability threshold is yet frozen.

### G. Day-0 convention

Leading architecture: use the measured SCC25 PBS day-0 state as the common pre-treatment branch point for PBS and cetuximab trajectories, while explicitly treating the repeated predictor as one shared measurement rather than two independent replicates.

### H-L

Still require prospective freezing of:

- conditioning refusal;
- model-adequacy refusal;
- non-iid uncertainty/sensitivity rule;
- cross-timescale daily/weekly transport rule;
- exact A3 material-conclusion agreement schema.

## COMPUTATIONAL POSTURE

Immediate SCC25/B3 work is not compute-limited.

- SCC25 G2: ordinary laptop CPU, roughly <1-2 GB practical working RAM, no GPU, seconds/minutes per deterministic pass;
- synthetic and leave-one-transition grids: minutes, CPU only;
- B3 regulon provenance/scoring qualification: modest CPU/RAM, no GPU;
- later frozen TCGA RNA source: `9457 x 22601 = 213,737,657` float values, about 1.71 GB decimal for one float64 matrix before copies/temporary arrays.

Recommended later TCGA envelope:

```text
16 GB RAM: feasible with memmap/chunking and strict copy control
32 GB RAM: recommended
64 GB RAM: comfortable for parallel resampling
GPU: not required
SSD: strongly preferred
```

Full plan:

`docs/GRI_CHI_BIO_COMPUTATIONAL_EXECUTION_PLAN_20260913.md`

## CURRENT CI STATE AT THIS CHECKPOINT

A previous CI pass failed only because the sequential synthetic calibration test imposed an unjustifiably strict numerical-recovery tolerance on a full-rank but ill-conditioned tiny design. The test was corrected to preserve the conditioning signal instead of suppressing it.

The newest CI rerun is the required confirmation before the current head can be called green. Do not treat this checkpoint text as evidence that the rerun has already completed successfully.

## FILE DEPENDENCIES

Later internal mapping still needs the already completed archives read-only:

- `Stage_C1_Result.zip`
- `Post_C1_Adversarial_Sensitivity_v2_2_Result.zip`

Do not rerun C1 or post-C1 sensitivity.

## SAFE RESUME POINT

Continue safe work through synthetic calibration interpretation, exact B3 source-export provenance, and D-L pre-outcome recommendation hardening.

Stop before:

- opening a real SCC25 trajectory under an incomplete D-L empirical freeze;
- choosing an exact G1 regulon panel from SCC25/TCGA candidate behavior;
- assigning a normalized empirical G1 under C3;
- interpreting the unit circle as a biological boundary.

## CLAIM CEILING

The A3+B3+C3 architecture is approved and frozen. The branch now contains executable guards and pre-outcome mechanics for the next temporal test. It does **not** support an admitted biological Chi, a normalized empirical G1, a cancer Chi map, or a biological `Chi_bio = 1` boundary.
