# P0 D2 RNA DISCOVERY target-construction freeze

**STATUS: FROZEN AFTER D1 CLOSED PASS AND BEFORE REAL P0 RNA TARGET VALUES ARE CONSTRUCTED OR INSPECTED**

D1 audit anchor: `GRI_v2/artifacts/P0_D1_DISCOVERY_SOURCE_AUDIT.md`

This gate implements only the RNA target side of the already-frozen P0 predictive protocol. It does not evaluate prediction, replication, selective prediction, biological chi, clinical outcomes, or Stage C1 biology.

## Scope

D2 operates only on the same 4,863 eligible DISCOVERY participants in the same 19 fully evaluable cancers closed at D1:

`BLCA, BRCA, CESC, COAD, HNSC, KIRC, KIRP, LGG, LIHC, LUAD, LUSC, OV, PAAD, PCPG, PRAD, SARC, STAD, THCA, UCEC`.

Participant identity is taken from the already-audited D1 DISCOVERY score table and is matched to the exact frozen Stage A Hallmark-union RNA cache by cancer plus participant root. No participant is added, reassigned, substituted, or rebalanced.

## Frozen upstream identities

- Stage A Hallmark-union RNA cache SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`.
- Hallmark membership SHA-256: `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`.
- D1 DISCOVERY methylation score SHA-256: `593d565085b797e8abfcf22c56b406c96edbdba59eac48fb57db62c90ffabed3`.
- D1 Hallmark eligibility SHA-256: `3a50c347f5713ca1415c18573736f6ba75a7ae6f347aa62709ae04be8682ab69`.

The D2 implementation may not substitute the full raw RNA source, a different cache, a different Hallmark release, historical GRI modules, or a result-selected target definition.

## RNA source representation

The P0 target uses the exact frozen Stage A cache field `expression_log2p1`, whose source transform was frozen before the P0 target experiment. D2 does not redefine that source transform.

P0 target PC1 is a separate leakage-controlled predictive target representation and does not replace the Stage A/Stage C1 network eigengene.

### Discovery RNA gene eligibility

Within each cancer's exact eligible DISCOVERY participant set, an RNA Hallmark gene is retained for D2 only when all of the following hold:

1. the gene exists in the exact frozen Hallmark-union cache and exact frozen Hallmark membership snapshot;
2. at least 95% of that cancer's DISCOVERY values are finite;
3. at least 20 DISCOVERY values are finite, preserving the already-frozen Stage A minimum-finite-sample safeguard;
4. the finite DISCOVERY values have strictly positive variance.

The 95% and 20-sample rules are inherited from the already-frozen Stage A RNA missingness policy. They are not chosen from P0 target behavior.

### Hallmark target eligibility

A D2 RNA Hallmark target is mapping-eligible only when at least 10 retained RNA genes remain in DISCOVERY. The value 10 is inherited from the already-frozen P0 Hallmark minimum and is frozen here before target values are constructed.

The semantic P0 branch uses only Hallmarks that are simultaneously:

- D1 methylation mapping-eligible on the relevant technical track; and
- D2 RNA mapping-eligible and PC1-evaluable.

At least 25 common eligible Hallmarks remain required for the full semantic branch. No Hallmark is replaced to meet that floor.

## Discovery-only target PC1

For every D2 mapping-eligible cancer/Hallmark:

1. compute each retained RNA gene's finite DISCOVERY mean;
2. impute any remaining DISCOVERY missing value with that same discovery finite mean;
3. center each gene using the frozen discovery mean;
4. do **not** variance-standardize the target genes for this P0 PC1, because the already-frozen P0 section 4.3 specifies an analogous centered source/target PC1 construction; the separate Stage A network eigengene remains unchanged;
5. fit PC1 using DISCOVERY only;
6. orient PC1 so its DISCOVERY correlation with the sample-wise unweighted mean of the retained uncentered RNA gene values is nonnegative;
7. if that orientation correlation is exactly zero or undefined, orient the largest-absolute loading positive.

The fitted discovery means and loadings are the only RNA transform parameters licensed for later REPLICATION and FINAL_HOLDOUT projection.

## Undefined-PC1 refusal

Before any real D2 target value is constructed, the following refusal behavior is frozen:

- if a mapping-eligible RNA Hallmark has no finite nonzero centered variance from which a PC1 can be identified, record `NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE`;
- do not substitute a mean score, another component, regularized direction, or another coordinate;
- retain mapping eligibility separately from PC1 evaluability.

## Leakage firewall

D2 fitting and every reported D2 statistic use DISCOVERY participant values only.

The Stage A NPZ container may necessarily be opened to retrieve the frozen expression array, but REPLICATION and FINAL_HOLDOUT rows may not be selected into any D2 fit, summary, orientation calculation, feature decision, threshold, or diagnostic. No held-out target score is generated in D2.

D2 must not use:

- REPLICATION or FINAL_HOLDOUT prediction error;
- held-out target scores;
- survival, treatment, recurrence, subtype, genomic outcome, RPPA outcome, or historical GRI result;
- biological chi, damping, EP, optimum, or preferred SymC pattern.

## Required outputs

D2 produces only:

- per-cancer/Hallmark RNA mapping and PC1 evaluability;
- DISCOVERY-fitted RNA target means/loadings;
- DISCOVERY RNA Hallmark PC1 scores;
- common D1-source/D2-target Hallmark inventory by technical track;
- explicit identity/hash/leakage guard fields and artifact hashes.

## Claim ceiling

D2 can establish only a leakage-controlled DISCOVERY RNA target representation. It cannot establish cross-layer association, predictive performance, replication, selective prediction/refusal utility, biological mechanism, clinical utility, causal direction, temporal dynamics, biological chi, or a promoted pan-cancer statement.

## Next gate after clean D2 audit

Implement and regression-test the frozen DISCOVERY audit/state machinery and P1 discovery model fitting, including the already-frozen B1 composition covariates and deterministic 5-fold ridge selection, before any REPLICATION or FINAL_HOLDOUT target score is generated or evaluated.
