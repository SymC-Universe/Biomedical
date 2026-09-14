# GRI Chi_bio R2 regulatory-module source survey

**Date:** 2026-09-13  
**Mode:** P0-D source/provenance comparison before empirical state freeze  
**Candidate family:** G1-S1-L3  
**Chi_bio:** `NOT_ADMITTED`

## Purpose

The S1 preselection audit identified a fixed, biologically interpretable regulatory-module state as the leading empirical route, but choosing the exact module basis changes the operator semantics. This source survey compares established transcription-factor/regulon resources before any cancer-specific G1 values are computed.

No resource is frozen by this document.

## Source family A: DoRothEA / literature-integrated TF regulons

Garcia-Alonso et al., *Genome Research* 2019, PMID 31340985, DOI 10.1101/gr.240663.118, benchmarked multiple human TF-target evidence sources and assembled an integrated resource for estimating TF activities. Their benchmark found comparatively strong performance for literature-curated interactions, followed by ChIP-seq-derived interactions, and explicitly documented low overlap among different regulon-construction strategies.

**GRI relevance**
- bulk transcriptomic use is native to the resource family;
- TF/regulon coordinates have direct regulatory semantics;
- confidence/evidence tiers provide a prospective route to a fixed basis;
- differences among source types provide a built-in representation-sensitivity test.

**Risk**
- inferred TF activity is a footprint score, not itself a dynamical generator;
- regulon overlap and context dependence must be quantified;
- confidence-tier selection must be frozen before G1 placement.

**Disposition:** `STRONG_R2_CANDIDATE_BASIS_FAMILY`.

## Source family B: CollecTRI signed TF-gene regulons

Müller-Dott et al., *Nucleic Acids Research* 2023, PMID 37843125, DOI 10.1093/nar/gkad841, presented CollecTRI-derived signed regulons covering 1,186 TFs and benchmarked them on TF perturbation experiments. The authors report that the signed CollecTRI-derived regulons outperformed other public regulatory-interaction collections for inferring TF activity changes and demonstrated use in cancer and single-cell settings.

**GRI relevance**
- signed interactions are particularly attractive for an operator-oriented project because regulatory direction is explicit;
- broad TF coverage supports a fixed global basis rather than cancer-specific module invention;
- perturbation benchmarking is closer to the intended regulatory semantics than mere coexpression agreement.

**Risk**
- 1,186 TF coordinates are still too large for an unconstrained operator under many available datasets;
- the resource integrates multiple prior-knowledge sources and therefore requires provenance/version freezing;
- TF-activity estimation and operator identification remain distinct steps.

**Disposition:** `LEADING_FIXED_REGULON_SOURCE_FOR_FURTHER_QUALIFICATION`, subject to dimensionality and overlap control.

## Source family C: VIPER / context-specific regulon activity

Alvarez et al., *Nature Genetics* 2016, PMID 27322546, DOI 10.1038/ng.3593, introduced VIPER for inferring protein activity from gene-expression regulons and experimentally evaluated the approach across TCGA-related cancer analyses. VIPER is useful here primarily as evidence that transcriptomic regulatory-footprint states can recover biologically meaningful regulator activity and can outperform mutation-only proxies in some perturbational contexts.

**GRI relevance**
- cancer-specific regulatory activity has strong precedent;
- regulator-activity coordinates are biologically interpretable;
- context-specific network inference can be used as a sensitivity route against fixed prior-knowledge regulons.

**Risk**
- context-specific networks learned from the same cancer cohort can entangle representation construction with the data being mapped;
- any ARACNE/VIPER-derived basis would require a strict construction/validation split;
- context specificity may impair pan-cancer coordinate identity.

**Disposition:** `HIGH_VALUE_CONTEXT_SPECIFIC_COMPARATOR_NOT_PRIMARY_FIXED_BASIS_YET`.

## Source family D: SCENIC regulons

Aibar et al., *Nature Methods* 2017, PMID 28991892, DOI 10.1038/nmeth.4463, introduced SCENIC, combining coexpression inference, motif enrichment, and regulon-activity scoring for single-cell RNA-seq. The method demonstrated regulatory-state identification in tumor and brain single-cell data.

**GRI relevance**
- explicit TF regulons and activity states;
- motif filtering offers a route beyond pure coexpression;
- potentially useful later for cell-resolved local-versus-embedded validation.

**Risk**
- the method is principally designed around single-cell data, whereas the current internal TCGA architecture is bulk;
- de novo regulons learned within each cohort can create transport and independence problems;
- direct use as the primary pan-cancer basis would require a stronger bulk-transfer argument.

**Disposition:** `RETAIN_FOR_CELL_RESOLVED_EXTERNAL_OR_EMBEDDING_TESTS`.

## Comparative pre-outcome ranking

### Current leading fixed-basis route

**CollecTRI / high-confidence signed prior-knowledge regulons** currently has the strongest combination of:

- regulatory semantics;
- explicit sign;
- broad human TF coverage;
- perturbation-based benchmarking;
- capacity to freeze one global resource before cancer mapping.

### Important comparator

**DoRothEA evidence-tiered regulons** remain important because their confidence structure and earlier benchmark allow a principled resource-sensitivity analysis rather than treating one regulon database as ground truth.

### Context-specific comparator

**VIPER with independently learned/frozen networks** can test whether a fixed global prior loses context-specific regulatory information.

### Later external/local-resolution test

**SCENIC or related single-cell regulon approaches** are better suited to later local-versus-embedded or cell-state validation than to defining the first bulk-TCGA state basis.

## Critical warning: regulon basis is not yet an operator

None of these resources licenses the shortcut

```text
TF activity matrix -> regulatory operator M_GRI
```

without a separate estimator derivation.

The resource can define the coordinates of `x`; it cannot by itself establish `dx/dt`, `Phi`, `D_x Phi`, or a transition matrix. Static TCGA samples are not timepoints of one trajectory.

Therefore this survey narrows the **state basis**, not the generator-estimation problem.

## Next safe step

Before freezing CollecTRI or another basis, complete a representation-feasibility audit that answers prospectively:

1. what fixed TF subset or confidence/evidence rule is used;
2. how overlapping target sets affect rank and dependence;
3. how the same basis transports across all cancers;
4. whether TF-activity coordinates or module-expression coordinates are the state variables;
5. what dimensionality is supportable for dynamic sources such as the SCC25 time course;
6. how methylation is allowed to modulate regulator coefficients without redefining the transcriptomic state;
7. how a fixed-basis route will be compared against an outcome-blind latent representation.

Only after those answers are frozen should the empirical R2 state be selected.