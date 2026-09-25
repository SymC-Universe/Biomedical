# Kizilirmak 2023 historical chi_GRI to observed dynamics decision packet

**Date:** 25 September 2026
**Status:** AUTHOR DECISION REQUIRED BEFORE OUTCOME OPENING
**Task:** `GRI_BIOCHI_B1_KIZILIRMAK2023_SOURCE_QUALIFICATION_20260925`

## Why this requires a scientific decision

The source permits a noncircular test of whether pre-stimulus transcriptomic variability carries information about later NF-kB behavior. It does not itself determine how the historical gene-wise RNA proxy should be reduced to the clonal-population level.

Those choices alter the estimand and cannot be selected after viewing the result.

## Option A — strict historical proxy, genome-wide
For every eligible gene and clone, compute historical `chi_GRI = sigma/(2 mu)` across the five untreated biological replicates on a source-qualified abundance scale. Compare the clone-level distribution of chi_GRI with a single predeclared observed dynamics endpoint.

Strength: least feature-selection freedom; closest to the original genome-wide GRI spirit.
Weakness: with n=5 per gene, individual chi estimates are noisy; genome-wide differences may be driven by unrelated expression programs.

## Option B — strict historical proxy, source-defined NF-kB circuit
Freeze the gene carrier from the source model/pathway membership before expression values are inspected. Compute gene-wise chi_GRI from the five untreated replicates and summarize only that frozen circuit. Compare with a single predeclared observed dynamics endpoint.

Strength: carrier is biologically matched to the later dynamics and does not use the outcome to select genes.
Weakness: narrower than historical genome-wide GRI and still requires a frozen reduction rule.

## Option C — both as primary + sensitivity
Use Option A as the primary no-selection analysis and Option B as a prospectively declared mechanistic sensitivity, with both frozen before any chi_GRI value is opened.

Strength: separates global proxy behavior from circuit-specific behavior and reduces the chance that one representation silently drives the conclusion.
Weakness: adds multiplicity and interpretive complexity; promotion must require coherent evidence rather than selecting the favorable lane.

## Recommended dynamic endpoint for freeze
Use source-defined **oscillatory fraction / peak-count distribution** as the direct oscillation endpoint, with AUC/persistence as a separately declared secondary endpoint. Do not manufacture a physical damping scalar from these observations.

## Expression-scale issue
Table S3 is described as log2 RPKM. Historical chi_GRI is scale-sensitive under nonlinear transforms. The strictest path is to retrieve/source-verify an unlogged abundance representation from GSE247446 if available. If only log2-RPKM is reproducibly available, the analysis must be labeled a transformed-scale proxy sensitivity and cannot be treated as direct reproduction of historical chi_GRI.

## Promotion ceiling
Even a positive result would support:
`pre-stimulus RNA fluctuation proxy contains information about later oscillatory/persistent NF-kB behavior in this source`.

It would NOT support:
- mu = omega;
- sigma = gamma;
- chi_GRI = physical damping ratio;
- a universal chi=1 biological boundary;
- cancer-wide generalization.

## Required author choice
Approve A, B, or C, or specify a different frozen carrier/reduction. No target chi_GRI values will be opened before that choice.


## AUTHOR DECISION — 25 September 2026

Approved design: **C, followed by D**.

### C — dual frozen analysis
- **A primary:** genome-wide historical-proxy analysis with no outcome-based gene selection.
- **B sensitivity/mechanistic lane:** source-defined NF-kB circuit frozen before chi_GRI values are inspected.
- Both lanes are reported whether concordant, discordant, null, or unstable.

### D — joint interpretation of A and B
D is not an independently tuned third analysis. It is the prespecified synthesis of the frozen A and B outputs.

D asks:
1. Do genome-wide and NF-kB-circuit chi_GRI organization point in the same direction with respect to independently observed later NF-kB dynamics?
2. If both associate with dynamics, is the circuit signal stronger, weaker, or simply different in form from the genome-wide signal?
3. If A is positive and B is null, does the information appear distributed beyond the local NF-kB circuit?
4. If A is null and B is positive, does the dynamical information appear localized to the relevant regulatory circuit and diluted genome-wide?
5. If A and B disagree in direction or rank ordering, does this indicate scale-dependent organization rather than a single scalar correspondence?
6. If both are null, historical chi_GRI receives no support from this source as a pre-stimulus predictor of later NF-kB dynamical phenotype.
7. No D conclusion may rescue a failed A or B by introducing new genes, transforms, endpoints, thresholds, or weights.

### D output rule
Report A and B separately first. Then report D as a relational interpretation with its own epistemic label. D may identify concordance, localization, distributed association, scale dependence, or joint null. It cannot promote chi_GRI to a physical damping ratio and cannot create a chi=1 boundary.

### Next exact action after approval
Materialize the source data and verify whether an unlogged untreated abundance representation is reproducibly available. Freeze expression scale, eligibility, primary oscillation endpoint, secondary persistence/AUC endpoint, nulls, and reduction statistics before computing any chi_GRI values.
