# GRI Chi_bio SCC25 R1 control-only rank decision packet

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome science-decision preparation  
**Candidate representation:** R1 control-only unsupervised transcriptomic basis  
**Decision made by this document:** NO  
**Chi_bio outcomes inspected:** NO

## 1. Why this is now the next true science choice

The G1/S1/L3 family, G2 comparator, source identities, synthetic known-truth behavior, transition-fit mechanics, and anti-leakage rules are already specified. The first real temporal operator cannot be estimated until the empirical transcriptomic state itself is frozen.

For R1 the remaining scientific choice is not merely whether to run PCA/SVD. It is how many control-derived dimensions are admitted and by what outcome-blind rule.

The rule must be frozen before inspecting:

- treated-state projections;
- candidate transition spectra;
- distance to unity;
- proliferation timing;
- ATAC agreement;
- single-cell carrier support;
- chronic-versus-short-term transport.

## 2. Hard algebraic ceilings

### Short-term daily source, GSE114446

PBS provides six ordered states (day 0-5), so a centered control-only SVD has rank at most five before any transition-model constraints.

A treatment-aware shared transition form using both arms can provide ten one-step transitions if the day-0 PBS state is prospectively licensed as the common pre-treatment state for both arms. Even then, fitting

```text
x_(k+1) = T x_k + B u_k + c
```

with one binary treatment input and intercept requires `d+2` linearly independent predictor columns. The formal full-rank ceiling is therefore `d <= 8` from transition count, but the control-fitted basis itself limits R1 to `d <= 5`.

These are mathematical ceilings, not recommended dimensions.

### Chronic weekly source, GSE98812

Eleven PBS states imply centered control-only rank at most ten. The previously derived shared-transition ceiling is `d <= 18`, so the control basis rather than the transition count is the tighter algebraic ceiling.

### Cross-timescale implication

If one R1 rule is intended to transport between the daily and weekly SCC25 sources without redefining the coordinate, it must be meaningful under the stricter short-term source. That makes a very low-dimensional state unavoidable.

## 3. Prior-art constraint

Dynamic Mode Decomposition and related reduced-order system-identification methods routinely use SVD/PCA-like subspace reduction before identifying a transition operator. DMD with control also provides established prior art for explicit exogenous input terms.

Relevant methods include:

- Schmid PJ, *Dynamic mode decomposition of numerical and experimental data*, J Fluid Mech 656 (2010), DOI `10.1017/S0022112010001217`;
- Proctor JL, Brunton SL, Kutz JN, *Dynamic Mode Decomposition with Control*, SIAM J Appl Dyn Syst 15 (2016), DOI `10.1137/15M1013857`;
- Askham T, Kutz JN, *Variable Projection Methods for an Optimized Dynamic Mode Decomposition*, SIAM J Appl Dyn Syst 17 (2018), DOI `10.1137/M1124176`;
- Schmid PJ, *Dynamic Mode Decomposition and Its Variants*, Annu Rev Fluid Mech 54 (2022), DOI `10.1146/annurev-fluid-030121-015835`.

This prior art removes any novelty claim from simply choosing a truncated SVD and fitting `T`. It also makes rank choice an explicit model-order decision rather than invisible preprocessing.

## 4. Candidate rank rules

### R1-A: fixed rank selected before looking at source spectra

Example form:

```text
r = fixed small integer
```

#### Advantages

- strongest protection from data-adaptive rank selection;
- simple clean-room reproducibility;
- no risk that control singular-value shape indirectly tunes the rank;
- identical rank can be imposed across daily and weekly sources.

#### Weaknesses

- the integer can be arbitrary unless independently justified;
- too small a rank may discard real regulatory structure;
- too large a rank may exhaust the very limited transition information.

#### Scientific burden

A fixed rank must have a reason beyond computational convenience.

## 5. R1-B: control-only cumulative-variance rule

Example form:

```text
choose smallest r whose control-only cumulative explained variance >= q
```

with `q` frozen before the singular values are inspected.

#### Advantages

- outcome-blind;
- reproducible;
- lets each source respond to its own measurement geometry.

#### Weaknesses

- cumulative variance is not dynamical identifiability;
- a fixed percentage can select different dimensions across sources, complicating cross-timescale transport;
- with only six daily control states, high variance thresholds can push to the sample-rank ceiling;
- variance directions need not be regulatory directions.

#### Cross-source issue

A coordinate whose dimension changes between daily and weekly sources is not literally the same state representation unless a further transport map is frozen.

## 6. R1-C: control-only predictive rank selection

Example form:

