# Su 2026 oncology P0-Q interim disposition

**Date:** 24 September 2026  
**Branch:** `bio-chi-oncology-p0q-20260924`  
**Status:** M397 source/model qualification closed; relational cross-system behavior gate remains open

## Source generator

The current publication equation is uniquely source-fidelity-supported under the predeclared dual-mapping adjudication. It produces lower joint two-state RMSE than the pinned public-code sign mapping in all eight source-defined scenarios and lower aggregate statewise variance-normalized SSE by many orders of magnitude.

The publication/code sign inconsistency remains preserved as a source Limit Map item. It is not silently repaired.

## Scalar disposition

**Disposition:** `P0Q_REFUSED_UNCERTAINTY_SENSITIVE_EQUIVALENT_NATIVE_INVARIANT`

Three of eight nominal best-fit scenarios contain a complex-conjugate pair, but five are real-only and therefore refuse the scalar constructor under the frozen same-mode rule.

The nominal complex cases are:
- ON_PP: 0.9896042374
- OFF_PN: 0.9170605214
- OFF_NN: 0.5464006946

However, every nominal complex scenario crosses the real/complex discriminant boundary within the frozen +/-1 reported-SEM corner grid, and each also has some unstable +/-1 SEM corners. The carrier class is therefore not robust to the available parameter uncertainty.

In addition, for this real 2x2 generator the scalar is algebraically identical to

`-trace(J)/(2*sqrt(det(J)))`

whenever a complex pair exists. The frozen numerical check confirms that identity to maximum absolute error 1.11e-16. The scalar is a compact native pole coordinate here, not additional information beyond trace and determinant.

This source therefore does not establish cross-system scalar transport into oncology under the current uncertainty gate.

## Modal disposition

**Disposition:** `P0Q_QUALIFIED_UNCERTAINTY_AWARE_NATIVE_GENERATOR_FAMILY`

The source defines a complete two-state generator for all eight scenarios, the source-derived module trajectories are reproducibly reconstructed, the current publication mapping reproduces them with positive/high statewise trajectory correlations, and nominal eigenvector conditioning is finite in all eight scenarios.

The complete representation is retained as an uncertainty-aware generator/modal family rather than a fixed pole taxonomy. Seven of eight scenarios cross the real/complex discriminant boundary somewhere in the +/-1 SEM corner grid, so individual real-versus-complex mode labels are uncertainty-sensitive. The full generator and its uncertainty map remain well defined; individual pole-type claims are correspondingly bounded.

This representation is equivalent to the source-native two-module ODE description plus explicit modal/conditioning metadata. No superiority or extra information over the native generator is claimed.

## Relational Bio Chi disposition

**Current disposition:** `P0Q_RELATION_SUPPORTED_DESCRIPTIVELY__C3_NOT_YET_SATISFIED`

The four matched drug-on/drug-off carriers show substantial nominal generator reorganization, with relative Frobenius changes from 0.629 to 0.972. No matched pair has a licensed scalar in both conditions, so scalar motion and scalar memory are refused rather than interpolated across a disappearing/reappearing carrier class.

The independently frozen M397 recovery endpoint shows realized transcriptomic return toward the pretreatment state after drug withdrawal. Thus realized recovery coexists with context-dependent local generator/modal reorganization and without a continuous matched scalar carrier.

That relation satisfies the predeclared compensation/reorganization hypothesis descriptively, but it does not yet satisfy the conglomerate held-out/prospective behavior gate because the M397 drug-on and drug-off coefficients were fit from the same source trajectory and the recovery outcome was already known before this P0-Q lineage.

## Next gate

Use the untouched-for-this-analysis HCC827 and HT-29 time-resolved treatment trajectories in Supplementary Data 8 and 9 as a no-retuning cross-cell-line behavior test of the frozen M397 drug-on generator family.

The cross-cell-line gate must be frozen before those expression values are opened:
- retain all four M397 polarity-defined carriers;
- use the exact M397 gene sets already frozen from Supplementary Data 4;
- reconstruct the corresponding carrier means in each external cell line;
- start each prediction at that cell line's observed Control state;
- transport the matching M397 drug-on generator unchanged;
- compare against a frozen constant-state baseline and direct source-native pole/generator predictions;
- do not select a favorable carrier after viewing results.

This gate is P0-Q transport, not P1 confirmation.
