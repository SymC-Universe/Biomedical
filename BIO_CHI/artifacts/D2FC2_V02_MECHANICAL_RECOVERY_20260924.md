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
