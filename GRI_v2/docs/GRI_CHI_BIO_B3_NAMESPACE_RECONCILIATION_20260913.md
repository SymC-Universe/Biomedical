# GRI Chi_bio B3 namespace reconciliation

**Date:** 2026-09-13  
**Research mode:** P0-D provenance / representation qualification  
**Chi_bio status:** `NOT_ADMITTED`

## Purpose

Record the resolution of the apparent zero-overlap result produced by the first GSE98812-to-regulon B3 probe without converting a namespace mismatch into a biological conclusion.

## What failed

The first exact-match probe compared the frozen raw GSE98812 `GENE` field directly with CollecTRI and DoRothEA target symbols.

The raw GSE98812 field is encoded as:

```text
SYMBOL|ENTREZID
```

whereas the regulon resources expose symbol-level target identifiers. Exact comparison of those two raw namespaces therefore returned zero matched regulon targets. That result is diagnostic of identifier incompatibility, not evidence that the SCC25 transcriptome lacks regulon support.

The historical raw probe is retained as a provenance negative control and is now explicitly labeled:

```text
DIAGNOSTIC_B3_RAW_IDENTIFIER_NAMESPACE_MISMATCH_EXPECTED
```

It is not an admissible regulon-support qualification.

## Canonical deterministic mapping

The canonical B3 support probe is now:

```text
src.probe_chi_bio_b3_network_symbol_mapping
```

The mapping rule is frozen and intentionally narrow:

1. split each raw GSE98812 identifier exactly once on the first pipe;
2. exclude only literal `?` symbols;
3. retain the exact left-side gene symbol;
4. use Entrez ID only for two source-specific historical-symbol disambiguations:
   - `SLC35E2|728661 -> SLC35E2B`
   - `SLC35E2|9906 -> SLC35E2A`;
5. require the resulting mapped symbols to be unique;
6. permit no fuzzy matching and no external bulk annotation table.

The frozen source contains 20,531 rows. Twenty-nine literal `?` rows are excluded, leaving 20,502 unique mapped symbols.

## Outcome-free support result

The mapped provenance probe executed successfully without opening expression values.

Using the predeclared minimum of five measured targets per regulator:

```text
CollecTRI
  total edges:                         42,990
  edges with exact mapped target:      41,550
  eligible regulators:                    766

DoRothEA A/B/C
  total edges:                         13,223
  edges with exact mapped target:      12,509
  eligible regulators:                    271

Eligible-regulator intersection:          249
```

The mapped overlap therefore establishes that the frozen GSE98812 namespace can support externally sourced signed-regulon representation work. It does not select an empirical state.

## Scientific boundary after reconciliation

This reconciliation does **not**:

- score TF activity;
- choose the final TF panel;
- choose a state dimension;
- choose TF-activity versus module-expression semantics;
- fit G1 or G2;
- compute Chi_bio;
- admit a biological unity boundary;
- use SCC25 treatment outcomes, TCGA outcomes, Atlas placement, or distance to unity to choose the representation.

The B3 architecture remains prospectively constrained. The next scientific task is to freeze a state-construction rule using outcome-independent representation, transport and identifiability criteria. Normalized empirical G1 remains separately blocked under C3 until restoration is independently resolved.

## Operational consequence

Treat the raw-identifier probe only as a namespace negative control. Treat the symbol-mapped probe as the canonical B3 overlap qualification. Any future source/schema drift that makes the raw probe unexpectedly overlap or invalidates the mapped uniqueness rules must stop execution for provenance review rather than being silently repaired.
