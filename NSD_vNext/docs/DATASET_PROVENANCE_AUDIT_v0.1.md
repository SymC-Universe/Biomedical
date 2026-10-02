# NSD Dataset Provenance and Hierarchy Audit v0.1

Date: 14 September 2026
Status: STRUCTURE FROZEN / FIRST PUBLIC DATASET HIERARCHY AUDITS COMPLETE

## 1. Purpose

This document defines the minimum provenance and independence record required before any dataset can contribute a numerical result to the rebuilt NSD manuscript.

The key correction is simple:

`epochs != trials != runs != sessions != subjects`

and none of those counts may be substituted for another because a larger number looks more impressive.

The first programmatic audits of real public EEG datasets are now included below. Their mixed outcomes are intentional evidence of the gate working.

## 2. Required dataset-level record

For every dataset:

| Field | Required? | Notes |
| --- | --- | --- |
| canonical dataset name | yes | preserve source naming |
| repository / accession / DOI | yes where public | exact release/version |
| source URL | yes where public | stable source preferred |
| license / terms | yes | redistribution and derivative restrictions |
| acquisition site(s) | yes where available | site is a possible confound |
| device / amplifier | yes where available | include hardware filters if known |
| montage / channel count | yes | preserve channel map |
| sampling rate | yes | original and post-resampling |
| recording state | yes | eyes closed/open, task, sleep, etc. |
| nominal recording duration | yes | plus usable duration after QC |
| participant inclusion criteria | yes | source-defined |
| participant exclusion criteria | yes | source-defined + project QC exclusions separately |
| diagnostic instrument / label source | clinical only | exact variable and source; downstream from structural Engine |
| age | where available | exact handling recorded; downstream covariate by default |
| sex/gender variable | where available | use source terminology; downstream covariate by default |
| medication | where available | missingness recorded |
| site/device covariates | where available | never silently ignored |
| raw-data availability | yes | raw / preprocessed / feature-only |
| checksum/version identity | where possible | R3 support |

## 3. Hierarchy table

For every dataset, produce an explicit reconciliation table:

| Level | Unique count | Identifier field(s) | Repeated? | Missing/ambiguous? |
| --- | ---: | --- | --- | --- |
| subjects | dataset-specific | authoritative subject ID | n/a | must be audited |
| sessions | dataset-specific | explicit session ID where available | yes/no | must be audited |
| runs | dataset-specific | explicit run ID | yes/no | must not be relabeled as session |
| trials/epochs | dataset-specific | event/epoch ID | yes/no | not an independent subject |
| channels/sensors | dataset-specific | channel label | yes/no | spatial structure preserved |

A result cannot be described as `N = ...` without naming which level the N refers to.

## 4. Metadata-join audit

Every join between physiology and metadata must record:
- left-table keys;
- right-table keys;
- expected cardinality;
- observed cardinality;
- unmatched records;
- duplicate-key collisions;
- resolution rule;
- quarantine count.

Prohibited rule:

> choose the first matching metadata row.

If more than one metadata record matches a physiological record and no scientifically defensible disambiguation exists, the record is quarantined.

Clinical labels and outcomes are also downstream-only metadata. They may evaluate an already defined structural representation but may not tune the Structural Engine.

## 5. Subject-independence audit

Before inference, answer:
1. Are multiple sessions present per subject?
2. Are multiple runs present per session?
3. Are multiple epochs used as observations?
4. Does train/test splitting keep all records from a subject on one side?
5. Does bootstrap/permutation preserve subject clustering?
6. Are site and subject partially confounded?
7. Are diagnoses repeated longitudinally or treated as fixed?
8. Is a physical session actually encoded, or is the analysis merely inferring one from run order?

Any analysis that splits epochs or sessions from one person across training and test sets is invalid for subject-level generalization unless the task is explicitly within-subject and labeled as such.

## 6. Recording-condition audit

Conditions must not be pooled merely to increase N.

Track separately where present:
- eyes closed;
- eyes open;
- resting/task;
- stimulus type;
- wake/sleep stage;
- pre/post intervention;
- medication on/off;
- acquisition day/session;
- time point;
- other source-defined state variables.

A pooled analysis requires a frozen reason and sensitivity check.

## 7. First public-dataset audit results

### 7.1 OpenNeuro ds003775 — SRM resting-state EEG

Programmatic metadata-only BIDS audit result:

- current Dataset DOI: `doi:10.18112/openneuro.ds003775.v1.2.1`
- BIDS version: `1.6.0`
- license: CC0
- participant-table rows: **111**
- BIDS subject directories: **111**
- duplicate participant IDs: **0**
- participant/tree mismatches: **0**
- explicit sessions: **153**
- subjects with >1 session: **42**
- task: `resteyesc`
- EEG file entries represented in public metadata tree: **153**
- channels TSV: **153**
- EEG JSON: **153**
- session-table issues: **0**

Decision:

`D2_HIERARCHY_VERIFIED`

Correct independence statement:

> 111 subjects contribute 153 sessions; 42 subjects are repeated.

