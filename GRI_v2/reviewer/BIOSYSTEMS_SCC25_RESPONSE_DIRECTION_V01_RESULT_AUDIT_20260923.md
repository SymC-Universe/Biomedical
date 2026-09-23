# BioSystems SCC25 cetuximab response/direction v0.1 result audit

**Date:** 23 September 2026  
**Status:** `P0_D_COMPLETE__E2_NOT_RESOLVED__E3_DIRECTION_NOT_SUPPORTED`  
**Workflow run:** `35892303709`  
**Workflow head:** `6f36e677324c784a639915e2fab9b362165929f8`  
**Artifact:** `10765188120`  
**Artifact digest:** `sha256:56c1fb018dd7220c8327a11fe455977e0c8436bb295162879c8923e3dd7560c2`

## Source

Hash-bound SCC25 weekly paired cetuximab sources:
- RNA: `GSE98812_GEOExprsData.txt.gz`, SHA-256 `1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5`;
- methylation: `GSE98813_series_matrix.txt.gz`, SHA-256 `c5ee581ee6dbb258bb352e86fd1a7aa5ed6f9979550352accaeca8b0d093292e`.

The first attempt failed mechanically because the processed RNA table uses source-native generation names rather than GSMs. The mapping `C1.PBS/C1.100nM ... C11.PBS/C11.100nM` was recovered from the older outcome-free source audit and bound to the frozen GSM manifest before rerunning. No endpoint, phase, statistic, or decision rule changed.

Source-defined phases:
- weeks 1-3: sensitive;
- weeks 4-8: resistance acquisition;
- weeks 9-11: late/stable resistant.

## E2 treatment-response architecture

Frozen observables:
- methylation distance = median absolute CTX-minus-PBS beta difference across C1 probes with finite support in all 22 weekly states;
- RNA distance = median absolute CTX-minus-PBS robust-z expression difference after fixed SYMBOL mapping/duplicate aggregation.

Methylation distances by week:
`0.00975, 0.01153, 0.01138, 0.01096, 0.01397, 0.01379, 0.01310, 0.01737, 0.01556, 0.01445, 0.01584`.

RNA distances by week:
`1.11991, 0.94330, 0.92511, 1.00412, 0.94905, 0.95263, 1.09666, 1.17209, 1.06824, 1.07435, 1.12857`.

Exact phase tests preserving the frozen 3/5/3 group sizes:
- methylation: Kruskal-Wallis H = `5.5030`, exact p = `0.05325`, BH q = `0.10649`;
- RNA: H = `1.8667`, exact p = `0.42489`, BH q = `0.42489`.

Frozen E2 support rule: **FAIL / NOT RESOLVED**.

The methylation distance shows a visually increasing late-course displacement, but the predeclared phase test does not cross the multiplicity-controlled decision rule and may not be rescued by a post-result trend test for the current claim.

## E3 temporal methylation-to-RNA direction

Support:
- 22,600 C1 methylation probes finite across all weekly states;
- 15,938 RNA genes after fixed symbol/MAD gate;
- 3,349 genes with both promoter-core methylation mapping and RNA support.

For each of the ten transitions, the primary comparison used absolute gene-wise Spearman association:
- forward = methylation(t) -> RNA(t+1);
- reverse = RNA(t) -> methylation(t+1).

Forward absolute rho:
`0.0028, 0.0189, 0.0114, 0.0031, 0.0033, 0.0447, 0.0153, 0.0489, 0.0524, 0.0396`.

Reverse absolute rho:
`0.0060, 0.0049, 0.0219, 0.0018, 0.0295, 0.0193, 0.0662, 0.0147, 0.0363, 0.0490`.

Primary mean forward-minus-reverse = `-0.0009029`.

Exact one-sided within-transition direction-swap p = `0.53906` over all 1,024 swaps.

Frozen E3 support rule: **FAIL**.

## Interpretation

This SCC25 trajectory does not establish that the frozen molecular distances track the published treatment-response phase under the predeclared phase test, and it supplies no evidence that methylation has stronger week-ahead directional association with RNA than the reverse direction.

The negative E3 result is particularly important: the current BioSystems manuscript must not upgrade its cross-sectional methylation-RNA coupling into a causal methylation-to-RNA claim from this trajectory.

A separately qualified direct methylation intervention can still test an intervention-consistent causal route. That follow-up is a new P0-D lane and may not retune the SCC25 result.

## Claim consequence

- treatment-response utility: **NOT ESTABLISHED** by E2;
- temporal methylation-to-RNA direction: **NOT SUPPORTED** by E3;
- SCC25 failures remain part of the record and are not hidden by later intervention results.
