# NSD P0 Rank-Signal versus Null Stress

Date: 2026-09-10/11
Status: **P0 DEVELOPMENT STRESS. NO REFUSAL THRESHOLD OR RANK SELECTOR FROZEN.**

## Why this stage exists

The truth-blind rank/order sweep showed that structured four-state systems usually produce a pronounced method-native singular gap at rank/order 4, while the weak-observability system instead produces its strongest gap at rank/order 2. That is useful, but a rule such as "choose the largest gap" is not sufficient because every finite spectrum has a largest adjacent ratio, including pure-noise and colored-background records.

The missing question is therefore:

> Does singular-gap **strength**, considered without truth access, carry enough information to distinguish structured discrete-mode systems from null/no-discrete-mode processes, or would a largest-gap rule manufacture structure from background variability?

## Fixed P0 measurement

For each record and for each method independently:

1. sweep candidate rank/order `1..6`;
2. expose every adjacent singular-gap ratio;
3. record the largest finite ratio and its argmax rank;
4. make **no rank selection** and apply **no pass/refuse threshold**;
5. inspect known construction class only afterward at the P0 evaluation layer.

The SSI-COV and Subspace-DMD singular spectra are method-native objects. Their numerical gap magnitudes are not assumed to be directly interchangeable.

## Structured families

The structured side reuses the already-committed six-condition stress generator and replicate identities:

- baseline stochastic;
- white sensor noise, 10% channel SD;
- colored sensor noise, 10%, rho 0.8;
- weak second mode, 5% observation scale, plus 5% white sensor noise;
- crowded modes plus 5% white sensor noise;
- condition-number 25 similarity plus 5% white sensor noise.

No structured challenge is changed after seeing the previous order/rank sweep.

## Null families

Five P0 null stressors are added:

- independent white noise;
- spatially mixed white noise;
- multichannel AR(1)-like colored noise with rho 0.8;
- mixed `1/f` noise with beta 1;
- mixed `1/f^2` noise with beta 2.

These nulls are deliberately heterogeneous. They test whether a gap-based operational selector would invent discrete modal structure in backgrounds that can have temporal or spatial correlation but contain no planted oscillator poles.

They are **not** asserted to exhaust the null structure of resting EEG.

## Promotion-debt rule

If the development distributions suggest a useful null-calibrated gap threshold, threshold family, or conjunction with cross-rank persistence, that idea becomes `DATA_DERIVED / POST_RESULT` at the moment it is proposed. It may be developed further, but it cannot become P1-confirmatory from these same records. A later untouched development/qualification family must pay the promotion debt before any P1 freeze.

## Scientific outcomes allowed

This stage can legitimately return any of the following:

- structured/null gap-strength separation;
- partial separation dependent on noise family;
- method-specific separation;
- weak-observability collapse to lower effective rank;
- no useful separation at all.

The last outcome would be important: it would rule out simple singular-gap strength as a trustworthy operational refusal gate.

No outcome from this stage is a neural regime, chi coordinate, phenotype, mechanism, or clinical result.
