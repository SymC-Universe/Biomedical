# Biomedical Tool Feasibility Gate — Draft

**STATUS: DRAFT — DOES NOT ALTER THE FROZEN C1 v2 SCIENTIFIC CONTRACT**

Date: 2026-08-30

## Purpose

Before investing heavily in Stage C1 or later biomedical branches, determine whether the mathematics under development can plausibly become a useful research tool rather than only an internally interesting analysis.

The historical GRI/SymC work is research ancestry, not a target to defend. This feasibility gate ranks candidate tools by scientific utility, differentiation from existing methods, technical buildability, falsifiability, and validation burden.

The frozen C1 v2 experiment remains intact. This gate changes sequencing and product strategy only: define the plausible tool first, then use C1 as one prospective real-data test of that tool architecture.

## Working conclusion

A generic multi-omics integration, latent-factor, clustering, or clinical-prediction tool is not a strong initial target. Those spaces are mature and crowded.

The strongest current candidate is a **pre-integration / cross-omic architecture auditor**: a research tool that answers whether two molecular layers contain statistically defensible shared organization, where that shared structure lives, whether it is semantically specific, and whether it survives known confounders and technical perturbations before the researcher commits to a fused latent model or downstream biological interpretation.

## Candidate A — Cross-omic architecture / integration-readiness auditor

### Scientist-facing question

> I have matched multi-omic measurements. Is there real shared structure worth integrating, what carries it, and is it robust to construction, patient alignment, semantic labels, technical filtering, and known confounders?

### Inputs

- two or more sample-aligned omics matrices;
- optional feature-to-gene / pathway / module mappings;
- optional measured covariates such as purity, immune fraction, batch, age, or other study-specific confounders;
- optional technical exclusion masks;
- no outcome labels required for the core audit.

### Core outputs

1. **Within-layer structure**
   - complete sample-space eigenspectrum / effective rank / participation structure;
   - marginal-preserving permutation comparison;
   - mode contributions back to measured features.

2. **Cross-layer sample geometry**
   - kernel / Gram alignment and principal-angle spectrum;
   - patient-alignment permutation null;
   - identification of global shared versus layer-specific geometry.

3. **Semantic / conglomeration specificity**
   - pathway/module-level cross-layer coupling;
   - label-scramble null separating generic correlation from biologically matched module correspondence;
   - traceability from module effects to the modal carrier.

4. **Confounder sensitivity**
   - raw versus covariate-residualized cross-layer architecture;
   - explicit distinction between shared signal that survives measured context and signal attributable to that context.

5. **Technical robustness**
   - publication/source-faithful and masked/filtered tracks run under identical logic;
   - result cannot be promoted solely because one preprocessing track is favorable.

6. **Refusal / decision states**
   - `NO_SHARED_STRUCTURE`: no defensible cross-layer structure above null;
   - `WITHIN_LAYER_ONLY`: organized individual layers but no cross-layer alignment;
   - `GLOBAL_SHARED_ONLY`: shared sample geometry without pathway/module specificity;
   - `SEMANTIC_SHARED_CONFOUNDED`: pathway-specific sharing that attenuates under measured covariates;
   - `SEMANTIC_SHARED_ROBUST`: pathway-specific sharing that survives the prespecified confounder and technical attacks.

These labels would be methodological decisions, not disease states or clinical classifications.

### Potential value

Many integration methods are designed to discover or enforce a joint representation. An audit layer has a different job: determine whether integration is warranted and what kind of shared structure is actually supported before fusion or downstream interpretation.

### Main novelty risk

None of the individual ingredients is novel by itself. Kernel alignment, latent/subspace analysis, permutation testing, confounder adjustment, and pathway-level methylation/expression coupling all have substantial prior literature. A publishable contribution would therefore have to come from a rigorously benchmarked **decision framework** that demonstrably reduces false shared-structure conclusions, identifies when integration is or is not justified, and traces accepted shared structure across modal, scalar, and system-level views.

### Plausibility

- engineering feasibility: **high**;
- immediate compatibility with current C1 mathematics: **high**;
- research usefulness if validated: **high**;
- current novelty confidence before benchmarking: **medium**;
- clinical readiness: **low / not the initial objective**.

## Candidate B — Regulatory architecture concordance mapper

### Scientist-facing question

> Which regulatory regions and biological programs show methylation/transcriptome concordance beyond patient matching, generic pathway correlation, technical probes, and measured composition?

### Output

Per pathway/module and regulatory stratum:

- cross-layer coupling strength;
- patient-alignment null effect;
- module-label null effect;
- composition-adjusted effect;
- technical-mask sensitivity;
- contributing probes/genes/modes.

