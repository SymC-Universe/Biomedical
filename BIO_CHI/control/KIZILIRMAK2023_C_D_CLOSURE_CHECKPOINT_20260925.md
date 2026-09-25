# Kizilirmak C+D closure checkpoint

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Task:** `GRI_BIOCHI_KIZILIRMAK_C_D_EXECUTION_20260925`  
**Status:** `P0_EXPLORATORY_RELATIONAL_SIGNAL_WITH_REPRESENTATION_LIMIT`

## Completed verified state

The source-native dynamics reproduced before the static RNA analysis. Clone R is substantially more oscillatory than clone B in both the primary Fig. 2 dataset and the independent Fig. 1 source replicate, while B has the larger AUC/persistence.

The genome-wide historical-proxy lane A is directionally concordant with the damping-like relational hypothesis: pre-stimulus median chi_GRI is higher in persistent B than oscillatory R. The sign survives all five leave-one-biological-replicate-out tests, all ten pooled-expression deciles, and all four frozen lower-mean threshold stresses.

Absolute chi_GRI remains strongly negatively associated with transformed mean abundance, as expected for CV/2. The B-R difference is nevertheless not explained by a lower B mean: the median log SD ratio B/R is 0.2054 whereas the median log mean ratio is 0.0114. The observed A contrast is primarily a dispersion difference on this transformed scale.

The source-defined four-gene NF-kB circuit lane B does not reproduce the same scalar ordering and is not robust as an aggregate. Failure decomposition shows stable component heterogeneity: Tnfrsf1a and Nfkbia have positive B-R chi contrasts in every leave-one-replicate-out check, while Rela and Tnfaip3 have negative contrasts in every check. Leave-one-gene-out circuit summaries change sign.

The source literature explains NF-kB dynamics through component-specific abundance roles, including baseline TNFR1 control of early activation and induced IkBa feedback control of persistence/oscillation. It does not use transcript CV as the mechanistic damping variable. The B failure is therefore consistent with a local circuit that requires component/modal organization rather than a scalar median of gene-wise CV/2.

## D interpretation

The frozen parent disposition remains `scale_or_representation_instability_no_promotion`.

The post-result mechanistic reading is narrower: a distributed pre-stimulus scalar proxy can show correspondence with later native dynamics while a local causal circuit refuses scalar aggregation because its components have different roles and directions. This is a candidate chi/X joint interpretation, not a physical identification of RNA mean with frequency or RNA SD with dissipation.

## Open issue requiring author decision

A cheap, source-native transport experiment is available in the same publication: Data S1 contains IL-1beta dynamics for B/R/G. The genome-wide A coordinate is unchanged. A source-defined B transport would require replacing the TNF-specific limiting receptor `Tnfrsf1a` with the source-identified IL-1beta limiting receptor `Il1rap`, retaining `Rela`, `Nfkbia`, and `Tnfaip3`.

That receptor substitution changes the mechanistic carrier and is therefore a scientific design choice rather than a mechanical continuation. No IL-1beta trajectory values have been opened in this investigation.

## Next exact action if approved

Freeze an IL-1beta C+D transport using the unchanged genome-wide A lane and source-native IL-1beta circuit `Il1rap, Rela, Nfkbia, Tnfaip3`; reproduce Fig. 5 dynamics first; then test A, B, and D with the same no-retuning and leave-one-replicate-out rules. Only after that transport result decide what enters the BioSystems main manuscript.

## Safe resume point

This checkpoint. No main-manuscript edits have been made from the new result.
