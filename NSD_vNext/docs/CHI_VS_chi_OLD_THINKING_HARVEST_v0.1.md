# NSD Chi vs chi / Old-Thinking Harvest v0.1

Date: 14 September 2026
Status: ACTIVE P0-D DISCOVERY NOTE / NOT A CLAIM
Governing baseline: SymC General Operations Manual v0.8.0 + NSD Project Protocol v0.1

## 1. Purpose

This note does not rehabilitate historical numerical claims. It asks a different question:

> Which architectural ideas in the older neuro papers are worth carrying forward because they generate useful, independently testable structure in the current NSD program?

The historical papers are used here as hypothesis lineage and design material. Exact old thresholds, disorder coordinates, treatment mappings, and universal-health claims are not imported.

A second purpose is to open an explicit **Capital-Chi versus local-chi investigation** without inventing a project-branded parameter.

## 2. Naming correction: no project-named system parameter

There will be **no `Chi_NSD`, no `chi_NSD`, and no whole-system parameter named after the research program or disease framework**.

The current GOM already points in the right direction: scalar, vector/modal, and conglomerate/system views are starting representations from which a fuller stability architecture may be reconstructed; modal and system objects must be named for the mathematics they actually instantiate.

Accordingly, the scientific writing will use established systems terminology.

### 2.1 Local scalar quantity

For a licensed second-order mode, the native quantity is the **modal damping ratio**, conventionally written `zeta_i` in control and vibration theory.

Within SymC cross-domain bookkeeping, the same licensed quantity may be cross-referenced as local `chi_i`, but the native term leads:

`modal damping ratio zeta_i <-> local chi_i only where the equivalence is exact or operationally validated`.

Other empirical coordinates remain named for what they are and are not renamed `chi` merely because they relate to stability.

### 2.2 System-level object

At the coupled-system level, the umbrella term is **embedded system stability** or **system-level stability structure**.

This is not a new parameter. It is the behavior of the coupled system after local dynamics, coupling, topology, feedback, spatial participation, input structure, and timescale are considered together.

The native mathematical object should be named directly when identified, for example:

- state-space **system matrix** `A`;
- local-linear **Jacobian** `J`;
- **transition / evolution operator**;
- DMD/Koopman-type operator where justified;
- neural-mass transfer operator or Jacobian where justified.

The corresponding established stability descriptors may include, where appropriate:

- **eigenspectrum**;
- **spectral abscissa** `alpha(A) = max Re(lambda_i(A))` for continuous-time asymptotic stability;
- **stability margin / stability radius** under the relevant definition;
- **modal damping ratios** for identified oscillatory modes;
- **non-normality**;
- **numerical abscissa / reactivity** for initial transient growth;
- **maximum transient gain** `G_max = sup_t ||exp(At)||`;
- **pseudospectrum / resolvent sensitivity**;
- **mode shapes / participation factors**;
- network/topological quantities when the question is explicitly topological.

No single one is presumed to be the complete system descriptor.

### 2.3 What “Capital Chi” means in this investigation

**Capital Chi is not a parameter name.** It is an internal research shorthand for the unresolved question:

> Is the fuller stability architecture that the GOM calls “progressively reconstructed chi” adequately represented by established system-level dynamical objects, and how does that architecture relate to local modal damping ratios?

In manuscripts, methods, code outputs, and tools, the established quantity name should be used instead of a branded Capital-Chi variable.

### 2.4 Relationship

The working hierarchy is:

`native observables -> local/modal models -> modal damping ratios where licensed -> coupled/modal/spatial organization -> system matrix/operator or other native system representation -> embedded system stability descriptors`

and **not**:

`whole-system stability = weighted average of local chi_i`.

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

Candidate native quantities include:

- relative modal frequency/decay geometry;
- coupling residuals;
- mode-shape or participation mismatch;
- phase-locking / coherence quantities where the signal model supports them;
- state-space distance under a stated metric;
- operator perturbation sensitivity.

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

**Forward value:** this becomes a direct falsifier of scalar-only reasoning.

The system-level representation must be able to distinguish:

`local modal damping approximately unchanged + local spectra approximately unchanged + coupling/topology altered -> embedded behavior materially altered`.

If a proposed whole-system scalar cannot distinguish this from the intact system, that scalar is insufficient for the question.

