# NSD T0 Engine Qualification Execution Ledger v0.1

Date opened: 14 September 2026
Status: ACTIVE
Target: T0 exit for the Neurophysiology Decision-Support Tool program

## 1. T0 exit definition

T0 exists to prove that the label-blind representation layer can recover known structure, refuse invalid reductions, preserve provenance, and operate on traceable real neurophysiology before any clinical model is allowed to matter.

T0 does **not** claim diagnosis, prognosis, a healthy chi range, or a universal neural stability scalar.

Provisional exit requirements:

1. deterministic provenance/hierarchy contracts;
2. metadata-role firewall;
3. signal-payload identity/readability gate;
4. generic label-blind signal QC;
5. descriptive spectral layer qualified on fixtures and real healthy data;
6. known-truth modal recovery for at least one native dynamical route;
7. scalar admission/refusal only after modal qualification;
8. local-versus-embedded stability known-truth tests;
9. nuisance/adversarial Limit Map;
10. repeat-session healthy qualification;
11. CI regression coverage;
12. versioned Engine outputs ready for Atlas serialization.

## 2. Mechanical verification

Latest confirmed full Engine contract suite before this ledger entry:

- GitHub Actions workflow: `NSD Engine Contracts`
- run: `34924760191`
- result: SUCCESS
- tests: **62 passed**
- runtime: 0.21 s

The suite includes provenance, hierarchy, metadata firewall, spectral/modal contracts, exact second-order fixtures, scalar admission/refusal, serialization, generic signal QC, local-versus-embedded 2x2 stability fixtures, and EDF-header tests.

Current branch CI continues to run after every relevant PR update; a green historical run is not substituted for the current head.

## 3. Local-versus-embedded stability program

Executable native-system fixtures now cover:

- same isolated local rates and same eigenspectrum with different coupling/non-normality and different reactivity;
- locally stable isolated components whose coupled system is globally unstable;
- an isolated unstable component whose coupled system is asymptotically stabilized;
- distinction between spectral abscissa and numerical-abscissa/reactivity behavior.

Implemented in:

`engine/nsd_engine/system_stability.py`

These fixtures operationalize the GOM rule:

`LOCAL DYNAMICAL IDENTITY != EMBEDDED REALIZED BEHAVIOR`

without introducing a project-branded whole-system parameter.

## 4. Generic signal QC

Implemented in:

`engine/nsd_engine/qc.py`

Current capabilities:

- per-channel finite/missing fraction;
- amplitude range;
- flat-channel detection;
- repeated numerical-extreme occupancy as a clipping/saturation indicator;
- channel-count accounting;
- conservative usable-duration bookkeeping;
- explicit caller-supplied thresholds;
- no hidden universal EEG-quality cutoffs.

The scientific rule is measurement first, task-specific admission threshold second.

## 5. First healthy real-data source: ds003775

Dataset identity:

- OpenNeuro `ds003775`;
- DOI `10.18112/openneuro.ds003775.v1.2.1`;
- NEMAR mirror `on003775/v1.0.0`;
- 111 subjects;
- 153 sessions;
- 42 repeat-session subjects;
- 64-channel BioSemi EEG;
- four-minute eyes-closed rest;
- 1024 Hz;
- average reference in the pinned raw release metadata.

### Gate state

- D0 discovery: CLOSED
- D1 provenance for pinned release: CLOSED FOR CURRENT SCOPE
- D2 hierarchy: VERIFIED
- D3 metadata/join: **VERIFIED FOR T0 HEALTHY QUALIFICATION**
- D4 signal input: **PILOT VERIFIED; DATASET-WIDE/REPEAT EXPANSION ACTIVE**
- D5 analysis ready: OPEN

### D3 artifact

`atlas/manifests/ds003775_metadata_role_manifest_v0.1.json`

Canonical manifest-body SHA-256:

`28d71314e720eb4be799525c27c89f1f5a6090f2464e8d82e0c071effe1afe1d`

Only identity/acquisition/recording-state metadata may enter structural feature construction. Age, sex, and all participant cognitive scores are downstream.

## 6. D4 payload verification already closed for one exact real recording

Pilot:

`sub-001 / ses-t1 / task-resteyesc`

Verified by GitHub Actions against the public NEMAR payload:

- exact annex MD5: PASS;
- exact expected byte count: PASS;
- EDF internal byte-count consistency: PASS;
- 64 channels: PASS;
- exact channel-label sequence: PASS;
- 1024 Hz on all channels: PASS;
- 240 s duration: PASS.

Workflow:

`NSD ds003775 D4 Pilot`

Successful run:

`34924760163`

Artifact:

`ds003775-d4-pilot-report`

This is D4 evidence for the named payload only. It does not promote the complete dataset.

## 7. Repeat-session D4 expansion now active

Frozen repeat subject:

`sub-069`

Public hierarchy exposes both:

- `ses-t1`, acquisition `2017-10-17T10:33:20`;
- `ses-t2`, acquisition `2018-10-16T11:12:04`.

Pinned annex identities:

- t1: 31,473,920 bytes; MD5 `656b7184b5ed01e36601b79a3bf38c52`;
- t2: 31,473,920 bytes; MD5 `0ecea6e69394a865f2fca83086f1b947`.

Expectation manifest:

`atlas/manifests/ds003775_sub069_repeat_d4_manifest_v0.1.json`

Generic verifier:

`engine/tools/d4_verify_edf_manifest.py`

CI workflow:

`NSD ds003775 D4 Repeat Pair`

Current purpose:

- confirm both longitudinal payload identities;
- verify both EDF headers against the same acquisition contract;
- establish a real two-session payload pair suitable for the first signal-level repeatability pilot.

No reliability result is claimed merely because both files pass D4.

## 8. Immediate execution order from here

1. close repeat-pair D4 CI;
2. implement sample-level EDF access with unit/scaling verification;
3. run generic label-blind QC on a frozen subset without tuning thresholds to clinical or outcome variables;
4. verify sample reader against known digital-to-physical conversion fixtures;
5. implement the first accepted descriptive PSD route;
6. run PSD/periodic-aperiodic qualification on known truth and the healthy pilot;
7. compare t1/t2 descriptive outputs for the repeat subject;
8. expand to the full repeat subset only after pilot behavior is mechanically and scientifically sane;
9. begin the first empirical Function/Limit Map;
10. then qualify state-space/modal estimators independently before local damping-ratio admission.

## 9. Stop lines

Still prohibited at T0:

- clinical classification;
- ASD feature selection;
- diagnosis-informed region selection;
- prognosis;
- treatment guidance;
- universal healthy stability boundaries;
- direct bandwidth-to-damping conversion;
- whole-brain chi;
- any claim that repeated-session similarity alone proves trait biology.

The intended T0 outcome is a trustworthy measurement and representation engine. Clinical usefulness is tested downstream rather than assumed upstream.
