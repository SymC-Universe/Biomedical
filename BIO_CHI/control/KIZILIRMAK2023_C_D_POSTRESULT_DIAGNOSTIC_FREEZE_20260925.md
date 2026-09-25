# Kizilirmak C+D post-result decomposition freeze

**Date:** 25 September 2026
**Task:** `GRI_BIOCHI_KIZILIRMAK_C_D_DIAGNOSTIC_20260925`
**Status:** POST-RESULT DIAGNOSTIC / PROMOTION DEBT ACTIVE
**Parent result:** `KIZILIRMAK2023_C_D_RESULT_PIN_V01.json`

## Purpose

Investigate the A-positive / B-discordant result without changing the frozen C+D outcome or searching for a favorable representation.

## Frozen diagnostic questions

1. **A ratio decomposition:** For every common eligible gene, decompose the B-versus-R change in historical chi_GRI into its SD and mean components:
   `log(chi_B/chi_R) = log(sd_B/sd_R) - log(mu_B/mu_R)`.
   Report medians and sign fractions for both components.

2. **Mean-dependence map:** Quantify within-clone association between chi_GRI and transformed mean abundance. This is a nuisance diagnostic, not a correction model.

3. **Expression-stratified stability:** Define deciles using the pooled B/R transformed mean, before evaluating within-decile Delta_A. Report all ten deciles. Do not select favorable bins.

4. **Threshold stress:** Apply only source-distribution-derived lower-mean exclusions at pooled-mean percentiles 0, 10, 25, and 50 and report Delta_A for all. This is post-result robustness only and cannot promote the result.

5. **B component decomposition:** For each of the four frozen circuit genes, report B-minus-R chi direction and all five leave-one-biological-replicate-out gene-wise contrasts. Report how many genes support/opppose the historical damping-like direction.

6. **B subset fragility:** Report all four leave-one-gene-out circuit medians. This diagnoses whether one component dominates; no subset becomes a new B analysis.

7. **Source-mechanism collision:** Keep separate the paper's source-reported abundance mechanism (baseline TNFR1 for early activation; induced Nfkbia/IkBa for persistence/oscillation) from the historical CV/2 proxy. No diagnostic may relabel abundance control as chi_GRI support.

## Decision rules

- If A changes sign broadly across expression strata or lower-mean stresses, classify `A_MEAN_SCALE_FRAGILE`.
- If A remains positive across all frozen strata/stresses but chi is strongly mean-dependent, classify `A_DIRECTION_ROBUST_BUT_MEAN_DEPENDENT`.
- If B genes split directions or leave-one-gene-out summaries change sign, classify `B_COMPONENT_HETEROGENEITY`.
- The parent D disposition remains `scale_or_representation_instability_no_promotion` regardless of these diagnostics.
- Any mechanistic reinterpretation produced here remains post-result and cannot enter the manuscript as confirmatory evidence without an independent test.
