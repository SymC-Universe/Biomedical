# Stage D Perturbation-Recovery-Transformation Freeze v0.1

Date frozen: 2026-09-08
Status: FROZEN BEFORE STAGE-D BIOLOGICAL OUTCOME INSPECTION
Branch: gri-stage-d-perturbation-recovery

## 1. Purpose

Stage D extends the completed static GRI architecture into a prospective perturbation-recovery program without modifying Stage C1, P0, or any prior frozen inference. The target is not cancer diagnosis, prognosis, treatment response, or a biological chi coordinate. The target is a narrower and falsifiable question:

> Can independently measured methylation architecture predict whether a perturbed regulatory system returns toward its pre-perturbation state, remains persistently displaced, or reorganizes into a new state after the perturbation is removed?

Stage D tests recovery and persistence in real perturbation datasets, then asks whether any prospectively defined recovery-associated architecture generalizes to independent experimentally ordered malignant-transformation systems.

## 2. Science firewall

1. Stage C1 remains immutable. Stage D cannot rescue, reinterpret, promote, demote, or overwrite any C1 result.
2. P0 FINAL_HOLDOUT remains closed. Stage D cannot retroactively change its model family, partition logic, selector, or claim ceiling.
3. No static coordinate is renamed resilience, rigidity, slack, stability, critical slowing, attractor depth, inheritance percentage, or biological chi unless a Stage-D experiment directly validates that interpretation.
4. Tumor stage is not treated as transformation pseudotime.
5. Resampling variance is not treated as temporal fluctuation or critical slowing.
6. Synthetic perturbation magnitude is an algorithm stress axis only and cannot define a biological cancer-transition threshold.
7. Scalar, modal, and conglomeration views remain separate. No master score is permitted in Stage D v0.1.
8. Failure, null, nonidentifiable, nonlinear-only, composition-sensitive, assay-sensitive, and out-of-domain outcomes remain valid outcomes and must be preserved.

## 3. Substrate-inheritance alignment

Stage D inherits the current substrate-inheritance evidence ladder conceptually, translated into biological measurement:

1. Parent characterization before child-outcome interpretation.
2. Explicit carrier or feature correspondence rather than numerical similarity alone.
3. Parent-to-child mapping rule frozen before target outcome inspection.
4. Prospective prediction against independently measured child state.
5. Intervention/counterfactual test in which the parent layer is perturbed and the child response is measured.
6. Specificity/null tests showing that generic, scrambled, or capacity-matched controls do not perform equally well.

Stage D may establish influence, conditional inheritance, or supporting inheritance evidence only within the biological dataset and assay scope actually tested. No universal substrate-inheritance claim is permitted.

## 4. Required views

### 4.1 Scalar

Retain only explicitly defined descriptive coordinates such as:
- spectral concentration S_spec;
- participation-ratio-based concentration S_PR;
- normalized residual displacement after perturbation;
- spectrally normalized realized cross-layer alignment, if denominator stability is adequate.

None is assigned a stability direction in advance unless that direction is itself the frozen hypothesis being tested.

### 4.2 Modal

Retain:
- eigenspectra;
- principal-angle subspace geometry;
- mode/subspace persistence, splitting, mixing, reconvergence, and extinction;
- carrier participation/localization where the assay permits it.

Degenerate/crowded sectors are compared as subspaces rather than forced one-to-one modes.

### 4.3 Conglomeration

Retain:
- Hallmark/program organization;
- pathway-level cross-layer coupling;
- 3D enhancer-promoter/contact organization when available;
- interaction structure among independently defined parent sources when available.

### 4.4 Relationship R and uncertainty U

R reports agreement/disagreement among scalar, modal, and conglomeration views without collapsing them to a master score.
U records uncertainty, nonidentifiability, support, assay/platform limitations, and refusal states separately for each view.

## 5. Primary datasets and roles

The following public experiments are frozen as Stage-D targets by accession, not by result direction.

### D1: GSE216989 / associated superseries GSE216986
Role: primary perturbation-withdrawal-recovery experiment.
Planned use: decitabine perturbation followed by recovery, with matched methylation, RNA, and promoter-capture Hi-C where available.
Primary question: after perturbation removal, how much of the methylation, RNA, and 3D-regulatory displacement persists, and do methylation-state changes predict later RNA/chromatin persistence?

### D2: GSE20945
Role: temporal perturbation-recovery replication / time-structure test.
Planned use: transient decitabine exposure with multiple later methylation and RNA measurements.
Primary question: is a recovery trajectory identifiable from multiple post-treatment time points, and do Stage-D coordinates predict that trajectory without forcing an exponential model when unsupported?

### D3: GSE231780 / associated series GSE231778
Role: independent experimentally ordered malignant-transformation challenge.
Planned use: BJ fibroblast progression through experimentally defined states including hTERT, SV40, and HRAS transformation with matched methylation and RNA measurements.
Primary question: do recovery-associated signatures defined from D1/D2 change in a preregistered direction across independently ordered transformation states?