The next gates are D3 reviewed metadata-role/join reconciliation and D4 actual signal-payload verification.

### 7.2 OpenNeuro ds005385 — Dortmund Vital Study

Programmatic metadata-only BIDS audit result:

- current Dataset DOI: `doi:10.18112/openneuro.ds005385.v1.0.3`
- BIDS version: `1.9.0`
- license: CC0
- participant-table rows: **608**
- BIDS subject directories: **608**
- participant/tree mismatches: **0**
- explicit sessions: **816**
- subjects with >1 session: **208**
- tasks: `EyesClosed`, `EyesOpen`
- EEG file entries represented in public metadata tree: **3264**
- events TSV: **3264**
- channels TSV: **3264**
- EEG JSON: **3264**
- sessions TSV: **608**
- session-table issues: **0**

Decision:

`D2_HIERARCHY_VERIFIED`

Correct independence statement:

> 608 subjects contribute 816 sessions; 208 subjects are repeated.

The next gates are D3 metadata-role/join reconciliation and D4 signal-payload verification.

### 7.3 OpenNeuro ds006780 — SFARI_EEG

This dataset produced a genuine provenance stop condition.

Current public sources disagree:
- README group counts total **138** participants;
- `participants.tsv` contains **136** rows;
- public BIDS tree contains **139** `sub-*` directories.

Tree-only subjects absent from `participants.tsv`:
- `sub-10708`
- `sub-10931`
- `sub-10950`

Additional discrepancy:
- `dataset_description.json` BIDS version: `1.9.0`;
- README text: BIDS `1.10.1`.

The README also states that resting blocks may span two recording sessions on different days, but the checked public structure contains:
- no `ses-*` hierarchy;
- no `*_sessions.tsv` mapping for those days.

Per-subject `*_scans.tsv` files contain session/acquisition fields, but inspected matched and unmatched participants use `n/a` rather than a recoverable physical session/day label. Therefore run numbers cannot be promoted to session identifiers by assumption.

Decision:

`D1_CONFLICTED / D2_FAIL_OR_QUARANTINE`

Safe statements at present:
- run identity is recoverable;
- subject identity is not cleanly reconciled across all public sources;
- the stated two-day resting-session structure is not recoverable from the audited public hierarchy;
- no between-day reliability claim may be made from this dataset unless an authoritative mapping is later found;
- a restricted participant-table/run-level subset could be considered only under a separately frozen protocol that explicitly accepts these limits.

This is not a mechanical nuisance to patch. It is the exact kind of ambiguity D2 is supposed to catch.

## 8. Historical continuity markers

Prior project notes mention:
- approximately 1,437 sessions in one compiled analysis;
- ASD and healthy/control groups;
- BCIAUT_P300 and other neurophysiological sources;
- a historical healthy-reference analysis.

Current status: `UNVERIFIED CONTINUITY MARKERS`.

These numbers/names are not entered as current dataset facts until the source files or exact code manifests are recovered.

The clean public datasets above provide a forward path that does not depend on reconstructing those historical counts from memory.

## 9. Current available historical manuscript package

The recovered 2025 NSD paper and supplement contain conceptual and proposed measurement protocols but do not provide the dataset-level information needed to populate this audit for the plotted figures.

Therefore the historical paper cannot be used to back-fill:
- participant counts;
- session counts;
- subject labels;
- site/device metadata;
- raw coordinate values.

## 10. Dataset admission states

Each dataset receives one state:

- `D0_DISCOVERED` — source identified;
- `D1_PROVENANCE_VERIFIED` — accession/version/license and basic acquisition verified without unresolved contradictions material to the task;
- `D2_HIERARCHY_VERIFIED` — subject/session/run/trial structure reconciled;
- `D3_METADATA_JOIN_VERIFIED` — labels/covariates joined safely and metadata roles explicitly separated from Engine-visible context;
- `D4_SIGNAL_INPUT_VERIFIED` — files/arrays match manifest and are readable;
- `D5_ANALYSIS_READY` — frozen inclusion/exclusion and split strategy complete.

Clinical analysis is prohibited before D5 for that specific task.

A dataset can fail or be quarantined at any stage even when it is scientifically attractive.

## 11. Required output files per admitted dataset

Suggested production artifacts:

```text
dataset_manifest.json
subject_session_map.csv
recording_condition_map.csv
metadata_role_manifest.json
metadata_join_audit.csv
exclusion_ledger.csv
provenance_checksums.txt
split_manifest.json
DATASET_CARD.md
```

## 12. Stop conditions

Pause a dataset and do not patch around it when:
- subject identity cannot be reconstructed safely;
- authoritative participant counts disagree materially;
- diagnosis is only inferable from filenames without authoritative metadata;
- session identity is ambiguous;
- run order is being used as a surrogate for physical sessions without an authoritative map;
- raw/preprocessed versions are mixed without lineage;
- site/device labels are missing in a way that makes a key comparison uninterpretable;
- license prohibits the planned use;
- feature files cannot be linked back to source recordings.

The correct response to an irreparable provenance hole is to narrow or replace the dataset, not to fill the gap with assumptions.