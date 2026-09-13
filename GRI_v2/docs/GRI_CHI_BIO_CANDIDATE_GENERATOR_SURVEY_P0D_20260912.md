# GRI Chi_bio candidate-generator survey

**Date:** 2026-09-12  
**Status:** P0-D DOMAIN-NATIVE GENERATOR SURVEY, NO CANDIDATE FROZEN  
**Chi_bio status:** `NOT_ADMITTED`  
**Cancer-specific Chi_bio values inspected:** NO  
**Unity placement inspected:** NO

## 1. Decision criterion

A candidate is interesting only if a native biological/dynamical model produces a system-level compressed coordinate with:

1. a defensible generator;
2. identifiable inputs;
3. a non-arbitrary normalization;
4. explicit modal/vector carrier structure;
5. an explicit relationship to conglomerate/system organization;
6. construction-aware uncertainty and refusal;
7. a natural reason for unity if `Chi_bio = 1` is to have boundary meaning;
8. a realistic path from current or available measurements to the required operator.

No candidate is ranked by where current cancers would land.

## 2. Candidate G1: normalized regulatory-interaction eigenvalue

### Native model

Guo & Amir, *Nature Communications* 2021, `doi:10.1038/s41467-020-20472-x`, analyze transcriptional regulatory-network stability. In their fast-mRNA-reduction model:

```text
dc/dt = beta0 [phi(c) - c]
J = beta0 (M - I)
M_ij = d phi_i / d c_j at steady state
```

The steady state is stable when the maximal real part of the eigenvalues of `M` is below 1; equivalently, the Jacobian eigenvalues remain in the left half-plane.

### Why this matters for Chi_bio

This is the first strong domain-native collision found in the current search where a **dimensionless regulatory interaction object has a natural unity stability boundary** rather than unity being imposed afterward.

A candidate of the general form

```text
candidate_G1 = max Re eig(M)
```

would inherit `1` from the governing model, not from cancer placement.

### Major cautions

- `M` is a local regulatory response/interactions matrix, not a covariance matrix;
- current TCGA C1 quantities do not directly estimate `M`;
- the model is a specific transcription/protein regulatory model, not automatically a methylation-RNA-tumor System Model;
- a local steady-state boundary is not automatically whole-tumor embedded stability;
- estimating `M` from one longitudinal trajectory can be underidentified;
- a system-level scalar still cannot replace the eigenvectors/eigenspaces or conglomerate context;
- the candidate may be negative or otherwise have a distribution unlike historical Chi expectations; that cannot be repaired by rescaling after inspection.

### Current disposition

`VERY_HIGH_PRIORITY_FOR_FORMAL_DERIVATION_REVIEW`, not frozen.

Reason: strongest natural unity boundary found so far with direct gene-regulatory stability meaning.

## 3. Candidate G2: discrete-time transition-operator spectral radius

### Native model

For a locally linear sampled process

```text
x_(t+1) = T x_t + B u_t + noise
```

the autonomous part is asymptotically stable when all eigenvalues of `T` lie inside the unit disk, i.e. `rho(T) < 1`.

### Strength

- unity is mathematically natural;
- modal/vector structure is explicit through the eigenvectors of `T`;
- time-course data can in principle estimate a reduced transition operator;
- external inputs can be modeled explicitly rather than hidden.

### Major cautions

- `rho(T)` depends on sampling interval and representation;
- a single forced trajectory is insufficient for a high-dimensional unconstrained operator;
- treating continual cetuximab exposure as autonomous dynamics would be invalid;
- high-dimensional regularization can determine the answer unless frozen independently;
- spectral radius alone can conceal non-normal transient amplification;
- reduced-state construction must be frozen before outcome inspection.

### Current disposition

`HIGH_PRIORITY_METHOD_CANDIDATE`, not frozen.

It is especially relevant to the 11-week SCC25 series, but only after a valid exogenous-input/reduced-state design is established.

## 4. Candidate G3: continuous-time Jacobian stability margin

### Native model

For

```text
dx/dt = f(x)
```

local stability at a fixed point is governed by the maximal real part of the Jacobian eigenvalues:

```text
Lambda = max Re eig(J)
stable if Lambda < 0
unstable if Lambda > 0
```

This is standard linear stability theory and is widely used in gene-regulatory models.

### Strength

- direct biological dynamical meaning when `J` is identifiable;
- explicit modes and response times;
- compatible with local perturbation-response experiments.

### Limitation for the requested unity boundary

The natural boundary is **0**, not 1. A transformation that shifts or rescales the boundary to 1 is scientifically acceptable only if the scale/offset is generated independently by the governing model. Simply defining `Chi_bio = 1 + Lambda/c` after seeing data would be prohibited.

### Current disposition

`HIGH_VALUE_GENERATOR_PRIMITIVE`, but not yet a natural `Chi_bio=1` coordinate by itself.

## 5. Candidate G4: homeostatic attraction versus stochastic diffusion

### Native precedent

Li et al., PNAS 2016 (`PMID 26929366`, `doi:10.1073/pnas.1519210113`) described cancer-cell attractor dynamics with a Fokker-Planck framework containing opposing homeostatic attraction and stochastic diffusion/noise.

