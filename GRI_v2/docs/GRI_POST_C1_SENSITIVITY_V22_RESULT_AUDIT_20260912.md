# GRI post-C1 adversarial sensitivity v2.2 result audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4 (2026-09-12)  
**Research mode:** P0-Q qualification/adversarial sensitivity  
**Historical C1 promotion:** unchanged  
**Biological chi:** NOT_ADMITTED

## 1. Source package and integrity

Audited user-returned result archive:

`POST_C~1.ZIP`

Archive SHA-256:

`85955af9e0d2333c651e445d75392b60ca9d25942a364fa29dc5c67b55bb3dd1`

Package-level checks:

- ZIP structural integrity: PASS.
- 15 archive members present.
- `SHA256SUMS.json` contains 14 member hashes and all 14 verified exactly.
- `RUN_SUMMARY.json` status: `POST_C1_SENSITIVITY_V2_2_COMPLETE`.
- frozen C1 contract SHA-1: `a39414c5990c234dc513569bd405b0237117d434`.
- frozen C1 implementation: `stage-c1-frozen-v2-exec-20260906.3`.
- 32 cancers, 100 resamples per cancer, B=199 repeated patient-permutation nulls.
- original completed C1 `WORKING_STATE` recorded read-only.

This is post-C1 sensitivity evidence. It cannot retroactively alter the prospective status or historical promotion label of Stage C1.

## 2. S0 canonical equivalence

**PASS.**

- 32/32 cancers passed.
- 6,400 canonical keys checked.
- maximum absolute reconstruction error observed: `9.71445146547012e-17`.
- frozen tolerance: `1e-10`.

Conclusion: the v2.2 worker reconstructed canonical C1 to numerical precision far inside the frozen tolerance before interpreting sensitivity outputs. No state-drift contradiction was found.

## 3. S1/S2 missingness sensitivity

### S1 burden structure

Only 5/32 cancers had variation in both methylation and RNA missingness burdens sufficient to define the planned cross-assay missingness correlation:

- COAD: rho = -0.079685
- PRAD: rho = -0.064534
- READ: rho = -0.288538
- STAD: rho = +0.241462
- UCEC: rho = -0.006395

The other 27 cancers are correctly labeled `NO_VARIATION_IN_ONE_OR_BOTH_BURDENS`.

### S2 interpretability

The frozen S2 rule states that a draw with degenerate burden structure is `S2_UNINFORMATIVE_DEGENERATE_BURDEN` and must not be counted as evidence that missingness projection changed or failed to change H2.

Primary-publication interpretable draws occurred only in:

- COAD: 100/100
- PRAD: 95/100
- READ: 100/100
- STAD: 92/100
- UCEC: 100/100

The interpretable-only primary-publication median S2 deltas are:

- COAD: 0.247768
- PRAD: 0.359133
- READ: 0.140435
- STAD: 0.292204
- UCEC: 0.244665

All 5/5 are positive; interpretable-only median delta = 0.247768.

### S2 semantic-output defect found during audit

`Post_C1_v2_Descriptive_Sign_Counts_NO_PVALUES.csv` reports S2 descriptive sign counts over all 32 cancer medians even though 27 cancers have zero interpretable S2 draws. The runner's `cancer_median_table()` preserves `s2_interpretable_true_count`, but `sign_counts_only()` does not use that eligibility status.

This is a science-adjacent summary defect, not a defect in the underlying S2 resample calculations. It overstates the evaluable cancer count for the missingness-projection sensitivity.

Correction preserved separately:

`artifacts/GRI_POST_C1_S2_INTERPRETABLE_ONLY_CORRECTION_20260912.csv`

Correct S2 evidentiary summary:

- PRIMARY_PUBLICATION: 5 eligible cancers, 5 positive, 0 negative, median interpretable-only delta 0.247768.
- MASKED_TECHNICAL: 5 eligible cancers, 5 positive, 0 negative, median interpretable-only delta 0.246100.

The original result archive is preserved unchanged.

## 4. S3 complete-case feature geometry

**Strong descriptive robustness.**

All 32 cancers on both technical tracks satisfy the frozen S3 interpretability floor.

Across cancer/track combinations:

- minimum methylation complete-case feature retention = 0.918016;
- minimum RNA complete-case feature retention = 0.925979.

Primary-publication cancer-level median delta:

- canonical H2: 0.232036;
- S3 complete-case: 0.232131.

