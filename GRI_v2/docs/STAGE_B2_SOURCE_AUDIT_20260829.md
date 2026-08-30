# Stage B2 source and coverage audit

Date: 2026-08-29

Status: PRE-BIOLOGICAL-ASSOCIATION SOURCE/HARMONIZATION AUDIT

## Scope

Stage B2 tests orthogonal static biological layers reserved before Stage B1 results. This audit covers source identity, acquisition size, hashes, exact Stage A matching, and coverage only. No association with Stage A/B1 network outcomes has been interpreted.

Terminology:

- LOH = loss of heterozygosity, a genomic state in which a region loses the distinction between the two inherited chromosome copies.
- RPPA = reverse-phase protein array, a protein-abundance assay.
- `n` = sample count. The existing primary coverage gate requires at least 30 matched samples within a cancer type.

## Workflow integrity

The first Stage B2 source-probe attempt failed before source probing because the workflow omitted installation of `pytest`. This was a mechanical CI setup defect. The scientific/source contract did not change.

After adding the missing test dependency, the B2 contract tests passed and the source probe ran. A second mechanical issue was then identified: current GDC `/files/{uuid}` metadata lookup returned 404 for legacy PanCanAtlas publication UUIDs even though `/data/{uuid}` acquisition worked. The probe was repaired to inspect the same working `/data/{uuid}` endpoint using an HTTP byte-range request that retrieves at most one byte while reporting the full content length. This repair changed metadata acquisition only, not source selection.

The final repaired B2 source-probe workflow completed successfully.

## Acquired small sources

### Aneuploidy / LOH context

- File: `ABSOLUTE_scores.tsv`
- GDC UUID: `0e8831f4-dd7e-4673-8624-b4519c2e0d65`
- Downloaded size: 456,006 bytes
- SHA-256: `4e115fd7408a06b002f34678fa46df0b05aa20ac71db57acf535238f37aa64c8`
- Source fields include `AS`, `ASprime`, `LOH_n_seg`, and `LOH_frac_altered`.
- Exact Stage A primary-sample-type matching: 9,167 / 9,546 samples.
- Coverage gate: 32 / 32 cancers have at least 30 matched samples.

### Copy-number burden/context

- File: `seg_based_scores.tsv`
- GDC UUID: `cbfe6a9d-c3be-4982-86c7-c476dc17ca10`
- Downloaded size: 454,662 bytes
- SHA-256: `4b63eefb164866a3c49c50c04ee423d3ad1c25540f7cf39e08d997b454a189d0`
- Source fields include `n_segs`, `frac_altered`, and `n_extrema`.
- Exact Stage A primary-sample-type matching: 9,308 / 9,546 samples.
- Coverage gate: 31 / 32 cancers have at least 30 matched samples.
- SKCM has zero eligible primary-tumor rows under the frozen primary-sample rule. Metastatic samples are not substituted to rescue coverage.

### RPPA protein abundance

- File: `TCGA-RPPA-pancan-clean.txt`
- GDC UUID: `fcbb373e-28d4-4818-92f3-601ede3da5e1`
- Downloaded size: 18,901,234 bytes
- SHA-256: `06246573836865589134bd9424189f81b0d9fb436fcbf5e72024225442c400de`
- 200 columns total in the source table, including sample/tumor identifiers and protein/phosphoprotein measurements.
- Stage A matches: 6,887 / 9,546 samples.
- 6,884 matches are exact primary-sample vial/root matches; 3 use an unambiguous patient-level fallback under the established matching rule.
- Coverage gate: 31 / 32 cancers have at least 30 matched samples.
- UVM has 12 matched cases and is excluded from the primary RPPA cross-cancer layer rather than lowering the gate.

## Deferred methylation sources

The repaired byte-range metadata probe established the actual acquisition scale without downloading these files.

### Merged 27K/450K methylation matrix

- File: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`
- Reported content length: 5,022,150,019 bytes, about 5.02 GB decimal.
- Status: deferred pending a frozen methylation feature-reduction/harmonization plan.

### 450K-only methylation robustness matrix

- File: `jhu-usc.edu_PANCAN_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC UUID: `99b0c493-9e94-4d99-af9f-151e46bab989`
- Reported content length: 41,541,692,788 bytes, about 41.54 GB decimal.
- Status: robustness-only and not appropriate for casual GitHub/local acquisition. It remains deferred unless a specific preregistered need justifies the cost.

## Interpretation boundary

This source/coverage audit does not establish that aneuploidy, LOH, copy-number burden, RPPA abundance, or DNA methylation predicts or explains the Stage A network coordinates. It establishes only that the pre-reserved sources are identifiable and that the first three have sufficient coverage for primary B2 analyses under the existing gates, with the noted SKCM and UVM exceptions.

B1 composition results may be carried as context covariates or decomposition information, but they may not be used to choose favorable B2 source variables.

## Next gate

Before calculating any B2 association:

1. define the meaning and admissible use of each genomic coordinate from source documentation rather than observed agreement with Stage A;
2. freeze handling of correlated genomic variables so redundancy is reported rather than hidden in a composite;
3. freeze RPPA feature representation and missingness rules without using RNA-network outcomes for selection;
4. define incremental-information tests against B1 composition and Stage A static baselines;
5. decide whether the approximately 5.02 GB merged methylation source adds enough independent value to justify a local acquisition, and if so freeze feature reduction before download/analysis;
6. retain the static claim ceiling. No dynamic, damping, transition, optimum, or chi claim is available from B2.
