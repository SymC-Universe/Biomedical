# NSD ds004148 D4 resting cross-session post-result audit v0.1

Date: 22 September 2026  
Status: COMPLETE D4 RAW-PAYLOAD EXPANSION / INDEPENDENT TRANSFER SOURCE PREPARED  
Program authority: SymC General Operations Manual v0.8.3  
Workflow: `NSD ds004148 D4 Resting Cross-Session Expansion`  
Run: `35769238959`  
Artifact: `ds004148-d4-resting-crosssession-v0-1`  
Artifact ID: `10713656180`  
Artifact ZIP SHA-256: `1823292c09c90e5c0614b631230b9e0bba052bf858d8ef6a58b6257e41bc8e27`

## Frozen scope

One prospectively selected subject, `sub-01`, was expanded across:
- session 1, 2 and 3;
- eyes-closed and eyes-open resting recordings.

Six raw BrainVision recording triplets were pinned before execution.

No NSD signal-derived feature or downstream participant variable was opened.

## Result

**6/6 recordings passed every frozen D4 check.**

Across all six recordings:
- exact annex MD5 and byte size passed for EEG, VHDR and VMRK;
- raw VHDR reported 61 channels;
- exactly 61 channel definitions were present;
- sampling was 500 Hz;
- binary format was 32-bit float;
- 61 x 500 x 300 x 4 predicted exactly 36,600,000 EEG bytes;
- each observed EEG payload was exactly 36,600,000 bytes;
- VHDR data/marker filenames matched the source triplet.

## Source discrepancy disposition

The source BIDS EEG JSON says 64 EEG channels, but:
- raw VHDR says 61;
- VHDR contains 61 channel definitions;
- BIDS channel tables contain 61 rows;
- binary layout is exactly consistent with 61 channels.

Therefore the operational source contract for the raw payload is:

`DS004148_RAW_CHANNELS = 61`.

The 64-channel JSON value remains a source metadata error/provenance anomaly. It is not corrected by padding, interpolation or synthetic channels.

## Independence firewall

No EEG-derived result was inspected while choosing:
- the subject;
- sessions;
- resting states;
- payload checks.

No participant questionnaire, symptom, behavior, sex or age field entered the Structural Engine preparation.

Therefore ds004148 remains available as an:

`INDEPENDENT_LABEL_BLIND_TRANSFER_CANDIDATE`.

This does not by itself make a future result P1. The exact future claim and MFR-14 status must be frozen separately.

## What is now mechanically ready

A future transfer task may use the raw 61-channel, 500-Hz, five-minute resting recordings under the exact pinned source lineage.

The transfer task still must freeze:
- preprocessing/standardization;
- representation;
- channel/spatial handling;
- subject/session hierarchy;
- comparator;
- uncertainty and effect-size rule;
- admission/refusal semantics;
- whether the test is P0-Q transfer qualification or a later MFR-14/P1 claim.

## Stop line

No signal-derived ds004148 result should be opened until that transfer design is frozen.

In particular this D4 result does not license:
- modal damping;
- local chi;
- whole-system chi;
- broader Chi claims on real EEG;
- questionnaire or clinical interpretation.
