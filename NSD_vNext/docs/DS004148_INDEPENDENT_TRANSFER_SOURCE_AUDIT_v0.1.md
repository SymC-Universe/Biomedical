# NSD ds004148 independent-transfer source audit v0.1

Date: 22 September 2026  
Status: D0-D3 CLOSED FOR TRANSFER PREPARATION; D4 PILOT RESOLVES RAW PAYLOAD TO 61 CHANNELS  
Program authority: SymC General Operations Manual v0.8.3

## Why ds004148 is being prepared

The current NSD modal/structural work needs an independent healthy transfer source that is not the ds003775 development/repeat-population dataset and does not use clinical labels.

OpenNeuro ds004148 is well suited for that role because it contains repeated EEG across multiple ordinary brain states. It is being prepared only as a label-blind independent-transfer/Function-Limit source. No EEG-derived NSD result has been opened here.

## Frozen public source

- OpenNeuro accession: `ds004148`
- DOI: `10.18112/openneuro.ds004148.v1.0.0`
- license: CC0
- public repository: `OpenNeuroDatasets/ds004148`
- pinned repository commit: `0c740d838a2c33feeec0b6e514aea323d0e65ca4`
- source BIDS version: 1.2

## Hierarchy recovered from the pinned tree

The pinned repository contains:

- **60 subjects**
- **180 subject-session directories**
- **3 sessions per subject**
- **900 raw BrainVision EEG payload triplets**
- **5 tasks per session**
- exactly **180 recordings for each task**:
  - eyesclosed
  - eyesopen
  - mathematic
  - memory
  - music

This is a complete 60 x 3 x 5 structural design in the pinned repository tree.

## Acquisition contract from source metadata

The public README/source sidecars describe:
- Brain Products acquisition;
- nominal 64-electrode system;
- 500 Hz sampling;
- five-minute recordings;
- impedance below 5 kOhm.

Example source `*_eeg.json` declares:
- `EEGChannelCount = 64`;
- reference FCz;
- 500 Hz;
- 300 s recording duration;
- 50 Hz line frequency.

## Important channel-count discrepancy

The source BIDS channel tables do **not** currently agree with the sidecar's declared EEG channel count.

Five prospectively inspected channel-table examples spanning:
- early and late subjects;
- session 1, 2 and 3;
- multiple tasks

each contained exactly **61 EEG rows**, from Fp1 through O2, while the paired/source EEG JSON declares **64 EEG channels**.

This matches the independent public metadata summaries that describe the machine-readable recordings as 61-channel data, despite the source README/sidecar language describing a 64-electrode acquisition system.

Current disposition:

`DS004148_CHANNEL_COUNT = SOURCE_METADATA_DISCREPANCY_61_TABLE_ROWS_VS_64_JSON_DECLARATION`.

This discrepancy is not normalized away.

## Metadata-role firewall

The participant table contains age, sex, anthropometrics, symptom/questionnaire scales, sleepiness, affect, mind-wandering and task-response measures.

For independent Structural Engine transfer:

### Engine-visible
- participant ID as identity only;
- session ID;
- task/recording state;
- source acquisition metadata needed for decoding and provenance.

### Downstream only
- age;
- sex;
- height/weight;
- SAS/SDS/ESS;
- ARSQ dimensions;
- KSS;
- PANAS;
- mini-NYC-Q items;
- task correctness/behavioral response summaries;
- any other questionnaire/behavioral field.

No downstream field may tune:
- signal preprocessing;
- modal model order;
- stationarity/refusal thresholds;
- local chi admission;
- broader Chi representation.

## Independence role

For the current lineage, ds004148 is:

`INDEPENDENT_LABEL_BLIND_TRANSFER_CANDIDATE`

provided its signal payload and channel semantics pass D4 before any structural outcome is opened.

It is not P1 clinical evidence and carries no disorder label role.

## D4 requirement

Before any real signal-derived transfer result:

1. pin one raw BrainVision recording by exact annex hash/size;
2. download the `.vhdr`, `.vmrk`, and `.eeg` payloads;
3. verify actual channel count and labels from the BrainVision header against the 61-row channel table and 64-channel JSON claim;
4. verify 500 Hz and 300 s where source-declared;
5. verify scale/unit decoding;
6. preserve any mismatch as a source anomaly rather than silently padding or dropping channels.

No real-EEG modal damping or local chi may be computed at D4.

## Current gate

D0 source identity: **PASS**  
D1 version/provenance: **PASS for pinned public commit**  
D2 hierarchy: **PASS**  
D3 metadata-role firewall: **PASS WITH SOURCE CHANNEL-COUNT DISCREPANCY**  
D4 payload/channel reconciliation: **NEXT**

The dataset should remain untouched for independent transfer until D4 is closed.


## D4 pilot resolution

Workflow run `35768880156` closed the first raw-payload reconciliation.

The pinned BrainVision VHDR contains `NumberOfChannels=61`, exactly 61 channel definitions, and 500 Hz sampling. The 32-bit binary layout predicts exactly 36,600,000 bytes for a 300 s recording, matching the downloaded EEG payload byte-for-byte.

Thus the raw payload and `channels.tsv` agree on 61 channels. The source `*_eeg.json` value of 64 is retained as a metadata inconsistency and must not be used to synthesize or pad channels.

Canonical audit:
`DS004148_D4_PILOT_POSTRESULT_v0.1.md`.

The next D4 action is a cross-session resting-state expansion before any independent signal-derived transfer outcome is opened.


## Cross-session D4 closure

Run `35769238959` verified six prospectively pinned resting recordings for `sub-01` across all three sessions and both eyes-closed/eyes-open states.

All 6/6 passed exact source identity, 61-channel VHDR definition, 500-Hz sampling, 32-bit-float binary layout, 300-s duration and exact expected byte count.

This makes the source mechanically ready for a prospectively frozen independent label-blind transfer task.

Canonical audit:
`DS004148_D4_RESTING_CROSSSESSION_POSTRESULT_v0.1.md`.

No signal-derived transfer result has been opened.
