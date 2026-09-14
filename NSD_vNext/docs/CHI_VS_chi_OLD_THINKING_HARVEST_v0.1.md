# NSD Chi vs chi / Old-Thinking Harvest v0.1

Date: 14 September 2026
Status: ACTIVE P0-D DISCOVERY NOTE / NOT A CLAIM
Governing baseline: SymC General Operations Manual v0.8.0 + NSD Project Protocol v0.1

## 1. Purpose

This note does not rehabilitate historical numerical claims. It asks a different question:

> Which architectural ideas in the older neuro papers are worth carrying forward because they generate useful, independently testable structure in the current NSD program?

The historical papers are used here as hypothesis lineage and design material. Exact old thresholds, disorder coordinates, treatment mappings, and universal-health claims are not imported.

A second purpose is to open an explicit **Chi versus chi** investigation for NSD, informed by the GOM and the oncology `Chi_bio` program.

## 2. Working Chi versus chi distinction

This is a project-local working distinction, not yet a program-wide notation rule.

### 2.1 Lowercase `chi`

Lowercase `chi_i` denotes a **local or mode-specific scalar stability coordinate** only where a native model licenses it.

For a licensed second-order mode this may be the ordinary damping ratio or an exactly derived equivalent. Other empirical coordinates remain named for what they are and are not renamed `chi` merely because they relate to stability.

Lowercase `chi` is therefore a possible consequence/readout of a qualified local dynamical model. It is not the definition of the full neural Stability Architecture.

### 2.2 Capital `Chi_NSD`

`Chi_NSD` is a **candidate higher-order system-level stability object** describing embedded realized behavior after local modes, coupling, topology, context, feedback, and system organization are considered together.

Current status:

`Chi_NSD = NOT_ADMITTED`

Critically, `Chi_NSD` is **not assumed to be scalar**. It may ultimately be:

- a system operator;
- an invariant derived from that operator;
- a structured tuple/state;
- a geometric object;
- a scalar with a natural boundary;
- or not identifiable as a coherent single object at all.

Capitalization is used here as a bookkeeping firewall against silently replacing system architecture with a local damping ratio.

### 2.3 Relationship

The working hierarchy is:

`native observables -> local/mode models -> {chi_i where licensed} -> coupled/modal/spatial organization -> embedded system object -> candidate Chi_NSD`

and **not**:

`Chi_NSD = weighted average of chi_i`.

A weighted average, weakest-link rule, or other aggregation may be retained as a baseline/comparator, but cannot become the definition merely because it produces a convenient number.

This implements the GOM distinction:

`LOCAL DYNAMICAL IDENTITY != EMBEDDED REALIZED BEHAVIOR`.

## 3. Old ideas worth carrying forward

### H1 — Multi-mode state before whole-system scalar

The older addiction work explicitly represented reward, control, stress, habit, interoception, and environment as separate local coordinates and introduced a coupling matrix rather than pretending the reward system was one oscillator.

**Forward value:** preserve the idea of a vector of local states plus coupling. Retire the old weighted `chi_net` as a definition.

Current translation:

`local scalar layer + modal/vector layer + coupling/conglomerate layer`.

### H2 — Relational mismatch can matter even when local states look acceptable

The older reward-control "phase divergence" idea treated disagreement between subsystems as important in its own right.

**Forward value:** test whether mismatch among locally qualified modes predicts or produces different embedded behavior. Do not retain historical numerical divergence thresholds.

Candidate objects include:

- pairwise mode mismatch;
- relative decay/frequency geometry;
- coupling residuals;
- cross-region participation mismatch;
- state-space distance after uncertainty normalization;
- loss of phase/temporal coordination where the native model supports it.

### H3 — Failure architecture can differ without requiring different scalar positions

The older dementia work separated candidate mechanisms into restoration/substrate failure, controller variance, interface/coupling mismatch, and topology failure.

**Forward value:** reuse these as **adversarial architecture families**, not as established disease assignments.

