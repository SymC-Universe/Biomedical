# GRI DoRothEA upstream-source provenance boundary

**Date:** 2026-09-13  
**Mode:** P0-D provenance qualification only  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.5  
**Architecture:** approved A3 + B3 + C3  
**Chi_bio:** `NOT_ADMITTED`

## Purpose

This record advances the DoRothEA branch of B3 as far as possible without making a hidden scientific, licensing, or cohort-independence choice. It freezes the exact upstream repository identities and records why a canonical empirical export is not yet licensed.

## 1. Pinned upstream identity

Repository:

`saezlab/dorothea`

Pinned commit:

`1461fb75e23e110c2281860526d4333920925282`

Relevant human data objects at that commit:

- general human object `data/dorothea_hs.rda`, Git blob `75c9c0b6f9e9cfc6c34f86e2e0bf0b055ce1d9d9`, 894,668 bytes;
- pancancer human object `data/dorothea_hs_pancancer.rda`, Git blob `f0289d0126281d7d64e04889149d3dc674cabc7e`, 469,992 bytes;
- full provenance-rich database `data/entire_database.rda`, Git blob `ea3eeec1f2fdd490cee4db7cd554fb48034ed0d7`, 2,787,988 bytes.

Repository documentation describes `dorothea_hs` as signed human TF-target interactions with confidence classes A through E, covering 1,395 TFs, 20,244 target genes, and 486,676 unique interactions.

## 2. Important cohort-independence distinction

The repository documentation states that the cancer-oriented `dorothea_hs_pancancer` differs from the general human object because TCGA gene-expression data was used instead of GTEx to infer the ARACNE component.

That matters directly for this GRI program. A DoRothEA sensitivity intended to challenge a TCGA-based GRI representation must not silently become partially TCGA-trained merely because the object is named `pancancer`.

Therefore:

`dorothea_hs_pancancer = NOT_SELECTED`

This is not a permanent rejection. Any later use requires an explicit independence adjudication before empirical outcome inspection.

## 3. License boundary

The pinned repository README states that the standard DoRothEA resource is intended only for academic use because some incorporated resources do not permit commercial use. It also points to a separate non-academic branch from which restricted resources are removed.

The current decoupler 2.2.0 wrapper makes `license` an explicit network-construction parameter. Thus `academic` versus another allowed route is not harmless download plumbing: it can change the returned network.

This record does not decide organizational license eligibility.

## 4. Confidence and weighting boundary

The pinned decoupler 2.2.0 wrapper also makes confidence levels and confidence weighting explicit construction parameters. If called with defaults it selects A/B/C and uses confidence divisors A=1, B=2, C=3, but those defaults are not automatically scientific approval.

Consequently this record does **not** freeze:

- confidence classes;
- confidence weights;
- exact source object;
- canonical exported edge set;
- TF panel;
- activity-scoring method;
- state dimension.

## 5. Firewall status

No SCC25 molecular matrix was opened for this decision. No TCGA expression was inspected to select the DoRothEA variant. No TF activity, operator, G1, G2, or Chi_bio value was computed.

Promotion effect: `NONE`.

## 6. Disposition

`PASS_UPSTREAM_SOURCE_IDENTITY_CANONICAL_EXPORT_BLOCKED_PENDING_LICENSE_CONFIDENCE_AND_OBJECT_FREEZE`

The useful result is not a chosen DoRothEA network. It is a clean boundary:

1. upstream identities are now immutable and reproducible;
2. the TCGA-derived pancancer object is flagged before it can contaminate an independence test;
3. licensing and confidence choices are exposed as real decisions rather than hidden software defaults;
4. exact canonical-export hashing can proceed immediately after those choices are prospectively frozen.

## 7. Next allowed action

Resolve, prospectively and without candidate outcomes:

1. permissible license route;
2. general human versus any alternative source object, with cohort-independence justification;
3. allowed confidence classes;
4. confidence weighting;
5. exact export transformation.

Only after that freeze should the exact DoRothEA export be acquired and byte-hashed.
