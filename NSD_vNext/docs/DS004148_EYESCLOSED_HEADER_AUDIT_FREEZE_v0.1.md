# NSD ds004148 Eyes-Closed Dataset-Wide Header Audit Freeze v0.1

Date: 25 September 2026
Status: FROZEN BEFORE DATASET-WIDE HEADER AUDIT
Maturity: D4 metadata/source gate; no signal-derived outcome
Program authority: SymC General Operations Manual v0.8.6

## Question

What exact channel-label topology is stable across all 60 ds004148 subjects and all three eyes-closed sessions, and does an exact cross-dataset coordinate space exist without renaming, interpolation, imputation, or case normalization?

This source-only gate is required before the prospectively authorized eyes-closed state-specificity test.

## Frozen scope

- dataset: ds004148 v1.0.0;
- pinned source commit: `0c740d838a2c33feeec0b6e514aea323d0e65ca4`;
- subjects: sub-01 through sub-60;
- sessions: session1, session2, session3;
- task: eyesclosed;
- records: 180 VHDR files;
- matched parent coordinate source: existing ds003775 matched descriptive reference;
- no EEG sample payload or signal feature is opened.

For each VHDR:
1. resolve its git-annex identity from the pinned source commit;
2. download the exact header from the declared NEMAR mirror;
3. verify byte size and MD5 against the annex key;
4. parse channel count, labels, sampling rate, binary format, and orientation.

## Required outputs

Report:
- all exact channel signatures;
- intersection and union across 180 records;
- session-specific intersections;
- variable channel labels and their source frequency;
- exact intersection with the existing ds003775 matched parent coordinate set;
- acquisition anomalies;
- whether a stable exact-label eyes-closed coordinate space exists.

## Interpretation firewall

This gate contains no spectral, periodic, aperiodic, modal, damping, local-chi, modal/vector-Chi, system/Bio-Chi, recovery, diagnosis, or population result.

A missing or variant label is a source-topology fact, not a neural phenotype.

## Continuation rule

If a stable exact-label common space exists, freeze the eyes-closed state-specificity signal test on that coordinate space before opening its signal outcomes.

If no coherent common space exists, preserve the failure and investigate a channel-set-aware representation rather than forcing rectangular identity.
