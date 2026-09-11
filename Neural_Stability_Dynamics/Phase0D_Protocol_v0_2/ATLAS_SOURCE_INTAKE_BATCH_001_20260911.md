# Neurostability Atlas Source Intake Batch 001

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **SOURCE ELIGIBILITY / INTAKE ONLY. NO ATLAS REFERENCE RANGE, ZONE, OR CLINICAL CLAIM FROZEN.**

## Intake purpose

Begin Atlas coordinate population from datasets that support native multichannel EEG structure while deliberately balancing nominal function, controlled perturbation/state change, and natural-limit behavior.

Source eligibility is assessed before coordinate extraction. Inclusion here does not imply that every source will contribute to every Atlas coordinate family.

## Candidate A001 - PhysioNet EEG Motor Movement/Imagery Dataset

Source identity: EEG Motor Movement/Imagery Dataset v1.0.0, PhysioNet, DOI `10.13026/C28G6P`.

Source-native facts relevant to Atlas intake:

- 64-channel scalp EEG;
- open-access files under the listed PhysioNet license;
- each subject completed 14 runs;
- runs 1-2 are one-minute eyes-open and eyes-closed baselines;
- remaining runs contain repeated motor execution / motor imagery task conditions;
- subject folders and EDF files are directly downloadable.

Primary Atlas roles:

- `NOMINAL_FUNCTION`: eyes-open / eyes-closed baseline;
- `PERTURBED_FUNCTION`: motor execution and motor imagery relative to baseline.

Coordinate potential:

- spectral/pole coordinates;
- observable order/rank;
- carrier/subspace structure;
- participation distribution;
- rest-to-task added/lost/shared structure;
- Function Map trajectories across baseline/task conditions;
- model-adequacy/open-channel descriptors.

Initial independence value:

High for a first-wave method/Atlas source because task labels define experimental condition but need not enter structural estimation. The dataset is external to NSD Engine development records.

Disposition: **PRIORITY_1_FIRST_WAVE_CANDIDATE**.

## Candidate A002 - Sleep-EDF Database Expanded

Source identity: Sleep-EDF Database Expanded v1.0.0, PhysioNet.

Source-native facts relevant to Atlas intake:

- 197 whole-night polysomnographic recordings;
- EEG includes Fpz-Cz and Pz-Oz derivations;
- accompanying EOG/chin EMG and event markers are available;
- hypnograms provide expert-scored sleep stages;
- database includes healthy subjects and subjects with mild difficulty falling asleep.

Primary Atlas roles:

- `NOMINAL_FUNCTION`: stable segments within ordinary sleep/wake states where model adequacy supports analysis;
- `PERTURBED_FUNCTION` / `BOUNDARY_OR_TRANSITION`: sleep-stage transitions.

Coordinate potential:

- frequency/pole/decay coordinates across sleep state;
- observable-order changes;
- state-transition Function/Limit trajectories;
- mode/subspace persistence or reorganization;
- model-adequacy sensitivity around transitions.

Important limitation:

Only two primary EEG derivations are available in the standard PSG files, so high-dimensional carrier/participation claims are more limited than in 64-channel datasets. The stage labels are downstream context and must not be used to force structural Engine outputs.

Disposition: **PRIORITY_1_STATE_TRANSITION_CANDIDATE**.

## Candidate A003 - CHB-MIT Scalp EEG Database

Source identity: CHB-MIT Scalp EEG Database v1.0.0, PhysioNet, DOI `10.13026/C2K01R`.

Source-native facts relevant to Atlas intake:

- scalp EEG from 22 pediatric subjects with intractable seizures;
- 23 cases;
- subjects were monitored for up to several days;
- 182 seizure onsets/ends are annotated;
- recordings were collected after withdrawal of anti-seizure medication as part of clinical evaluation;
- open files include long interictal records and seizure annotations.

Potential Atlas role:

- candidate `RARE_NATURAL_LIMIT` and `BOUNDARY_OR_TRANSITION` source for seizure transitions;
- interictal periods may provide within-system comparison context but are not a healthy normative baseline.

Coordinate potential:

