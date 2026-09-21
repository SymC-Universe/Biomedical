# GRI composition-robustness comparator decision packet

**Date:** 2026-09-21  
**Status:** SCIENTIFIC DECISION PACKET / NO METHOD SELECTED  
**Historical B1/C1 result:** immutable

## Trigger

The current strongest cross-layer TCGA analyses adjust for ABSOLUTE purity and a methylation-derived leukocyte fraction. External literature establishes that tumor purity and broader cell-mixture structure can materially alter bulk molecular correlation and clustering. Therefore the two-covariate projection is retained as a useful bounded sensitivity but is no longer treated as comprehensive composition control.

## External benchmark evidence

### Aran, Sirota & Butte 2015
Nature Communications 6:8971, DOI 10.1038/ncomms9971.

Pan-cancer TCGA analysis showing tumor purity is biologically and analytically consequential and can alter expression associations.

### Chu et al. 2022, BayesPrism
Nature Cancer 3:505-517, DOI 10.1038/s43018-022-00356-3.

Cancer-focused Bayesian deconvolution using scRNA-seq references. The method explicitly models differences between bulk and single-cell reference expression. The paper also warns that missing cell states in the reference can distort assignments.

### Tran et al. 2023
Nature Communications 14:5758, DOI 10.1038/s41467-023-41385-5.

Breast-TME benchmark of BayesPrism, Scaden, CIBERSORTx, MuSiC, DWLS, hspe, CPM, Bisque and EPIC. Performance depends on tumor purity, lineage granularity, absent cell types and subtype. BayesPrism and DWLS were among the strongest overall performers; no method was perfect.

### Malik et al. 2026
Computational Biology and Chemistry, article 109370, DOI 10.1016/j.compbiolchem.2026.109370.

Recent reference-based benchmark. MuSiC, DWLS and BayesPrism were strong under baseline conditions; BayesPrism was comparatively robust to reference mismatch. This is current benchmark evidence, not a reason to select BayesPrism post hoc.

### Genome Biology 2026 real-bulk benchmark
DOI 10.1186/s13059-026-03942-1.

Real-bulk cancer benchmarking found BayesPrism and ReCIDE strong in the evaluated settings, again demonstrating that method performance is scenario dependent.

## Candidate families

| Candidate | Strength for this GRI question | Main liability |
| --- | --- | --- |
| BayesPrism | cancer-oriented; can infer malignant/nonmalignant fractions and adjust reference mismatch; strong benchmark record | needs suitable scRNA reference; reference incompleteness can misassign signal; computational cost |
| DWLS | strong cell-fraction performance in TME benchmarks; granular immune performance can be competitive | reference/marker construction choices matter |
| MuSiC | established multi-subject single-cell reference method; strong in some current benchmarks | benchmark performance is context dependent; may be less tumor-specific |
| CIBERSORTx | widely used, cross-platform/batch-aware options, interpretable fractions | reference/signature and platform choices can dominate; not consistently best |
| EPIC | simpler signature-based tumor/immune/stromal framework; lower infrastructure burden | lower resolution and less adaptable to unmodeled states than single-cell-reference methods |
| ReCIDE | strong recent real-bulk benchmark candidate | newer method; must be qualified for exact TCGA setting and source availability before use |

## Decision dimensions that must be frozen before result inspection

1. **Purpose:** sensitivity analysis only, or a new primary composition model?
2. **Cancer coverage:** one method/reference must cover the intended cancer set without selectively dropping difficult lineages.
3. **Reference provenance:** pan-cancer reference versus cancer-specific reference; exact source, version, annotation and preprocessing.
4. **Malignant-cell handling:** whether malignant cells are explicitly modeled or only purity is included.
5. **Granularity:** major compartments versus detailed immune/stromal subtypes.
6. **Missing-reference behavior:** explicit policy when a cell state is absent from the reference.
7. **Same-question metric:** whether the historical H2/H3 conclusions survive after the new projection or conditioning.
8. **No favorable-method selection:** compare the frozen selected method plus, if affordable, one independent sensitivity method; do not choose whichever preserves GRI.
9. **Claim ceiling:** even a pass establishes robustness to tested composition models, not true cell-resolved causality.

## Recommended decision structure

The strongest *candidate* for a primary deep composition attack is BayesPrism because it is cancer-focused and has repeatedly strong benchmark performance, but this packet does **not** select it.

A defensible freeze would require first identifying a reference strategy compatible with the actual TCGA cancer set. If no single reference strategy supports the intended pan-cancer analysis without major missing-state asymmetry, the program should prefer a narrower cancer-stratified test or refuse a global composition-independence claim.

## Possible outcomes

- `ROBUSTNESS_SUPPORTED_UNDER_DEEPER_COMPOSITION_MODEL`
- `ROBUSTNESS_PARTIAL_CANCER_DEPENDENT`
- `COMPOSITION_DEPENDENT`
- `REFERENCE_DEPENDENT`
- `METHOD_DEPENDENT`
- `NOT_EVALUABLE_WITH_AVAILABLE_REFERENCE`

None of these outcomes retroactively alters the historical B1/C1 execution record. They alter only what downstream interpretation may inherit from it.
