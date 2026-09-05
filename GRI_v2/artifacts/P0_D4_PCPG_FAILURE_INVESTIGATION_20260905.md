# P0 D4 PCPG outlier and failure investigation

Date: 2026-09-05
Status: POST-HOC DIAGNOSTIC ONLY — NOT ELIGIBLE TO RETUNE P3

## Executive result

PCPG is the only D4 cancer where the frozen ALL_METHYLATION_RIDGE model does not beat COVARIATE_ONLY at the cancer-median normalized-MSE level. The observed difference is -0.069487 (positive would favor ALL_METHYLATION_RIDGE). PCPG is also the only D4 cancer whose five-state result moves from DISCOVERY GLOBAL_SHARED_ONLY/CAUTION to REPLICATION WITHIN_LAYER_ONLY/REFUSE.

The failure is real under the frozen metric, but it is not a uniform collapse. It decomposes into three interacting features:

1. PCPG is the smallest complete-case replication cohort (n=30; raw n=34), so the cancer-level median is comparatively unstable.
2. The prediction failure is sharply target-heterogeneous: ALL_METHYLATION_RIDGE beats COVARIATE_ONLY on 25/50 Hallmarks and loses on 25/50. SAME_HALLMARK_ONLY is actually the best median model in PCPG (median nMSE 0.478856), while ALL_METHYLATION_RIDGE is 0.622144 and COVARIATE_ONLY is 0.552657.
3. One participant, TCGA-RW-A681, is an extreme RNA-space outlier but not a comparable methylation-space outlier. Removing that one participant changes the cancer-median ALL-vs-COVARIATE difference from -0.069487 to +0.011217. This is a diagnostic sensitivity result only; the participant remains in the frozen D4 result.

## Frozen D4 result for PCPG

- replication participants: 34
- composition-complete participants: 30
- DISCOVERY state: GLOBAL_SHARED_ONLY / CAUTION
- REPLICATION state: WITHIN_LAYER_ONLY / REFUSE
- reason code: TECHNICAL_TRACK_DISAGREEMENT
- within-layer methylation: detected, delta S_spec 0.471683, p=0.025
- within-layer RNA: detected, delta S_spec 0.549520, p=0.025

### Global audit screens

RAW PRIMARY_PUBLICATION:
- CKA 0.163119
- null median 0.030028
- delta CKA 0.133091
- p=0.075
- FAIL only because p exceeds frozen 0.05 threshold

RAW MASKED_TECHNICAL:
- CKA 0.163010
- delta CKA 0.125334
- p=0.025
- PASS

ADJUSTED PRIMARY_PUBLICATION, n=30:
- CKA 0.212496
- delta CKA 0.139841
- p=0.025
- PASS

ADJUSTED MASKED_TECHNICAL, n=30:
- CKA 0.212722
- delta CKA 0.140820
- p=0.050
- PASS

Thus the PCPG state failure is not disappearance of cross-layer structure. Three of four global screens pass, and both within-layer structures are strongly detected. The failure is the frozen primary raw-screen p-value plus disagreement with the technical track.

## Predictive failure anatomy

Cancer-median metrics:

- ALL_METHYLATION_RIDGE: median nMSE 0.622144; median R2 0.489068
- COVARIATE_ONLY: median nMSE 0.552657; median R2 0.493904
- SAME_HALLMARK_ONLY: median nMSE 0.478856; median R2 0.544241
- MEAN_ONLY: median nMSE 1.253781

So the methylation-rich model still predicts much better than the discovery mean-only reference, but does not outperform the covariate-only comparator under the frozen primary pairing metric in PCPG.

ALL_METHYLATION_RIDGE wins exactly 25/50 Hallmarks against COVARIATE_ONLY and loses 25/50. The median target-wise advantage is essentially centered at zero (-0.00170); the cancer-level negative median difference is therefore driven by a relatively balanced target mixture rather than failure across nearly every target.

Largest ALL_METHYLATION_RIDGE losses versus COVARIATE_ONLY include:
- inflammatory response: -0.245454 nMSE advantage
- allograft rejection: -0.226469
- KRAS signaling up: -0.208947
- TNFA/NFKB: -0.204372
- interferon-gamma response: -0.195499
- IL6/JAK/STAT3: -0.191306
- complement: -0.188156
- coagulation: -0.175802
- apoptosis: -0.155315
- IL2/STAT5: -0.147431

Largest gains include:
- fatty-acid metabolism: +0.702710
- spermatogenesis: +0.394100
- KRAS signaling down: +0.377056
- androgen response: +0.255877
- Hedgehog signaling: +0.205055
- oxidative phosphorylation: +0.178109
- estrogen response late: +0.155093

This pattern is consistent with a mixture in which some metabolic/endocrine programs retain useful methylation-to-RNA predictability while several inflammatory/immune/stromal-like programs are better captured by composition covariates or are poorly transported by the discovery multivariate mapping.

## Participant-level sensitivity

A post-hoc participant bootstrap of the frozen PCPG predictor outputs was run without refitting models or transforms.

Observed cancer-median difference (COVARIATE_ONLY minus ALL_METHYLATION_RIDGE): -0.069487.

Bootstrap 95% interval: approximately [-0.180, +0.096].
- P(difference > 0): 0.340
- P(difference < 0): 0.660

