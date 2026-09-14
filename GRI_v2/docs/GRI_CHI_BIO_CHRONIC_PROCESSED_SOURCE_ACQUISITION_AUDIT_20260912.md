# GRI Chi_bio chronic SCC25 processed-source acquisition audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D source acquisition / provenance / structure preflight  
**Chi_bio outcomes computed:** NO  
**Feature selection performed:** NO  
**State reduction fitted:** NO

## 1. Execution identity

GitHub Actions workflow `GRI Chi_bio chronic source probe` run **#3** (`34738887992`) completed successfully.

Uploaded provenance artifact:

```text
name:   gri-chi-bio-chronic-source-probe
ID:     10312219338
SHA256: ebe1489a417511fb1dfa58c31e5effc4901b772780583a878d8045012a26fe37
```

The workflow downloaded only public processed/metadata files that had first passed a size preflight. The approximately 499 MB raw methylation IDAT TAR was deliberately **not** downloaded because it is not needed for the present source-identity gate.

## 2. GSE98812 processed RNA source

Downloaded:

```text
GSE98812_GEOExprsData.txt.gz
SHA256: 8b69cab4612f4787bedbc9ce9414ba321fc1c4bcba7ac63d50687e42d8a1b474
compressed bytes: 2,430,267
```

The shallow probe found:

```text
header field count: 20,532
first-data-row field count: 23
header begins: cgi.Symbol, cgi.Transcript, chr, pos, posEnd, ...
```

This is **not yet licensed as a simple gene-by-22-sample matrix**. The table orientation and field semantics require a dedicated anatomy audit before any expression adapter is written.

Frozen disposition:

```text
source acquired/hash-bound: PASS
molecular-table anatomy:    OPEN
state extraction:           PROHIBITED UNTIL ANATOMY VERIFIED
Chi_bio use:                NONE
```

No attempt was made to infer the 20,532 header fields or 23 data fields from filename alone.

## 3. GSE98812 GEO series matrix

Downloaded:

```text
GSE98812_series_matrix.txt.gz
SHA256: 36fe26fb75134f05cabbf63fb3e18859204748e166963a7f34a27576fff304f0
compressed bytes: 5,495
```

Verified source metadata:

- 22 sample titles;
- 22 GEO sample accessions;
- weekly PBS/CTX ordering over weeks 1-11;
- no value-table header found in this series-matrix file.

Therefore this file is useful as an **exact sample-identity / ordering metadata source**, not as the molecular expression matrix.

The 22 accessions correspond to the frozen main chronic trajectory:

```text
GSM2612466 ... GSM2612487
```

with PBS/CTX week roles already preserved in `gri_scc25_paired_timecourse_manifest_p0d_v0_1.json`.

## 4. GSE98813 methylation series matrix

Downloaded:

```text
GSE98813_series_matrix.txt.gz
SHA256: 2bc72da999dfcd4601909979ce0559948f445915484b6b3a35c386ca71c1e885
compressed bytes: 143,991,614
```

Verified structure:

- 23 sample titles;
- 23 GEO sample accessions;
- one baseline sample plus 22 weekly PBS/CTX states;
- value-table header found;
- 24 table fields: `ID_REF` + 23 GSM value columns.

The sample range is:

```text
GSM2612501 ... GSM2612523
```

with `GSM2612501` as the baseline source role and `GSM2612502 ... GSM2612523` as the frozen 22-state main weekly trajectory.

This processed methylation matrix is therefore structurally usable for a future substrate/context adapter once feature-universe, missingness, transformation, and cross-modal rules are prospectively frozen.

No methylation Chi_bio or cross-modal statistic was computed.

## 5. GSE98813 supplementary file list

Downloaded:

```text
filelist.txt
SHA256: efd1f17880389cf1eda6fde3b85f0c174ef8e79700a8b2f404271b36d06e0fca
bytes: 6,234
lines: 45
```

The file lists raw IDAT resources/hashes and is retained as provenance for the raw-source lineage.

The raw archive:

```text
GSE98813_RAW.tar
preflight size: 499,036,160 bytes
```

was not downloaded under run-economy rules because the current question is source identity and processed-source feasibility, not raw-array reprocessing.

## 6. Exact source-role separation after acquisition

```text
GSE98812_series_matrix.txt.gz
    -> weekly RNA sample identity/order metadata

GSE98812_GEOExprsData.txt.gz
    -> processed RNA molecular source, anatomy still to verify

GSE98813_series_matrix.txt.gz
    -> baseline + weekly methylation molecular matrix and metadata

GSE98813_filelist.txt
    -> raw-IDAT provenance index

GSE98813_RAW.tar
    -> not acquired; not currently needed
```

These roles may not be collapsed merely because the files share a GEO study lineage.

## 7. Important implications for the chronic source manifest

The original 22-state RNA/methylation pairing remains supported as source identity, but the processed-source audit adds two important constraints:

1. RNA sample identity/order is verified independently in the series metadata, while the processed RNA table still needs an anatomy map before values are adapted.
2. the methylation processed matrix explicitly contains a baseline sample in addition to the 22 main states; that baseline remains excluded from the main ordered trajectory unless a future role is separately frozen.

No completed source acquisition licenses a state reduction or candidate formula.

## 8. Next safe source work

Before an outcome-bearing chronic temporal run:

1. map the exact anatomy/orientation of `GSE98812_GEOExprsData.txt.gz` without feature selection;
2. bind the processed RNA sample/value roles to the 22 frozen GEO accessions;
3. verify methylation row count, probe identifiers, missingness encoding, and value domain without selecting probes;
4. freeze the transcriptomic feature-universe/transformation rule;
5. freeze the R1 state reduction/rank design;
6. only then extract a state trajectory.

## 9. Epistemic disposition

```text
chronic public processed-source acquisition: PASS
source hashes:                              BOUND
RNA sample metadata identity:              PASS
RNA processed-table anatomy:               OPEN
methylation processed value-table anatomy: BASIC STRUCTURE PASS
raw methylation reprocessing:               NOT NEEDED / NOT PERFORMED
feature selection:                          NOT PERFORMED
state reduction:                            NOT FROZEN
candidate Chi_bio values:                   NOT COMPUTED
biological unity boundary:                  NOT_ADMITTED
```
