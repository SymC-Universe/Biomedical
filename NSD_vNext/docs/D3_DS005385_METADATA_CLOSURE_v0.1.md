# NSD ds005385 D3 metadata-role closure v0.1

Date: 22 September 2026  
Status: D3 METADATA ROLE/JOIN CONTRACT CLOSED; D4 PENDING  
Program authority: SymC General Operations Manual v0.8.3

## Source pinned

Dataset:
- OpenNeuro `ds005385`;
- DOI `10.18112/openneuro.ds005385.v1.0.3`;
- public source repository `OpenNeuroDatasets/ds005385`;
- pinned repository commit `6a558cd5852503e66df9ac7fdac2f3a7f4ed5f12`.

The already-audited D2 hierarchy remains:
- 608 subjects;
- 816 sessions;
- 208 repeat subjects;
- no participant/tree mismatch.

## Metadata dictionary issue resolved

The previously unresolved meanings of `late_ses1` and `late_ses2` are now explicit in the source `participants.json`.

They are counts of late triggers, with the source warning that affected datasets are probably not continuous.

Therefore these fields are **not** demographic variables, session identifiers, neural features, or modal-quality scores.

They are frozen as `OTHER` source quality/provenance bookkeeping and:
- do not enter Structural Engine feature construction;
- do not tune modal admission/refusal thresholds;
- may be used later only under a prespecified signal-QC sensitivity/exclusion rule.

The source also explicitly warns that EDF physical min/max header specifications may contain invalid values and should be ignored. That becomes a D4 decoding constraint.

## Role map

Participant table:
- `participant_id`: IDENTITY, Engine-visible only as a key;
- `age`, `sex`, `handedness`: DEMOGRAPHIC_COVARIATE, downstream only;
- `session1`, `session2`: OTHER availability/bookkeeping;
- `late_ses1`, `late_ses2`: OTHER source-quality bookkeeping.

Recording state comes from BIDS structure:
- session identity from `ses-1` / `ses-2`;
- recording year from each `*_sessions.tsv`;
- eyes-open/eyes-closed from task;
- before/after cognitive battery from acquisition `pre` / `post`.

The four within-session recording conditions remain separate:
- pre EyesClosed;
- pre EyesOpen;
- post EyesClosed;
- post EyesOpen.

## D3 disposition

`D3_METADATA_JOIN_VERIFIED_FOR_LABEL_BLIND_ENGINE_AND_ATLAS_PREPARATION`.

This earns metadata-role closure. It does not make the dataset D5 analysis-ready.

## Next gate

D4 must verify representative real payloads against the source acquisition contract before broad signal processing:
- EDF/readability and byte identity where obtainable;
- 64 channels;
- 1000 Hz source sampling;
- recording duration/condition;
- channel order/sidecars;
- safe digital-to-physical decoding that does not trust the source-warned invalid physical min/max header values.

Only after D4 may a ds005385 P0-Q Function/Limit task be frozen.
