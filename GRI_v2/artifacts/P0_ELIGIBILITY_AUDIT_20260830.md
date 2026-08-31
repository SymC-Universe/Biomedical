# P0 sample-eligibility audit

Date: 2026-08-30

Status: **PASS — P0 sample eligibility closed**

Upstream split anchor:

- `p0_preeligibility_split_manifest.csv` SHA-256: `12b85d67d06e57c6d1be914444c65aa526f2b821e117725dd036142cc6b0a825`
- frozen matched universe: 9,460 participants across 32 cancers
- partition reassignment remains forbidden

Returned eligibility artifacts:

- `P0_ELIGIBILITY_SUMMARY.json` SHA-256: `31e096f18bdf1cc4af72a95685daf248c40daa86c3af836478a89d4b0ebd7ff0`
- `p0_sample_eligibility.csv` SHA-256: `4a906d2d80ab36af0cc1dc8f9d8dcb834cfc717021a355c78c089f5cc665e3c2`
- `p0_partition_eligibility_counts.csv` SHA-256: `78e859cb5a74ee71e4eb8318c1995dcbcc780a5cfeb996d9cf4c53cf23886640`

## Independent reconstruction

The returned files were independently reconstructed before this audit was recorded.

- sample rows: **9,460 / 9,460**
- participant-root uniqueness: **PASS**
- methylation-sample-root uniqueness: **PASS**
- deterministic P0 split reconstruction mismatches: **0**
- frozen partition counts reconstructed exactly: DISCOVERY 5,643; REPLICATION 1,888; FINAL_HOLDOUT 1,929
- eligibility-rule mismatches: **0**
- frozen per-sample rule: at least 95% finite across exactly 22,601 PRIMARY_PUBLICATION probes
- corresponding minimum finite-probe count: **21,471**
- methylation probe rows observed: **22,601**
- count-table field mismatches after reconstruction from the sample-level file: **0**

## Eligibility outcome

- eligible participants: **9,457 / 9,460**
- ineligible participants: **3**

The three ineligible samples are retained as negative QC outcomes rather than silently removed from provenance:

- BRCA / `TCGA-C8-A134` / FINAL_HOLDOUT / 20,695 finite probes
- LUSC / `TCGA-37-3789` / FINAL_HOLDOUT / 21,208 finite probes
- OV / `TCGA-23-1027` / DISCOVERY / 21,240 finite probes

Exactly **19 cancers** satisfy the already-frozen requirement of at least 30 eligible participants independently in DISCOVERY, REPLICATION, and FINAL_HOLDOUT:

`BLCA, BRCA, CESC, COAD, HNSC, KIRC, KIRP, LGG, LIHC, LUAD, LUSC, OV, PAAD, PCPG, PRAD, SARC, STAD, THCA, UCEC`

The eligible DISCOVERY counts in those 19 cancers sum to **4,863**.

The 13 non-fully-evaluable cancers remain excluded from the fully evaluable P0 branch under the frozen rule. No cancer is rebalanced, rescued, or reassigned.

## Pan-cancer promotion ceiling

The P0 protocol requires at least 24 fully evaluable cancers for a promoted pan-cancer predictive statement. Only 19 can qualify under the already-frozen split and eligibility result.

Therefore:

- `pan_cancer_promotion_possible_under_p0 = false`
- any P0 pan-cancer aggregate is **descriptive only**
- the 24-cancer floor is **not** changed after seeing this result

This is a consequence of the frozen design, not a software failure.

## Leakage / claim audit

The eligibility run reports and the returned artifacts are consistent with the following:

- methylation beta values were read only to count per-sample finite values for the frozen eligibility rule;
- predictive target values were not read;
- RNA Hallmark target values were not read;
- no biological association was performed;
- no biological chi coordinate was used;
- no partition reassignment occurred;
- Stage C1 science was not modified.

## Next gate

Advance only the 19 fully evaluable cancers to **DISCOVERY-only source preprocessing**:

1. retain methylation probes per cancer using the frozen DISCOVERY >=95% finite rule;
2. freeze each retained probe's DISCOVERY finite-sample median for later imputation;
3. construct PRIMARY_PUBLICATION and frozen MASKED_TECHNICAL source tracks;
4. construct PROMOTER_CORE / TSS200 gene scores and methylation Hallmark PC1 representations using DISCOVERY only;
5. do not read REPLICATION or FINAL_HOLDOUT methylation values in this D1 gate;
6. do not read RNA predictive target values in this D1 gate;
7. audit the resulting source transforms before opening the next target/model gate.

No P0 endpoint, null, threshold, partition, or Stage C1 assumption is changed by this audit.
