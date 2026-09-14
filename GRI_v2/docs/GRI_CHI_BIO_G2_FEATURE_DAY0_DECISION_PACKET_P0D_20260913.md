# GRI Chi_bio G2 feature-universe and day-0 decision packet

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome representation qualification  
**Source:** GSE114446 SCC25 short-term bulk RNA-seq  
**Approved rank architecture:** A3 (`r=2` and `r=3`)  
**Chi_bio:** `NOT_ADMITTED`  
**Real G2 trajectory inspected:** NO

## 1. Why these two choices matter

With only six PBS molecular states, PCA rank is capped at five regardless of how many genes are supplied. Adding more genes therefore does not create more temporal observations; it changes only the geometry from which the `r=2/3` state is extracted.

Likewise, the source has one PBS day-0 state and CTX measurements beginning on day 1. Whether the PBS day-0 state is licensed as the common pre-treatment origin determines whether the treatment arm contributes four or five observed one-step transitions.

Both choices affect identifiability and therefore must be fixed before the treated trajectory is opened for candidate analysis.

## 2. Feature candidate F1: external annotation universe only

Example:

```text
fixed GENCODE-v26 gene class, such as protein-coding genes
no SCC25 abundance-based selection
```

### Strengths

- maximum protection from treatment/data-driven feature selection;
- directly tied to the source annotation version;
- simple cross-run provenance.

### Weaknesses

- retains genes with effectively unmeasured/near-zero expression in SCC25;
- low-count stochastic variation can contaminate Euclidean geometry;
- an annotation class is biological metadata, not a measurement-quality filter.

## 3. Feature candidate F2: PBS-control-only detectability filter

Example class:

```text
normalize counts under the frozen normalization rule
retain genes meeting a fixed abundance/detectability floor in a fixed number of the six PBS states
freeze threshold before treated projection
```

### Strengths

- treatment states cannot determine feature admission;
- removes effectively unmeasured genes before PCA;
- naturally aligned with the approved R1 control-only basis.

### Weaknesses

- can exclude treatment-emergent genes that are silent in controls;
- exact threshold and required number of PBS states become part of the hypothesis;
- a threshold chosen after inspecting control distributions would still be data-adaptive unless the rule itself is prospectively fixed.

## 4. Feature candidate F3: external annotation intersected with PBS detectability

```text
fixed annotation class
INTERSECT
prospectively fixed PBS-only detectability rule
```

### Strengths

- separates biological identity from measurement adequacy;
- preserves treatment independence;
- avoids tens of thousands of effectively absent features;
- easy to transport into the chronic SCC25 source if the same annotation/identifier rule is available.

### Weaknesses

- still requires a prospective detectability threshold;
- treatment-emergent genes absent at baseline remain excluded;
- daily and weekly datasets may differ in quantification/preprocessing and therefore need an explicit intersection/transport policy.

### Current recommendation for later freeze

`F3` is the cleanest architecture for review: fixed GENCODE-compatible gene semantics plus an outcome-blind PBS-only detectability floor.

No exact abundance threshold is selected here.

## 5. Feature candidate F4: treatment-aware variable/high-information genes

Examples include selecting genes by:

- treated-versus-PBS differential expression;
- time-course variance across both arms;
- association with proliferation;
- maximum treated/control separation;
- best spectral behavior.

These are **not admissible for the first confirmatory G2 representation**, because the trajectory later being evaluated would help define its coordinate system.

They may remain exploratory comparators only after the primary representation is frozen.

## 6. Day-0 option D0-1: no inferred treated day-0 state

Use only observed CTX days 1-5.

Then:

```text
PBS transitions = 5
CTX transitions = 4
combined = 9
```

For the treatment-interaction model with additive input + intercept:

```text
r=2 -> 6 design columns
r=3 -> 8 design columns
```

Both remain algebraically possible, but `r=3` leaves only one row beyond the column count before any conditioning concern.

### Strength

Uses only arm-specific observed records exactly as labeled.

### Weakness

Throws away the natural pre-treatment branch point and makes the treatment arm start after exposure has already begun.

## 7. Day-0 option D0-2: common pre-treatment state

Prospectively license SCC25 PBS day 0 as the shared pre-treatment initial molecular state for both future branches:

```text
PBS: day0 -> day1 -> ... -> day5
CTX: day0(shared pre-treatment) -> CTX day1 -> ... -> CTX day5
```

Then:

```text
PBS transitions = 5
CTX transitions = 5
combined = 10
```

### Scientific rationale

Cetuximab/PBS treatment begins after the pre-treatment culture state; before treatment assignment there is not yet a distinct cetuximab molecular state. Treating the measured day-0 SCC25 PBS sample as a shared branch point therefore encodes a common pre-intervention initial condition rather than fabricating a post-treatment observation.

### Risks

- the same measured day-0 vector appears as the predictor for the first transition in both arms, so those two transition rows are not independent replicates;
- uncertainty/adequacy logic must preserve that shared-origin dependence;
- the convention is valid only if source timing confirms that day 0 precedes the treatment trajectory represented by day 1 onward.

### Current recommendation for later freeze

`D0-2` is preferred because it encodes the experimental branch point and gives the treatment trajectory its observed pre-intervention origin, while explicitly treating the duplicated predictor as one shared measurement, not two independent samples.

## 8. Consequence for uncertainty

Under D0-2, the 10 transition equations do **not** equal 10 independent biological replicates. They are two serial descendants of one shared initial measurement.

Therefore:

- row count may establish algebraic rank;
- row count must not be converted into naive iid degrees of freedom;
- leave-one-transition diagnostics are sensitivity analyses, not bootstrap biological replication;
- any model-conditional uncertainty must state that it does not estimate between-replicate biological variance.

## 9. Current recommendation bundle for review

```text
feature architecture: F3
  fixed annotation semantics
  + prospectively fixed PBS-only detectability rule

day-0 architecture: D0-2
  common measured pre-treatment SCC25 day-0 state
  + explicit shared-origin dependence
```

Exact detectability threshold and exact gene-identifier handling remain to be frozen.

No real candidate result was used to formulate this recommendation.
