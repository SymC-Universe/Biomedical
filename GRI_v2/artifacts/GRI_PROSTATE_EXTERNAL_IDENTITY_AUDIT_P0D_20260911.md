# GRI prostate external cross-modality identity audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / IDENTITY QUALIFICATION  
**Scientific outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

Study: `Race-specific coregulatory and transcriptomic profiles associated with DNA methylation and androgen receptor in prostate cancer`

Source series:

- `GSE262522` — HumanMethylation450, 68 samples;
- `GSE262524` — MethylationEPIC, 53 samples;
- `GSE237995` — RNA-seq, 121 samples.

The GEO source records give the same overall study design of 58 AA samples (31 tumor, 27 adjacent) and 63 EA samples (31 tumor, 32 adjacent), total 121.

## Identity reconstruction rule

Use the exact GEO sample **Title** string as the cross-modality identity key, preserving:

`PT-<participant>_<T|NT>_<AA|EA>`

No fuzzy matching, participant-only fallback, row-order assumption, value-based matching, or outcome-dependent selection was used.

The 68 HumanMethylation450 titles and 53 EPIC titles were transcribed from the complete GEO series sample lists, combined as exact strings, and compared against the complete 121-title RNA-seq series list.

## Result

```text
GSE262522_450K_TITLE_COUNT = 68
GSE262524_EPIC_TITLE_COUNT = 53
METHYLATION_UNION_TITLE_COUNT = 121
GSE237995_RNA_TITLE_COUNT = 121

METHYLATION_450K_EPIC_TITLE_OVERLAP = 0
METHYLATION_RNA_INTERSECTION = 121
METHYLATION_ONLY = 0
RNA_ONLY = 0

EXACT_CROSS_MODALITY_TITLE_BIJECTION = PASS
```

Therefore every source-listed methylation sample title has one source-listed RNA sample title with the exact same participant/tissue/race identity string, and every source-listed RNA title has one methylation counterpart across the union of the 450K and EPIC arms.

## Important structure retained

The 450K and EPIC arms are disjoint by exact sample title. They partition the 121 methylation measurements rather than duplicating the same sample titles across platforms.

The source family contains both tumor (`T`) and adjacent non-tumor (`NT`) samples. Some participants have only one tissue state in the source list, and no synthetic counterpart is invented. Exact title matching preserves those source asymmetries automatically.

## Platform context

The published study methods report harmonization of the 450K and EPIC methylation arrays on 449,636 shared probes before downstream analysis. That provides an independently published platform-harmonization route, but any GRI implementation must still reconstruct and freeze its own source/probe gate before biological evaluation rather than assuming the published processed object is automatically equivalent to the GRI representation.

## Protocol interpretation

This result upgrades the source family from `PENDING_EXACT_ID_OVERLAP` to:

`EXACT_CROSS_MODALITY_IDENTITY_PASS`

and supports its use as a high-priority **candidate** for:

- `NOMINAL_FUNCTION` external static architecture mapping;
- platform-transport Function/Limit mapping across 450K and EPIC;
- tumor-versus-adjacent context mapping;
- future Regulatory Substrate Atlas construction.

It does **not**:

- select this cohort as the decisive P1 test;
- inspect any GRI result on this cohort;
- freeze a comparator or endpoint;
- establish external GRI validity;
- establish clinical utility;
- establish biological chi;
- convert the source family into confirmatory evidence.

## Current state

`SOURCE_IDENTITY_GATE = PASS`

`CROSS_MODALITY_TITLE_BIJECTION = 121_OF_121`

`PLATFORM_PARTITION = 68_450K_PLUS_53_EPIC`

`OUTCOME_STATUS = UNOPENED_FOR_GRI_P1_PURPOSES`

`RESEARCH_STATUS = P0_D_SOURCE_QUALIFIED_CANDIDATE`

## Next non-outcome source gates

Before any future scientific freeze/use:

1. verify exact downloadable processed/raw file identities and hashes;
2. reconstruct 449,636-shared-probe platform intersection from the actual source files or a frozen documented equivalent;
3. verify gene/RNA identifier convention and expression preprocessing;
4. preserve tumor/adjacent and AA/EA metadata separately;
5. audit missingness and sample support without evaluating GRI performance;
6. define whether a future use is Atlas construction, P0-D Function/Limit mapping, or a separately frozen P1 test.
