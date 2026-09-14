# NSD Forward Dataset Candidates v0.1

Date: 14 September 2026
Status: ACTIVE SOURCE-CANDIDATE AUDIT / NO DATASET YET PROMOTED TO D5
Purpose: identify public, traceable neurophysiology capable of replacing the weak provenance of the historical NSD figures rather than attempting to rescue untraceable coordinates.

## 1. Selection rules

A useful forward dataset should maximize:
- raw or minimally processed neurophysiology;
- stable public accession/version;
- explicit license;
- subject/session/run hierarchy;
- enough channels to preserve spatial organization;
- repeated conditions or sessions where possible;
- native clinical/behavioral metadata where appropriate;
- compatibility with strong native comparators;
- sufficient sample size for subject-level inference;
- no need to infer diagnosis from filenames or hand-built labels.

A dataset name such as “healthy” or “autism” is not itself an admission criterion. The actual cohort metadata must be audited.

## 2. Highest-priority clinical candidate — SFARI_EEG / OpenNeuro ds006780

### Verified public identity

- OpenNeuro accession: `ds006780`
- version/DOI presently cited by the repository: `10.18112/openneuro.ds006780.v1.0.0`
- dataset name: `SFARI_EEG multi-paradigm dataset (BIDS)`
- BIDS dataset type: raw
- license: CC0
- acquisition: BioSemi ActiveTwo, 64 channels, BioSemi64 montage
- sampling rate: 512 Hz
- power-line frequency: 60 Hz
- groups reported by the dataset README: 66 ASD, 44 typically developing (TD), 28 unaffected siblings (SIB)
- age range: 8–13 years
- diagnostic provenance for ASD includes DSM-5 clinical assessment and ADOS-2 in the principal route, with documented alternative assessment for a subset affected by pandemic masking constraints.

### Resting-state structure

The public README states:
- 1-minute eyes-open resting-state blocks;
- maximum of six 1-minute blocks per participant;
- blocks can span two recording sessions on different days.

This is unusually useful for NSD because the same dataset can address:
- within-subject block stability;
- between-day stability where repeat data exist;
- ASD versus TD architecture;
- familial-liability structure using the sibling group;
- scalar-admission/refusal repeatability;
- spatial/modal organization;
- ordinary spectral comparators.

### Multi-paradigm value

The dataset also contains multiple sensory, attentional, motor, and face/object paradigms. These provide future controlled-state/perturbational opportunities without immediately requiring a new experiment.

Published analyses already use portions of this dataset, including 2026 work on face-processing oscillatory dynamics and auditory steady-state responses. This means NSD must compare against those native analyses rather than treat the data as an untouched conceptual blank slate.

### Current NSD disposition

`PRIORITY A — PRIMARY PEDIATRIC ASD/TD/SIB FORWARD CANDIDATE`

Reasons:
1. raw BIDS;
2. strong subject/clinical metadata;
3. 64-channel spatial information;
4. repeat resting blocks over two days;
5. explicit sibling group creates a biologically interesting intermediate comparison without inventing a coordinate;
6. public CC0 provenance;
7. multiple paradigms permit Function/Limit testing beyond resting spectra.

Important caveat:
The TD participants can support an initial same-acquisition pediatric reference, but the healthy/reference model must be frozen independently of ASD outcome optimization. External pediatric transfer remains desirable.

## 3. Highest-priority healthy reliability candidate — SRM Resting-state EEG / OpenNeuro ds003775

### Verified public identity

- OpenNeuro accession: `ds003775`
- current NEMAR page identifies OpenNeuro version `v1.2.1`
- NEMAR DOI: `10.82901/nemar.on003775`
- license: CC0
- 111 healthy control subjects
- 64 electrodes, BioSemi ActiveTwo
- 4 minutes continuous eyes-closed EEG
- some subjects have repeat recordings at a later time point
- raw rereferenced data plus a derived cleaned dataset are available
- demographic and cognitive-test information are included.

### NSD value

This is a compact, high-value qualification dataset for:
- label-blind spectral and modal adequacy;
- test-retest behavior where repeat sessions exist;
- no-peak/refusal reproducibility;
- comparing raw versus provided-cleaned representations without clinical-label pressure;
- preliminary Function/Limit mapping.

### Current NSD disposition

`PRIORITY A — HEALTHY ENGINE-QUALIFICATION / RELIABILITY CANDIDATE`

It should not be treated as the final lifespan Atlas by itself because sample size, age structure, and repeat-session coverage need exact audit.

## 4. Strong adult Atlas candidate — Dortmund Vital Study / OpenNeuro ds005385

### Verified public identity

- OpenNeuro accession: `ds005385`
- dataset described in Scientific Data (2024)
- current OpenNeuro/NEMAR material describes 64-channel resting EEG from 608 healthy adults aged 20–70 years;
- eyes-open and eyes-closed recordings;
- 3-minute recordings before and after a roughly 2-hour cognitive task battery;
- approximately 5-year follow-up for 208 participants;
- BIDS format.

### NSD value

This dataset is stronger than a one-time normative sample for several reasons:
- broad adult age range;
- large N;
- EO/EC state manipulation;
- pre/post cognitive-load state change;
- long-term follow-up subset;
- direct use for age/function/recovery/stability mapping;
- excellent opportunity to distinguish trait, immediate state, and long-term change.

### Current NSD disposition

