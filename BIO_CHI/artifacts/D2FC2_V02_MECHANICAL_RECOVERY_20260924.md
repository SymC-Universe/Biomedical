# D2FC2 v0.2 mechanical recovery record

**Date:** 24 September 2026  
**Scientific freeze:** `BIO_CHI/config/D2FC2_NFKB_INDEPENDENT_MODAL_P1_FREEZE_v0_2.json`  
**Status:** MECHANICAL_RECOVERY_IN_PROGRESS  
**Scientific result inspected:** NO

The publication-defined training/validation partition, generator pair rule, scalar definition, numerical tolerance, empirical-frequency rule, held-out support criterion, falsifiers, and claim ceiling remain unchanged.

## Attempt 1

Workflow run `36032806692` failed before scientific analysis at the first SimBiology equilibration call.

Failure:
- custom code overwrote `RuntimeOptions.StatesToLog` with species only;
- source-defined observables require constant parameters such as `h2`, `kdNFKB`, `h3`, `kdP`, `ps`, and `kv`;
- SimBiology therefore refused expression validation.

Repair:
- remove the species-only logging override;
- preserve the logging layout created by the source model itself.

No scientific output was produced.

## Attempt 2

Workflow run `36033103372` passed expression validation but failed at the first 10-day equilibration simulation with NaN/Inf right-hand-side warnings followed by CVODES convergence failure at t=0.

Source audit showed why:
- the source model initializes Gaussian IKK input coefficients at zero;
- the repeated-assignment expression can therefore be undefined before a concrete IKK profile is loaded;
- the authors' `RunAverageIKKTrajectory.m` always applies a source IKK profile with `UpdateParameters(...,1)` before calling `SimulateModel`;
- the authors' `SimulateModel.m` uses absolute and relative tolerances of `1e-8` for the 10-day equilibration.

Repair committed at `69ca8a838ef538b08a7efc1caee2b6263bcfefff`:
- load the publication-native **Control** IKK profile before TR=0 equilibration;
- use the source-native `1e-8` tolerances;
- retain the source model's own `StatesToLog` layout.

The Control profile belongs to the publication training set. No held-out validation NF-kB trajectory was used to select this repair.

## Current execution

Workflow run `36041986061` executes the unchanged v0.2 scientific gate after the source-fidelity repair.

If it fails mechanically again, repair only source execution fidelity. If it reaches an adjudicated scientific result, preserve that result exactly and do not retune the gate.


## Attempt 3 contract-implementation audit

Workflow run `36041986061` completed and produced an artifact, but its own adjudicator returned `INVALID_TEST_SOURCE_PARTITION`.

The artifact was opened to diagnose that invalid-test status. Two implementation discrepancies with the already-frozen v0.2 contract were identified:

1. The freeze states that the publication-defined training and validation conditions are addressed by name rather than row position. The implementation nevertheless required the entire CSV to match one hard-coded row order. The source CSV instead lists the four publication training conditions first, followed by the five validation conditions. The validation conditions themselves were found and processed by name. The hard-coded whole-file order check was therefore an accidental carryover and not part of the frozen scientific requirement.

2. The freeze specifies a `maximum matched pair relative complex spread`. The implementation calculated the maximum relative spread over the entire spectrum, including near-zero real modes. This can diverge solely because a denominator is near zero and is not the frozen complex-pair stability criterion.

The artifact contained numerical scientific fields and was therefore viewed during this diagnosis. It remains invalid for admission under its own `INVALID_TEST_SOURCE_PARTITION` status and cannot be used to tune thresholds, pair rules, validation conditions, or expected direction.

Mechanical contract-alignment repair committed at `66e4bf361d9e5831a8137a3b88f118247a47ae54`:
- source partition validity is checked by exact named membership and uniqueness, independent of row order;
- numerical spread is computed only across the nonreal positive-imaginary representatives required by the frozen pair criterion.

No frozen numerical threshold, pair-count rule, scalar definition, held-out condition, empirical peak rule, or support criterion changed.

Because numerical fields from the invalid artifact were visible before this repair, the corrected rerun retains explicit provenance debt and must not be described as a pristine never-viewed P1 test. Its role is bounded independent external qualification under a repaired implementation of the pre-existing freeze.
