# Healthy Perturbation and Recovery Dataset Triage v0.1

**Date:** 2026-10-01  
**Status:** DATASET DISCOVERY / NOT YET A RECOVERY BASELINE  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Independence rule:** native external neuroscience only; no NSD metric is used for selection or thresholding.

## Purpose

Identify healthy-human datasets capable of distinguishing direct return, incomplete return, overshoot, transient return followed by rebound, oscillatory recrossing, and durable post-perturbation shift.

A pre/post pair alone can establish displacement but usually cannot distinguish the full trajectory taxonomy. Priority therefore goes to datasets with repeated or continuous post-perturbation observations.

## Priority A: paired associative stimulation EEG

Dataset/data descriptor:
- Shikauchi & Kitajo, CBS Data Sharing Platform, DOI 10.60178/cbs.20240220-001;
- open data descriptor: “Electroencephalographic responses before, during, and after upper limb paired associative stimulation”;
- raw EEG/EOG/EMG from nine participants;
- preprocessed EEG from seven participants with adequate quality;
- sequential pre-PAS, during-PAS, and post-PAS measurements;
- two distinct timing intervals provide a built-in manipulation of plasticity response.

Why it matters:
- directly contains before/during/after perturbation structure;
- can test whether post-stimulation neural features return, overshoot, rebound, or remain displaced;
- repeated stimulation permits cumulative-response questions.

Limit:
- small N;
- should be a trajectory/mechanism benchmark, not a population normative sample.

## Priority B: real-time brain-state-dependent TMS

Dataset:
- OpenNeuro ds005779 / NEMAR on005779;
- 19 healthy participants;
- EEG plus multiple training/testing TMS conditions and resting data;
- high/low/random brain-state-triggered stimulation conditions.

Why it matters:
- perturbation magnitude is not the only variable; pre-perturbation brain state is explicitly relevant;
- useful for testing state-conditioned response and whether similar TMS input produces different trajectories from different starting states.

Limit:
- large dataset and complex event structure;
- not automatically a recovery dataset until post-event observation windows are qualified.

## Priority C: single-pulse open-loop TMS-EEG

Dataset:
- OpenNeuro ds002094 / NEMAR on002094;
- resting and TMS-EEG tasks.

Why it matters:
- clean perturbational-response benchmark;
- can establish immediate evoked displacement and return timescales at native EEG level.

Limit:
- single-pulse response may characterize local/short-horizon recovery rather than baseline migration.

## Priority D: multi-dose tES with concurrent EEG/behavior

Dataset:
- OpenNeuro ds003670 / NEMAR on003670;
- 19 participants, 62 sessions;
- nine HD-tES conditions over three cortical targets and three waveforms;
- >783 stimulation trials;
- EEG, ECG, EOG, continuous vigilance/behavior.

Why it matters:
- repeated-dose perturbation structure;
- permits within-person dose/state/history effects;
- behavioral covariates can help distinguish adaptive from functionally adverse shifts.

Limit:
- concurrent stimulation artifacts and session structure require native source-specific preprocessing.

## Priority E: test-retest TMS-EEG

Dataset:
- Zenodo record 10004794;
- 24 healthy participants;
- three identical TMS-EEG sessions one week apart;
- three cortical targets;
- active and optimized-sham conditions.

Why it matters:
- gives a healthy repeatability distribution for perturbational responses;
- critical for deciding whether an apparent response change exceeds ordinary TMS-EEG variability.

## Recovery-dataset admission criteria

Before a dataset is used to define a healthy recovery envelope it must support:
1. a pre-perturbation baseline;
2. known perturbation timing;
3. enough post-perturbation sampling to distinguish at least one trajectory class beyond simple displacement;
4. within-person identity;
5. source-specific artifact handling;
6. perturbation dose/intensity metadata;
7. state/context metadata where available;
8. a native response representation with acceptable repeatability;
9. no threshold selected from disorder data.

## Planned order

1. finish static/state healthy baseline reproduction with Dortmund and HarMN;
2. use test-retest TMS-EEG to quantify perturbational-response measurement noise;
3. use PAS-EEG as the first explicit before/during/after trajectory benchmark;
4. test brain-state conditioning with ds005779;
5. use multi-dose tES for repeated-perturbation/history effects;
6. only then define prospective healthy capture/overshoot/rebound envelopes.

