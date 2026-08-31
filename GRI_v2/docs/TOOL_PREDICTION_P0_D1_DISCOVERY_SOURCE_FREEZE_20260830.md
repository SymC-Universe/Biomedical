# P0 D1 discovery-only methylation source preprocessing freeze

**STATUS: FROZEN AFTER P0 SAMPLE ELIGIBILITY PASS AND BEFORE D1 SOURCE-FEATURE RESULTS**

Date: 2026-08-30

Eligibility audit anchor: `GRI_v2/artifacts/P0_ELIGIBILITY_AUDIT_20260830.md`

This D1 gate implements the next already-authorized P0 step without opening predictive RNA target values or either held-out methylation partition.

## Scope

D1 is source-side preprocessing only. It operates on the 4,863 eligible DISCOVERY participants belonging to the 19 cancers that already passed the frozen >=30-per-partition P0 eligibility rule:

`BLCA, BRCA, CESC, COAD, HNSC, KIRC, KIRP, LGG, LIHC, LUAD, LUSC, OV, PAAD, PCPG, PRAD, SARC, STAD, THCA, UCEC`.

The remaining cancers are not rescued or rebalanced. The fixed P0 pan-cancer promotion floor remains unreachable, so future P0 pan-cancer aggregates remain descriptive only.

## Frozen source operations

Within each cancer's eligible DISCOVERY partition:

1. retain a PRIMARY_PUBLICATION probe only when at least 95% of DISCOVERY samples are finite;
2. freeze the imputation value as the median across finite DISCOVERY values for that probe;
3. define MASKED_TECHNICAL as the exact intersection of the DISCOVERY-retained PRIMARY_PUBLICATION probes with the already-frozen C1A 579-probe technical mask;
4. use `PROMOTER_CORE = TSS200` as the P0 source regulatory stratum;
5. per sample and gene, compute the median across unique retained TSS200 probes mapped to that gene;
6. count a methylation Hallmark as mapping-eligible only when it has at least 10 mapped genes and at least 10 contributing methylation probes;
7. fit Hallmark PC1 centering and loadings in DISCOVERY only;
8. orient PC1 so its DISCOVERY correlation with the sample-wise unweighted Hallmark gene mean is nonnegative; if that correlation is exactly zero or undefined, orient the largest-absolute loading positive.

The exact Stage C1A annotation and technical-mask lineage remains frozen. Multi-gene TSS200 probes may contribute to every annotation-supported gene, but each probe contributes at most once to a given gene. No nearest-gene invention is permitted.

## Pre-result undefined-PC1 rule

P0 previously fixed the PC1 representation but did not need to specify behavior for a mathematically undefined zero-variance Hallmark. Before D1 real source-feature outputs are inspected, the behavior is now concretized:

- if a mapping-eligible Hallmark has no finite nonzero centered variance from which a PC1 can be identified, record `NOT_EVALUABLE_ZERO_OR_INVALID_VARIANCE`;
- do not substitute a mean score, alternative component, regularized direction, or another coordinate;
- retain the Hallmark's mapping-eligibility result separately from its PC1 evaluability status.

This is a refusal rule for an undefined computation, not a new biological threshold or a result-dependent rescue.

## Leakage firewall

D1 may read methylation beta values for **DISCOVERY only**.

D1 must not read or use:

- REPLICATION methylation beta values;
- FINAL_HOLDOUT methylation beta values;
- RNA expression/Hallmark predictive target values;
- survival, treatment, recurrence, subtype, genomic outcome, RPPA outcome, or historical GRI result;
- biological chi, damping, EP, optimum, or preferred SymC pattern.

The exact 5.02 GB methylation source is hash-verified before the D1 stream. The Hallmark membership snapshot is also hash-verified before construction.

## Required outputs

D1 produces:

- per-cancer probe retention and DISCOVERY imputation medians;
- per-cancer/per-track Hallmark mapping and PC1 evaluability;
- DISCOVERY-fitted methylation Hallmark PC1 transform definitions;
- DISCOVERY methylation Hallmark PC1 scores;
- explicit source/partition/no-target guard fields and artifact hashes.

## Claim ceiling

D1 can establish only **DISCOVERY-only methylation preprocessing and source-feature construction**. It cannot establish cross-layer prediction, replication, selective prediction/refusal performance, a biological mechanism, clinical utility, causal direction, temporal dynamics, biological chi, or a promoted pan-cancer statement.

## Next gate after a clean D1 audit

Freeze and regression-test the real RNA target-construction and discovery audit/model implementation before any held-out target evaluation. No P0 threshold, null, state rule, partition, or Stage C1 assumption may be changed in response to D1 results.
