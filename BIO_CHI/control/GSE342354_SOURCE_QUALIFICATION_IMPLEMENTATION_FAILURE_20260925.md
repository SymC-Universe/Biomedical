# GSE342354 source-qualification implementation failure audit

**Date:** 25 September 2026  
**Branch:** `bio-chi-u2os-cccp-recovery-p0q-20260925`  
**Authority:** SymC GOM v0.8.6  
**Affected run:** `36217341417`  
**Artifact:** `10897504676`  
**Artifact digest:** `sha256:42f923eea395d6ecbb3012594c95b1608fa0abf6ba1178845f736a6954e5d918`  
**Classification:** IMPLEMENTATION-LEVEL DIRECTORY-PARSER FAILURE / BIOLOGICAL ANALYSIS UNOPENED

## Failure

The first source-qualification implementation parsed every HTML `href` returned by the NCBI FTP directory page as though it were a file in the requested GEO directory. An external HHS vulnerability-disclosure footer link was therefore passed through `urljoin`, after which the script attempted to download it as a processed GEO source and received HTTP 403.

The failure occurred before the source-qualification manifest was finalized and before any expression value was parsed or any biological recovery calculation was performed.

## Evidence that the GEO source itself was reachable

Before the external footer link caused termination, the run had successfully downloaded:

- `GSE342354_series_matrix.txt.gz` (3,023 bytes);
- `GSE342354_Processed_data.txt.gz` (14,586,789 bytes).

Those files were preserved inside the failed workflow artifact. Their presence narrows the root cause to link filtering rather than NCBI/GEO access.

## Mechanical repair

The rerun may change only directory parsing:

- reject absolute/external URLs and footer/navigation links;
- retain only file basenames belonging to the requested NCBI GEO directory;
- preserve the frozen accession, sample identities, file-size caps, hashing rules, and source-only claim ceiling.

No biological decision rule exists yet and no expression values may be opened during the repaired source qualification.

## Epistemic consequence

Run `36217341417` remains part of the provenance record. It is not evidence for or against recovery, biological chi, `Chi_bio`, or `chi_bio`.
