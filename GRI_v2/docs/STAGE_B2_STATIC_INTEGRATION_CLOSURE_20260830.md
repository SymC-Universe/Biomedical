# Stage B2 static multiomic integration closure

Date: 2026-08-30

Status: STAGE B2 STATIC ARCHITECTURE CLOSED; NO MASTER SCORE OR DYNAMIC CLAIM

## Purpose

This document integrates the closed Stage A, Stage B1, Stage B2 genomic, and Stage B2 RPPA results into one bounded static architecture. It does not create a new fitted model, combine coordinates into a master score, or reinterpret cross-sectional measurements as dynamics.

The component audits remain authoritative for their own calculations:

- Stage A/A1: `STAGE_A1_AUDIT_20260829.md` and `STAGE_A1_1_AUDIT_20260829.md`
- Stage B1: `STAGE_B1_AUDIT_20260829.md`
- Stage B2 preregistration: `STAGE_B2_PREREGISTRATION_20260829.md`
- Stage B2 RPPA: `STAGE_B2_RPPA_AUDIT_20260829.md`
- Stage B2 genomic: `STAGE_B2_GENOMIC_AUDIT_20260830.md`

## What is now established as a development architecture

### 1. Static RNA organization is reproducible

The Stage A Hallmark map retains separate RNA observables `V`, `L`, `C_in`, and `C_out`. Fixed-sample-size calibration showed that finite sample size inflates absolute-correlation magnitude but does not erase the retained module topology.

This earns a reproducible static RNA measurement layer. It does not earn a damping, recovery, criticality, or biological-chi interpretation.

### 2. Composition is a real but incomplete contributor

Stage B1 shows that independently measured tumor purity and methylation-derived leukocyte fraction explain a concentrated part of the RNA network geometry, especially in immune/inflammatory Hallmarks.

The broader topology persists after composition adjustment. Raw and adjusted maps therefore remain complementary context views rather than one being defined as the corrected or healthier state.

### 3. The admitted genomic burden coordinates are weak distributed decomposers, not a master organizer

Stage B2 tested five independently documented genomic coordinates under same-patient construction nulls and kept them separate.

Their specific effects on the Hallmark RNA map are small at the cancer and module levels, and the 50-module ordering is preserved at very high rank agreement after genomic residualization. Comparable bounded shifts remain in the prespecified increment-beyond-B1 branch.

This earns retention of the five genomic coordinates as static decomposition axes. It does not support replacing the RNA network architecture with a genomic burden scalar or claiming that genomic burden is the causal substrate of that architecture.

### 4. RNA state is coupled to an orthogonal protein/phosphoprotein layer

The RPPA branch shows patient-aligned Hallmark RNA eigengene coupling to an independently measured 189-feature protein/phosphoprotein panel above the block-permutation construction floor.

The broad coupling remains positive after purity/leukocyte adjustment across all eligible cancers in that sensitivity branch.

This earns retention of an orthogonal protein layer and a global cross-assay coupling coordinate. It does not establish pathway-specific protein control, causality, an optimum, or a dynamic mechanism.

## Integrated interpretation

The closed static evidence does not support a single scalar description of the cancer state.

A better-supported representation is layered:

- RNA variability/lineage and Hallmark network organization;
- composition/context;
- genomic burden/decomposition;
- orthogonal protein/phosphoprotein coupling;
- a still-deferred genome-wide methylation layer;
- future dynamic response measurements.

The layers are neither assumed independent nor forced into a common scale. Each keeps its own measurement definition, null construction, uncertainty, and claim ceiling.

The strongest cross-layer conclusion available at this point is therefore architectural:

> The PanCanAtlas cancer state contains a reproducible Hallmark RNA organization that is only partly explained by measured composition and the five admitted genomic burden coordinates, while carrying detectable patient-aligned information into an independently measured protein/phosphoprotein layer.

This statement is cross-sectional and non-causal.

## Consequence for the substrate-inheritance investigation

Stage B2 does not establish substrate inheritance. Inheritance requires ordered or temporal evidence showing that an underlying state constrains subsequent response or organization.

However, Stage B2 materially narrows the next question. A substrate investigation should not treat genomic burden alone as the hidden state behind the RNA map. The surviving candidates now include regulatory/epigenetic state, protein-state organization, unmeasured cellular context, and genuine dynamical response structure.

The next stages must therefore distinguish persistent organization from mere same-time association.

## Modal + scalar + conglomeration architecture

The next investigation will preserve three complementary views rather than asking one representation to do all explanatory work.

### Modal view

The modal view resolves the internal modes carrying the organization. Depending on the next dataset, this may include eigenspectra, mode participation, spectral gaps, mode stability across perturbations, or other mode-resolved response structure.

The existing PC1 variance fraction is one modal summary, not a complete modal analysis.

### Scalar view

Scalar coordinates are allowed only as compressed summaries of empirically supported structure. Existing static scalars such as `V`, `L`, `C_in`, `C_out`, genomic coordinates, and RNA/RPPA global coupling retain their specific measurement meanings.

No current scalar is biological chi.

A future chi coordinate may be tested only if same-coordinate `Gamma` and `Omega` are independently measurable and satisfy `CHI_ADMISSION_RULES.md`.

### Conglomeration view

The conglomeration view captures system-level organization: module-to-module relations, cross-layer organization, community or hierarchical structure, and the integrated behavior of the measured system.

This is not reducible to the scalar view. It asks how the pieces organize together even when individual coordinates remain distinct.

### Reporting rule

When all three views are available, they must be reported together:

`modal structure + scalar coordinates + conglomeration/system organization`.

A scalar may compress the state but cannot replace the modal carrier or the integrated system architecture that gives the scalar meaning.

## Genome-wide methylation gate

Genome-wide DNA methylation remains deferred rather than rejected.

Its scientific role was pre-reserved before the current B2 association results and remains independently motivated as a regulatory/epigenetic measurement layer. Its admission must not be justified by whether the genomic or RPPA result was favorable.

Before any genome-wide matrix is downloaded for association testing, a separate prospective specification must freeze:

1. the 27K/450K platform-harmonization rule;
2. probe-quality exclusions;
3. probe-to-feature or probe-to-gene reduction;
4. the primary methylation coordinates;
5. matching and minimum-sample rules;
6. the construction null;
7. the relationship, if any, to Hallmark modules;
8. the claim ceiling and non-claims;
9. the 450K-only robustness role.

No methylation association result may be inspected before that specification is frozen.

## What Stage B2 does not earn

Stage B2 does not establish:

- a master cancer stability score;
- a biological chi coordinate;
- `chi = 1` as an optimum or treatment target;
- damping, recovery, relaxation, or intrinsic response rates;
- causal substrate inheritance;
- a critical point or phase transition;
- a preferred healthy/pathological direction for any retained static coordinate;
- a claim that genomic, RNA, protein, or composition measurements are interchangeable.

## Next gate

The static B2 architecture is closed.

The next legitimate work is prospective rather than retrospective:

1. freeze the genome-wide methylation extension specification or explicitly close that extension without inspecting its association results;
2. freeze the next modal + scalar + conglomeration protocol before new predictive or dynamic endpoints are examined;
3. select ordered perturbation/time-course datasets and established benchmark models;
4. test whether cross-layer organization predicts or constrains subsequent response;
5. only then evaluate whether any same-coordinate dynamic pair licenses a biological chi construction.
