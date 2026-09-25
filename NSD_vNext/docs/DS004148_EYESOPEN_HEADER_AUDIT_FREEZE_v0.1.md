# NSD ds004148 Eyes-Open Dataset-Wide Header Audit Freeze v0.1

Date: 25 September 2026
Status: FROZEN BEFORE DATASET-WIDE HEADER AUDIT
Maturity: D4 metadata/source root-cause audit; no signal-derived outcome
Program authority: SymC General Operations Manual v0.8.6

## Question

What channel-label topology is actually stable across all 60 ds004148 subjects and all three eyes-open sessions, and is the v0.1 MFR-14 `CPz` failure a local anomaly, a session3-specific pattern, or a broader dataset property?

## Frozen scope

- dataset: ds004148 v1.0.0;
- pinned source commit: `0c740d838a2c33feeec0b6e514aea323d0e65ca4`;
- subjects: sub-01 through sub-60;
- sessions: session1, session2, session3;
- task: eyesopen;
- records: 180 VHDR files;
- no EEG feature extraction.

For each VHDR:
1. resolve its git-annex key from the pinned source commit;
2. download the VHDR from the declared NEMAR mirror;
3. verify exact MD5 and byte size from the annex key;
4. parse channel count, channel labels, sampling interval/rate, binary format and orientation.

## Required outputs

Report:
- exact channel-label list for every subject/session;
- number of unique channel-set signatures;
- frequency of each signature;
- intersection across all 180 records;
- intersection within each session;
- channels whose presence/absence varies;
- per-session presence counts for every variable channel;
- subject/session matrix for `CPz`;
- exact intersection with the 59-label ds003775/sub-01 matched reference;
- whether a cohort-stable replication space exists without interpolation or renaming.

## Interpretation firewall

This audit contains no spectral, periodic, aperiodic, modal, chi, capital-Chi, clinical or recovery result.

A missing channel is a source/topology fact. It is not a neural absence phenotype.

No channel is silently synthesized, renamed, interpolated, or imputed.

## Checkpoint continuation

If a stable common label set exists, automatically freeze the next independent-subject replication on that set using subjects whose signal outcomes have not been inspected for the new version.

If no coherent common set exists, investigate a channel-set-aware spatial representation rather than forcing rectangular channel identity.
