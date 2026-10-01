# Dortmund Full Healthy Native Reproduction Freeze v0.1

**Date:** 2026-10-01  
**Status:** FROZEN EXTERNAL-BASELINE REPRODUCTION DESIGN  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Source:** Park et al., Frontiers in Aging Neuroscience (2026), DOI 10.3389/fnagi.2026.1869339  
**Dataset:** OpenNeuro `ds005385`, snapshot `1.0.3`  
**Scientific ceiling:** reproduce independent native healthy EEG reference structure only; no NSD (chi), (Chi), or (Chi_{\mathrm{arc}}).

## Frozen cohort

Use all 608 participants in the pinned `participants.tsv`.

Use every available resting-state EDF in:
- session 1 / baseline;
- session 2 / follow-up where present;
- eyes closed and eyes open;
- pre-task and post-task.

No participant or recording is excluded by an NSD outcome. Recording exclusion occurs only under the source preprocessing/QC rule below.

## Frozen preprocessing

For each EDF independently:

1. load continuous EDF;
2. EEG channels only;
3. apply 50 Hz notch filter;
4. band-pass 1–45 Hz;
5. average reference;
6. segment into non-overlapping fixed 2-s epochs;
7. reject an epoch when EEG peak-to-peak amplitude exceeds 150 μV;
8. reject the recording if fewer than five clean epochs remain;
9. retain clean-epoch count as QC evidence;
10. no manual artifact rejection;
11. no ICA.

## Frozen conventional features

PSD:
- Welch on clean 2-s epochs;
- analysis range 1–30 Hz;
- target frequency resolution approximately 0.9766 Hz.

Bands:
- delta 1–4 Hz;
- theta 4–8 Hz;
- alpha 8–13 Hz;
- beta 13–30 Hz.

Primary:
- **occipital alpha relative power** from O1/Oz/O2: alpha power relative to total 1–30 Hz power;
- **global theta/alpha ratio**: global theta power divided by global alpha power.

Supplementary:
- **occipital alpha peak frequency**: maximum of mean O1/Oz/O2 PSD within 8–13 Hz, with no peak-presence exclusion.

No aperiodic decomposition is included in this reproduction because the source-complete normative paper explicitly did not separate periodic and aperiodic components. The separate state/longitudinal aperiodic paper remains a secondary baseline lane.

## Frozen statistical reproduction

Fit participant-random-intercept mixed models for the two primary outcomes.

Fixed effects:
- sex, male vs female reference female;
- eye state, EO vs EC reference EC;
- timepoint, pre vs post reference post;
- session, follow-up vs baseline reference baseline;
- standardized age;
- standardized-age squared;
- age × eye state;
- age × timepoint.

Primary source comparison targets:

Occipital alpha relative power:
- EO vs EC β = -0.2197;
- pre vs post β = -0.0256;
- follow-up vs baseline β = -0.0115;
- age z β = -0.0537;
- age × EO β = 0.0071;
- age × pre β = 0.0088;
- age² β = 0.0039.

Global theta/alpha ratio:
- EO vs EC β = 0.3218;
- pre vs post β = 0.0139;
- follow-up vs baseline β = -0.0158;
- age z β = 0.0457;
- age × EO β = -0.0270;
- age × pre β = -0.0080;
- age² β = -0.0141.

The reproduction reports coefficients, SEs, confidence intervals, retained recording count, QC losses, and deviations from source values. No post-result parameter changes are permitted to improve agreement.

## Neutral compute segmentation

The recording-level transform is independent and deterministic. To keep each Kaggle job below session/runtime limits, execution is partitioned by participant age group exactly as the paper reports:

- 20–29;
- 30–39;
- 40–49;
- 50–59;
- 60–70.

Each chunk uses identical code and outputs one row per recording plus source/QC identity. Chunks may execute separately because no model is fit inside a chunk.

Only after all chunks are merged is the frozen mixed model fit once to the full retained recording table.

Chunking does not create independent evidence.

## Stop/failure rules

Preserve:
- inaccessible/missing EDF;
- channel-set mismatch;
- filter/epoch failure;
- fewer than five clean epochs;
- numerical/model failure;
- source coefficient mismatch.

Do not change filters, thresholds, bands, channel cluster, feature definitions, or model terms after seeing reproduction results.

A material mismatch triggers source/implementation investigation before any healthy normative envelope is promoted.
