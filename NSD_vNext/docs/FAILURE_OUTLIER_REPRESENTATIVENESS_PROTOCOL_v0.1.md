# Bio Chi Failure, Outlier, and Representativeness Protocol v0.1

Status: ACTIVE QUALIFICATION GOVERNANCE  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Primary investigation: Bio Chi  
Repository: \`SymC-Universe/Biomedical\`  
Branch: \`nsd-rebuild-gom-v0.8.0\`

## Purpose

Bio Chi intentionally uses adversarial known truths to expose failure modes before real-EEG local chi is licensed. That is scientifically necessary, but it creates a second risk: a rare, boundary-local, or synthetic failure can consume the investigation even when it is not representative of the broader admissible regime.

This protocol requires failures and outliers to be investigated fully **without allowing them to silently become the center of the research program**.

The governing distinction is:

\[
\text{failure importance}
\neq
\text{failure prevalence}.
\]

A rare failure can still define a valid refusal boundary or expose a logical flaw. It must not, however, be described as typical behavior or used to redirect the central biological interpretation unless its prevalence, mechanism, or scientific severity warrants that move.

## Required analysis for every failure or outlier

Every meaningful failure, false selection, nonconvergence, refusal, anomalous fit, or extreme observation must be evaluated along five separate axes.

1. **Root cause.** Determine whether the event arises from implementation, transport/infrastructure, estimator conditioning, optimization, sampling/aliasing, finite-sample noise, model-family misspecification, true structural behavior, or another identifiable mechanism.

2. **Reproducibility.** Determine whether the event is isolated, seed-dependent, condition-dependent, boundary-local, reproducible over a region, or systematic.

3. **Distributional position.** Locate the event within the full relevant distribution. Record the denominator, not only the failure count. An event described as an outlier must be shown relative to peers rather than declared exceptional from a single trace.

4. **Parameter-space prevalence.** Determine whether the event occupies a narrow adversarial corner, a boundary neighborhood, a broad portion of the qualified truth space, or an empirically common region. Synthetic prevalence must not be presented as biological prevalence.

5. **Scientific consequence.** Separate:
   - a failure that invalidates a universal claim;
   - a failure that requires a refusal boundary;
   - a failure that reveals estimator weakness;
   - a failure that is practically negligible over the representative region;
   - a failure that is currently too rare or weakly characterized to justify changing the main route.

## Representative lane and adversarial lane

Qualification must preserve two complementary lanes.

**Representative lane.** This maps ordinary/interior behavior over the admissible truth space using balanced or space-filling coverage that is not selected because a model previously failed there. Its purpose is to characterize what usually happens across the investigated domain.

**Adversarial lane.** This deliberately targets boundaries, alias conditions, singularities, colored forcing, collision surfaces, near-critical regions, and previously observed failures. Its purpose is to falsify shortcuts, define refusals, and expose mechanisms.

Results from the adversarial lane may constrain interpretation of the representative lane, but adversarial frequency must not be mistaken for real-world frequency.

A research direction should not be dominated by one adversarial mechanism unless at least one of the following is true:

- it occurs across a substantial region of the representative qualification space;
- it is reproducible across conditions or seeds and materially biases the primary claim;
- it exposes a logical nonidentifiability or semantic failure that invalidates the claim even when rare;
- independent empirical evidence indicates that the mechanism is common in the biological system under study.

Otherwise the failure remains mapped, preserved, and incorporated into refusal/uncertainty logic without monopolizing the next experiments.

## Plotting and reporting rule

Plots must show the full distribution honestly.

For every figure or diagnostic summary involving failures/outliers:

- retain all valid observations unless an exclusion is prospectively defined and reported;
- show the denominator and failure/refusal count;
- display central tendency and spread together with individual observations or an equivalent full-distribution representation when feasible;
- identify outliers without deleting them from the plot or denominator;
- distinguish mechanical/infrastructure failures from scientific outcomes;
- distinguish representative-grid points from deliberately adversarial points;
- show both successful and failed/refused cases on the same scale where scientifically meaningful;
- do not rescale axes solely to make an outlier dominate the visual story;
- do not present a boundary-focused panel as if it represents the population frequency of that behavior;
- when a failure rate is reported, provide the exact numerator/denominator and the sampling design that generated it.

A separate zoomed failure panel is allowed when mechanism requires detail, but it must accompany a context plot showing where that case lies within the whole investigated distribution.

## Majority-behavior guard

Before a failure becomes the justification for changing the main estimator family, biological interpretation, or next primary experiment, the working record must answer:

- How many cases were evaluated?
- How many showed the failure?
- Was the sample balanced, representative, or adversarially enriched?
- Where in parameter space did the failures occur?
- Did the same mechanism appear under independent seeds, durations, rates, or truth families?
- Does the failure materially change chi, pole lineage, prediction, or refusal status?
- Is the mechanism plausible and common in the intended biological domain, or only possible?
- Would ignoring the failure invalidate a universal claim, or merely limit scope?

If these questions cannot yet be answered, the failure remains an open qualification issue but does not automatically become the main Bio Chi hypothesis.

## Application to the current Bio Chi lane

The current colored-process extra-pole failure is important because it falsifies the shortcut that a C1Q win establishes second-order continuous lineage. It therefore justifies a refusal/control branch.

It does **not** currently establish that colored third-pole contamination is the dominant or even common form of neural dynamics. The present colored control is an adversarial known truth. Its scientific role is to test whether the N-B1 admission logic can be fooled.

Likewise, D\\C and S\\D controls establish family-scope failure modes and sampling semantics. Their frequency in synthetic qualification packets is determined by design and must not be interpreted as their prevalence in biology.

The central Bio Chi lane therefore remains broader than any one failure mechanism:

\[
\text{native biological dynamics}
\rightarrow
\text{modal lineage qualification}
\rightarrow
\text{sampling and identifiability}
\rightarrow
\text{predictive closure}
\rightarrow
\text{local chi if licensed}.
\]

Adversarial failures constrain this route; they do not replace it.

## Living-record requirement

Every future scientific failure/outlier entered into \`BIO_CHI_WORKING_SCIENTIFIC_STATE.md\` must include, when available:

- root-cause class;
- reproducibility class;
- numerator/denominator;
- whether the experiment was representative, balanced qualification, or adversarially enriched;
- parameter-space location;
- effect size or consequence for the primary claim;
- whether the event changes the main route, adds a refusal boundary, or remains a mapped edge case.

If prevalence is unknown, state **PREVALENCE UNKNOWN** rather than implying rarity or commonness.

## Threshold impact

This protocol freezes **no numerical threshold**.

It establishes reporting and prioritization rules only. Any later prevalence threshold, outlier criterion, or promotion rule requires its own prospective calibration and scientific approval.

## Current interpretation ceiling

This protocol does not:
- license real-EEG local chi;
- demote a valid refusal because it is rare;
- permit exclusion of inconvenient failures;
- make synthetic frequency a biological prevalence estimate;
- require every outlier to become a separate research program;
- alter C/D/S mathematics, predictive approximate closure, or N-B2/N-B3.
