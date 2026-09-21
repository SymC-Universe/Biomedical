# GRI SCC25 source-native CoGAPS comparator feasibility audit

**Date:** 2026-09-21  
**Status:** P0-D LITERATURE COLLISION / COMPARATOR COVERAGE REPAIR  
**Outcome-bearing GRI rerun:** NONE

## 1. Gap being repaired

The existing G2 system-identification literature collision correctly mapped DMD, DMDc, reduced-rank state-space identification and time-varying operator methods. It did not explicitly place the **source study's own CoGAPS analysis** into the comparator map.

That omission matters under the current GOM because comparator coverage is function-specific. The source-native method must be considered where it answers the same biological question.

## 2. What the published source actually did

Stein-O'Brien et al. (Genome Medicine 2018; DOI 10.1186/s13073-018-0545-2) measured RNA-seq and DNA methylation weekly during development of cetuximab resistance in SCC25, with time-matched PBS controls.

Their source-native analysis:

- filtered RNA genes using longitudinal fold-change/control-replicate rules;
- filtered methylation features using methylation-state switching rules;
- applied CoGAPS independently to expression and methylation;
- ran CoGAPS over 2-10 dimensions for expression and 2-5 for methylation;
- used ClutrFree robustness analysis to select 5 expression dimensions;
- reported up to 3 methylation resistance patterns beyond replicate technical variation;
- used PatternMarker and gene-set analyses to interpret the temporal patterns;
- reported immediate/early transcriptional response and later resistance-associated methylation changes.

These published dimensions and feature filters were selected in the source study. They are **not** untouched choices for a new GRI confirmatory analysis.

## 3. Comparator function split

### Function A: temporal molecular-program description
Question: can the method recover interpretable evolving response/resistance programs across time?

**Source-native comparator:** published/reproduced CoGAPS analysis.

A GRI capital-Chi temporal architecture cannot claim unique descriptive value without confronting this result.

### Function B: one-step transition prediction
Question: can the current state predict the next state under a frozen information budget?

**Fair comparators:** persistence, arm-specific mean-next-state, DMD/DMDc/reduced-rank state-space models.

CoGAPS is not automatically a fair forecast comparator because its published objective is latent pattern decomposition, not one-step predictive error.

### Function C: treatment-associated operator reorganization
Question: does a treatment-dependent transition operator improve out-of-sample transition prediction over a restricted shared operator?

**Fair comparator:** restricted shared-T model and independently justified controlled/time-varying state-space alternatives.

The source paper's observation of evolving molecular patterns does not by itself establish that G2's treatment-interaction operator should win this predictive comparison.

## 4. Consequence for current chronic G2 wording

The chronic G2 result remains:

> within the frozen low-dimensional weekly G2 representation, the shared-operator model passed its predictive adequacy rule and the treatment-interaction operator did not earn support.

It must not be paraphrased as:

> cetuximab does not reorganize the biological system.

The published source found evolving transcriptional and epigenetic programs across resistance development. Those findings and the G2 result address different objects and can coexist.

## 5. Consequence for chi <-> Chi joint investigation

CoGAPS becomes a required external/native reference for the **broader temporal-organization** side of the SCC25 joint-meaning test.

A scientifically useful test is whether:

- local G2 scalar/modal dynamics and CoGAPS-like broader temporal programs covary;
- one changes without the other;
- either adds held-out information after the other is known;
- the broader capital-Chi representation can reproduce or improve on source-native descriptive structure without using the source's phenotype-defined interpretation to tune itself.

## 6. Current disposition

`COMPARATOR_COVERAGE_GAP_REPAIRED_IN_PRINCIPLE`

No computation is authorized by this audit alone. Any direct CoGAPS reproduction must freeze the reproduction purpose, source version, dimensions/selection rule, preprocessing, and whether the goal is historical reproduction, known-truth qualification, or same-task competition.
