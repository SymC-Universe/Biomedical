# BioSystems claim-extension P0-D protocol - 23 September 2026

**Status:** ACTIVE / OUTCOME-UNOPENED AT FREEZE  
**Branch:** `biosystems-claim-extension-p0d-20260923`  
**Parent scientific release:** BioSystems v20 compact-margin read-through state  
**Purpose:** Test whether selected current nonclaims can be narrowed using small, source-qualified external/perturbational datasets without reopening the heavy TCGA C1 computation.

## Governance

This extension is exploratory P0-D unless a later untouched confirmation is separately frozen. It may narrow or support future manuscript language, but it may not retroactively convert post-result exploration into the original C1/P1 confirmatory spine.

The universal dynamical boundary is deliberately excluded from this extension.

## E1 - second external H1 transport in breast cancer

**Question:** Does the H1 within-methylation covariance result transport beyond prostate into an independent breast-cancer 450K cohort?

**Source:** GSE58999, 44 matched primary breast tumors and regional/lymph-node metastases.

**Primary analysis:** primary-tumor methylation only.

**Frozen representation:** exact C1 22,601 probe identity carrier, same technical-mask definitions, no outcome-informed probe selection.

**Sample rule:** select 30 primary tumors by deterministic SHA-256 ordering of source patient IDs before methylation values are inspected. Use the exact paired metastases from the same 30 participants as a state sensitivity. Full 44-pair H1 is a mandatory secondary sensitivity.

**H1 statistic:** same spectral-concentration statistic as the BioSystems manuscript.

**Null:** within-probe patient permutation, B=999 for the n=30 primary and paired-metastasis lanes; B=199 allowed for full-n=44 sensitivity if runtime requires it, with the Monte-Carlo resolution stated.

**Primary P0-D success condition:** positive H1 excess relative to the construction null in the frozen primary n=30 lane and concordant sign in masked and full-cohort sensitivities.

**Failure consequence:** preserve as nontransport; do not alter probe/sample rules.

## E2 - treatment-response architecture in SCC25

**Question:** Do simple, prospectively defined methylation/RNA distances change across independently published cetuximab response/resistance phases?

**Source:** GSE98813 methylation + GSE98812 RNA, SCC25, PBS vs 100 nM cetuximab, G1-G11.

**Independent phenotype labels from publication:**
- sensitive: G1-G3;
- resistance acquisition: G4-G8;
- late/stable resistance: G9-G11.

These labels are source-derived and are not defined from the new molecular outputs.

**Methylation representation:** frozen C1 probe carrier where source support exists; treated-minus-time-matched-control probe differences.

**RNA representation:** frozen Hallmark-union genes where source support exists; treated-minus-time-matched-control log-expression differences.

**Primary treatment-response observables:**
- robust methylation distance from matched control per generation;
- robust RNA distance from matched control per generation;
- phase ordering and the predeclared G4 breakpoint.

**Claim ceiling:** molecular architecture associated with treatment-response phase in one cell-line model. No patient clinical-utility claim.

## E3 - methylation-to-RNA temporal-direction attack

**Question:** In the SCC25 perturbation trajectory, does methylation state at generation t carry more directional information about RNA at t+1 than the reverse RNA(t) -> methylation(t+1) comparison?

**Feature mapping:** only genes with frozen promoter-core methylation mapping and RNA support.

For each transition t -> t+1:
- forward statistic: association of treated-minus-control promoter methylation at t with treated-minus-control RNA at t+1;
- reverse statistic: association of treated-minus-control RNA at t with treated-minus-control promoter methylation at t+1.

Use the same association convention in both directions.

**Primary adjudication:** paired forward-versus-reverse comparison across the ten ordered transitions.

**Claim ceiling:** temporal-direction evidence only. Because cetuximab can drive both layers, even a forward excess does not establish methylation causality by itself.

**Causal promotion requirement:** a separate direct methylation-perturbation source must agree before wording can advance from temporal precedence to intervention-supported methylation-to-RNA regulation.

Candidate small intervention sources are source-qualified next without opening outcome-based selection:
- HCT116/DKO1 DNMT-loss multiomic source GSE60106;
- targeted or pharmacologic methylation-perturbation sources may be used only after exact source/mapping qualification.

## E4 - recovery dynamics after treatment withdrawal

**Question:** Does a cancer transcriptional state measurably return toward its pre-treatment state after drug removal?

**Primary source:** frozen M397 melanoma trajectory, exact processed object `GSE134459_Reversible_RPKM_values.txt.gz`, SHA-256 `1ec204f02187289fdc0d718fe2291d34f2e3e6b943dcdf8fe627718d75a42d8c`.

**Frozen simple recovery metric:**
1. use all genes with finite nonnegative values at every frozen M397 timepoint;
2. transform `log2(RPKM + 1)`;
3. baseline is Day 0;
4. at each timepoint compute median absolute log-expression displacement from Day 0 across retained genes;
5. no outcome-based gene filtering or module fitting.

**Primary recovery test:** among the six post-removal points (days 4,10,15,17,30,35), test whether displacement decreases with days-after-removal and whether Day35 displacement is lower than Day4.

**Secondary check:** compare post-removal endpoint with the final drug-on state.

**Claim ceiling:** realized transcriptomic recovery/reorganization in this melanoma trajectory under this distance definition. No universal recovery law and no scalar chi_bio construction.

## E5 - diagnostic/prognostic feasibility

Current H1/H2/H3 are cohort-level statistics and are not automatically patient-level biomarkers.

Before any clinical-utility analysis, require an already-defined or prospectively frozen patient-level representation.

### Diagnostic lane

Preferred low-cost source: independent prostate tumor/adjacent cohort because labels are explicit and external.

A diagnostic experiment may use prospectively frozen patient-level methylation Hallmark scores or another existing patient-level representation, with pair-grouped cross-validation and a simple capacity-matched baseline.

**Allowed claim:** tissue-state discrimination in the tested cohort.

**Forbidden claim:** diagnostic utility or deployable biomarker without independent clinical validation.

### Prognostic lane

The Ramakrishnan prostate study defines progression-free survival and contains patient-level clinical outcomes in its supplementary materials. The source is eligible for a low-cost exploratory prognostic test only if:
- outcome rows can be mapped exactly to the external molecular participants;
- a patient-level representation is frozen before PFS values are opened for the new analysis;
- censoring/time definitions are source-verified;
- nested/model-selection leakage is prevented.

If those gates fail, prognosis remains `NOT_TESTABLE_WITH_CURRENT_FROZEN_OBJECTS` rather than being forced.

## Stability Architecture citation

The accepted/published physical Stability Architecture paper may be cited as lineage/context only:

Christensen N. Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration. Scientific Reports. 2026. doi:10.1038/s41598-026-56887-7.

It must be the final bibliography entry and must not be used as evidence that a cancer dynamical boundary, biological damping ratio, or biological chi has been established.

## Stop rule

Stop and surface a science decision only if a test requires:
- inventing a patient-level biomarker from a cohort-level endpoint after viewing outcomes;
- changing the C1 probe/mask representation based on new results;
- choosing a recovery metric after opening the M397 trajectory;
- changing the published G4 treatment-response phase boundary;
- or promoting a temporal association into causality without a direct intervention source.

Mechanical/source failures are repaired or recorded without changing these rules.
