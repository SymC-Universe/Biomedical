# NSD Baseline Recovery, Resilience, and Baseline Migration Plan v0.1

**Status:** DEVELOPMENT / PROSPECTIVE FRAMEWORK  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Scope:** healthy-brain recovery envelope, repeated incomplete recovery, adaptive baseline formation, and maladaptive baseline migration.  
**Scientific ceiling:** no universal tipping threshold; no claim that repeated recovery failure causes a new baseline until prospective temporal/causal criteria are satisfied.

## 1. Root question

How far can a healthy brain be displaced from its current normative operating region and still recover, and does repeated incomplete recovery predict or cause persistent migration to a new baseline?

The target is not one healthy point. Let the current baseline architecture be a conditional distribution:

\[
B_k = P(X\mid C_k)
\]

where \(X\) contains the native and, when licensed, stability variables relevant to the observation level, and \(C_k\) contains age, state, task, sleep/arousal, medication/substance status, recording context, and other frozen covariates.

A perturbation \(P_n\) produces a trajectory \(X_n(t)\).

## 2. Perturbation-response quantities

For each perturbation:

### Initial displacement

\[
D_n = d(X_n(t_0^+), B_{n^-})
\]

where \(d\) is a prospectively frozen multivariate distance appropriate to the representation.

### Peak displacement

\[
D_n^{\max}=\max_{t\in[0,T]} d(X_n(t),B_{n^-}).
\]

### Recovery time

\[
\tau_n = \inf\{t: d(X_n(t),B_{n^-})\le \epsilon_B
\text{ and remains within the band for }T_s\}.
\]

The recovery band \(\epsilon_B\) and sustain time \(T_s\) must be learned/frozen from healthy repeatability, not selected from disorder outcomes.

### Residual displacement

\[
r_n=d(X_n(T),B_{n^-}).
\]

### Recovery completeness

A perturbation may be classified prospectively as:
- COMPLETE_RETURN;
- DELAYED_COMPLETE_RETURN;
- INCOMPLETE_RETURN;
- NEW_BASELINE_CANDIDATE;
- NONIDENTIFIABLE.

No label is assigned from a single arbitrary threshold.

## 3. Baseline migration

A post-perturbation state is not called a new baseline merely because it differs from the old one.

A baseline migration candidate requires:
1. persistent displacement beyond normal within-person drift;
2. repeated occupancy over prospectively defined independent observations/sessions;
3. internal stability/reproducibility of the new state;
4. exclusion or modeling of ordinary state/context changes;
5. evidence that the new state predicts future perturbation response better than the prior baseline;
6. no dependence on one measurement modality or one outcome-driven threshold.

Define the migration vector conceptually as:

\[
M_n = B_{n^+}-B_{n^-}.
\]

The actual baseline representation may be nonlinear/distributional and need not be expressible by subtraction.

## 4. Three distinct outcomes

### A. Resilient return

The system is displaced but returns to the same normative basin.

Prediction:
- increasing perturbation size may lengthen recovery without changing the durable baseline.

### B. Adaptive baseline formation

The system does not return exactly to the old baseline but establishes a new stable configuration that preserves or improves function.

Examples may include:
- learning;
- training;
- development;
- compensatory reorganization;
- successful treatment adaptation.

A new baseline is therefore not automatically pathology.

### C. Maladaptive baseline migration

The post-perturbation state becomes persistent and is associated with degraded function, reduced future resilience, pathological symptoms, or increased susceptibility to subsequent perturbations.

This is the candidate NSD transition of greatest interest.

## 5. Repeated-recovery-failure hypothesis

Primary hypothesis:

> Repeated incomplete recovery increases the probability or magnitude of subsequent baseline migration, after controlling for perturbation magnitude, state, context, and prior baseline trajectory.

For perturbation sequence \(P_1,\ldots,P_N\), test whether:

\[
r_n,\tau_n,D_n^{\max}
\]

predict subsequent:

\[
M_{n+1}
\]

and whether the predictive relationship accumulates with repeated failures.

Competing explanations must be separated:

1. **CAUSAL_ACCUMULATION**  
   incomplete recovery contributes to later baseline migration;

2. **COMMON_CAUSE**  
   declining underlying resilience causes both poor recovery and baseline drift;

3. **REVERSE_CAUSALITY**  
   baseline migration begins first and makes recovery appear worse;

4. **STATE_CONFOUNDING**  
   apparent migration is due to sleep, medication, task, stress, substance exposure, or other context;

5. **MEASUREMENT_DRIFT**  
   apparent migration is instrumental/preprocessing/site artifact;

6. **NO_RELATION**.

## 6. Resilience margin

Rather than one universal threshold, estimate a subject/state-specific perturbation-response curve.

Conceptually:

\[
\mathcal{R}(A)=
P(\text{return to prior basin}\mid \text{perturbation magnitude }A,C).
\]

A resilience margin may be operationalized only if the data support a transition region in which probability of return declines with perturbation magnitude/frequency/duration.

Candidate quantities:
- maximum observed recoverable displacement;
- recovery-time slope with perturbation magnitude;
- residual-displacement slope;
- probability of baseline migration;
- change in future recovery after prior perturbations;
- hysteresis;
- critical slowing or rising autocorrelation where justified;
- change in local \(\chi\), modal \(\Chi\), and system \(\Chi_{\mathrm{arc}}\) separately.