The complete-case restriction therefore leaves the broad global patient-geometry signal essentially unchanged. This supports robustness to feature-level missingness handling within the tested TCGA state. It does not establish external generality.

## 5. S4 top-mode ablation and synthetic calibration

Primary-publication cancer-level median H2 delta:

- canonical: 0.232036;
- top-1 ablated: 0.105693;
- top-3 ablated: 0.055151.

The median top-1/canonical ratio is 0.4300; the median top-3/canonical ratio is 0.2272.

All 32 cancers retain positive median residual alignment after top-1 and top-3 ablation, but the effect is strongly attenuated.

Frozen interpretation:

- persistence supports detectable residual geometry beyond the removed leading directions;
- attenuation shows that leading modes carry substantial alignment;
- persistence does not imply an exact biological mode count;
- the synthetic reference is a power/interpretability calibration, not a biological fit.

The synthetic calibration behaves in the expected direction: median headroom falls from 0.2555 without ablation to 0.0758 after top-1 and 0.0511 after top-3 across the frozen known-truth grid.

Conclusion: the observed cross-omic geometry is neither a pure single-leading-mode artifact nor uniformly distributed. It contains substantial leading-mode contribution plus detectable residual structure beyond the first three directions.

## 6. S6 B=199 formal post-C1 sensitivity inference

Only S6 receives formal post-C1 directional sensitivity inference under the frozen plan.

### PRIMARY_PUBLICATION raw family

- H2: 32/32 positive; median delta 0.232036; one-sided sign p = 2.328306e-10; BH q = 3.492460e-10.
- H3a: 32/32 positive; median delta 0.100222; one-sided sign p = 2.328306e-10; BH q = 3.492460e-10.
- H3b: 29 positive / 3 negative; median delta 0.020245; one-sided sign p = 1.278007e-06; BH q = 1.278007e-06.

### PRIMARY_PUBLICATION purity/leukocyte-projected family

- H2_adj: 27/27 positive; median delta 0.214854; one-sided sign p = 7.450581e-09; BH q = 1.117587e-08.
- H3a_adj: 27/27 positive; median delta 0.053838; one-sided sign p = 7.450581e-09; BH q = 1.117587e-08.
- H3b_adj: 21 positive / 6 negative; median delta 0.008454; one-sided sign p = 2.962306e-03; BH q = 2.962306e-03.

The MASKED_TECHNICAL family gives the same qualitative result.

Interpretation:

- H2 global geometry survives the stronger repeated-null test.
- H3a patient-coupling advantage survives the stronger repeated-null test.
- H3b remains much smaller and more support-sensitive and must remain described as a small recurrent same-label advantage, not a strong per-cancer mechanism.
- none of these p/q values upgrades historical C1 status.

## 7. S7 TSS200-restricted methylation H2

Primary-publication TSS200 median delta = 0.235492 versus canonical all-probe H2 median delta = 0.232036.

Across cancers, Spearman rank correlation between TSS200 and canonical H2 cancer-level deltas is approximately 0.9868.

All 32 cancer medians remain positive on the primary-publication track.

Conclusion: broad patient-geometry alignment does not depend on retaining the entire methylation probe universe and is reproduced by the frozen TSS200 promoter-core representation. This is a feature-universe robustness result, not evidence that promoter methylation is the sole or causal mechanism.

## 8. S11 composition-complete gated adjusted sensitivity

The gated design yields 30 evaluable cancers; DLBC and THYM remain below the frozen >=30 composition-complete participant requirement.

PRIMARY_PUBLICATION:

- gated H2_adj: 30/30 positive; median delta 0.219984.
- gated H3a_adj: 30/30 positive; median delta 0.062625.
- gated H3b_adj: 25 positive, 4 negative, 1 tie; median delta 0.010456.

This materially strengthens the interpretation that the broad projected H2/H3a architecture is not an artifact of inheriting the original fixed-draw membership pattern. H3b remains the weak/support-sensitive branch.

No new p value or promotion is attached to S11.

## 9. S12 projection-conditioning audit

Projection matrices are numerically well behaved in the executed draws:

### Canonical composition-complete draws

- n = 720
- median purity/leukocyte r = -0.7881
- median VIF = 2.6390
- maximum VIF = 24.6511
- median standardized-covariate condition number = 2.9048
- maximum condition number = 9.8282
- maximum projection symmetry error = 1.88e-13
- maximum projection idempotence error = 3.66e-13
- design rank = 3 for every retained row

