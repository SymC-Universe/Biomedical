# NSD Dataset Provenance and Hierarchy Audit v0.1

Date: 14 September 2026
Status: STRUCTURE FROZEN / POPULATION PENDING SOURCE RECOVERY

## 1. Purpose

This document defines the minimum provenance and independence record required before any dataset can contribute a numerical result to the rebuilt NSD manuscript.

The key correction is simple:

`epochs != trials != sessions != subjects`

and none of those counts may be substituted for another because a larger number looks more impressive.

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
| diagnostic instrument / label source | clinical only | exact variable and source |
| age | where available | exact handling recorded |
| sex/gender variable | where available | use source terminology |
| medication | where available | missingness recorded |
| site/device covariates | where available | never silently ignored |
| raw-data availability | yes | raw / preprocessed / feature-only |
| checksum/version identity | where possible | R3 support |

## 3. Hierarchy table

For every dataset, produce an explicit reconciliation table:

| Level | Unique count | Identifier field(s) | Repeated? | Missing/ambiguous? |
| --- | ---: | --- | --- | --- |
| subjects | PENDING | PENDING | n/a | PENDING |
| sessions | PENDING | PENDING | yes/no | PENDING |
| runs | PENDING | PENDING | yes/no | PENDING |
| trials/epochs | PENDING | PENDING | yes/no | PENDING |
| channels/sensors | PENDING | PENDING | yes/no | PENDING |

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

## 5. Subject-independence audit

Before inference, answer:
1. Are multiple sessions present per subject?
2. Are multiple runs present per session?
3. Are multiple epochs used as observations?
4. Does train/test splitting keep all records from a subject on one side?
5. Does bootstrap/permutation preserve subject clustering?
6. Are site and subject partially confounded?
7. Are diagnoses repeated longitudinally or treated as fixed?

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
- time point;
- other source-defined state variables.

A pooled analysis requires a frozen reason and sensitivity check.

## 7. Historical continuity markers

Prior project notes mention:
- approximately 1,437 sessions in one compiled analysis;
- ASD and healthy/control groups;
- BCIAUT_P300 and other neurophysiological sources;
- a historical healthy-reference analysis.

Current status: `UNVERIFIED CONTINUITY MARKERS`.

These numbers/names are not entered as current dataset facts until the source files or exact code manifests are recovered.

## 8. Current available historical manuscript package

The recovered 2025 NSD paper and supplement contain conceptual and proposed measurement protocols but do not provide the dataset-level information needed to populate this audit for the plotted figures.

Therefore the historical paper cannot be used to back-fill:
- participant counts;
- session counts;
- subject labels;
- site/device metadata;
- raw coordinate values.

## 9. Dataset admission states

Each dataset receives one state:

- `D0_DISCOVERED` — source identified;
- `D1_PROVENANCE_VERIFIED` — accession/version/license and basic acquisition verified;
- `D2_HIERARCHY_VERIFIED` — subject/session/run/trial structure reconciled;
- `D3_METADATA_JOIN_VERIFIED` — labels/covariates joined safely;
- `D4_SIGNAL_INPUT_VERIFIED` — files/arrays match manifest and are readable;
- `D5_ANALYSIS_READY` — frozen inclusion/exclusion and split strategy complete.

Clinical analysis is prohibited before D5 for that specific task.

## 10. Required output files per admitted dataset

Suggested production artifacts:

```text
dataset_manifest.json
subject_session_map.csv
recording_condition_map.csv
metadata_join_audit.csv
exclusion_ledger.csv
provenance_checksums.txt
split_manifest.json
DATASET_CARD.md
```

## 11. Stop conditions

Pause a dataset and do not patch around it when:
- subject identity cannot be reconstructed safely;
- diagnosis is only inferable from filenames without authoritative metadata;
- session identity is ambiguous;
- raw/preprocessed versions are mixed without lineage;
- site/device labels are missing in a way that makes a key comparison uninterpretable;
- license prohibits the planned use;
- feature files cannot be linked back to source recordings.

The correct response to an irreparable provenance hole is to narrow or replace the dataset, not to fill the gap with assumptions.