No resilience margin may be interpreted as a universal human threshold.

## 7. Healthy-brain calibration

The healthy/reference program must first estimate:

- ordinary displacement from baseline under normal tasks/states;
- distribution of recovery times;
- distribution of residual displacement;
- day-to-day and session-to-session baseline drift;
- learning/adaptation-associated baseline migration;
- sleep/arousal-related movement;
- age/development effects;
- perturbation-response repeatability;
- probability of spontaneous return from large but ordinary deviations.

This creates a healthy resilience envelope rather than a healthy point.

## 8. Ethical human design

Humans are not deliberately pushed until pathological recovery failure.

Use:
- naturally occurring perturbations;
- normal cognitive/sensory tasks;
- eyes-open/eyes-closed transitions;
- safe non-invasive stimulation where independently justified;
- medication on/off or treatment transitions already occurring clinically;
- sleep/wake and fatigue states within ethical protocols;
- pain flare/recovery observations;
- affective/stress episodes captured observationally;
- cue/withdrawal/recovery cycles in addiction cohorts;
- longitudinal disease progression;
- existing controlled datasets.

Stronger perturbation-response boundaries should first be explored in:
- synthetic known-truth systems;
- established biophysical models;
- animal data where ethically and scientifically appropriate;
- existing stimulation datasets.

## 9. Domain-specific baseline-migration questions

### Pain
Does repeated acute or subacute pain with incomplete recovery predict transition toward persistent pain-network organization?

### BPD
Do repeated affective perturbations show shortened inter-episode return, incomplete return, or persistent baseline migration, and is this distinct from ordinary high affective variability?

### MDD
Does recurrence reflect increasing sensitivity/lower perturbation requirement, incomplete recovery, persistent baseline displacement, or multiple mechanisms?

### ADHD-I and ADHD-HI
Are observed fluctuations stable developmental traits, context-dependent state shifts, compensatory organizations, or impaired recovery after attentional/inhibitory challenge?

### Autism
Is atypical organization a stable developmental baseline, a different healthy-like basin, a context-sensitive architecture, or a pathological recovery deficit? Do not assume deviation equals deterioration.

### Parkinson's
How does progressive neurodegeneration alter recovery margin, compensatory baseline formation, and eventual failure of compensation?

### Addiction
Does repeated intoxication/withdrawal/cue exposure produce measurable incomplete return and progressively shifted reward/stress baselines consistent with allostatic models?

## 10. Relation to stability notation

### Lowercase \(\chi\)

May contribute a local recovery/damping coordinate only where licensed.

Questions:
- does \(\chi\) change during recovery?
- does post-perturbation \(\chi\) return to its prior normative distribution?
- does repeated residual \(\Delta\chi\) predict baseline migration?

### Capital \(\Chi\)

Captures modal/vector reorganization.

Questions:
- does recovery involve return of modal organization even when scalar measures normalize?
- can the same local \(\chi\) coexist with different recovery capacity?
- does repeated perturbation reorganize modal participation/coupling?

### \(\Chi_{\mathrm{arc}}\)

Candidate overall architecture only after sufficient system-level structure is qualified.

Questions:
- does the system return to the same architecture?
- does it form a new adaptive architecture?
- does a persistent maladaptive architecture become an alternative attractor?

## 11. Strong falsifiers

The baseline-migration hypothesis is weakened if:
- recovery metrics do not predict later baseline position;
- baseline shifts occur without preceding recovery impairment;
- apparent migration disappears after state/context adjustment;
- native measures fully explain migration and stability variables add nothing;
- within-person reliability is too poor to identify baseline changes;
- repeated perturbation exposure does not alter future recovery;
- disorder-associated states behave as static trait differences rather than transitions from prior baselines.

## 12. Literature anchors

- homeostatic plasticity stabilizes neural function around operating ranges and can adjust synaptic/intrinsic properties after perturbation;
- dynamical-systems psychiatry explicitly models health as a basin of attraction with finite resilience and disorders as possible alternative attractors;
- addiction allostasis predicts progressively shifted reward/stress operating points when counter-regulation repeatedly fails to return to the prior homeostatic range;
- recurrent depression literature includes kindling/sensitization hypotheses in which recurrent episodes may alter subsequent stress sensitivity;
- pain chronification literature supports active maladaptive plasticity and network reorganization rather than merely prolonged nociception.

These are neighboring native frameworks, not evidence that one universal NSD baseline-migration mechanism already exists.

## 13. Immediate experimental order

1. estimate healthy baseline drift and healthy recovery envelopes;
2. establish repeatability of recovery quantities;
3. test natural repeated perturbations in healthy/reference datasets;
4. determine whether incomplete healthy recovery predicts short-term baseline movement;
5. map the same quantities within each target disorder;
6. compare disorder trajectories to the normative recovery envelope;
7. test whether repeated recovery failure precedes persistent migration;
8. only then evaluate whether \(\chi\), \(\Chi\), or \(\Chi_{\mathrm{arc}}\) contributes information beyond native measures.