### D4: GSE91071 / associated series GSE91069
Role: transformation-resistance / contrast experiment.
Planned use: early-passage, near-senescent, senescent, immortalized, oncogene-exposed, and transformed fibroblast states.
Primary question: do Stage-D recovery-associated signatures distinguish experimentally transformable from refractory/resistant states under the detector class actually supported by the data?

No dataset may be dropped because its outcome is unfavorable.

## 6. Data provenance and acquisition

For each accession, the acquisition record must include:
- GEO/SRA/BioProject accession;
- exact downloaded filename(s);
- download URL or authoritative source path;
- byte size;
- SHA-256 after download;
- assay type;
- sample/condition manifest;
- original platform annotation version;
- date acquired;
- whether raw or processed data are used;
- transformation/imputation steps;
- software/environment identity.

Processed public matrices may be primary when raw reconstruction is computationally disproportionate, provided the processed artifact is authoritative, hash-locked, and its provenance is explicit. Raw reconstruction remains a reproducibility path rather than a prerequisite unless a processed artifact fails validation.

## 7. Primary recovery endpoints

For an assay/layer state vector x, define control-corrected acute and recovered displacements only after matched control structure is established:

Delta_P = x_perturbed - x_control_early
Delta_R = x_recovered - x_control_late

Primary persistence ratio:

Q_residual = ||Delta_R|| / ||Delta_P||

with norm, feature universe, scaling, and control matching fixed per assay before result inspection.

Interpretation is descriptive only:
- Q_residual near 0: little acute displacement remains at the recovery endpoint;
- Q_residual near 1: endpoint displacement is comparable in norm to the acute perturbation;
- Q_residual > 1: endpoint displacement exceeds the acute displacement in that representation.

Q_residual is not a recovery rate and is not assigned a healthy/pathological direction by itself.

For datasets with multiple post-withdrawal time points, recovery-rate models may be fit only after model-family competition is prespecified. Candidate families must include at minimum:
- no-recovery / persistent-offset model;
- single-exponential return;
- biexponential return where sample support permits;
- nonparametric monotone/spline trajectory as a descriptive fallback.

A time constant tau is reported only if the selected/frozen model is identifiable and passes residual/uncertainty checks.

## 8. Cross-layer perturbation prediction

Primary Stage-D inheritance-style test:

> Does the methylation perturbation state measured before or at the acute post-perturbation time predict independently measured later RNA and/or chromatin recovery/persistence better than prespecified generic, scrambled, and capacity-matched controls?

Required controls where data permit:
1. patient/sample-label shuffle preserving per-feature marginals;
2. feature-label or Hallmark-label scramble;
3. size-matched shuffled Hallmark membership;
4. equal-dimensional unsupervised methylation compression;
5. composition/cell-state covariates if independently measured or defensibly estimated without target leakage;
6. treatment/dose controls and vehicle controls where available;
7. assay/platform/batch indicators where identifiable.

No control may be selected post-result because it produces a favorable comparison.

## 9. Spectral CKA bounds

For centered PSD kernels K_M and K_R with eigenvalues lambda_i and mu_i sorted descending:

E_perm[CKA] = tr(K_M) tr(K_R) / ((n-1)||K_M||_F ||K_R||_F)

and

CKA_max = sum_i lambda_i mu_i / (||K_M||_F ||K_R||_F)

by the von Neumann trace inequality under optimal eigenspace alignment with fixed spectra.

Candidate spectrally normalized realized alignment:

A_realized = (CKA_obs - E_perm[CKA]) / (CKA_max - E_perm[CKA])

This coordinate is descriptive unless separately validated. It is not called slack, resilience, rigidity, or inheritance. If the denominator is numerically small or uncertainty makes the ratio unstable, the coordinate is refused.

Empirical B-permutation distributions remain mandatory for finite-sample calibration when CKA is used inferentially.

## 10. Nonlinear detector rule

Because prior synthetic testing retained a nonlinear-only failure, Stage D must not interpret a negative linear-kernel CKA, Spearman, or linear ridge result as absence of cross-layer dependence.

Before biological Stage-D results are inspected, one nonlinear secondary detector family must be fixed. The preferred candidate is RBF-kernel CKA/HSIC with bandwidth chosen independently of target outcome, plus explicit synthetic calibration and a refusal rule for unstable bandwidth/small-n conditions.

Linear and nonlinear branches remain separate and are both reported.

## 11. Transformation challenge

D3/D4 do not substitute for longitudinal recovery. They test whether signatures learned or frozen from D1/D2 are associated with independently ordered malignant-transformation states.

Forbidden interpretations:
- stage progression as proof of recovery failure;
- correlation with transformation state as proof that loss of recovery causes cancer;
- retrospective selection of features that best order the transformation sequence.

Promotable result:
A Stage-D signature defined before D3/D4 outcome inspection changes in the frozen direction across the experimental transformation sequence and/or distinguishes transformation-resistant from transformable states better than matched controls.

