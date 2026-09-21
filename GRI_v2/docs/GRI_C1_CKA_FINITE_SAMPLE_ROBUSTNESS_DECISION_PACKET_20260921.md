# GRI C1 CKA finite-sample robustness decision packet

**Date:** 2026-09-21  
**Status:** P0-Q POST-RESULT ROBUSTNESS DESIGN / NOT FROZEN  
**Historical C1 result:** immutable  
**Purpose:** challenge whether the frozen C1 cross-omic alignment conclusion depends materially on the finite-sample bias properties of the original linear CKA statistic.

## 1. Trigger

Frozen Stage C1 uses n=30 patient draws and very high-dimensional methylation/RNA representations. Linear CKA is an established representation-similarity statistic and is mathematically related to the RV coefficient. Subsequent methodological work has highlighted finite-sample bias of conventional CKA in low-n/high-dimensional settings.

This challenge is therefore activated under the GOM foundational-dependency and domain-informed-mediation rules.

It does **not** assert that historical C1 is wrong. C1 also used patient-alignment permutation nulls and the post-C1 analysis repeated the effect under B=199 null inference, which already attacks a major class of dimensionality-driven artifacts.

## 2. Claim under challenge

Historical claim to preserve:

> aligned methylation/RNA patient geometry exceeds the frozen patient-alignment null within the C1 representation.

Not under test here:

- causality;
- biological chi;
- substrate inheritance;
- damping;
- external generality;
- a claim that the absolute numerical CKA value has biological units.

## 3. Competing explanations

### H-original
The positive aligned-minus-null effect reflects patient-specific cross-omic geometry and survives a finite-sample-bias-resistant similarity estimator.

### H-bias
The effect is materially dependent on the biased CKA/RV-family estimator under the n<<p geometry and weakens or changes conclusion under an independently justified debiased estimator.

### H-mixed
Patient-specific alignment remains detectable, but effect magnitude/ranking changes enough that absolute-geometry or confidence interpretations must be narrowed.

## 4. Candidate sensitivity estimators

No estimator is selected by this packet.

Candidate families to qualify prospectively:

1. **unbiased-HSIC normalized linear CKA**, using a source-verified U-statistic/unbiased HSIC implementation;
2. **diagonal-removed / lower-triangular centered Gram estimator** with a published finite-sample bias analysis;
3. **RV2 / diagonal-removed RV-family statistic** as an independent linear cross-product similarity sensitivity.

The exact implementation must be verified against its primary methodological source and known-truth fixtures before real C1 data are reopened.

## 5. Same-question design

For each historical C1 resample where both layers are valid:

- preserve the exact patient draw;
- preserve exact methylation and RNA feature matrices;
- preserve preprocessing;
- preserve the exact frozen patient-alignment permutation stream where mathematically valid;
- compute original CKA and each qualified sensitivity statistic;
- compute aligned-minus-patient-null effects on each statistic's native scale;
- aggregate at the cancer level exactly as a post-result sensitivity, not as a replacement preregistration.

Primary robustness object is categorical:

> does patient-specific aligned geometry remain directionally detectable across cancers under the finite-sample-bias-resistant estimator?

No requirement is imposed that the numerical effect sizes equal the original CKA scale.

## 6. Before-result stopping rule

Before real data are reopened, freeze:

- exact sensitivity estimator(s);
- code/reference identity;
- null compatibility;
- invalid/undefined handling;
- cancer-level aggregation;
- material-conclusion agreement rule;
- multiplicity family if more than one sensitivity is promoted beyond descriptive robustness.

Possible outcomes:

- `ROBUSTNESS_SUPPORTED`: material alignment conclusion survives;
- `ROBUSTNESS_DEPENDENT`: conclusion depends materially on estimator;
- `FOUNDATIONAL_REVISION_REQUIRED`: original interpretation no longer survives the bounded challenge;
- `CHALLENGE_INVALID`: selected estimator does not answer the same object;
- `INDETERMINATE`.

## 7. Promotion effect

A pass does not create external validation or biological mechanism. A fail does not erase the historical result; it narrows what the historical statistic can support and propagates only to claims that depend on CKA-based cross-omic geometry.

## 8. External basis

- Kornblith et al. (2019), ICML/PMLR 97, established CKA as a representation-similarity statistic and noted its relation to RV/CCA families.
- Zhu et al. (2017), Scientific Reports, used omic similarity matrices and kernel alignment in TCGA, establishing direct multi-omics prior art.
- Murphy, Zylberberg & Fyshe (2024), ICLR Representational Alignment Workshop / arXiv:2405.01012, demonstrated a low-n/high-dimensional bias concern for conventional CKA and motivated debiased alternatives.

The 2024 source is challenge literature, not treated as a definitive adjudication of the C1 result.
