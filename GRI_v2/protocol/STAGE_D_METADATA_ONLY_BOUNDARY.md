# Stage D Metadata-Only Boundary

D0 metadata/design inspection may use:
- accession descriptions;
- sample titles;
- treatments;
- doses;
- time points;
- replicate labels;
- assay/platform identities;
- file names, sizes, and hashes;
- batch identifiers;
- protocol text needed to map design.

D0 may not inspect:
- numeric methylation matrices;
- numeric RNA matrices;
- numeric contact matrices;
- outcome clustering;
- differential statistics;
- effect direction/magnitude;
- features selected by biological contrast.

If a metadata file embeds numeric assay values, the script must either parse only declared metadata fields or hold for review rather than silently using the values.