Failure is retained if the signature does not generalize.

## 12. Regulatory-context depth

A biological analogue of substrate-depth robustness will be tested descriptively when mapping permits. Nested methylation contexts are declared before outcome inspection, for example:
1. promoter-core;
2. promoter + proximal regulatory context;
3. linked distal regulatory elements supported by independent 3D-contact annotation;
4. broader methylome representation.

The question is whether child prediction/recovery diagnostics converge or remain context-sensitive as additional parent regulatory structure is admitted.

No context depth is selected because it gives the most favorable biological result.

## 13. Evidence labels

Allowed Stage-D labels:
- NO_DETECTABLE_INFLUENCE_UNDER_SUPPORTED_DETECTORS
- SUBSTRATE_INFLUENCE
- CONDITIONAL_INHERITANCE_SUPPORT
- PERTURBATION_PREDICTION_SUPPORT
- RECOVERY_ASSOCIATION_SUPPORT
- TRANSFORMATION_GENERALIZATION_SUPPORT
- NONLINEAR_ONLY_SUPPORT
- COMPOSITION_SENSITIVE
- ASSAY_SENSITIVE
- CONTEXT_DEPTH_SENSITIVE
- NONIDENTIFIABLE
- OUT_OF_DOMAIN
- REFUSE

No physical/biological chi label is available in Stage D v0.1.

## 14. Promotion ladder

Stage-D promotion is conjunctive, not score-based.

D-P1: perturbation changes the independently defined parent layer above matched control/noise floor.
D-P2: later child response is predicted above generic/scrambled/capacity-matched controls.
D-P3: prediction survives prespecified technical/composition attacks where evaluable.
D-P4: withdrawal/recovery structure is observed and the parent representation predicts persistence or return.
D-P5: a signature frozen from D1/D2 generalizes to at least one independent transformation challenge D3/D4.
D-P6: intervention specificity is supported strongly enough that generic shared-state explanations no longer perform equally well.

No result above D-P4 is required for the current paper to remain valid. A higher-gate failure narrows the new extension but does not erase lower-gate findings.

## 15. Compute architecture

Authoritative repository: GitHub.

GitHub responsibilities:
- frozen contracts/configs;
- source and unit tests;
- small synthetic calibrations;
- provenance manifests and hashes;
- compact result summaries;
- figure/table regeneration;
- CI validation.

Kaggle responsibilities:
- large public matrix acquisition/caching;
- memory-heavy EPIC/WGBS/RNA/3D-contact preprocessing;
- repeated null/sensitivity calculations that benefit from up to approximately 30 GiB RAM;
- checkpointed Stage-D heavy runs.

PowerCell responsibilities:
- long-running or restart-sensitive computations;
- independent reruns/cross-checks;
- jobs too long for standard GitHub CI or awkward for Kaggle session lifetimes.

One canonical Python implementation must drive all backends. Kaggle/PowerCell launchers may select environment/resource paths but may not contain alternative scientific logic.

## 16. Execution order

0. Complete/continue already-frozen post-C1 v2.1 sensitivity independently; Stage D must not rewrite its outcome.
1. Build authoritative acquisition manifests for D1-D4 without opening/plotting outcome contrasts beyond metadata needed for sample mapping.
2. Validate sample-condition manifests and assay overlap.
3. Freeze exact feature universes, transformations, controls, nonlinear detector, norms, and model-competition rules.
4. Run D1 primary perturbation-withdrawal-recovery analysis.
5. Run D2 temporal replication/model-identifiability analysis.
6. Freeze D1/D2-derived candidate recovery signatures before D3/D4 outcome evaluation.
7. Run D3 transformation-sequence challenge.
8. Run D4 transformation-resistance contrast.
9. Run all frozen nulls, capacity controls, context-depth diagnostics, and technical attacks.
10. Integrate all outcomes, favorable or unfavorable, into the manuscript and supplement.
11. External adversarial review before claim promotion.

## 17. Falsification conditions

The intended resilience-failure hypothesis is weakened or rejected if, under adequate support:
- methylation perturbation does not predict later RNA/chromatin recovery better than matched generic controls;
- recovery-associated signatures fail to reproduce across D1/D2;
- transformation challenges show no prespecified relationship to D1/D2 recovery signatures;
- generic composition/assay structure performs equally well;
- only post-hoc feature selection produces apparent success;
- apparent effects vanish under capacity-matched or nonlinear/linear detector comparison;
- result direction depends materially on a chosen context depth, preprocessing choice, or assay subset selected after outcome inspection.

## 18. Claim ceiling before execution

Before Stage-D results exist, the strongest permitted statement is:

> Static GRI analyses establish reproducible methylation/RNA architecture and internal predictive transport. Stage D prospectively tests whether those measurements extend to perturbation response, recovery/persistence, and independent experimentally ordered transformation systems. No recovery, resilience, causal inheritance, malignant-transition, or clinical diagnostic claim has yet been established by Stage D.