### H5 — Multi-timescale disagreement is potentially independent information

The older pain/NSD work repeatedly used short-versus-long timescale divergence, variance changes, residence/breach duration, and return behavior.

**Forward value:** retain these as candidate temporal descriptors while discarding old universal thresholds.

Candidate temporal layer:

- mean state;
- variance;
- derivative/drift;
- curvature/acceleration where justified;
- perturbation recovery time;
- residence distribution;
- cross-timescale disagreement;
- state-transition structure.

These should remain distinct until dependency/redundancy is measured.

### H6 — Recovery is a different property from location

The old papers often distinguished crossing a preferred region from remaining there or returning after perturbation.

**Forward value:** a static coordinate and a recovery property should not be treated as the same quantity.

This suggests a future distinction between:

- state/location;
- asymptotic stability;
- resilience/recovery;
- transient amplification;
- structural/network organization.

A system can share the same instantaneous local modal damping ratios and still differ in all of the latter properties.

### H7 — The old "translation layer" intuition survives, but not as forced numerical equivalence

The Alzheimer work tried to place control-theory, viscoelastic, electrophysiological, and clinical views into one translation layer.

**Forward value:** retain the cross-representation goal, but reinterpret it as a **structured correspondence problem** rather than assuming all native measures are numerically the same scalar.

The question becomes:

> Which native quantities describe the same dynamical property, which describe different properties, and what transformations or coupling relations connect them?

### H8 — Sense -> infer -> map -> act remains a useful tool architecture

The older pain/PD control diagrams separated sensing, computation/state estimation, intervention, and safety.

**Forward value:** preserve the architecture separation for future tool work:

`measurement -> Engine inference/refusal -> Atlas interpretation -> clinical/research action layer`.

The action layer remains downstream and unearned at the current evidence stage.

## 4. Lesson transferred from the oncology Chi-vs-chi investigation

The oncology investigation supplied a useful general rule:

Do not construct a system scalar by averaging scalar/modal/conglomerate features. Search first for a **native system object** from which those views may arise together.

The analogous NSD question is:

> Can a coupled neural System Model provide a native operator whose modal structure, local damping ratios, spatial participation, and system-level stability behavior are different projections of the same underlying dynamics?

Candidate operator families already allowed by current NSD architecture include:

- state-space system matrices;
- DMD/Koopman-style transition operators;
- output-only modal operators;
- qualified neural-mass Jacobians/transfer operators.

No operator is privileged yet.

## 5. Established neural-dynamics terminology changes the test

An operator-first route creates an important complication: **eigenvalues alone need not capture system behavior**.

In established dynamical-systems and theoretical-neuroscience terminology, a stable non-normal recurrent system can have negative spectral abscissa and still exhibit substantial **transient amplification**. The eigenspectrum describes asymptotic stability, while non-normality, numerical abscissa/reactivity, propagator singular values, and pseudospectral structure describe complementary aspects of transient behavior and perturbation sensitivity.

Therefore the system-level program must not search for one replacement scalar by default.

Live possibilities are:

1. asymptotic stability and transient amplification are separate necessary descriptors;
2. a known native stability margin or robust-stability quantity becomes sufficient for a specific frozen question;
3. multiple system-level coordinates are required;
4. a non-scalar operator/spectrum/geometry is the least-lossy representation.

## 6. Chi-versus-chi known-truth program

The title remains “Chi versus chi” because it refers to the GOM research question, not to a new variable. The actual test outputs use native terminology.

### CVX-01 — Same local damping-ratio vector, different coupling

Construct two coupled systems with identical local second-order factors and identical modal damping ratios but different coupling matrices.

Question: do spectral abscissa, transient gain, mode shapes, or other native system descriptors distinguish the embedded behavior?

### CVX-02 — Different local damping-ratio vectors, compensated embedded behavior

Construct different local factors whose coupling/feedback produces similar system-level response.

Question: does local difference necessarily imply system-level difference?

### CVX-03 — Locally stable, globally unstable

Each isolated subsystem is stable; coupling produces an unstable global mode.

Primary descriptors: full-system eigenspectrum and spectral abscissa.

### CVX-04 — Locally unstable, globally stabilized

At least one isolated component is unstable or poorly damped; feedback/coupling stabilizes the embedded system.