This means the PCPG direction is much less stable than the 18/19 pan-cancer sign result. It should be treated as a genuine frozen failure, but not as evidence of a large, precise PCPG-specific negative effect.

Leave-one-participant-out analysis:
- 29/30 leave-one-out samples retain a negative cancer-median difference.
- removing TCGA-RW-A681 alone flips the difference to +0.011217.

TCGA-RW-A681 therefore has unusually high influence on the exact median comparison.

### TCGA-RW-A681 diagnostic

Frozen covariates:
- ABSOLUTE purity: 0.98
- leukocyte fraction: 0.0280084

Relative to the 30 complete PCPG participants:
- methylation Hallmark score space: not an extreme outlier; no Hallmark exceeds |z|=2; multivariate standardized-distance rank 8/30
- RNA Hallmark score space: strongest multivariate outlier in the cohort; 21/50 Hallmarks exceed |z|=2 and one exceeds |z|=3; standardized-distance rank 1/30

For this participant ALL_METHYLATION_RIDGE loses to COVARIATE_ONLY on 45/50 Hallmarks. Large RNA deviations occur in NOTCH, WNT/beta-catenin, interferon-gamma, EMT, inflammatory response, IL6/JAK/STAT3, allograft rejection, complement, p53 and related programs, while methylation scores are not comparably extreme.

This is exactly the kind of sample for which a frozen methylation-to-RNA map can fail: RNA occupies a state not proportionally represented in the methylation projection.

No exclusion is permitted. The participant remains part of D4 and P3 rules must not be changed because of this observation.

## Semantic failure across all 19 cancers

The more important failure is not PCPG-specific. Hallmark-label specificity remains broadly unsupported.

Across 76 replication audit screens:
- RAW PRIMARY_PUBLICATION: 0/19 full semantic passes
- RAW MASKED_TECHNICAL: 1/19 full semantic passes, PRAD only
- ADJUSTED PRIMARY_PUBLICATION: 0/19
- ADJUSTED MASKED_TECHNICAL: 0/19

Patient-alignment effects are common, especially in raw data, but label-specific effects largely disappear under the frozen label null and composition adjustment. PRAD briefly crosses the semantic threshold on RAW MASKED_TECHNICAL (delta A_label 0.116331, p=0.025) but fails PRIMARY_PUBLICATION and both adjusted tracks. It therefore cannot be promoted.

This reinforces the D3 conclusion: there is reproducible patient-aligned/global cross-layer organization, but the data do not support a stable one-to-one Hallmark-label semantic interpretation.

## Other structured failures

### COAD
COAD is the only cancer failing both adjusted global screens:
- adjusted PRIMARY delta CKA 0.039789, p=0.075
- adjusted MASKED delta CKA 0.038366, p=0.050

Raw global structure passes both tracks. This suggests that much of COAD's raw cross-layer geometry is vulnerable to composition adjustment. COAD nevertheless remains GLOBAL_SHARED_ONLY under the frozen state logic because its raw global evidence is coherent and within-layer structure is present.

### PRAD
PRAD carries TECHNICAL_TRACK_DISAGREEMENT because RAW MASKED_TECHNICAL alone crosses the full semantic rule while PRIMARY_PUBLICATION and both adjusted screens do not. The correct interpretation is instability of semantic specificity to technical masking/composition, not positive semantic validation.

### Hallmark preservation
PCPG has the lowest discovery-to-replication positive-both Hallmark preservation fraction of all 19 cancers:
- PCPG: 10/45 = 0.2222
- next lowest LIHC: 15/45 = 0.3333
- range among the remaining cancers extends to HNSC 25/45 = 0.5556

This supports PCPG as a genuine transportability outlier at the Hallmark-effect level, independent of the single primary prediction metric.

## External biological context, not used to score D4

Published PCPG work provides a plausible biological reason to expect transport difficulty, but does not prove the cause of this D4 failure. TCGA integrated profiling divides PCPG into multiple molecular classes including kinase-signaling, pseudohypoxia, Wnt-altered and cortical-admixture groups. Later single-nucleus/bulk work reports even finer gene-expression subtypes and marked genotype, methylation, vascular, stromal and immune differences. Therefore a 30-case replication subset can contain substantial latent subtype heterogeneity that a single pan-PCPG discovery mapping does not model explicitly.

PCPG is also known for relatively sparse lymphocyte infiltration with macrophage/stromal variation, making the very low leukocyte fraction observed here biologically plausible. However, no TCGA molecular-subtype annotation for TCGA-RW-A681 was established in this diagnostic, so assigning that participant to a particular PCPG subtype would be speculation.

## Scientific disposition

1. Keep PCPG as a frozen D4 failure. Do not remove RW-A681.
2. Do not tune the P3 architecture, thresholds, predictors, or refusal rule in response.
3. Preserve PCPG as a named prospective stress case for FINAL_HOLDOUT.
4. Preserve the broader semantic failure as a central result, not a nuisance.
5. For later external validation, pre-specify PCPG molecular subtype/genotype stratification if such annotations are available before outcomes are inspected. That would test whether transport failure is subtype-conditioned rather than globally PCPG-specific.
6. The strongest current tool claim remains: frozen methylation-derived prediction adds held-out value over composition covariates in 18/19 cancer types, while semantic Hallmark-label specificity does not generalize robustly and the architecture correctly refuses one unstable cancer.
