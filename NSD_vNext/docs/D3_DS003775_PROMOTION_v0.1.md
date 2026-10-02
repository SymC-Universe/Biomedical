# ds003775 D3 Metadata/Join Promotion v0.1

Date: 14 September 2026
Status: `D3_METADATA_JOIN_VERIFIED` FOR THE FROZEN T0 HEALTHY QUALIFICATION SCOPE
Dataset: OpenNeuro `ds003775`, DOI `10.18112/openneuro.ds003775.v1.2.1`
Mirror used for public metadata inspection: NEMAR `on003775/v1.0.0`

## 1. Scope of this promotion

This promotion is deliberately narrow. It covers the metadata and join structure needed for:

> label-blind T0 Structural Engine qualification and repeatability analysis on the healthy SRM resting-state EEG dataset.

It does **not** promote the signal payload to D4, does not certify preprocessing, and does not authorize cognitive outcomes to enter feature construction.

## 2. D2 invariants inherited

The existing public-tree audit established:

- 111 participant-table rows;
- 111 BIDS subject directories;
- 0 duplicate participant IDs;
- 0 participant/tree subject mismatches;
- 153 explicit sessions;
- 42 subjects with repeated sessions;
- 153 EEG recording files represented by the audited hierarchy;
- 153 channels TSV files;
- 153 EEG JSON sidecars;
- 0 session-table inconsistencies.

These remain the identity/join backbone for the T0 scope.

## 3. Reviewed participant-table roles

Engine-visible participant-table field:

- `participant_id` -> identity only.

Downstream demographic covariates:

- `age`;
- `sex`.

Downstream cognitive/phenotype outcomes:

- `ravlt_*`;
- `ds_*`;
- `tmt_*`;
- `cw_*`;
- `vf_*`.

No diagnosis field exists in the participant table. Cognitive scores are not allowed into Structural Engine feature construction.

## 4. Participant metadata missingness

The pinned public participant table contains 111 rows.

Observed missing values (`n/a`) in the reviewed columns:

| Column | Missing count |
| --- | ---: |
| participant_id | 0 |
| age | 0 |
| sex | 0 |
| ravlt_* | 0 across reviewed RAVLT fields |
| ds_* | 0 across reviewed digit-span fields |
| tmt_2 | 0 |
| tmt_3 | 4 |
| tmt_4 | 1 |
| cw_* | 0 across reviewed color-word fields |
| vf_1 | 5 |
| vf_2 | 5 |
| vf_3 | 4 |

These missing cognitive outcomes do not affect T0 Engine qualification because they are downstream-only fields.

## 5. Engine-visible recording metadata for this scope

Only metadata needed to identify and interpret the recording may enter T0 structural inference:

- BIDS subject identity;
- BIDS session identity;
- run identity where present;
- task/recording state (`resteyesc`);
- sampling frequency;
- channel name/type/status where present in the BIDS recording metadata.

Age, sex, and cognitive scores remain downstream. They may later describe Atlas structure under a separately frozen question but cannot tune signal/model extraction.

## 6. Join cardinality and ambiguity decision

For the frozen T0 scope:

- participant identity is one row per subject;
- one subject may contribute multiple sessions;
- session is therefore not treated as an independent subject;
- no unmatched participant/tree subject is currently present;
- no duplicated participant-table field family requires reconciliation;
- no many-to-many clinical join is needed for Engine construction.

Therefore no ambiguous metadata record requires quarantine at D3 for this dataset/task.

## 7. Versioned manifest

Canonical machine-readable role manifest:

`NSD_vNext/atlas/manifests/ds003775_metadata_role_manifest_v0.1.json`

The manifest stores the reviewed roles, missingness counts, D2 join invariants, release identity, and the frozen T0 scope.

Its canonical body SHA-256 is:

`28d71314e720eb4be799525c27c89f1f5a6090f2464e8d82e0c071effe1afe1d`

The hash is over the manifest body excluding the `canonical_body_sha256` field, serialized with sorted keys and compact JSON separators.

## 8. D3 decision

All D3 requirements needed for the frozen T0 task are now met:

1. fields used by the task have explicit roles;
2. subject/session join cardinality has been audited;
3. unmatched/ambiguous subject records are absent for the current release;
4. no duplicate metadata-column conflict exists;
5. Engine-visible fields contain no clinical label/outcome leakage;
6. demographic/cognitive fields are explicitly downstream;
7. participant-table missingness is quantified;
8. the role manifest is versioned and hashed.

Decision:

`ds003775 -> D3_METADATA_JOIN_VERIFIED (T0 scope)`

## 9. Next gate: D4 signal identity/readability

D4 remains open and must verify actual EEG payloads rather than metadata counts alone.

Minimum D4 checks:

- byte/payload accessibility for a frozen pilot subset;
- file-format readability through the selected native reader;
- identity agreement between loaded recording and BIDS subject/session/run/task path;
- sampling frequency agreement with sidecar/reader;
- channel count/name/type reconciliation;
- recording duration;
- raw-versus-derived identity and preprocessing lineage;
- units/scaling interpretation;
- no silent file substitution;
- deterministic source-file hash/provenance record where practical.

No spectral, modal, Atlas, or diagnostic result may be called analysis-ready until D4 closes.
