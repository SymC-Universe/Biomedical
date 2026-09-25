# Kizilirmak context-gating diagnostic implementation amendment

**Date:** 25 September 2026  
**Parent freeze:** `KIZILIRMAK2023_CONTEXT_GATE_DIAGNOSTIC_FREEZE_20260925.md`

## Source-native first-peak implementation

- Smooth each single-cell NCI trace using the MATLAB `smooth` default equivalent: centered 5-point moving average with shortened endpoint spans.
- Detect peaks using local prominence (q>0.15), matching the source.
- The early-activation value for a cell is the NCI value at the **first detected real peak**.
- Cells with no detected real peak are excluded from the first-peak summary but remain in the oscillatory-fraction denominator.
- Clone-level first-peak value is the median across cells with a detected peak.

## Frozen source-rank adjudication

**TNF-alpha**
- Source-native limiting receptor: `Tnfrsf1a`.
- Untreated receptor mean must rank `B > R > G`.
- Reproduced median first-peak value must rank `B > R > G` for a full rank match.

**IL-1beta**
- Source-native limiting receptor: `Il1rap`.
- The source states `B approximately G > R`, with B-G not significantly different.
- Therefore the frozen test does **not** demand a B-vs-G ordering.
- It requires R to be the lowest receptor-mean clone and the lowest median-first-peak clone, with B and G occupying the top two positions in both.

If both stimulus-specific tests pass, classify `CONTEXT_GATING_LIMIT_OF_GLOBAL_STATIC_SCALAR`. Otherwise classify `CONTEXT_GATE_EXPLANATION_INCOMPLETE`.

No fitted model, combined score, or post-result weighting is permitted.