Question: which local properties survive embedding, and which are altered by closed-loop organization?

### CVX-05 — Topology failure with preserved local spectra

Hold local generators approximately fixed while rewiring or weakening long-range coupling.

Question: can system-level organization fail without a material local scalar shift?

### CVX-06 — Non-normal transient amplification

Use asymptotically stable systems with increasing non-normality/reactivity and transient gain.

Question: how much important behavior is missed by eigenvalues or modal damping ratios alone?

### CVX-07 — Cross-timescale divergence

Construct identical long-term mean behavior with different short-timescale variance/recovery structure.

Question: is timescale disagreement independent information after controlling for local modal parameters?

### CVX-08 — Recovery mismatch

Construct states with the same instantaneous local descriptors but different perturbation return times and overshoot/transient gain.

Question: which established recovery/resilience descriptors are required?

### CVX-09 — Representation disagreement

Generate a system where spectral, state-space, and spatial representations are each individually reasonable but do not map one-to-one.

Question: what can be translated and what must remain distinct?

### CVX-10 — Structural refusal phenotype

Construct/identify cases where local scalar admission repeatedly fails while other modal/system structure remains reliable.

Question: is refusal merely technical, or can stable refusal patterns become an independently reproducible phenotype after quality controls?

## 7. Promotion path for any whole-system scalar

No whole-system scalar receives a project-specific name.

If one becomes useful, it must retain the established name of the mathematical quantity it actually is, or receive a neutral descriptive name only after the derivation establishes that it is genuinely new.

Required sequence:

1. semantic freeze of the scientific question;
2. native system-object inventory;
3. dependency/independence map;
4. identifiability analysis;
5. known-truth CVX program;
6. label-blind real-data qualification;
7. comparison against vector/modal/system baselines;
8. external/untouched test;
9. only then assess whether one existing scalar, several coordinates, or a non-scalar representation is sufficient.

Possible outcomes:

- `EXISTING_NATIVE_SCALAR_SUFFICIENT`;
- `MULTIPLE_NATIVE_STABILITY_DESCRIPTORS_REQUIRED`;
- `NONSCALAR_SYSTEM_REPRESENTATION_REQUIRED`;
- `SYSTEM_LEVEL_REDUCTION_NOT_IDENTIFIABLE`;
- `PROPOSED_REDUCTION_SUBTRACTS_INFORMATION`.

## 8. Immediate consequence for the manuscript and Engine

The forward paper should treat local damping ratio as one possible **model-conditional consequence** of the neural Stability Architecture, not as its starting definition.

The forefront becomes:

`native signal -> qualified local modes -> coupling / topology / spatial participation -> native system representation -> established system-level stability descriptors`.

The GOM’s broader “progressively reconstructed chi” remains the research architecture. It does **not** require us to introduce a new Capital-Chi parameter.

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

Those ideas now re-enter the program only as explicit, independently testable architecture using established terminology wherever possible. The old work remains valuable as a hypothesis generator even where its original confidence exceeded its evidence.

## 10. First exact coupled-second-order result

Date: 22 September 2026

The CVX program now has an executable second-order known-truth result rather than only a design proposal.

Workflow:
- `NSD Chi-vs-System Coupled Known Truth`;
- run `35759456553`;
- artifact `nsd-chi-system-coupled-known-truth-v0-1`;
- artifact ZIP SHA-256 `b58c3e84194d6e303dcc1b1763b87466bf1364e2d5d4ffa832d0c687220cfd8b`.

Exact findings:
1. identical local damping ratios and identical full eigenspectra can coexist with substantially different transient amplification and return behavior;
2. identical local damping ratios can coexist with different embedded modal spectra after coupling;
3. locally stable second-order components can form a globally unstable coupled system.

Thus the joint lowercase-chi / broader-system target is not merely a semantic distinction. In exact known truth:
- local damping;
- embedded asymptotic spectrum;
- transient reactivity/gain;
- recovery

are separable properties.

Canonical result audit:
`CHI_SYSTEM_COUPLED_KNOWN_TRUTH_POSTRESULT_v0.1.md`.

No whole-system scalar is promoted. The empirical NSD question remains whether analogous system/operator structure can be identified from neural data with sufficient reproducibility and model adequacy.
