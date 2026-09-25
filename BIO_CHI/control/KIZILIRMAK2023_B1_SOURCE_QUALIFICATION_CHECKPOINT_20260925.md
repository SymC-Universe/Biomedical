# Kizilirmak 2023 B1 source qualification checkpoint

**Date:** 25 September 2026
**Branch:** `gri-biochi-bridge-p0q-20260925`
**Task:** `GRI_BIOCHI_B1_STATIC_TO_NATIVE_DYNAMICS_20260925`
**Source:** Kizilirmak et al., iScience 2023, DOI 10.1016/j.isci.2023.108573, GEO GSE247446
**Disposition:** `PASS_STATIC_TO_OBSERVED_DYNAMICS_SOURCE / REFUSE_CLEAN_NATIVE_SCALAR_B1`

## TASK_ID
`GRI_BIOCHI_B1_KIZILIRMAK2023_SOURCE_QUALIFICATION_20260925`

## AUTHORITATIVE_INPUTS
- publication and STAR Methods
- GEO GSE247446 identity
- Table S3 described as log2 RPKM expression for 5 biological replicates per clone/condition
- Data S1 described as single-cell NF-kB dynamics reproducing Figures 1,2,5,6
- existing B1 calibration re-entry checkpoint
- GRI project guardrails

## COMPLETED_VERIFIED_STATE
1. Clone B, R, and G transcriptomes include five untreated biological replicates per clone before TNF stimulation.
2. Later NF-kB dynamics are directly observed by live-cell GFP-p65 imaging in hundreds of cells per clone.
3. Clone B is source-described as more persistent, clone R as sharper/more oscillatory, and clone G as weakly activated; dynamic features include first peak, timing, AUC, number of peaks, inter-peak period, and peak ratios.
4. RNA and dynamics are source-matched at clonal-population level, not the same individual cells.
5. The source ODE is a multi-state NF-kB feedback model. Clone-specific simulations are not independently fitted generators: clone R prototypical parameters are selected from randomized prior parameters subject to observed peak constraints, then B/G parameters are altered using transcriptomic ratios for activating complexes, total NF-kB, and Nfkbia transcription.
6. The publication does not report a clone-specific Jacobian/eigenvalue decomposition or an uncertainty-robust complex-mode damping scalar.
7. Therefore deriving a clone-specific chi_bio from that transcriptome-constrained generator and then testing the same RNA against it would violate B1 independence.

## OPEN_ISSUES
A weaker but noncircular question remains executable:
Does historical `chi_GRI = sigma/(2 mu)`, computed only from untreated replicate RNA, stratify independently observed later NF-kB dynamical behavior across the frozen source clones?

This would be a proxy-to-behavior test, not a proxy-to-physical-damping calibration.

Before values are opened for this new test, the following scientific choices must be frozen:
- expression scale: source Table S3 log2-RPKM versus a source-qualified unlogged/raw abundance representation if retrievable;
- gene carrier: genome-wide eligible genes versus a prospectively specified source-defined NF-kB circuit;
- clone-level reduction of gene-wise chi_GRI: e.g. median/distributional summary versus a circuit-level multivariate test;
- primary observed dynamic endpoint: oscillatory fraction/peak count, persistence/AUC, or a predefined composite; no endpoint selection after seeing chi_GRI.

## NEXT_EXACT_ACTION
Obtain author decision on the proxy-to-observed-dynamics freeze. After approval, materialize the source data, freeze exact preprocessing/carrier/endpoint/nulls, run the analysis, checkpoint the result, and only then decide whether the BioSystems main manuscript changes.

## SAFE_RESUME_POINT
This checkpoint.

## SCIENTIFIC_STATE_CHANGED
Yes. A source has been identified that can test static pre-stimulus RNA proxy versus later observed dynamics, but not clean static proxy versus an independently identified physical damping scalar.