`PRIORITY A — ADULT NEUROSTABILITY ATLAS / FUNCTION-MAP CANDIDATE`

Caveat:
It is not age-matched to the pediatric SFARI ASD cohort and therefore cannot simply become the reference distribution for that clinical comparison. It is a separate adult Atlas component.

## 5. Complementary adult reference — LEMON / MPI Leipzig Mind-Brain-Body

### Verified characteristics

Current public NEMAR material reports:
- resting EEG for approximately 215 participants with EEG data;
- younger adults and older adults;
- 62 EEG channels;
- BrainVision actiCHamp;
- 2500 Hz sampling;
- approximately 16 minutes alternating eyes-open/eyes-closed blocks.

Published descriptions can use slightly different source cohort counts (for example 227 recruited participants versus the EEG-available subset). Exact version-specific participant reconciliation is therefore required before quoting N in an NSD result.

### NSD value

- strong EO/EC contrast;
- long resting duration;
- high sampling rate;
- age-stratified reference;
- independent acquisition platform for transfer testing relative to BioSemi datasets.

### Current NSD disposition

`PRIORITY B — EXTERNAL ADULT TRANSFER / ACQUISITION-ROBUSTNESS CANDIDATE`

It is especially valuable after the Engine is frozen because acquisition transfer is part of the Limit Map.

## 6. Large pediatric/transdiagnostic source — Healthy Brain Network EEG releases

### Verified public characteristics

Current OpenNeuro/NEMAR releases describe:
- more than 3,000 participants across 11 releases;
- ages approximately 5–21 years;
- 129-channel EGI/Geodesic EEG in the cited NEMAR releases;
- resting state plus multiple passive and active tasks;
- extensive behavioral/psychopathology information;
- BIDS organization;
- release-specific datasets/licensing, with current NEMAR releases reporting CC-BY-SA 4.0.

### Critical naming caveat

**Healthy Brain Network is not equivalent to a healthy-control-only cohort.** The project was designed around child/adolescent mental health and includes typical and atypical development/psychopathology. NSD must construct cohort definitions from authoritative participant metadata rather than use the project name as a health label.

### NSD value

Potentially exceptional for:
- developmental Function Map;
- symptom-dimensional analyses;
- transdiagnostic comparison;
- external pediatric transfer;
- testing whether NSD adds anything beyond large conventional EEG/behavioral models.

### Current NSD disposition

`PRIORITY B — LARGE PEDIATRIC/TRANSDIAGNOSTIC TRANSFER SOURCE`

Do not use as a healthy Atlas until a defensible healthy/reference subset is defined independently and audited.

## 7. Proposed forward data sequence

The current best evidence-building order is:

### Phase D-A — healthy Engine qualification

Use `ds003775` first for a manageable 64-channel healthy reliability pass.

Purpose:
- prove the pipeline can ingest a real BIDS EEG hierarchy;
- map ordinary fit/refusal rates;
- test repeated-session behavior;
- compare raw and cleaned data where appropriate;
- expose implementation failures before diagnosis enters.

### Phase D-B — adult Function/Limit Atlas

Use `ds005385` for large-sample adult state/age/longitudinal mapping.

Purpose:
- function before disease;
- EO/EC and pre/post task effects;
- age structure;
- 5-year stability/change;
- define where candidate features are trait-like versus state-like.

### Phase D-C — pediatric ASD/TD/SIB test

Use `ds006780` after Engine rules are frozen enough to resist label-driven tuning.

Purpose:
- ASD versus TD;
- sibling intermediate group;
- repeated rest blocks/two-session reliability;
- spatial/modal organization;
- no-peak/refusal states;
- comparison with conventional spectral and already-published analyses.

### Phase D-D — transfer

Use LEMON and/or HBN as acquisition/development/transdiagnostic transfer sources depending on the exact result emerging from D-A through D-C.

## 8. Why this materially changes the historical dependency

The forward NSD program does **not** need the untraceable 2025 plot inputs to continue scientifically.

Those old figures can remain provenance of the idea while current public datasets provide a stronger evidence route with:
- immutable accessions;
- public metadata;
- explicit participant hierarchy;
- established licenses;
- raw signals;
- independent prior literature;
- enough structure to test failure as well as success.

This is preferable to reconstructing old hand-built coordinates from memory.

## 9. Current dataset gate status

| Dataset | D0 discovered | D1 provenance verified | D2 hierarchy verified | D3 metadata join verified | D4 signal input verified | D5 analysis ready |
| --- | --- | --- | --- | --- | --- | --- |
| ds003775 | YES | PARTIAL | PENDING LOCAL/PROGRAMMATIC AUDIT | PENDING | PENDING | NO |
| ds005385 | YES | PARTIAL | PENDING LOCAL/PROGRAMMATIC AUDIT | PENDING | PENDING | NO |
| ds006780 | YES | PARTIAL | PENDING LOCAL/PROGRAMMATIC AUDIT | PENDING | PENDING | NO |
| LEMON/NEMAR nm000179 | YES | PARTIAL | PENDING LOCAL/PROGRAMMATIC AUDIT | PENDING | PENDING | NO |
| HBN EEG releases | YES | PARTIAL | PENDING RELEASE-BY-RELEASE AUDIT | PENDING | PENDING | NO |

`PARTIAL` means public identity/acquisition/license facts have been checked at source level but files have not yet been ingested and reconciled by the NSD Engine.

No dataset is promoted to analysis-ready merely because its web page is complete.