### Plausibility

- engineering feasibility: **high**;
- biological interpretability: **high**;
- novelty risk: **medium-high**, because established tools already connect methylation and expression at gene/enhancer level;
- recommended role: **module inside Candidate A unless benchmarking establishes a distinct advantage**.

## Candidate C — Patient stratifier / predictor

A supervised clinical or molecular classifier could eventually use architecture-derived features, but it is not a sensible first product.

Reasons:

- current C1 statistics are primarily cohort/resample-level rather than validated single-patient scores;
- supervised multi-omics classification is extremely crowded;
- a predictive endpoint and held-out validation cohort would need to be chosen prospectively;
- any architecture feature would have to beat strong conventional and modern multi-omics baselines.

Plausibility now: **defer**.

## Candidate D — Biological chi / master stability estimator

No current static data license a biological Gamma/Omega pair or biological chi. The final biomedical tool does not need chi at all.

Plausibility now: **not an active tool target**.

## Minimum viable research tool

Do not begin with a clinical dashboard or a large prediction platform. The minimum useful version should accept two matched matrices plus optional covariates/modules and return a reproducible audit report containing:

1. within-layer organization versus marginal-preserving nulls;
2. cross-layer geometry versus patient-permutation null;
3. module/pathway specificity versus label-permutation null;
4. raw versus confounder-adjusted architecture;
5. technical-track robustness;
6. mode-to-feature/module traceability;
7. explicit refusal state when integration is unsupported.

A CLI/Python API is sufficient for the first research release.

## Pre-C1 feasibility experiments

Before full biological execution, build and test the mathematical kernel on synthetic ground-truth systems with no unrevealed C1 biological data.

Required scenarios:

1. independent layers with identical marginal feature distributions;
2. one shared latent factor across layers;
3. several shared factors plus layer-specific factors;
4. apparent shared structure generated only by a common confounder;
5. global shared geometry with deliberately scrambled module labels;
6. module-specific shared structure with weak global alignment;
7. technical outlier/cross-reactive features producing spurious alignment;
8. unequal feature counts and missingness;
9. nonlinear shared structure that a linear audit should correctly fail to capture rather than overclaim.

The tool must show calibrated refusal on null cases and correct qualitative separation among these regimes before C1 is treated as more than a case-study execution.

## Baseline competition required before claiming a new method

At minimum compare the relevant capability against established categories such as:

- latent-factor integration (e.g. MOFA+);
- patient-similarity fusion (e.g. SNF / modern graph integration);
- joint/individual subspace decomposition (e.g. DIVAS/JIVE-family approaches);
- confounder-adjusted cross-omic association methods;
- simple kernel alignment / RV-style similarity baselines;
- methylation-expression regulatory tools where Candidate B is evaluated;
- supervised approaches only if a later predictive endpoint is introduced.

The question is not whether the proposed tool can reproduce those methods. It must demonstrate a useful decision or diagnostic that the baseline does not already provide adequately.

## Kill criteria

Stop developing Candidate A as a standalone tool if prospective simulations/benchmarks show any of the following:

- refusal states are poorly calibrated under null data;
- confounding routinely appears as robust shared structure;
- the method cannot distinguish generic patient geometry from semantic/module-specific sharing;
- its outputs are effectively equivalent to an existing method without a meaningful gain in interpretability, robustness, or decision quality;
- results are unstable to minor technical choices despite the frozen robustness tracks;
- no external dataset reproduces the useful behavior seen in TCGA.

## Relationship to frozen C1 v2

C1 v2 remains a valid prospective experiment and must not be retuned based on this feasibility exercise.

If Candidate A remains plausible after synthetic/baseline testing, C1 becomes its first major real-data case study:

- C1 H1 tests whether methylation has within-layer organization above exact probe-marginal null;
- H2 tests global cross-layer patient geometry;
- H3 tests semantic Hallmark specificity;
- adjusted H2/H3 test known composition sensitivity;
- the primary/masked tracks test technical robustness.

If the candidate tool fails feasibility testing, C1 may still be run to close the preregistered scientific question, but the program should not build a large software product around it.

## Next gate

Before opening C1 beta-value biology:

1. finish the immutable C1 v2 freeze record;
2. implement only the general mathematical audit kernel needed for synthetic tests;
3. run the synthetic ground-truth feasibility suite;
4. compare against the strongest relevant simple/established baselines;
5. decide GO / NARROW / STOP for the candidate tool;
6. only then invest in the full TCGA C1 execution path.
