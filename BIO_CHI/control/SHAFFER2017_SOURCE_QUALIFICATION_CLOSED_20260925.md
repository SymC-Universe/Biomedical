# Shaffer 2017 GRI ↔ Bio Chi checkpoint

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** SOURCE/CARRIER QUALIFICATION CLOSED / METHOD-SELECTION GATE OPEN

GSE97679 and GSE97681 source qualification is now complete at the metadata/carrier level.

GSE97679 established a 63,682-gene common universe across both processed RNA runs, with all primary timepoint/population sample identifiers mapped and week-1 represented in both sequencing runs.

GSE97681 now independently passes the processed-source metadata audit. All five processed count tables are retrievable, all contain the same 63,682-gene universe and gene-set hash as GSE97679, and the source sample identities mechanically support the pre-frozen evidence roles:

- WM989 contains paired drug/no-drug material plus 48-hour and 7-day holiday states suitable for source-internal perturbation/recovery validation after the method is frozen.
- WM983B contains paired drug/no-drug material and longitudinal drug-state records including week 1, week 3, and week 5, suitable for same-source cross-cell-line transport after the method is frozen.
- These remain same-publication evidence and are not external confirmation.

No gene-effect statistic, resistance-marker selection, modal calculation, B2/B3 endpoint, or chi_bio calculation was used to qualify the sources.

The remaining gate is no longer source access. It is scientific method selection: count filtering, normalization/batch treatment, modal construction, the exact B2 statistic, comparator choice, and validation endpoint must be chosen from native-method review before target expression effects are opened.

Next safe work is literature/source-method review and preparation of candidate methods. Promotion of one candidate to the authoritative analysis freeze is science-adjacent and must be explicitly adjudicated rather than silently chosen.