### Gated adjusted draws

- n = 3,000
- median purity/leukocyte r = -0.7821
- median VIF = 2.5752
- maximum VIF = 29.9550
- median standardized-covariate condition number = 2.8598
- maximum condition number = 10.8541
- maximum projection symmetry error = 2.22e-13
- maximum projection idempotence error = 4.96e-13
- design rank = 3 for every retained row

Conclusion: the projection computation itself is numerically stable, but purity and leukocyte fraction are strongly anticorrelated and some draws have substantial multicollinearity. This remains an interpretive limitation. Future implementations should retain the frozen plan's recommendation to prefer QR/SVD projection for numerical transparency.

## 10. Technical-mask sensitivity

The MASKED_TECHNICAL and PRIMARY_PUBLICATION tracks remain extremely similar for the principal H2-related sensitivities. The technical mask therefore does not appear to drive the broad geometry result within this post-C1 analysis.

This remains descriptive P0-Q evidence, not an external validation claim.

## 11. Scientific disposition

### Supported within current TCGA P0-Q qualification

- canonical C1 reconstruction is exact within frozen tolerance;
- broad methylation/RNA patient geometry survives B=199 repeated nulls;
- the result survives complete-case feature restriction;
- the result persists under TSS200-only methylation restriction;
- residual geometry persists after removal of the leading one and leading three kernel eigenmodes, although strongly attenuated;
- H2/H3a survive purity/leukocyte projection in both inherited and composition-complete gated designs;
- technical masking does not materially reorganize the principal result;
- numerical projection behavior is stable.

### Narrowed / limited

- S2 missingness projection is broadly unevaluable because 27/32 cancers lack variation in one or both missingness burdens; evidence is limited to COAD, PRAD, READ, STAD, and UCEC.
- H3b remains small, support-sensitive, and unsuitable for cancer-specific mechanistic interpretation.
- purity/leukocyte projection is not comprehensive cell-composition adjustment.
- TCGA remains cross-sectional and cannot establish temporal progression, recovery, resilience, treatment response, substrate inheritance, or causality.
- this post-C1 work is P0-Q and cannot retroactively create pristine P1 confirmation.
- biological chi remains NOT_ADMITTED.

## 12. v0.7.4 implications

The sensitivity gate that previously blocked final GRI scope disposition is now computationally closed, subject to the S2 summary correction above.

Final production System Model/Engine scope should now be reconciled against v0.7.4 before freeze. In particular, the next audit must explicitly address:

1. local versus embedded regulatory stability rather than inferring system-level state from lower-level coordinates;
2. pre-Atlas coordinate independence;
3. separation of participation, observability, identifiability, coordinate estimation, regime placement, and uncertainty where meaningful in GRI;
4. hierarchical closure before any lower-scale regulatory representation is treated as an effective higher-scale component;
5. recovery/resilience and cross-scale prediction families only where future temporal/perturbational evidence licenses them;
6. experimental-opportunity and literature-collision records for substantial biologically testable questions;
7. attribution/nearest-prior-art and residual-novelty accounting;
8. run-economy, preflight, pilot, checkpoint, and AI-continuity controls for future expensive computation;
9. milestone balance so representative function, perturbation/transition coverage, and limits remain proportionate.

## 13. Remaining scientific stop boundaries

1. Historical equal-dimensional/capacity-matched comparator freeze remains referenced but not recovered. It must not be invented. A new replacement design would be new P0-Q science-adjacent work and requires explicit scientific selection/freeze.
2. Decisive external P1 dataset/task/comparator/MFR-14 selection remains unfrozen.
3. Independent Regulatory Substrate Atlas remains to be locked for confirmatory use.
4. Authoritative manuscript edits remain separate and require explicit requested scope.
5. Draft protocol-integration PR should remain unmerged until the v0.7.4 delta audit and final scientific-scope disposition are complete.

## 14. Current project state

**STATUS:** Post-C1 sensitivity v2.2 completed and audited; S0 passed; broad H2/H3a architecture survives the frozen post-C1 adversarial suite; H3b remains weak/support-sensitive; one S2 summary-eligibility defect was identified and corrected without altering the original archive.

**PURPOSE:** P0-Q qualification under v0.7.4.

**NEXT ACTION:** synchronize the GRI System Model/Engine capability map with these returned results and perform the v0.7.4 delta audit before final scope freeze; continue comparator-provenance recovery in parallel.

**USER ACTION:** NONE for this result audit.
