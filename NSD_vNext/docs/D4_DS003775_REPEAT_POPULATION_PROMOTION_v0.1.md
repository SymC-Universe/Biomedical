# ds003775 D4 Repeat-Population Promotion v0.1

Date: 18 September 2026  
Status: VERIFIED FOR FROZEN 42-SUBJECT REPEAT SUBSET  
Dataset: OpenNeuro `ds003775`  
Pinned mirror/release: NEMAR `on003775/v1.0.0`  
Workflow: `NSD ds003775 42-Subject Repeat Population`  
Run: `35304835270`  
Result: SUCCESS

## 1. Promotion decision

The exact 42-subject repeat-session subset used for T0 healthy qualification is promoted to:

`D4_SIGNAL_INPUT_VERIFIED_FOR_FROZEN_REPEAT_SUBSET`

Scope:

- 42 unique subjects;
- two repeat sessions per subject;
- 84 total EEG payloads;
- exact release-manifest scope frozen before subject jobs;
- each payload downloaded from the pinned release;
- each payload re-verified against its exact manifest identity before numerical analysis;
- all 42 subject jobs completed successfully.

This promotion is deliberately narrower than a dataset-wide D4 promotion.

It does **not** assert that every non-repeat recording among the 111 subjects has independently passed D4.

## 2. Evidence chain

The population workflow performed, in order:

1. load the committed 42-subject repeat index;
2. build the exact pinned-release manifest;
3. require 42 subjects and 84 recordings;
4. extract each subject's two-session manifest;
5. download the exact pinned pair;
6. run the D4 EDF/payload verifier;
7. only after D4 success, run Welch and descriptive periodic/aperiodic analysis;
8. aggregate only after every subject job succeeded.

The resulting population summary was generated only because the full matrix completed successfully.

## 3. Why this gate matters

The future decision-support system needs a traceable statement stronger than “the file opened.”

For this frozen subset, the analysis chain now records that the numerical features came from the exact intended public payloads under the expected hierarchy, not from inferred filenames, substituted files, or silently mismatched sessions.

This is part of R3 provenance reconstruction as well as T0 measurement qualification.

## 4. What D4 does not establish

D4 verification does not establish:

- artifact-free EEG;
- scientific preprocessing adequacy;
- feature reliability;
- modal identifiability;
- a healthy reference range;
- diagnosis;
- prognosis;
- clinical utility.

Those are separate downstream gates.

## 5. Downstream state

For this repeat subset:

`D0 -> CLOSED`  
`D1 -> CLOSED FOR PINNED SCOPE`  
`D2 -> VERIFIED`  
`D3 -> VERIFIED FOR T0 SCOPE`  
`D4 -> VERIFIED FOR FROZEN 42-SUBJECT REPEAT SUBSET`  
`D5 -> OPEN`

D5 remains open because analysis-readiness requires the qualified measurement layers, repeatability/Limit Map interpretation, and versioned output contract to close, not merely readable payloads.
