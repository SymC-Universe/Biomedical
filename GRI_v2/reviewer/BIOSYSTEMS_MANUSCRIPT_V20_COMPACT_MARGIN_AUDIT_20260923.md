# BioSystems manuscript v20 compact-margin repair - 23 September 2026

**Status:** COMPLETE / PRIVATE READ-THROUGH CANDIDATE  
**Branch:** `biosystems-manuscript-v20-compact-margins-20260923`  
**Scientific parent:** v19 reader-facing revision  
**Change class:** layout-only repair

## Purpose

Restore the compact manuscript margins used before the v19 GOM-formatting experiment while retaining 11 pt text and every scientific/textual revision introduced in v19.

## Exact layout change

v19:
`\usepackage[margin=1in]{geometry}`

v20:
`\usepackage[top=0.55in,bottom=0.72in,left=0.72in,right=0.72in]{geometry}`

No other manuscript content was changed.

## Effect

- v19 main: 13 pages
- v20 main: **11 pages**
- abstract remains **133 words**
- font size remains **11 pt**
- all 18 bibliography entries remain cited
- Data and Code pointer remains on the current immutable scientific snapshot

## Files

- `GRI_BioSystems_working_v20_R1_2026-09-23.tex`
  - SHA-256 `0e3ce82f7c4c287f2c96da57ec29d73f908dfcc4d6643398eddaf9e5943ba672`
- `GRI_BioSystems_working_v20_R1_2026-09-23.pdf`
  - SHA-256 `f30ec65c9c086098460642fb77be3236d2ace36adfb5775920c2ef19c330b8ad`
  - 11 pages
- `BioSystems_Resubmission_v20_Readthrough_20260923.zip`
  - SHA-256 `de8fb737d8a3b3a9baab327d1474f75fd0ad193d2905134491e81585bd9eab31`

## QA

- compiled twice successfully;
- PDF preflight: openable, searchable, non-encrypted, not scanned;
- all 11 pages rendered at 150 dpi;
- title/abstract page, figure-bearing Results page, and final references page visually inspected;
- no clipping, figure overflow, malformed glyphs, or layout break detected.

## Scientific disposition

**NO SCIENTIFIC CHANGE.**  
No endpoint, cohort, null, threshold, denominator, multiplicity family, claim, citation role, or interpretation was altered.

**STATUS: COMPLETE / READY FOR USER READ-THROUGH**
