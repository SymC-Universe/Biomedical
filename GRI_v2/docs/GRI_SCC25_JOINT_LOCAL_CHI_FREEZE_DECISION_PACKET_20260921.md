# GRI SCC25 joint local-dynamics <-> broader-Chi prospective freeze decision packet

**Date:** 2026-09-21/22  
**Status:** SCIENTIFIC DECISION GATE / NO JOINT OUTCOMES OPENED  
**Purpose:** define the remaining choices that must be made before testing whether broader system organization conditions local dynamics, and whether local dynamics predict future system organization.

## Status entering this gate

The following are already resolved and are not reopened here:

- source: Stein-O'Brien SCC25 weekly time course, GSE98812/GSE98813/GSE98815;
- main trajectory: 11 weeks x 2 arms, 20 one-step transitions;
- RNA source and methylation source identities: frozen and hash-bound;
- proliferation: external validation phenotype, not state-construction input;
- current scalar chi branch: **REFUSED** for the frozen R1/A3 G2 representation;
- `rho(T)`: model-class spectral quantity only, not biological chi;
- local object for this joint experiment: native reduced RNA/modal state, denoted `z_t`;
- source-native CoGAPS: comparator/prior evidence, not independent confirmation;
- published outcome/time-informed feature filters: prohibited as neutral SymC feature construction.

No joint local/system prediction has been run.

## Scientific question

The first-direction question is:

[
H_{Chi	o local}:
P(z_{t+1}mid z_t,S_t,u_t)
quad	ext{contains held-out information beyond}quad
P(z_{t+1}mid z_t,u_t),
]

where `S_t` is an independently constructed methylation/context representation and `u_t` is treatment arm/input.

The reciprocal question is:

[
H_{local	oChi}:
P(S_{t+1}mid S_t,z_t,u_t)
quad	ext{contains held-out information beyond}quad
P(S_{t+1}mid S_t,u_t).
]

The joint external-outcome question is:

[
P(Y_{t+1}mid z_t,S_t,u_t)
]

versus local-only and context-only models, where `Y` is the preserved proliferation phenotype.

This first test deliberately uses methylation/context as the non-algebraically-guaranteed system information. RNA-derived `T`, `rho(T)`, and modal quantities are **not** added back to the "broader" predictor when predicting the RNA state, because that would partially build the answer into the input.

## Decision 1: methylation/context representation

Three defensible options remain.

### A. PBS-control-only unsupervised methylation basis

Fit a small basis from the 11 PBS methylation states only, then project both arms.

**Strengths**
- mirrors the already-qualified R1 RNA independence logic;
- treatment trajectory does not define the context basis;
- computationally simple;
- supports rank-matched sensitivity.

**Liabilities**
- only 11 control states;
- variance directions need not be regulatory;
- platform-scale methylation makes estimator stability important;
- weak mechanistic interpretation.

### B. externally fixed biological-module methylation representation

Map CpGs to prospectively fixed gene/regulatory modules and summarize module methylation without learning the basis from the SCC25 trajectory.

**Strengths**
- stronger independence from SCC25 outcomes;
- clearer biological interpretation;
- directly tests whether a distinct substrate/context layer adds information.

**Liabilities**
- CpG-to-gene/region mapping and aggregation are themselves scientific choices;
- promoter-only mapping would be biologically too narrow;
- module panel must be fixed externally;
- dimensionality must remain small relative to 20 transitions.

### C. both A and B as coequal representations

Require material conclusions to agree, or return `REPRESENTATION_DEPENDENT`.

**Strengths**
- strongest direct attack on representation dependence;
- fits the existing A3 philosophy.

**Liabilities**
- doubles analysis branches;
- with a tiny time series, disagreement may be common and power lower;
- interpretation is more complex.

**Recommendation for discussion:** C is scientifically strongest if the goal is architecture rather than maximizing a positive result. A supplies a purely data-geometric context view; B supplies a biologically structured context view. This recommendation is pre-result and does not freeze either basis.

## Decision 2: validation geometry

### V1. Preserve historical leave-one-transition-out

Train on 19 transitions, predict the omitted transition, repeated across all 20.

**Strength:** direct comparability with existing G2 D1/D2.

**Limit:** for a time series, training can include weeks later than the held-out transition.

### V2. Rolling-origin / forward-chaining

For each arm, train only on earlier transitions and predict the next future transition after a minimum burn-in.

**Strength:** closer to the intended predictive direction and resistant to future-to-past leakage.

**Limit:** very small training sets, fewer evaluable transitions, unstable higher-dimensional models.

### V3. Co-primary V1 + V2 with agreement required

Use LOTO for continuity and rolling-origin as the temporal-direction stress test.

