# Stentor 2026 cross-system path-transport closeout

**Date:** 26 September 2026  
**Branch:** `bio-chi-stentor-cross-system-p0q-20260926`  
**Status:** CLOSED VALID P0-Q CROSS-SYSTEM RESULT  
**Authority:** SymC GOM v0.8.6

## Status

The Stentor cross-system experiment is closed using the prospectively amended source-run analysis unit. The source-controlled behavioral object contains 1,200 selected cells across 12 stimulation-frequency × recovery-interval conditions. Those cells map to 171 source experimental runs; the primary inferential unit is the median frozen representation within each represented source run.

No source-feature failure occurred. The nested-cell classifier is retained only as descriptive sensitivity and cannot promote or rescue the source-run result.

## Primary result

The frozen representation was

[
R_{mathrm{Stentor}}=
[H1_{mathrm{depth}}, Recovery, H2_{mathrm{depth}}, AUC_{mathrm{shift}}].
]

Stimulation interval (60, 120, or 180 s) was treated as perturbation-path identity. Recovery interval (1, 2, 3, or 5 h) was the held-out transport context.

Using leave-one-recovery-interval-out multinomial classification on source-run medians:

- observed balanced accuracy: **0.4639841**;
- concentration/context-stratified permutation-null 97.5th percentile: **0.4177844**;
- upper-tail permutation value: **0.0014993**;
- permutations: 2,000.

All four held-out recovery intervals remained above three-class chance individually, with balanced accuracies 0.5291, 0.4501, 0.4477, and 0.4358.

The frozen primary disposition is:

`CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q`.

This is an architecture-level cross-system result. It does not establish that Stentor and E. coli share a molecular mechanism, numerical coordinate system, or universal stability law.

## Recovery-only control

The recovery coordinate alone also retained stimulation-frequency path information across unseen recovery duration:

- observed balanced accuracy: **0.4561351**;
- null 97.5th percentile: **0.4140139**;
- upper-tail permutation value: **0.0009995**.

The prospectively exhaustive secondary disposition is therefore:

`PATH_INFORMATION_NOT_SEPARATED_FROM_RECOVERY_ONLY_P0Q`.

This prevents an overclaim. The full representation detects path organization, but the experiment does not establish that the three added coordinates are uniquely required for path prediction beyond recovery itself.

## Representation adequacy

The separate 12-condition representation-adequacy test strongly refuses one-dimensional compression:

- PC1 variance fraction: **0.7346072**;
- maximum absolute standardized one-dimensional reconstruction residual: **1.1628776**;
- one-dimensional adequacy: **false**.

The frozen disposition is:

`MULTICOORDINATE_CONDITION_REPRESENTATION_REQUIRED_P0Q`.

Thus the system-level condition architecture is multicoordinate even though stimulation-frequency classification is not separable from the recovery coordinate alone.

## Biological chi hierarchy

- biological chi: `CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q`;
- `Chi_bio`: `MULTICOORDINATE_CONDITION_REPRESENTATION_REQUIRED_P0Q`;
- `chi_bio`: `NOT_OPENED_NOT_LICENSED`.

The source supplies behavioral learning/recovery trajectories, not an independently identified damped modal carrier. No scalar is invented from empirical response summaries.

## Cross-system interpretation relative to Meneses E. coli

The architectural recurrence is narrower than "the same biology."

Meneses E. coli showed that a multicoordinate motor-recovery vector detects perturbation path across unseen dose while collapse depth alone did not satisfy its frozen gate. Stentor shows that stimulation-frequency path also transports across unseen recovery interval and that the 12-condition architecture is strongly multicoordinate. However, Stentor recovery alone also detects stimulation-frequency path.

The commonality is therefore **relational/contextual organization under perturbation and recovery**, not an identical minimal representation, identical mechanism, or universal scalar.

## Workflow identity

Canonical run: `36285086980`  
Canonical workflow head: `56533470bca936e370758a3f12e9890a3eca4769`  
Artifact: `10920058447`  
Artifact digest: `sha256:d10818d9549deb2f9df2e9dadd296861f5c5cd1714e0513669631e82fe5e2931`  
Result JSON SHA-256: `246f129ddc8e8623bc99115311425fc8c3f38aba72fef8b3aa0a35a6cce2adb9`

## What happens next and why

The immediate cross-system question is answered positively but with a narrower secondary interpretation than the Meneses depth control. The next experiment should not search for a shared numerical scalar. It should test a third direct biological system with explicit perturbation/context structure and proper replicate units, asking whether whole-event organization transports and what minimum native representation is actually required.

A useful next target should preferably expose a source-native dynamical carrier rather than only behavioral summaries, because that would allow scalar `chi_bio` to be either genuinely licensed or refused on native-model grounds.

## What the user needs to do

Nothing at this checkpoint. The result, source hash, experimental-unit amendment, workflow identity, and claim ceiling are preserved in GitHub.
