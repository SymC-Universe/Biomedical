# DMD Comparator Noise Reconciliation

Date: 2026-09-10
Status: **P0 COMPARATOR-SCOPE CORRECTION. NOT P1-FROZEN.**

## Why this correction is required

The initial comparator proposal identified DMD as the leading direct neural structural/modal comparator candidate because it addresses spatiotemporal eigenmode structure and has direct neural applications. A deeper method review shows that using only standard/exact DMD on noisy measurements would not satisfy the General Protocol requirement to use the strongest fair native comparator.

Dawson, Hemati, Williams & Rowley (2016), *Characterizing and correcting for the effect of sensor noise in the dynamic mode decomposition*, Experiments in Fluids 57:42, DOI `10.1007/s00348-016-2127-7`, analytically showed that standard DMD is biased by sensor noise and evaluated bias-correction, forward-backward, and total-least-squares-inspired alternatives.

Hemati, Rowley, Deem & Cattafesta (2017), *De-biasing the dynamic mode decomposition for applied Koopman spectral analysis of noisy datasets*, Theoretical and Computational Fluid Dynamics 31, 349-368, DOI `10.1007/s00162-017-0432-2`, developed the total DMD / noise-aware total-least-squares route and showed that noise-aware treatment can improve dynamical recovery when snapshot measurements are imprecise.

Askham & Kutz (2018), *Variable Projection Methods for an Optimized Dynamic Mode Decomposition*, SIAM Journal on Applied Dynamical Systems 17, 380-416, DOI `10.1137/M1124176`, reported reduced noise bias for optimized DMD relative to standard DMD in numerical examples.

## Consequence

The comparator question is therefore refined from:

`SSI-COV versus standard DMD`

to:

`SSI-COV versus a good-faith noise-aware DMD family candidate, with standard DMD retained only as a diagnostic baseline`.

This does **not** freeze TLS-DMD, optimized DMD, robust DMD, or any other variant as the final P1 comparator. The exact noise structure and target object must match the final P1 question before comparator identity is frozen.

## P0 action

1. retain exact DMD as a transparent baseline;
2. add a total-least-squares DMD implementation as the first noise-aware comparator candidate;
3. qualify exact and TLS-DMD on known-truth deterministic and sensor-noise constructions;
4. include SSI-COV, exact DMD and TLS-DMD in the same P0 stress matrix;
5. preserve all failures and do not select a winner from P0 development evidence;
6. revisit whether optimized/robust DMD is required before final MFR-05 freeze.

## Claim ceiling

This reconciliation is about comparator fairness only. It does not establish that TLS-DMD is neural-native, optimal for EEG, superior to SSI-COV, or the eventual P1 comparator. It also does not alter any NSD scientific threshold, chi interpretation, regime boundary, or biological claim.
