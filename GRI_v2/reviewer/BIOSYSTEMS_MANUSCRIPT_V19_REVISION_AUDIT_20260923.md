# BioSystems manuscript v19 revision audit - 23 September 2026

**Status:** COMPLETE / PRIVATE READ-THROUGH CANDIDATE  
**Branch:** `biosystems-manuscript-v19-20260923`  
**Scientific parent:** `biosystems-meat-bone-v18-20260923`  
**GOM authority:** SymC General Operations Manual v0.8.6, with the user's project-specific clarification that the lay explanation map is an internal evaluation artifact and is not part of the BioSystems submission package.

## Purpose

Revise the reader-facing main manuscript without reopening scientific analysis.

No dataset, endpoint, null, threshold, denominator, multiplicity family, cohort, seed, or interpretation rule changed.

## Changes

1. Abstract reduced to **133 words**, below the requested 150-word ceiling.
2. Abstract retains the current claim ceiling:
   - H1 is the strongest cross-source result;
   - tumor-normal RNA contrasts remain composition-unadjusted;
   - external H2/H3a show no detectable transport;
   - causality, recovery dynamics, treatment response, tumor-cell-intrinsic effects, and clinical utility are not established.
3. Main manuscript moved to the GOM default **11 pt / 1-inch margin** working layout.
4. `natbib` numeric citation handling and hidden hyperlink styling were enabled.
5. The three bibliography entries left unused after the meat/bone trim now have explicit scientific roles:
   - Gevaert 2015 and Kim 2020 support the motivation for separating within-methylation covariance from methylation-expression coupling;
   - Ding 2021 supports the statistical-testing interpretation of representation similarity.
6. Bibliography audit now returns **18 cited / 18 present / 0 unused / 0 missing**.
7. Data and code availability now points to immutable scientific snapshot `biosystems-meat-bone-v18-20260923` rather than the superseded final-polish branch.
8. Supplementary Information remains v15 and scientifically unchanged.
9. No lay explanation material was inserted into the manuscript or supplement. The lay map remains an internal Atlas evaluation artifact only.

## Private files

Main:
- `GRI_BioSystems_working_v19_R1_2026-09-23.tex`
- SHA-256 `a47bcf91301c409121e9459cf9a0fabeafd93bedd8940eeca0979068d685dfd4`
- `GRI_BioSystems_working_v19_R1_2026-09-23.pdf`
- SHA-256 `3ffc102717b90bbbc6f1563e80167d5af159007e90eb59fcb212b152085444a2`
- 13 pages
- abstract: 133 words

Private read-through package:
- `BioSystems_Resubmission_v19_Readthrough_20260923.zip`
- SHA-256 `b41305df5c3f317ef876811fd79c319e54200417f2a9c66849056a3769871826`

## QA

- PDF compiled twice successfully.
- PDF preflight: 13 pages, openable, searchable, non-encrypted, not scanned.
- Rendered all 13 pages at 150 dpi.
- First page, figure-bearing body pages, Data/Code page, and references were visually inspected.
- No clipping, black boxes, broken glyphs, or figure overflow observed.
- Main source contains no en dash or em dash characters.
- No first-person authorial prose was found; the only single-letter "I" hit is within a cited article title/author string.

## Scientific disposition

This is a manuscript presentation revision only.

**STATUS: COMPLETE / READY FOR USER READ-THROUGH**
