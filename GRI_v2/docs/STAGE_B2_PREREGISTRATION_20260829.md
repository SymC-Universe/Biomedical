# Stage B2 orthogonal static integration preregistration

Date: 2026-08-29

Status: FROZEN BEFORE ANY STAGE A/B1/B2 BIOLOGICAL ASSOCIATION RESULT

## Purpose

Stage B2 asks whether pre-reserved genomic and protein measurements explain, extend, or remain largely independent of the Stage A static RNA map. It does not attempt to recover the historical GRI scalar and it does not introduce a biological chi coordinate.

The analysis is intentionally separated into:

1. documented genomic coordinates;
2. an orthogonal RPPA protein/phosphoprotein panel;
3. a separately deferred genome-wide DNA-methylation layer.

No B2 variable is selected because it agrees with Stage A or Stage B1.

## Primary-source definitions used for genomic coordinates

The admitted genomic coordinates are limited to fields whose meanings can be stated from the PanCanAtlas literature before association testing.

### Aneuploidy score: `AS`

Taylor et al., Cancer Cell 2018, defined the aneuploidy score as the total burden or number of chromosome-arm-level copy-number gain/loss events in each sample. Their arm calls were derived from ABSOLUTE-based copy number and an arm-level clustering procedure.

Reference: Alison M. Taylor et al. "Genomic and Functional Approaches to Understanding Cancer Aneuploidy." Cancer Cell 33(4), 2018. DOI: 10.1016/j.ccell.2018.03.007.

### LOH scores: `LOH_n_seg` and `LOH_frac_altered`

Knijnenburg et al., Cell Reports 2018, state that the two LOH scores are the total number of segments with loss-of-heterozygosity events and the fraction of the genome containing LOH events, computed from ABSOLUTE output.

Reference: Theo A. Knijnenburg et al. "Genomic and Molecular Landscape of DNA Damage Repair Deficiency across The Cancer Genome Atlas." Cell Reports 23(1), 2018. DOI: 10.1016/j.celrep.2018.03.076.

### SCNA burden: `n_segs` and `frac_altered`

The same Knijnenburg et al. analysis defines two somatic copy-number-alteration burden scores. `n_segs` is the number of segments in the copy-number profile. `frac_altered` is the fraction of profiled base pairs in segments with log2 fold-change greater than +0.1 or less than -0.1 from baseline ploidy.

### Columns withheld from the primary analysis

`ASprime` and `n_extrema` exist in the downloaded source files, but a sufficiently explicit primary-source definition was not verified before association testing. They therefore remain source-audit fields only. They may be admitted later only through a documented prospective amendment made before their relationship to Stage A/B1 outcomes is examined.

This is not a claim that those columns are invalid. It is a measurement-provenance decision.

## Genomic analysis

Five coordinates are retained separately:

- `ANEUPLOIDY_AS`
- `LOH_SEGMENT_COUNT`
- `LOH_GENOME_FRACTION`
- `SCNA_SEGMENT_COUNT`
- `SCNA_ALTERED_FRACTION`

They are expected to be correlated because they measure overlapping forms of chromosomal alteration. No composite burden score is constructed. Redundancy is reported rather than compressed away.

For each eligible cancer and each coordinate:

- sample 30 matched primary tumors without replacement;
- repeat 100 deterministic resamples;
- calculate the unchanged Stage A network metrics on the same 30 patients;
- residualize gene expression on the genomic coordinate and recalculate the network metrics;
- construct a null by permuting only the genomic coordinate within the same 30 patients before residualization;
- summarize the actual-versus-permuted difference and preservation/change of the 50-module ordering.

The factor being tested is therefore not whether high genomic burden is "good" or "bad." The question is whether measured genomic variation accounts for reproducible structure in the static RNA coherence/coupling map beyond the generic effect of fitting a covariate.

## Increment beyond Stage B1 composition

A secondary, already frozen test asks whether each genomic coordinate contributes information beyond tumor purity and methylation-derived leukocyte fraction.

Within cancers with at least 30 jointly matched cases:

1. build the B1 composition-only residual map;
2. build a composition-plus-genomic residual map;
3. build a null map in which purity/leukocyte remain attached to the patient and only the genomic coordinate is permuted;
4. compare the full model with that construction-preserving null while retaining the composition-only map as reference.

This prevents a genomic coordinate from receiving credit for structure already attributable to the B1 composition variables.

## RPPA protein layer

The PanCanAtlas RPPA file is a direct protein/phosphoprotein assay and is not reconstructed from RNA. Published TCGA RPPA work describes the panel as an orthogonal proteomic complement to genomic and transcriptomic data and documents normalization procedures designed to mitigate batch effects.

Reference: Rehan Akbani et al. "A pan-cancer proteomic perspective on The Cancer Genome Atlas." Nature Communications 5, 2014. DOI: 10.1038/ncomms4887.

The final PanCanAtlas file contains 198 measurement columns. Nine have large source-availability gaps. The primary B2 panel therefore uses the 189 columns that satisfy the prospectively fixed common-panel rule: at least 95% finite across all 6,887 Stage-A-matched primary RPPA samples plus nonzero finite variance. In this source, those 189 admitted features are complete across the matched set.

Two protein-only static coordinates are calculated within fixed n=30 resamples:

- `RPPA_PAIRWISE_MEDIAN_ABS`: median absolute pairwise Pearson correlation among the fixed 189 protein/phosphoprotein measurements;
- `RPPA_PC1_VARIANCE_FRACTION`: first-principal-component variance fraction after within-resample feature standardization.

Neither coordinate has an optimum direction.

### RNA-protein bridge

For each Hallmark RNA eigengene, `RNA_RPPA_GLOBAL_COUPLING` is defined as the median absolute Pearson correlation between that eigengene and each of the fixed 189 RPPA measurements across the same matched patients.

The construction null permutes RPPA patient rows as a block relative to RNA. This preserves the complete protein covariance structure but breaks patient-level RNA-protein alignment.

This bridge is deliberately called global protein-panel coupling. It does not claim that an RPPA antibody belongs to a specific Hallmark pathway, and no antibody-to-gene/pathway mapping is inferred from column names in the primary test.

A prespecified sensitivity analysis residualizes both RNA eigengenes and RPPA measurements on B1 purity plus leukocyte fraction before recomputing the bridge. Raw and context-adjusted results are both retained.

## Deferred DNA methylation

The merged 27K/450K PanCanAtlas methylation matrix is approximately 5.02 GB. The 450K-only robustness matrix is approximately 41.54 GB.

Neither is downloaded for B2 association testing until a probe-to-feature reduction and 27K/450K harmonization rule is frozen independently of Stage A/B1/B2 association results. The 450K-only matrix remains robustness-only unless a specific prospective need justifies its acquisition.

## Claim ceiling

Stage B2 may support statements about static multiomic association, decomposition, redundancy, and cross-assay coupling.

It cannot establish:

- causal regulation;
- damping or recovery rates;
- a transition or phase boundary;
- criticality;
- an optimum state;
- treatment response;
- a biological chi coordinate.

If a B2 coordinate shows no reproducible incremental information, that null result is retained and is a valid outcome.

Machine-readable specification: `config/stage_b2_integration_plan.json`.