The current Engine should be challenged with systems where failure arises from:

1. local mode/restoration change;
2. controller/noise/parameter variance;
3. interface or coupling transformation;
4. topology/network organization;
5. combinations of the above.

### H4 — Normal local observables can coexist with failed system organization

The old FTD framing emphasized a particularly valuable possibility: local spectral power may appear comparatively preserved while long-range organization fails.

**Forward value:** this becomes a direct falsifier of scalar-only NSD.

A candidate `Chi_NSD` architecture must be able to represent the case:

`local chi_i approximately unchanged + local spectra approximately unchanged + coupling/topology altered -> embedded behavior materially altered`.

If a proposed system scalar cannot distinguish this from the intact system, it is insufficient for that question.

### H5 — Multi-timescale disagreement is potentially independent information

The older pain/NSD work repeatedly used short-versus-long timescale divergence, variance changes, residence/breach duration, and return behavior.

**Forward value:** retain the quantities as candidate temporal descriptors, while discarding old universal thresholds.

Candidate temporal layer:

- mean state;
- variance;
- derivative/drift;
- curvature/acceleration;
- perturbation recovery time;
- residence distribution;
- cross-timescale disagreement;
- state-transition structure.

These should remain distinct until dependency/redundancy is measured.

### H6 — Recovery is a different property from location

The old papers often distinguished crossing a preferred region from remaining there or returning after perturbation.

**Forward value:** a static coordinate and a recovery property should not be treated as the same quantity.

This suggests a future distinction between:

- position/state;
- resilience/recovery;
- transient amplification;
- structural organization.

A system can share the same instantaneous local `chi_i` values and still differ in all three of the latter properties.

### H7 — The old "translation layer" intuition survives, but not as forced numerical equivalence

The Alzheimer work tried to place control-theory, viscoelastic, electrophysiological, and clinical views into one translation layer.

**Forward value:** retain the cross-representation goal, but reinterpret it as a **structured correspondence problem** rather than assuming all native measures are numerically the same scalar.

The question becomes:

> Which native quantities describe the same system property, which describe different properties, and what transformations/couplings connect them?

That is a Capital-Chi question.

### H8 — Sense -> infer -> map -> act remains a useful tool architecture

The older pain/PD control diagrams separated sensing, computation/state estimation, intervention, and safety.

**Forward value:** preserve the architecture separation for future tool work:

`measurement -> Engine inference/refusal -> Atlas interpretation -> clinical/research action layer`.

The action layer remains downstream and unearned at the current evidence stage.

## 4. Oncology lesson transferred to NSD

The `Chi_bio` oncology investigation created an important template:

Do not construct a system scalar by averaging scalar/modal/conglomerate features. Search for a **native system object** from which those views arise together.

In oncology, the candidate route became operator-first:

`coupled regulatory operator -> eigenspectrum/eigenvectors -> candidate boundary scalar`.

The analogous NSD question is:

> Can a coupled neural System Model provide an operator whose modal structure, local dynamical scalars, spatial participation, and system-level stability are different projections of the same underlying object?

Candidate operator families already allowed by current NSD architecture include:

- state-space system matrices;
- DMD/Koopman-style transition operators;
- output-only modal operators;
- qualified neural-mass Jacobians/transfer operators.

No operator is privileged yet.

## 5. Important consequence from native neural dynamics

An operator-first route creates a useful complication: **eigenvalues alone need not capture system behavior**.

Non-normal recurrent neural systems can be asymptotically stable while still producing large transient amplification. Therefore a Capital-Chi construction based only on a dominant eigenvalue or spectral radius could miss clinically or functionally important embedded behavior.

This creates three live possibilities:

1. `Chi_NSD` is a scalar boundary coordinate and transient amplification is an independent component;
2. `Chi_NSD` requires both asymptotic and transient terms;
3. the correct system object is non-scalar, and forcing a scalar destroys necessary information.

All three remain open.

## 6. Chi-versus-chi known-truth program

