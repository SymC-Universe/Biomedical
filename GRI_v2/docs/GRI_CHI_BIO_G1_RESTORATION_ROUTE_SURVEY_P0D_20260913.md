# GRI Chi_bio G1 restoration-route survey

**Date:** 2026-09-13  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Research mode:** P0-D source / experimental-opportunity survey  
**G1 status:** restoration decomposition unresolved  
**Chi_bio:** `NOT_ADMITTED`

## 1. Why this survey exists

The current G1 identifiability attack established an algebraic fact:

```text
J = K - R
```

can be identified in principle from suitable dynamics without uniquely identifying `K` and `R` separately. A normalized G1 coordinate therefore requires independent information about restoration/turnover. B3 regulon activity can improve the state basis, but it does not by itself solve this decomposition.

This survey asks a narrower question: **what independent restoration measurements actually exist or are experimentally feasible for the intended squamous-carcinoma state?**

No restoration value, common `beta`, module-level `R`, or normalized G1 is frozen here.

## 2. What would count as restoration evidence

For a transcript with approximately first-order decay,

```text
m(t) = m(0) exp(-r t)
```

its measured half-life gives

```text
r = ln(2) / t_half.
```

That is legitimate gene-level turnover information when the experimental assumptions are adequate.

It does **not** automatically establish any of the following:

```text
R = beta I
R_B3 = diagonal matrix of TF-target mean decay rates
R_B3 = ULM-weighted mean transcript decay
R_B3 = protein degradation rate
```

Those are distinct model choices requiring derivation and validation.

## 3. Same-cell-line SCC25 evidence already in the literature

Published oral/head-and-neck squamous-cell studies demonstrate that transcript stability can be measured directly in SCC25 using transcriptional shutoff.

Examples include:

- METTL3 / c-MYC work using actinomycin-D RNA-stability measurements in SCC25 and CAL27 cells (PMCID `PMC7057159`);
- METTL3 / FGFR3 work using actinomycin-D RNA stability and cycloheximide protein-stability assays in SCC25 (PMCID `PMC9516809`, PMID `36167542`);
- NSUN2 / LAMC2 work using SCC25/HSC3 actinomycin-D sampling at 0, 2, 4, and 8 h (PMCID `PMC11591655`);
- FTO / PKM2 work using SCC25/CAL27 actinomycin-D sampling at 1, 3, and 6 h (Head & Face Medicine 2025, DOI `10.1186/s13005-025-00547-0`);
- older E2F1 work reporting SCC25 transcriptional inhibition and mRNA-stability behavior after actinomycin D.

### What these sources earn

They establish that **direct restoration/decay measurement is experimentally feasible in SCC25** and has already been used repeatedly in this cell line.

### What they do not earn

They are targeted-gene experiments, not a transcriptome-wide SCC25 restoration operator. They cannot justify a common scalar `beta` across the B3 state, and a handful of gene half-lives cannot be substituted for `R`.

## 4. Nearby transcriptome-wide metabolic-labeling evidence

GEO series `GSE222021` (`SRSF2 safeguards efficient transcription of DNA damage and repair genes`, Cell Reports 43, 114869, 2024; PMID `39446588`) contains metabolic-labeling / SLAM-seq measurements in the squamous carcinoma cell line **FaDu**.

The public series includes control and SRSF2-depleted FaDu SLAM-seq samples at approximately:

```text
15 min
30 min
60 min
```

with multiple replicates and processed SLAM-seq files including:

```text
GSE222021_normalized_counts_RC.txt.gz
GSE222021_normalized_counts_TcRC.txt.gz
```

The same GEO series also contains conventional SCC25 RNA-seq, but the public 15/30/60-minute SLAM-seq sample series is FaDu rather than SCC25.

### Why this source matters

A pulse-labeling series can, under an explicit kinetic model, constrain transcript production/turnover without relying on cross-sectional covariance. This makes `GSE222021` a potentially useful **external restoration-method / representation-sensitivity source**.

### Why it cannot simply become SCC25 `R`

FaDu and SCC25 are different squamous carcinoma cell lines. Turnover is gene- and context-dependent. Transporting FaDu decay rates directly into SCC25 would therefore require an explicit transfer test and cannot be assumed.

## 5. Broad mammalian turnover compendia

The existing G1 identifiability attack already cites the mammalian transcript half-life compendium of Agarwal & Kelley, Genome Biology 23, 245 (2022), DOI `10.1186/s13059-022-02811-x`.

Such compendia are useful for:

- expected ranges;
- gene-level turnover heterogeneity;
- method comparison;
- designing synthetic restoration distributions;
- falsifying an unjustified universal common-restoration assumption.

They are not SCC25-specific restoration truth.

## 6. Protein-turnover and proteomic data

