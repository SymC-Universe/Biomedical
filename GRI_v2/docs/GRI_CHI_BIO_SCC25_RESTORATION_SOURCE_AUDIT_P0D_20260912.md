# GRI Chi_bio SCC25 restoration / RNA-turnover source audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D source qualification / identifiability support  
**Approved family:** G1/S1/L3  
**Chi_bio status:** `NOT_ADMITTED`

## 1. Question

The G1 identifiability attack established that a numerical normalized G1 coordinate requires restoration/turnover information in addition to an effective local Jacobian. The immediate literature question was therefore:

> Is there an independently measured transcriptome-scale RNA turnover/restoration dataset in SCC25, or a sufficiently close source, that can identify the required restoration structure without tuning it to Chi_bio outcomes?

This search was performed before any SCC25 Chi_bio trajectory was computed.

## 2. Search result

A targeted literature search located multiple **gene-specific** SCC25/OSCC mRNA-stability experiments, but did not locate a transcriptome-wide SCC25 RNA-decay/half-life dataset adequate to identify an `R` operator for the full S1 state.

The absence statement is intentionally scoped:

```text
NO TRANSCRIPTOME-WIDE SCC25 RESTORATION SOURCE LOCATED IN THIS TARGETED PASS
```

It is not a claim that no such dataset exists anywhere.

## 3. SCC25-specific evidence located

Several studies directly measure individual transcript stability in SCC25 or closely related OSCC models using transcriptional arrest and qPCR.

Examples include:

- METTL3/YTHDF1 regulation of **c-MYC** mRNA stability in SCC25 and CAL27 using actinomycin D;
- METTL3 regulation of **FGFR3** mRNA stability in SCC25/SCC9;
- FTO-related regulation of **PD-L1** stability in an SCC25-derived arecoline-exposed model;
- FTO regulation of **ACSL3/GPX4** stability in SCC25/SCC1;
- recent FTO/YTHDF2 work measuring **PKM2** stability in SCC25/CAL27;
- NSUN2 work measuring RNA stability in SCC25/HSC3.

These studies are useful because they show directly that restoration/decay behavior is biologically measurable in SCC25-family systems and can change under regulatory perturbation. They are not sufficient to supply a transcriptome-wide diagonal or matrix `R` for the G1 state.

## 4. Broader transcriptome-wide turnover evidence

Agarwal and Kelley assembled a large mammalian compendium of transcriptome-wide mRNA decay measurements. The final publication reports 39 human and 27 mouse transcriptome-wide decay-rate datasets and shows substantial gene-level variation, technical noise, measurement bias, and sequence/biochemical determinants of half-life.

This strongly argues against treating a universal transcriptome-wide restoring rate as a default physical fact.

However, a broad mammalian consensus half-life resource is not an SCC25-specific restoration measurement and cannot be promoted to decisive G1A evidence without a transport argument.

Potential role:

```text
broad mammalian half-life resource = prior / plausibility / sensitivity input
not = SCC25-specific restoration truth
```

## 5. Consequence for G1A

G1A requires

```text
R = beta I.
```

The currently located evidence does not justify a common transcriptomic `beta` in SCC25. In fact, both the broader mammalian decay literature and gene-specific SCC25 stability experiments make heterogeneous turnover a material competing explanation.

Therefore:

```text
G1A empirical SCC25 qualification = NOT CURRENTLY LICENSED
```

unless a deliberately reduced state can independently justify an effective common restoration timescale.

A reduced module/state representation could in principle have an approximately common effective timescale even when individual transcripts do not. That is a new model claim requiring prospective validation, not something inferred from the gene-level literature.

## 6. Consequence for G1B

G1B requires a symmetric production/regulatory Jacobian plus SPD restoration structure.

The literature located in this pass does not justify symmetry of the SCC25 regulatory operator. Contemporary GRN literature instead treats regulatory networks as directed mechanistic structures and warns against confusing statistical association with causal regulation.

Therefore:

```text
G1B empirical SCC25 qualification = NOT CURRENTLY LICENSED FOR A GENERAL GRN
```

It remains a mathematically valid known-truth subclass and could become relevant only if a specific reduced gradient-like representation is independently derived.

## 7. What would actually resolve the restoration problem

The most useful evidence classes would be:

1. SCC25 transcriptome-wide metabolic-labeling decay data (for example 4sU/SLAM-seq/TimeLapse-seq/BRIC-like measurements) under the relevant state/context;
2. a prospective perturbation experiment measuring a reduced state and its relaxation/turnover independently of the candidate Chi trajectory;
3. an externally validated mechanistic reduced model whose restoring parameters are measurable and whose transfer to SCC25 is justified;
4. a direct generator model in which production/restoration decomposition is unnecessary, which is one reason G2 remains the leading empirical comparator.

## 8. Experimental-opportunity implication

If no suitable public transcriptome-wide SCC25 turnover source is found after a broader collision pass, a feasible future wet-lab experiment would not need to measure all 20,000 genes merely to rescue G1.

A more efficient prospective design would first freeze a low-dimensional transcriptomic state on independent grounds, then measure its perturbation/relaxation timescales and regulatory response under controlled conditions. Such an experiment would test the actual G1 restoration assumption rather than merely collecting more static expression data.

No experiment is authorized or required at this stage. Existing literature and G2 temporal analysis should be exhausted first under the protocol's experimental-opportunity rule.

## 9. Current source disposition

```text
SCC25 transcriptome-wide decay source:     NOT LOCATED IN TARGETED PASS
SCC25 gene-specific stability evidence:    LOCATED / SUPPORTS HETEROGENEITY AS MATERIAL
broad mammalian transcriptome decay data:  LOCATED / PRIOR-LEVEL ONLY
G1A common beta assumption:                NOT JUSTIFIED
G1B symmetry assumption:                   NOT JUSTIFIED FOR GENERAL GRN
G2 comparator importance:                  INCREASED
```

## 10. Current scientific consequence

This source audit does not falsify the approved G1 family outright. It does remove the option of casually treating `R=beta I` as an empirical SCC25 fact.

The next G1 step must either:

- derive and validate a reduced state with an independently measurable effective restoration scale;
- find stronger turnover data;
- derive another exact normalization appropriate to a directed heterogeneous system; or
- follow the precommitted failure branch toward G2 rather than force a unity coordinate.