Add the following adversarial families before clinical interpretation.

### CVX-01 — Same local chi vector, different coupling

Construct two coupled systems with identical local second-order factors and identical `{chi_i}` but different coupling matrices.

Question: can the system architecture distinguish different embedded behavior?

### CVX-02 — Different local chi vectors, compensated embedded behavior

Construct different local factors whose coupling/feedback produces similar system-level response.

Question: does a proposed Capital-Chi construction avoid falsely treating local difference as whole-system difference?

### CVX-03 — Locally stable, globally unstable

Each isolated subsystem is stable; coupling produces an unstable global mode.

This directly tests the GOM local-versus-embedded firewall.

### CVX-04 — Locally unstable, globally stabilized

At least one isolated component is unstable or poorly damped; feedback/coupling stabilizes the embedded system.

Question: what local properties survive embedding, and what does not?

### CVX-05 — Topology failure with preserved local spectra

Hold local generators approximately fixed while rewiring or weakening long-range coupling.

Question: can system-level organization fail without a material local scalar shift?

### CVX-06 — Non-normal transient amplification

Use stable eigenspectra with increasing non-normality/transient gain.

Question: does the architecture detect meaningful transient instability missed by asymptotic eigenvalue criteria?

### CVX-07 — Cross-timescale divergence

Construct identical long-term mean behavior with different short-timescale variance/recovery structure.

Question: is timescale disagreement independent information after controlling for mean/local chi?

### CVX-08 — Recovery mismatch

Construct states with the same instantaneous coordinates but different perturbation return times and overshoot.

Question: does recovery require a separate architecture component?

### CVX-09 — Representation disagreement

Generate a system where spectral, state-space, and spatial representations are each individually reasonable but do not map one-to-one.

Question: what can be translated and what must remain distinct?

### CVX-10 — Structural refusal phenotype

Construct/identify cases where local scalar admission repeatedly fails while other modal/system structure remains reliable.

Question: is refusal merely technical, or can stable refusal patterns become an independently reproducible phenotype after quality controls?

## 7. Promotion path for Capital Chi

`Chi_NSD` may not be promoted because the architecture is aesthetically coherent.

Required sequence:

1. semantic freeze;
2. candidate system-object inventory;
3. dependency/independence map;
4. identifiability analysis;
5. known-truth CVX program;
6. label-blind real-data qualification;
7. comparison against vector/modal/system baselines;
8. external/untouched test;
9. only then, if a scalar emerges, test whether any natural boundary such as unity has independent meaning.

Possible outcomes are explicitly:

- `SCALAR_CAPITAL_CHI_ADMITTED`;
- `NONSCALAR_CAPITAL_CHI_ARCHITECTURE`;
- `MULTIPLE_SYSTEM_COORDINATES_REQUIRED`;
- `CAPITAL_CHI_NOT_IDENTIFIABLE`;
- `CAPITAL_CHI_SUBTRACTS_INFORMATION`.

The program is not required to produce a scalar.

## 8. Immediate consequence for the NSD manuscript and Engine

The forward paper should treat lowercase local `chi` as one possible **model-conditional consequence** of the neural Stability Architecture, not as its starting definition.

The forefront becomes:

`native signal -> qualified local modes -> relational/coupled organization -> embedded stability architecture -> Chi_NSD question`.

Damped-oscillator `chi` remains scientifically important where it is licensed, but it is downstream of the broader reconstruction rather than the universal lens through which every neural feature is forced.

## 9. Why the old papers still matter

Their useful continuity is not the old numerical answers. It is that, before the current protocol existed, the papers repeatedly reached for:

- multiple local modes;
- coupling matrices;
- regional divergence;
- topology failure;
- controller variance;
- cross-timescale disagreement;
- recovery/residence;
- multimodal structure;
- and systems-within-systems.

Those ideas now re-enter the program only as explicit, independently testable architecture. The old work therefore remains valuable as a hypothesis generator even where its original confidence exceeded its evidence.