### Strength

- directly expresses a balance between stabilizing return and stochastic spreading;
- biologically close to the intended system-level stability concept;
- naturally connects state distribution, perturbation, return, and escape.

### Limitation

No universal unity coordinate follows from the published framework without specifying the state-space metric, restoring operator, diffusion tensor, basin scale, and normalization. Bulk cross-sectional TCGA is insufficient to identify this dynamical balance.

### Current disposition

`HIGH_CONCEPTUAL_RELEVANCE / UNITY_NOT_YET_LICENSED`.

## 6. Candidate G5: landscape barrier versus noise/transition drive

### Native precedent

Li & Wang 2014 (`PMID 25232051`, `doi:10.1098/rsif.2014.0774`) quantified cancer-state stability using landscape barrier heights and transition paths.

A barrier-to-noise quantity can sometimes be dimensionless in stochastic escape theory.

### Strength

- system-level stability and transition interpretation;
- natural relationship to escape probability/rate;
- potential bridge to Function/Limit mapping.

### Limitation

A ratio equal to 1 is not established as a universal cancer stability transition. Landscape/barrier reconstruction is itself model-dependent and may be poorly identifiable from current GRI bulk data.

### Current disposition

`SECONDARY_CANDIDATE_FAMILY / NO_UNITY_LICENSE`.

## 7. Candidate G6: lower-level dynamical `chi_dyn`

The existing biomedical rule reserves

```text
chi_dyn = Gamma / (2 |Omega|)
```

for a genuine same-mode dissipative/restoring response when all hard gates pass.

### Strength

- unity has a natural boundary in the licensed second-order model;
- directly exposes mode-level under/critical/overdamped response where such a model is biologically valid.

### Why it is not automatically Chi_bio

`chi_dyn` is a mode/local-response coordinate. A system-level `Chi_bio` cannot be obtained by averaging mode-level `chi_dyn` values unless a separate hierarchical-closure derivation shows that the compression preserves the higher-level quantity being claimed.

### Current disposition

`POSSIBLE_COMPONENT_OR_SPECIAL_CASE`, not the system-level definition.

## 8. Candidate G7: robust feedback/small-gain style coordinate

Feedback-system theory often provides unity conditions on a loop-gain or induced-gain quantity. A regulatory System Model could in principle yield a system-level `gain < 1` stability condition.

### Strength

- unity can be natural;
- explicitly relational and embedded;
- compatible with input/output perturbation experiments.

### Limitations

- a sufficient gain condition may be conservative rather than an exact transition;
- definition depends strongly on selected inputs, outputs, norms, and feedback partition;
- current GRI has not yet frozen a native biological input/output feedback decomposition.

### Current disposition

`METHOD_FAMILY_TO_KEEP_VISIBLE`, not currently identifiable enough for freeze.

## 9. Pre-outcome comparison

| Candidate | Native biological stability meaning | Natural unity | Modal structure preserved | Current TCGA alone sufficient | Temporal source path | Current priority |
|---|---|---:|---:|---:|---:|---|
| G1 normalized regulatory interaction eigenvalue | strong/local GRN | YES in specific model | YES | NO | YES with perturbation/operator identification | VERY HIGH |
| G2 discrete transition spectral radius | strong/local sampled dynamics | YES | YES | NO | YES | HIGH |
| G3 continuous Jacobian margin | strong/local dynamics | natural boundary is 0 | YES | NO | YES | HIGH primitive |
| G4 attraction/diffusion balance | strong attractor concept | NOT YET | YES/tensor form | NO | needs population dynamics | HIGH conceptual |
| G5 barrier/noise | strong transition landscape | NOT UNIVERSAL | partly | NO | possible | SECONDARY |
| G6 chi_dyn | strong when second-order mode valid | YES | mode-specific | NO | possible | SPECIAL CASE |
| G7 feedback gain | strong if I/O model native | potentially YES | operator-dependent | NO | perturbational | KEEP VISIBLE |

## 10. Key finding before the scientific stop

The search no longer supports the statement that we do not know how a biologically native unity boundary *could* arise.

A concrete domain-native route exists in published gene-regulatory stability mathematics: a normalized interaction matrix can have a maximal-real-eigenvalue stability boundary at **1**.

However, this does **not** establish that this published matrix is the correct GRI `Chi_bio` object. The current work must still answer:

- can the corresponding operator be derived for the actual GRI scalar/modal/conglomerate System Model?
- can it be identified from available measurements without circularity?
- does it remain meaningful under methylation/RNA coupling and tumor context?
- does a cancer-level scalar preserve necessary mode/system information?
- does external evidence validate it?

## 11. Next scientific boundary

Safe work has narrowed the competition enough that **G1 and G2 deserve formal candidate derivations first**, with G3 as the underlying continuous-time reference and G4 retained as a qualitatively different stochastic-attractor family.

Choosing one of these as the frozen definition of `Chi_bio`, choosing the state variables used to construct its operator, or choosing a dimension-reduction rule that changes the operator is science-changing work.

No candidate is frozen by this survey. No cancer-specific Chi_bio values may be computed from these candidates until that freeze decision is explicitly reviewed.