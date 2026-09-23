# BioSystems HCI-005 decitabine intervention v0.1 result audit

**Date:** 23 September 2026  
**Status:** `P0_D_INTERVENTION_CONSISTENT_COUPLING_SUPPORTED`  
**Workflow run:** `35893879712`  
**Workflow head:** `82806b030348190eb9d96b5bf92ce34d5f929138`  
**Artifact:** `10766370550`  
**Artifact digest:** `sha256:ddd68fc0159b3c41b4e1aa73baad96d980f5abd2fe60430f4cf36eea01e06c2c`

## Source qualification

HCI-005 endocrine-resistant breast-cancer PDX:
- methylation: GEO `GSE171069`, 4 vehicle + 4 decitabine EPIC samples;
- RNA: GEO `GSE171073`, 4 vehicle + 4 decitabine RNA-seq samples;
- same treatment design / matched multiomic tumor cohort;
- source-native RNA annotation: GENCODE v33.

Frozen source hashes:
- methylation series matrix: `65ee8783e9d47f568a94a35944719c1aae1df0c693150dd2bcdba44b876c55ad`;
- RNA count table: `1cbd6826074498a57025124da0a2857f1248338b21aaf1e3034cea48c7f68397`;
- GENCODE v33 GTF: `4e8afc75f90821668b0a8f45a33c31a792b4b4f754621d76ad9e50b0492a3a89`;
- C1 probe carrier: `589365b92797f6e0ea479b75437c44ed86327cfc86b3e7caf7df01b4be2bcdd9`.

Identifier-only qualification before value opening mapped 60,550 RNA Ensembl identifiers to symbols and found 3,487 genes overlapping the frozen promoter-gene namespace.

## Frozen test

### Manipulation check

Across C1 probes finite in all eight samples:

`median_probe[mean(Decitabine beta) - mean(Vehicle beta)]`

was tested against all `C(8,4)=70` treatment assignments.

### Gene-matched coupling

For each frozen promoter-core gene:
- methylation object = per-sample median beta over retained mapped C1 promoter probes;
- RNA object = GENCODE-v33 symbol counts, duplicate Ensembl-to-symbol mappings summed, DESeq-style median-ratio normalization, then `log2(normalized_count+1)`;
- gene delta = Decitabine group mean minus Vehicle group mean.

Primary coupling:
Spearman correlation across genes between promoter-methylation delta and RNA delta.

Two frozen nulls:
1. `B=9,999` deterministic RNA gene-identity permutations;
2. all 70 synchronous treatment-label assignments across the eight multiomic tumor identities.

Support required:
- measurable demethylation on the C1 carrier;
- negative gene-matched rho;
- gene-identity p <= 0.05;
- treatment-assignment p <= 0.05.

## Result

- retained C1 probes: **21,439**
- RNA symbols after GENCODE mapping/aggregation: **60,520**
- size-factor genes: **25,317**
- matched promoter/RNA analysis genes: **3,317**

Manipulation:
- global C1 methylation delta = **-0.002252595**
- exact treatment-assignment p = **0.0285714**
- manipulation gate: **PASS**

Gene-matched methylation/RNA coupling:
- Spearman rho = **-0.1073377**
- gene-identity permutation p = **0.0001**
- exact synchronous treatment-assignment p = **0.0285714**
- coupling gate: **PASS**

## Interpretation

This result supports **intervention-consistent inverse promoter-demethylation/RNA coupling in one decitabine-treated endocrine-resistant breast-cancer PDX model**.

The result is stronger than cross-sectional correlation because the methylation layer was directly perturbed pharmacologically and both the methylation manipulation and gene-matched RNA relation survive frozen nulls.

It does **not** establish:
- that methylation change is locally causal for every individual gene;
- a pan-cancer methylation-to-RNA causal law;
- that the TCGA H2/H3a signal is entirely causal;
- clinical treatment-response prediction;
- diagnostic or prognostic utility;
- a biological chi or universal dynamical boundary.

The negative SCC25 temporal-direction result remains part of the evidence record and is not overwritten by this positive intervention result.

## Epistemic class

`P0_D_POSTRESULT_DIRECT_INTERVENTION_SUPPORT`

This result may narrow the manuscript's blanket causal nonclaim if clearly labeled as a post-result external intervention extension. It does not become part of the original untouched C1/P1 confirmatory spine.
