# GRI Chi_bio literature-collision audit

**Date:** 2026-09-12  
**Status:** P0-D LITERATURE COLLISION / PRIOR-ART AUDIT  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Pre-search design anchor:** `GRI_CHI_BIO_EXPERIMENTAL_OPPORTUNITY_PRESEARCH_20260912.md`  
**Chi_bio status:** `NOT_ADMITTED`  
**External GRI outcome status:** `UNOPENED`

## 1. Purpose

This pass was performed only after the Chi_bio experimental-opportunity designs were preserved. It asks which planned experiments or conceptual targets are already answered, partly answered, method-available, conflicting, or still residual.

Finding prior work is treated as useful known-truth opportunity and prior art, not as a failure of novelty.

## 2. Highest-value collision: dense paired RNA + DNA-methylation resistance time course already exists

### Source

Stein-O'Brien G, Kagohara LT, Li S, et al. **Integrated time course omics analysis distinguishes immediate therapeutic response from acquired resistance.** Genome Medicine. 2018;10:37.  
PMID: `29792227`  
PMCID: `PMC5966898`  
DOI: `10.1186/s13073-018-0545-2`  
RNA-seq: `GSE98812`  
DNA methylation: `GSE98813`  
SuperSeries: `GSE98815`

### Source-qualified design facts

The study used the cetuximab-sensitive HNSCC cell line SCC25. Cells were treated with 100 nM cetuximab every three days for 11 weeks, with time-matched PBS controls. Samples were harvested weekly from generations G1-G11. RNA-seq and DNA methylation were measured on the same samples; methylation used the Illumina HumanMethylation450 BeadChip. A proliferation assay supplied a phenotype external to the omics coordinate construction.

The paper reports 22 main time-course samples: 11 cetuximab-treated generations and 11 PBS control generations. GEO additionally contains parental/baseline and independent stable resistant-clone measurements. The main paper distinguishes early sensitive response, progressive resistance, and later stabilized resistant growth behavior.

### Important limitations

- one cell-line model;
- time-point cultures were generated from replicated flasks but pooled for high-throughput assays, so there is not an independent biological-replicate panel at each week;
- treatment continues through the time course rather than providing a perturb-and-release/washout design;
- weekly sampling can resolve an ordered trajectory but may be too coarse for some fast local response models;
- acquired-resistance evolution is not the same question as recovery after perturbation;
- cell-line dynamics do not establish patient-level or pan-cancer transport.

### Collision disposition

**Experiment A, dense perturb-and-release:** `PARTIALLY_ANSWERED`. Dense paired regulatory/transcriptomic time-series evidence exists, but a true release/recovery phase does not.

**Experiment B, acquisition of treatment resistance:** `SUBSTANTIALLY_ANSWERED_AS_A_SOURCE_ARCHITECTURE`. The exact Chi_bio question remains unanswered because no Chi_bio construction exists or was tested.

**Chi_bio opportunity:** very high. This source may permit testing whether a frozen candidate system-level coordinate tracks an independently measured change in resistance state without requiring a new wet-lab experiment first.

## 3. Native stability prior art: cancer attractors and perturbation-driven return/escape are established

### Li et al. 2016

Li Q, Wennborg A, Aurell E, et al. **Dynamics inside the cancer cell attractor reveal cell heterogeneity, limits of stability, and escape.** PNAS. 2016;113(10):2672-2677.  
PMID: `26929366`  
PMCID: `PMC4790994`  
DOI: `10.1073/pnas.1519210113`

This work explicitly models cancer-cell populations as dynamical states around attractors. Selected subpopulations repopulated the original basin within days to weeks, edge states were less stable, regulatory perturbations could drive jumps to nearby attractors, and a Fokker-Planck description represented opposing homeostatic attraction and stochastic diffusion.

### Collision disposition

`ESTABLISHED_BEFORE_THIS_WORK` for the broad ideas that:

- cancer states can be studied as attractor-like dynamical organization;
- stability can be probed through return/repopulation after perturbation;
- attraction and stochastic spreading can oppose one another;
- perturbation can induce transition between state basins.

This does **not** define or validate GRI `Chi_bio`, a Chi=1 boundary, or the current cross-omic scalar/modal/conglomerate architecture.

## 4. Native stability prior art: potential landscapes and barrier-height stability are established

### Li & Wang 2014

Li C, Wang J. **Quantifying the underlying landscape and paths of cancer.** Journal of the Royal Society Interface. 2014;11(100):20140774.  
PMID: `25232051`  
PMCID: `PMC4191109`  
DOI: `10.1098/rsif.2014.0774`