- transition trajectories in spectral/pole structure;
- observable-order/reorganization changes;
- carrier/subspace change;
- model-adequacy breakdown/recovery;
- rare-limit Function/Limit behavior.

Critical confounds / admission conditions:

- medication withdrawal is a material context variable;
- pediatric intractable-epilepsy population is not representative of general neural dynamics;
- seizure cases must not be selected because NSD already produces an extreme coordinate;
- rare-limit eligibility must be established from source-native seizure annotation/context independently of Engine output;
- no seizure-derived value may define a nominal Atlas zone.

Disposition: **PRIORITY_1_RARE_NATURAL_LIMIT_CANDIDATE_WITH_STRICT_CONFOUND_FIREWALL**.

## Candidate A004 - TDBRAIN

Source identity: van Dijk et al., *Scientific Data* 9, 333 (2022), DOI `10.1038/s41597-022-01409-z`; TDBRAIN data repository DOI `10.70303/syn25671079` as reported by the data descriptor.

Source-native facts relevant to Atlas intake:

- large lifespan raw EEG archive collected over approximately two decades;
- original descriptor reports 1274 participants and 1346 EEG sessions;
- heterogeneous psychiatric/clinical population with demographic and clinical metadata;
- standardized two-minute eyes-open and two-minute eyes-closed resting recordings;
- additional auditory oddball and visual 1-back task information/data availability is described;
- raw full time-series EEG and complementary preprocessing code are available under repository access/data-use conditions.

Coordinate potential:

- large-scale resting-state spectral/pole distributions;
- eyes-open / eyes-closed perturbation trajectories;
- lifespan dependence;
- carrier/subspace and participation distributions;
- method robustness across a large heterogeneous archive.

Why it is not the first calibration anchor:

TDBRAIN's size and metadata make it extremely valuable, but the archive is strongly entangled with psychiatric indications, diagnosis, treatment and outcome metadata. Using it as the first Atlas coordinate anchor would create unnecessary risk that phenotype structure silently defines what 'normal' or 'stable' is before the coordinate rules are independently established.

Initial use should therefore be restricted to:

- source/method feasibility;
- explicitly selected condition-independent or label-blind coordinate mapping;
- later lifespan/cross-system coverage after the first-wave coordinate extraction rules are stable;
- never phenotype-driven Engine tuning.

Disposition: **HIGH_VALUE_DEFERRED_CALIBRATION_SOURCE / LATER_CROSS_SYSTEM_COVERAGE**.

## Batch-001 balance

| Source | Primary role | First-wave status |
|---|---|---|
| EEG Motor Movement/Imagery | nominal + controlled task perturbation | PRIORITY 1 |
| Sleep-EDF Expanded | functional state + transition | PRIORITY 1 |
| CHB-MIT | boundary / rare natural limit | PRIORITY 1 with confound firewall |
| TDBRAIN | large heterogeneous cross-system/lifespan source | deferred as calibration anchor |

This deliberately avoids building the initial Atlas solely from disease cohorts or solely from resting healthy data.

## First extraction order

1. Start with EEG Motor Movement/Imagery because the same subjects provide eyes-open, eyes-closed and controlled task conditions with 64 channels, giving a compact first test of spectral + modal + conglomerate coordinate extraction without requiring clinical labels.
2. Add Sleep-EDF to test whether coordinate definitions remain meaningful when channel dimensionality is low and state transitions are externally annotated.
3. Add CHB-MIT only under the rare-natural-limit firewall and keep seizure eligibility independent of NSD outputs.
4. Bring TDBRAIN in after extraction/version rules are stable enough that its phenotype metadata cannot back-drive coordinate definitions.

## Coordinate freeze firewall

Batch 001 does not authorize:

- healthy reference intervals;
- disease reference intervals;
- diagnostic thresholds;
- universal frequency/decay/rank zones;
- chi coordinates;
- a claim that seizure/sleep/task transitions share one universal mechanism;
- a claim that any one dataset is representative of human neural dynamics.

The next step is to create source-specific extraction manifests for A001-A003 and populate native spectral/context coordinates before any derived Atlas zone is considered.
