# Stentor cross-system habituation/recovery transport freeze v0.1

**Date:** 26 September 2026  
**Branch:** `bio-chi-stentor-cross-system-p0q-20260926`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct-behavior cross-system transport qualification

## Scientific purpose

The preceding Meneses *E. coli* gate found that perturbation-path identity was detectably encoded in a multicoordinate recovery representation at an unseen dose, while collapse depth alone did not satisfy its frozen detection rule. The next question is whether that architectural property appears in a biologically different direct-measurement system.

This experiment does **not** require the same coordinates, molecular carrier, or mechanism to recur. It asks whether a whole perturbation/recovery event in another organism similarly requires relational organization beyond a single recovery coordinate.

## Source

Ramdas, Doan, Theroux, and Gershman (2026), *A quantitative portrait of habituation in Stentor coeruleus*.

Pinned source repository:

- repository: `tejasramdas/stentor_habituation`
- commit: `8704c114555af3477a1dd7471beedde205fed263`
- README blob: `ea68552d6c84e36d9ab7b2e87b72a7902b9ed113`
- loader blob: `7f36a9dff75096b6b4ef2ad4f05d889cde968e0f`
- collated-data LFS OID: `sha256:b84054675f8a608471da1d9cccd051c1fb9503d35b3c9b5b9f6ebc378e75054f`
- collated-data declared size: `13922257` bytes
- current reviewed-preprint DOI: `10.7554/eLife.112314.1`
- original bioRxiv DOI: `10.64898/2026.06.09.731162`

The published qualitative findings were visible during source selection, including frequency-sensitive recovery and partial decoupling of recovery from potentiation. The experiment is therefore literature-open and cannot be described as blinded discovery or confirmation.

## Source analysis object

Use the source `processed_data/collated.jld2` object and the source-defined `control_data` matrix for each condition. The source code constructs 12 condition keys:

- ISI = 60, 120, 180 s;
- ITI = 3600, 7200, 10800, 18000 s.

Each `control_data` matrix is expected from source code to contain two consecutive 60-stimulus trials (rows 1--60 and 61--120) and the source-controlled cell sample in columns.

The source-controlled object is primary because the authors explicitly use it to equalize initial-response composition across conditions before inference. No attempt will be made to reconstruct omitted raw-video processing or to substitute the precomputed MCMC chains for the behavioral data.

## Whole biological event

Repeated mechanical stimulation reduces contraction responsiveness (habituation), a rest interval permits partial response recovery, and the second stimulation series can habituate differently from the first.

The whole event is the joint relation among:

1. stimulation frequency;
2. rest/recovery duration;
3. first-trial response loss;
4. post-rest response recovery;
5. second-trial response loss and relearning organization.

## Frozen per-cell representation

For every source-controlled cell, define from the binary/response-valued 120-stimulus trajectory:

- `H1_depth` = mean(trial 1 stimuli 1--10) - mean(trial 1 stimuli 51--60);
- `Recovery` = mean(trial 2 stimuli 1--10) - mean(trial 1 stimuli 51--60);
- `H2_depth` = mean(trial 2 stimuli 1--10) - mean(trial 2 stimuli 51--60);
- `AUC_shift` = mean(trial 1 stimuli 1--60) - mean(trial 2 stimuli 1--60).

The frozen multicoordinate representation is

[
R_{Stentor}=[H1_{depth}, Recovery, H2_{depth}, AUC_{shift}].
]

No coordinate is dropped for being negative, zero, or extreme. A cell is excluded only if its source-controlled 120-point trajectory contains nonfinite values or fewer than 120 rows are available for the condition. Exclusions are preserved in a failure ledger.

## Primary cross-system path test

Treat ISI (60, 120, 180 s) as the perturbation-path label and ITI (1, 2, 3, 5 h) as the transport context.

Perform leave-one-ITI-out classification:

1. hold out one complete recovery interval;
2. train on cells from the other three recovery intervals;
3. standardize the four frozen coordinates using training-fold statistics only;
4. fit multinomial logistic regression with fixed L2 regularization `C=1.0`, balanced class weights, and no hyperparameter tuning;
5. predict the three ISI labels for cells in the held-out recovery interval.

Aggregate all four held-out folds and report balanced accuracy.

### Primary null

Use 2,000 permutations with seed `20260926`. Within each ITI separately, permute ISI labels while preserving all cell representation vectors, then repeat the complete leave-one-ITI-out pipeline.

### Primary decision

- `CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q` if observed full-vector balanced accuracy is strictly greater than the 97.5th percentile of the stratified permutation null.
- `CROSS_SYSTEM_PATH_ORGANIZATION_NOT_DETECTED_P0Q` otherwise.

A non-detection is not equivalence and does not invalidate the Meneses source-specific result.

## Recovery-only control

Repeat the identical classifier and null using only `Recovery`.

Frozen secondary interpretation:

- full vector detects and recovery-only does not: `MULTICOORDINATE_PATH_INFORMATION_BEYOND_RECOVERY_ONLY_P0Q`;
- both detect: `PATH_INFORMATION_NOT_SEPARATED_FROM_RECOVERY_ONLY_P0Q`;
- only recovery detects: `RECOVERY_DOMINANT_PATH_SIGNATURE_P0Q`;
- neither detects: `PATH_SIGNATURE_UNRESOLVED_P0Q`.

No effect-size increment threshold is added after the Meneses secondary-taxonomy gap; this four-way rule exhaustively names all detection combinations before result inspection.

## Representation-adequacy control

Independently of classification, standardize the four condition-level medians across the 12 ISI x ITI conditions and compute singular values/PC1 variance fraction.

One-dimensional adequacy requires both:

- PC1 variance fraction >= 0.95;
- maximum absolute standardized reconstruction residual <= 0.10.

This is descriptive representation adequacy and cannot override the primary path test.

## Biological chi hierarchy

- **biological chi:** the whole frequency/rest/habituation/recovery/relearning relation;
- **Chi_bio:** the minimum multicoordinate response organization required by the frozen tests;
- **chi_bio:** not opened. Binary contraction trajectories and empirical learning/recovery summaries do not by themselves identify a source-native damped modal scalar.

No `chi_bio=1` boundary is used.

## Cross-system promotion rule

A positive primary result means only that a path-sensitive multicoordinate organization appears in a second direct biological system under its own native observables. It does not imply numerical universality, common mechanism, identical latent coordinates, or a universal scalar.

Cross-system architecture is **not** promoted beyond P0-Q unless the source data themselves pass the frozen gate.

## Failure and source rules

- Failure to retrieve the Git LFS data is a source-transport failure, not a scientific negative.
- Failure to decode the pinned JLD2 object is an implementation/source-interface failure.
- Missing expected condition keys or a condition with zero eligible cells returns `INSUFFICIENT_SOURCE_COVERAGE`.
- Zero-variance training coordinates return a frozen representation refusal for that fold; no coordinate is silently dropped.
- All source, implementation, and scientific failures are preserved separately.

## Claim ceiling

This experiment can establish only whether stimulation-frequency path information transports across unseen recovery duration in the released source-controlled Stentor behavioral object, and whether the event is adequately one-dimensional under the frozen representation. It cannot establish a molecular memory mechanism, universal learning law, consciousness claim, common mechanism with *E. coli*, or scalar `chi_bio`.