**Recommendation for discussion:** V3. If broader context appears useful only when future states are allowed into the training set, the conditioning claim should narrow or refuse.

## Decision 3: incremental-value statistic

The target should be **prediction improvement**, not contemporaneous correlation.

Candidate primary object:

[
Delta E =
E_{mathrm{local only}}
-
E_{mathrm{local+context}},
]

where `E` is held-out normalized squared error / NRMSE computed under the frozen validation geometry.

Recommended supporting diagnostics:

- fraction of held-out transitions improved;
- arm-specific effects;
- transition-level error differences;
- effect consistency across r=2/r=3 local representations;
- context-representation agreement;
- time-alignment null.

No universal numeric improvement threshold is frozen here.

## Decision 4: time-alignment null

A high-value non-circular null is to circularly shift the methylation/context sequence within arm while preserving its internal serial order, then rerun the same held-out comparison.

This asks whether the **correctly aligned** broader architecture adds more predictive information than a context trajectory with similar marginal and serial structure but the wrong biological timing.

Because only 10 transitions per arm exist, the exact null support is small. The null should therefore be treated as finite exact/permutation evidence, not asymptotic high-power inference.

**Recommendation for discussion:** include this null. It directly attacks the possibility that any smooth time-varying second modality will appear useful merely because both modalities drift over the 11 weeks.

## Decision 5: interaction term

A fully expanded `z x S` interaction is dangerous with only 20 transitions.

Options:

- **I0:** no interaction in the first primary test; additive conditional information only;
- **I1:** one predeclared low-rank bilinear interaction, with fixed regularization;
- **I2:** interaction exploratory only after primary additive test, carrying promotion debt.

**Recommendation for discussion:** I0 primary, I2 exploratory. A full interaction model would consume too much of the available information budget before a basic conditional effect is established.

## Decision 6: outcome classes

Recommended categorical outcomes:

```text
SYSTEM_CONDITIONS_LOCAL
LOCAL_CONDITIONS_SYSTEM
BIDIRECTIONAL_COMPLEMENTARITY
LOCAL_SUFFICIENT
CONTEXT_SUFFICIENT
REDUNDANT_REPRESENTATIONS
REPRESENTATION_DEPENDENT
TIME_ALIGNMENT_DEPENDENT
SCALAR_REFUSED_SYSTEM_USEFUL
BOTH_INADEQUATE
STANDARD_TOOLKIT_SUBSUMES
```

No positive class is preferred.

## Decision 7: source-native / standard-toolkit comparison

The first joint model must not be compared only against itself.

For temporal-program description:
- published CoGAPS result is source-native prior art.

For one-step prediction:
- persistence;
- arm-specific mean-next-state;
- existing D1 shared-operator model;
- DMD/DMDc or equivalent reduced state-space comparator where same-question.

For multi-view temporal integration:
- a time-aware standard method such as MEFISTO is a candidate comparator, but its exact role must match the frozen question and its complexity must be supportable by the tiny trajectory.

The project may report `STANDARD_TOOLKIT_SUBSUMES` if the standard/native route contains the same information with no defensible SymC increment.

## Recommended freeze candidate, not yet authorized

The cleanest first joint test is:

```text
local object:
  current admitted R1/A3 RNA modal state z_t, r=2 and r=3 coequal

broader independent context:
  methylation S_t under two coequal representations:
  A = PBS-control-only unsupervised basis
  B = externally fixed biological-module basis

primary direction:
  z_(t+1) ~ z_t + treatment
  versus
  z_(t+1) ~ z_t + S_t + treatment

reciprocal direction:
  S_(t+1) ~ S_t + treatment
  versus
  S_(t+1) ~ S_t + z_t + treatment

validation:
  V1 LOTO for continuity
  plus V2 rolling-origin for temporal-direction stress
  material disagreement => REPRESENTATION_DEPENDENT / TEMPORAL_VALIDATION_DEPENDENT

joint phenotype:
  proliferation remains unopened until all construction and decision rules are frozen

interaction:
  not primary; exploratory only after additive conditional test

time-alignment null:
  within-arm circular shift of S_t

scalar chi:
  absent by current refusal, not imputed from rho(T)
```

## Why this is the current stop point

Choosing A/B/C, V1/V2/V3, the exact module basis, dimensionality, regularization and numerical promotion rule changes the scientific question and can change the answer.

Those values therefore cannot be filled mechanically after the existing outcomes are known.

Everything up to this point can be prepared without opening the joint result. The next step after explicit freeze is to implement the exact source adapter and known-truth fixtures, then run a tiny preflight before the full 20-transition outcome-bearing analysis.
