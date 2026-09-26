# NSD ds004148 D4 pilot post-result audit v0.1

Date: 22 September 2026  
Status: COMPLETE D4 RAW-PAYLOAD RECONCILIATION FOR PINNED PILOT  
Program authority: SymC General Operations Manual v0.8.3  
Workflow: `NSD ds004148 D4 Pilot`  
Run: `35768880156`  
Artifact: `ds004148-d4-pilot-report-v0-1`  
Artifact ID: `10713187157`  
Artifact ZIP SHA-256: `481f4a6ea4072acbbb931f372eb7e0cca1271247eb873098a5fa5e7e8f2483dd`

## Question

Does the raw BrainVision payload resolve the source disagreement between:
- BIDS EEG JSON: 64 EEG channels;
- BIDS channels TSV: 61 EEG rows?

No EEG-derived scientific feature was opened.

## Pinned pilot

`sub-01 / ses-session1 / task-eyesclosed`

Exact source identities:
- EEG binary: 36,600,000 bytes, MD5 `0fceeb9eb4163b86b815061f8fff80d7`;
- VHDR: 1,122 bytes, MD5 `c5e313903936ef2fb9c1b3e0bfd61593`;
- VMRK: 5,960 bytes, MD5 `372402829a14249220eb8365f964d2de`.

All exact identities passed.

## Raw BrainVision result

The VHDR reports:
- `NumberOfChannels = 61`;
- exactly 61 channel definitions;
- sampling interval 2,000 microseconds;
- sampling rate 500 Hz;
- multiplexed data orientation.

The binary layout independently closes the count:

`61 channels x 500 samples/s x 300 s x 4 bytes/sample = 36,600,000 bytes`

which is exactly the observed EEG binary size.

Therefore:

`DS004148_RAW_PAYLOAD_CHANNEL_COUNT = 61`.

The BIDS `channels.tsv` agrees with the raw payload. The paired/source `*_eeg.json` declaration of `EEGChannelCount = 64` is a source-metadata inconsistency and must not be used to pad three synthetic channels.

## Claim ceiling

This earns only raw-payload identity and structural reconciliation.

It does **not** establish:
- artifact-free EEG;
- spectral reliability;
- modal adequacy;
- local chi;
- capital Chi;
- cognitive-state effects;
- questionnaire associations;
- clinical utility.

## Independence state

The dataset remains an independent, label-blind transfer candidate. No NSD signal-derived transfer result has yet been opened.

## Next mechanical gate

Before opening an independent transfer task, extend D4 across:
- all three sessions;
- at minimum both resting tasks (eyes-closed and eyes-open);
- exact raw BrainVision identities and structural semantics.

Only after that expansion should the project freeze a transfer question and then open signal-derived evidence.