HNSCC has substantial public proteomic and phosphoproteomic coverage, including CPTAC-HNSCC and SILAC-based HNSCC datasets. These establish important downstream molecular structure but ordinary abundance proteomics is **not protein turnover**.

A protein degradation rate also does not automatically equal transcript restoration for a transcriptomic/regulon-activity state.

Protein-turnover evidence should therefore be treated as a distinct candidate restoration layer only if the final state semantics require it and the mapping is derived prospectively.

## 7. B3-specific restoration problem

The frozen B3 scoring layer returns regulator-activity coordinates inferred from signed target-gene expression patterns.

Therefore the relevant restoration question is not simply:

```text
What is the half-life of each target transcript?
```

It is:

```text
What independently measured relaxation / turnover operator applies to the chosen B3 regulatory coordinates?
```

A simple target-level average is not licensed because:

1. ULM coordinates are weighted relational statistics, not concentrations of a single molecule;
2. regulons overlap strongly;
3. target genes have heterogeneous decay rates;
4. the B3 state may undergo a later control-only low-dimensional rotation;
5. production feedback and decay can mix under that projection.

## 8. Candidate restoration routes, ranked

### Route R1: same-system direct perturbation-relaxation measurement

**Scientific strength: highest.**

After the final B3 SCC25 state is frozen, impose a perturbation that suppresses or changes production and measure a sufficiently dense time series to estimate relaxation in the same frozen coordinates.

Possible laboratory implementations include:

```text
4sU / SLAM-seq pulse or pulse-chase
transcriptional shutoff followed by RNA-seq
other validated nascent/old-RNA labeling methods
```

The analysis must be designed before observing the relaxation outcome.

This route has the strongest chance of identifying an `R` relevant to the actual B3 state rather than borrowing turnover from another representation.

### Route R2: SCC25 transcriptome-wide metabolic labeling from existing public data

**Scientific strength: high if found. Current status: NOT FOUND in this survey.**

Targeted SCC25 decay measurements exist, but this survey has not identified a public transcriptome-wide SCC25 pulse-labeling series equivalent to the FaDu series.

Continue literature/data-archive collision search before concluding none exists.

### Route R3: FaDu SLAM-seq external transfer test

**Scientific strength: medium as external validation, insufficient as automatic SCC25 calibration.**

Use `GSE222021` to develop and falsify the restoration estimator on a nearby squamous-cell representation. Any transfer to SCC25 must be separately tested.

### Route R4: broad mammalian half-life prior

**Scientific strength: low for direct calibration, useful for falsification/sensitivity.**

Use external half-life distributions to test whether G1 conclusions survive plausible heterogeneous `R`. Do not use them as SCC25 truth.

### Route R5: common-restoration scalar `R = beta I`

**Current status: NOT LICENSED.**

This is mathematically convenient but biologically unsupported at present. It may become an explicitly testable reduced-module hypothesis, but it cannot be assumed merely because the source model used a common kinetic scale.

## 9. Pre-outcome computational program

Before any normalized empirical G1 value is opened:

1. finish B3 matched-network state identifiability;
2. if B3 passes, freeze the final B3 empirical state construction;
3. build synthetic systems with heterogeneous known restoration rates and known `K`, `R`, and `J`;
4. test candidate module-level restoration estimators on those systems;
5. use FaDu SLAM-seq, if technically adequate after source audit, as an external real-data estimator test;
6. continue searching specifically for transcriptome-wide SCC25 turnover data;
7. only then decide whether a common scalar, diagonal module restoration, full reduced `R`, or refusal is supported.

## 10. Experimental opportunity

If a new experiment becomes necessary, the cleanest high-value experiment is not another steady-state SCC25 RNA-seq snapshot. It is a **prospectively designed SCC25 production/turnover time course** that can be projected into the already frozen B3 coordinates.

Conceptually:

```text
frozen SCC25 B3 state
        +
metabolic labeling / shutoff time course
        ->
coordinate-specific relaxation evidence
        ->
independent R candidate
        +
independently estimated effective J
        ->
G1 decomposition test
```

This experiment would attack the exact algebraic gap rather than add another correlated observable.

## 11. Current disposition

```text
Independent restoration measurement: FEASIBLE IN PRINCIPLE
Same-cell targeted SCC25 decay evidence: EXISTS
Same-cell transcriptome-wide SCC25 turnover source: NOT YET FOUND
Nearby squamous transcriptome-wide SLAM-seq source: EXISTS (FaDu, GSE222021)
B3 module-level R mapping: UNRESOLVED
Common beta assumption: NOT LICENSED
Normalized empirical G1: CLOSED
Chi_bio: NOT_ADMITTED
```

The restoration lane can now proceed independently without contaminating B3 state qualification.