```text
predeclare candidate ranks r in a small bounded set
choose r by a control-only one-step prediction criterion
never use treated states or phenotype to select r
```

Possible mechanics include leave-one-transition-out or rolling-origin error on the PBS sequence.

#### Advantages

- ties model order to the temporal task rather than static variance;
- treated trajectory remains untouched;
- directly asks whether added dimensions improve control-dynamics reconstruction.

#### Weaknesses

- the daily PBS series contains only five one-step transitions, making resampling extremely small and unstable;
- rank selection and transition estimation reuse nearly the same sequence;
- apparent predictive differences can be dominated by one transition;
- a flexible selection criterion can overfit even without treatment labels.

#### Disposition

Scientifically attractive in larger temporal data, but weak as the sole first-rank selector for six daily control states.

## 7. R1-D: singular-value/noise thresholding

A rank can in principle be selected by a prospectively fixed singular-value threshold or an optimal hard-threshold estimator under an explicit noise model.

#### Advantages

- mathematically defined;
- can separate obvious low-rank signal from a noise floor under suitable assumptions.

#### Weaknesses

- transcriptomic count noise and six-state temporal sampling do not automatically satisfy the idealized random-matrix/noise assumptions behind generic optimal thresholds;
- preprocessing strongly affects the singular spectrum;
- the rule still requires a frozen normalization/noise model before use.

#### Disposition

Retain as a sensitivity or future option, not the cleanest primary rule for the first SCC25 pass.

## 8. R1-E: common dimension chosen by cross-source intersection before outcomes

A rank can be selected from source architecture alone so the same dimension exists in both daily and weekly control bases.

For example, the candidate rule could constrain the state to a small prespecified range compatible with the daily control rank and use the same `r` in both sources.

#### Advantages

- directly protects cross-timescale comparability;
- avoids defining a different coordinate in each dataset;
- makes transport failure interpretable.

#### Weaknesses

- still needs a principled way to choose the exact integer;
- common dimension does not guarantee common biological meaning;
- separate bases of the same dimension can still represent different subspaces.

## 9. Strongest current recommendation for review

For the **first G2 feasibility test**, the cleanest architecture is now:

```text
R1 control-only basis
+ one common predeclared low dimension across SCC25 daily and weekly sources
+ basis fit independently within each PBS control sequence
+ treated states projected without refitting
+ explicit principal-angle/subspace transport diagnostic between control bases
+ no proliferation/ATAC/scRNA use in rank selection
```

The unresolved item is the exact dimension.

Given only six daily PBS states, the scientifically conservative review range is:

```text
r in {2, 3}
```

not because either rank has already performed better, but because:

- both are comfortably below the daily rank ceiling of five;
- both leave more transitions than predictor dimensions in the shared `T+B u+c` design;
- neither requires examining the singular-value spectrum first;
- they are small enough to expose whether a coherent low-order operator exists before scaling complexity;
- the protocol explicitly favors the smallest adequate pilot before broad expansion.

This document does **not** choose between `r=2` and `r=3`.

## 10. Why not inspect both and choose the prettier result

Running both ranks as equal confirmatory alternatives and then selecting whichever gives a cleaner unity crossing would violate the coordinate-independence rule.

If both are to be run, their roles must be frozen in advance, for example:

```text
primary rank = one predeclared value
sensitivity rank = the other predeclared value
```

with no promotion based on which one looks better.

Alternatively, one can define a precommitted robustness condition such as:

```text
material conclusions must agree across r=2 and r=3 or return REPRESENTATION_DEPENDENT_NO_TRANSFER
```

That is a different scientific design and must itself be frozen before outcomes.

## 11. Remaining choices bundled with rank

An empirical R1 freeze also needs:

- count transformation / normalization;
- feature-universe rule;
- whether each source gets its own PBS-fitted basis or one external basis is transported across sources;
- day-0 treatment initialization convention for GSE114446;
- shared `T+B u+c` versus separate-arm `T` primary model;
- residual/conditioning refusal thresholds;
- uncertainty procedure appropriate to tiny serial time series.

These cannot be inferred from existing Chi outcomes because none have been computed.

## 12. Exact stop boundary

The safe mathematical, source, provenance, and implementation work can continue up to the point of preparing the empirical runner. But **choosing the primary empirical state/rank design changes the scientific definition of the first real temporal test.**

The current leading decision is therefore:

```text
PRIMARY R1 DESIGN:
A) fixed r=2, r=3 as frozen sensitivity
B) fixed r=3, r=2 as frozen sensitivity
C) require representation robustness across both without designating one winner
D) another prospectively justified rule
```

No option is selected in this packet.
