# GRI Chi_bio G1 restoration-identifiability closure plan

**Date:** 2026-09-14  
**Status:** PROSPECTIVE P0-D/P0-Q PLAN; NO G1 REOPENING YET  
**Program authority:** SymC General Operations Manual v0.8.0  
**Branch:** `gri-v071-protocol-integration-20260910-chi-bio`

## Scientific question

Can the existing SCC25 temporal evidence and independently justified RNA-kinetic information constrain the restoration component of the G1 regulatory generator tightly enough that normalized empirical G1 becomes identifiable without assigning a convenient common restoration constant or tuning toward `Chi_bio = 1`?

The task is an inverse/identifiability problem. The objective is not to produce a favorable scalar. The allowed terminal states are:

- `G1_RESTORATION_IDENTIFIABLE`;
- `G1_RESTORATION_PARTIALLY_IDENTIFIABLE_WITH_BOUNDED_VALIDITY`;
- `G1_RESTORATION_NOT_IDENTIFIABLE`;
- `SOURCE_INCOMPATIBLE_OR_INSUFFICIENT`.

No biological unity-boundary interpretation is opened by any of these states.

## Existing constraint

The frozen G2 temporal program estimates a discrete transition operator `T` over a fixed sampling interval `Delta t`. Where a continuous-time embedding is mathematically admissible,

`T = exp(J Delta t)`

links the observed discrete operator to an effective continuous-time generator `J`. The effective `J` combines regulatory interaction, self-effects, degradation/restoration, and any other dynamics represented by the fitted state coordinates. Therefore G2 constrains the combined generator but does not uniquely identify a regulatory/restoration decomposition.

## Prospective sequence

### R0 — preserve the existing evidence

Do not retune, rerun, or reinterpret the frozen G2/B3 results. Existing SCC25 transition operators and their declared sensitivity envelopes are read-only inputs.

### R1 — discrete-to-continuous admissibility audit

For each frozen G2 operator and uncertainty/sensitivity realization:

1. test whether a real continuous-time generator is admissible under the relevant matrix-logarithm conditions;
2. enumerate or bound materially admissible logarithm branches where non-uniqueness exists;
3. reject embeddings that require unsupported complex/branch structure for the biological state definition;
4. preserve branch ambiguity as uncertainty rather than selecting the branch that favors G1.

Output: an admissible family `J_eff`, not one preferred generator.

### R2 — restoration structure only, not restoration values

Use only the biological structure that is independently justified before G1 interpretation. In standard gene-regulatory ODE formulations, degradation can enter as a negative diagonal term distinct from off-diagonal regulatory production/interaction terms. This licenses testing diagonal positive restoration matrices `D = diag(d_i)` as a structural family; it does not license numerical `d_i` values by assumption.

Primary reference basis:

- Chen et al. (2021), PMCID `PMC8291590`: explicit separation of transcript decay/diagonal terms from off-diagonal regulation in a GRN Jacobian.

### R3 — SCC25-matched kinetic-information audit

Determine whether the SCC25 source data used by the temporal program preserve enough raw RNA-seq structure for condition-matched kinetic inference.

Primary route if technically compatible:

- INSPEcT-minus (`INSPEcT−`), Furlan et al., *Genome Research* 2020, DOI `10.1101/gr.260984.120`, PMID `32978246`, PMCID `PMC7605262`.

INSPEcT− can infer synthesis, processing, and degradation kinetics from steady-state or time-course total RNA-seq without metabolic labeling by modeling premature and mature RNA. Compatibility must be demonstrated from the actual SCC25 source files. A processed expression matrix alone is not sufficient evidence that the required premature/mature information is recoverable.

If source compatibility fails, record `SOURCE_INCOMPATIBLE_OR_INSUFFICIENT`; do not reconstruct missing precursor information from downstream expression summaries.

### R4 — independent kinetic bounds, not substitutions

Use independent transcript-stability measurements only as plausibility bounds/sensitivities unless the biological system and condition are directly matched.

References:

- Imamachi et al. (2014), BRIC-seq, DOI `10.1016/j.ymeth.2013.07.014`, PMID `23872059`: genome-wide transcript half-life measurement by BrU pulse-chase sequencing.
- Tani et al. (2012), PMCID `PMC3337439`: transcriptome-scale mammalian RNA half-lives by BRIC-seq.
- Saunders et al. (1998), PMID `9563476`: direct E2F1 mRNA stability measurements in SCC25, establishing that transcript-stability behavior is measurable and condition-dependent in this cell line, but not supplying a genome-wide restoration operator.

These sources may reject biologically implausible inferred decay regimes or define broad prior envelopes. They may not be copied into SCC25 gene-specific restoration values merely to obtain normalization.

### R5 — decomposition/identifiability test

For each admissible `J_eff` and restoration family `D`, define the regulatory component consistently with the G1 model and ask whether materially distinct `D` values can reproduce the same observed temporal operator while changing the normalized G1 conclusion.

The decisive question is invariance, not proximity to unity:

- if the G1 qualitative/quantitative conclusion is stable across the full empirically admissible restoration family and uncertainty, classify as identifiable within that stated regime;
- if only a bounded subset is stable, classify as partially identifiable and state that validity regime;
- if plausible restoration choices materially alter the result, retain `NOT_IDENTIFIABLE`.

No threshold may be selected because it places a cancer, trajectory, or model near `1`.

### R6 — Function/Limit Map output

Report both:

- Function Map: restoration ranges/structures over which G1 inference is invariant;
- Limit Map: restoration uncertainty, matrix-log branch ambiguity, source incompatibility, or decomposition non-uniqueness that changes the G1 inference.

## Independence classes

Keep these evidence roles separate:

- existing G2 SCC25 dynamics: **condition-matched, not independent of the temporal evidence being decomposed**;
- INSPEcT− inference on the same SCC25 experiment: **condition-matched but method-derived from the same experiment; not independent validation**;
- SCC25-specific historical transcript-stability measurements: **cell-line matched but sparse and condition-different unless exact conditions match**;
- BRIC-seq/other cell-line genome-wide half-life atlases: **methodologically independent but biologically non-matched; bounds/sensitivity only**.

No combination of these labels may be described as fully independent SCC25 genome-wide restoration measurement unless such a dataset is actually located or generated.

## Hard prohibitions

Do not:

- assign a common beta/restoration constant to create a unity-normalized coordinate;
- import HeLa/HEK293/global median half-lives as SCC25 gene-specific truth;
- select a matrix-log branch because it yields a preferred G1 result;
- use TCGA/Atlas placement or cancer outcome to choose restoration values;
- reinterpret G2 mathematical unit-circle position as a biological `Chi_bio = 1` boundary;
- reopen the failed B3 representation as part of this restoration analysis.

## Manuscript rule

Until R1-R6 are completed, manuscript language must state that the present work **constrains but does not directly measure a genome-wide SCC25 restoration operator**. If the inverse program succeeds, the manuscript may report a bounded/identifiable restoration family with its independence limitations. If it fails, the failure itself becomes the final G1 Limit-Map result.