This work constructed a cancer gene-regulatory potential landscape with normal, cancer, and apoptosis attractors. Barrier heights between attractors were used as global stability quantities and transition paths were analyzed kinetically.

### Collision disposition

`ESTABLISHED_BEFORE_THIS_WORK` for:

- cancer-regulatory landscapes;
- attractor/barrier interpretations of global network stability;
- transition-path analysis among cancer-related states.

Therefore GRI must not claim novelty merely for introducing a system-level cancer stability landscape, basin, barrier, transition, or attractor concept.

## 5. Critical-transition / tipping-point framing is established prior art

### Shin & Cho 2023

Shin D, Cho KH. **Critical transition and reversion of tumorigenesis.** Experimental & Molecular Medicine. 2023;55:692-705.  
PMID: `37009794`  
PMCID: `PMC10167317`  
DOI: `10.1038/s12276-023-00969-3`

The review synthesizes attractor-landscape approaches to cancer reversion and explicitly frames tumorigenesis as a possible critical transition/tipping-point problem involving network rewiring, multistability, perturbation, and barrier changes.

### Collision disposition

`ESTABLISHED_BEFORE_THIS_WORK` for the general claim that cancer may be analyzed using critical-transition/tipping-point and reversion frameworks.

This makes an eventual `Chi_bio = 1` claim more demanding, not less: unity would need its own derivation and independent boundary evidence rather than borrowing meaning from the existence of cancer tipping-point literature.

## 6. Pre-search experiment-by-experiment disposition

| Frozen pre-search experiment | Collision result | What remains genuinely open for Chi_bio |
|---|---|---|
| A. Dense perturb-and-release regulatory time course | `PARTIALLY_ANSWERED` | release/recovery-specific paired multi-omic data; candidate-specific identifiability |
| B. Paired acquisition of treatment resistance | `SUBSTANTIALLY_AVAILABLE` | freeze Chi_bio candidate first; test without outcome-guided tuning |
| C. Longitudinal tumor evolution | `PARTIALLY_AVAILABLE` from already source-qualified GRI candidates | exact candidate transport, treatment-aware interpretation, hierarchical closure |
| D. Known-truth synthetic generator | `METHODS_EXIST; GRI-SPECIFIC HARNESS NOT BUILT` | construction-aware recovery/refusal harness for whichever generator survives derivation |
| E. Atlas-blind external transport | `NOT YET ANSWERED FOR CHI_BIO` | frozen coordinate, frozen external task, untouched decisive evidence |

## 7. Consequence for candidate-generator search

The collision pass materially narrows what can legitimately be claimed as new.

The following are not candidate novelty claims:

- cancer attractor dynamics;
- stability landscapes;
- barrier heights as stability descriptors;
- tipping points/critical transitions in cancer;
- longitudinal omics of resistance;
- methylation-expression temporal integration;
- ordinary state-space, factorization, or network approaches.

A possible residual GRI contribution, if it survives later testing, is narrower: a preregistered/refusal-capable system-level `Chi_bio` construction that preserves explicit scalar/modal/conglomerate dependencies, is constructed before Atlas interpretation, survives construction-aware known-truth and adversarial tests, transports externally, and earns any unity-boundary meaning independently. This is a **candidate residual contribution only**, not a present novelty claim.

## 8. Immediate source priority

The SCC25 cetuximab time course (`GSE98812` + `GSE98813`) is promoted only within **P0-D source priority**, not evidentiary status:

```text
source_priority = VERY_HIGH
research_role = PERTURBED_FUNCTION + BOUNDARY_OR_TRANSITION
p1_status = NOT_SELECTED_NOT_FROZEN
gri_outcome_status = UNOPENED
selection_basis = SOURCE_ARCHITECTURE_AND_TEMPORAL_RESOLUTION_NOT_GRI_AGREEMENT
```

It should undergo an exact source/identity/representation audit before any Chi_bio computation.

## 9. Current residual question

After this collision pass, the central unanswered question remains:

> Can a system-level dimensionless coordinate be derived from the current regulatory System Model, without outcome or Atlas tuning, that preserves scientifically necessary scalar/modal/conglomerate distinctions and predicts a domain-native stability/transition property on untouched evidence?

The literature reviewed here does not answer that question and does not establish that unity is its boundary.

**Chi_bio remains `NOT_ADMITTED`.**