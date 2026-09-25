# Bio Chi oncology re-entry checkpoint

Date: 24 September 2026
Status: ACTIVE P0-Q ONCOLOGY QUALIFICATION
Branch: bio-chi-oncology-p0q-20260924
Parent: bio-chi-closure-p0q-20260924 at ead67809dd77baf785850c9cbbc470c1430af5aa

## Scientific fork resolved

The ERK B3 cycle remains closed at partial transport: chi_bio representation-class transport supported, ERK model-specific Chi_bio refused under the frozen complete-modal gate, and Bio Chi cross-system transport not opened.

The user directed the investigation back into oncology rather than opening a post-result replacement ERK representation. The ERK refusal remains immutable.

## Oncology entry system

First target: Su et al. 2026 BRAF-mutant melanoma reversible-transition system, DOI 10.1038/s41467-026-71349-4.

Pinned public code:
- repository: jihoonlee0/melanoma_reversible_transition
- commit: a2b2119f6d69d49e33ff4b57fb04b2b1eaf5fe68
- model file: Runge-Kutta4,5-250124.py
- blob: 9105d12c4717e8abca64ec6cad002084d07534ec

Existing M397 recovery results remain post-result P0-D evidence and are not untouched confirmation.

## Source-native generator

The source code defines:
dg1/dt = alpha1 - beta1*g1 - a1*g2
dg2/dt = alpha2 + a2*g1 - a3*g2

Therefore each fitted source scenario has generator:
J = [[-beta1, -a1], [a2, -a3]]

The exact source scenario, polarity, condition mapping and fitted coefficients must be frozen before SymC modal calculations.

## Frozen qualification sequence

1. Freeze Supplementary Data 5 or equivalent source-data identity, hash, parameter table, and scenario labels.
2. Reproduce source-native two-module trajectories from published coefficients and source initial conditions where available.
3. Inventory the complete 2D eigenstructure for every eligible source-defined scenario. No outcome-based scenario dropping.
4. Construct chi_bio only for genuine complex-conjugate eigenfactors using chi_bio = -Re(lambda)/|lambda|. Real-only scenarios are scalar refusals.
5. Candidate Chi_bio is the complete two-mode generator/eigenstructure plus source mapping, uncertainty/conditioning, and trajectory-reproduction metadata.
6. Compare against simpler native descriptions: raw eigenvalues, trace, determinant, discriminant, direct decay/growth rate, and oscillation frequency where present.
7. Freeze a forward-versus-reverse relational test before combining modal results with the already-known recovery/hysteresis trajectory.
8. Test whether the cross-level relation adds information beyond the simpler native descriptions. This is the oncology Bio Chi conglomerate gate.

## Non-vacuity rule

The Su model is affine-linear in its fitted module coordinates. Matrix-exponential agreement with the same generator is algebraically expected and is not sufficient for Chi_bio admission. Qualification also requires source-trajectory reproduction, source mapping, uncertainty/conditioning where available, and native/simple comparators.

## Relation to GRI

GRI remains a separate static molecular-organization evidence layer. It cannot supply missing dynamics and cannot be relabeled as chi_bio. A later bridge may test whether static GRI organization predicts independently measured dynamic Bio Chi behavior only where a shared carrier/sample mapping exists.

## Ceiling

P0-Q only. No universal biological chi, chi=1 boundary, or universal cancer-stability law is claimed.

## Stop condition

Stop for scientific intervention only if source scenario-to-parameter mapping is ambiguous, a new representation would need to be invented after viewing results, the source model cannot reproduce declared trajectories under published values, or frozen three-object definitions/inherited dispositions would need changing.
