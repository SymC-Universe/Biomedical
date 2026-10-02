# NSD Dataset Metadata Role Manifests v0.1

Date: 14 September 2026
Status: FIRST REVIEWED ROLE PASS / D3 NOT YET COMPLETE
Purpose: state which dataset metadata may be visible to the label-blind Structural Engine, which fields are provenance-only, and which fields are strictly downstream clinical/demographic information.

## 1. Role policy

The executable Engine currently recognizes these metadata roles:

- `IDENTITY`
- `ACQUISITION`
- `RECORDING_STATE`
- `DEMOGRAPHIC_COVARIATE`
- `CLINICAL_LABEL`
- `CLINICAL_OUTCOME`
- `OTHER`

Only the following roles may enter structural feature construction:

`IDENTITY + ACQUISITION + RECORDING_STATE`

Demographics, diagnoses, symptom scores, cognitive outcomes, medication, and other downstream variables may be joined later for Atlas description or clinical evaluation but may not tune the Structural Engine.

Dataset bookkeeping fields can be used to audit availability/inclusion, but they are not automatically signal features.

## 2. OpenNeuro ds003775

Current `participants.tsv` columns:

```text
participant_id
age
sex
ravlt_1
ravlt_5
ravlt_tot
ravlt_imm
ravlt_del
ravlt_rec
ravlt_fp
ds_forw
ds_back
ds_seq
ds_tot
tmt_2
tmt_3
tmt_4
cw_1
cw_2
cw_3
cw_4
vf_1
vf_2
vf_3
```

### Reviewed role mapping

| Column(s) | Role | Structural Engine? | Notes |
| --- | --- | --- | --- |
| `participant_id` | `IDENTITY` | YES | subject key only |
| `age`, `sex` | `DEMOGRAPHIC_COVARIATE` | NO | Atlas/covariate layer downstream |
| `ravlt_*` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | memory-performance variables; not structural inputs |
| `ds_*` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | digit-span variables |
| `tmt_*` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | trail-making variables |
| `cw_*` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | cognitive-task variables |
| `vf_*` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | verbal-fluency variables |

Recording condition, sampling/acquisition metadata, and session identity must come from BIDS hierarchy/sidecars rather than participant cognitive scores.

### D3 implication

No participant-level outcome variable is needed to qualify the Engine on this healthy dataset. This makes `ds003775` particularly suitable for the first label-blind structural pass.

## 3. OpenNeuro ds005385

Current `participants.tsv` columns:

```text
participant_id
sex
age
handedness
session1
late_ses1
session2
late_ses2
```

### Reviewed role mapping

| Column(s) | Role | Structural Engine? | Notes |
| --- | --- | --- | --- |
| `participant_id` | `IDENTITY` | YES | subject key only |
| `sex`, `age`, `handedness` | `DEMOGRAPHIC_COVARIATE` | NO | Atlas/covariate layer downstream |
| `session1`, `session2` | dataset availability/bookkeeping (`OTHER`) | NO as feature | may audit expected session availability; explicit BIDS session hierarchy remains authoritative |
| `late_ses1`, `late_ses2` | dataset timing/bookkeeping (`OTHER`) pending definition audit | NO | can be used downstream only after exact source meaning is verified |

Eyes-open/eyes-closed and other recording-state variables are derived from BIDS task/session structure, not from demographic fields.

### D3 implication

The participant table is simple and poses low leakage risk, but the exact semantics of `late_ses1` / `late_ses2` should be verified before any temporal interpretation.

## 4. OpenNeuro ds006780 / SFARI_EEG

Current `participants.tsv` columns:

```text
participant_id
age
sex
group
handedness
completed_ASSR
completed_AVSRT
completed_Beep-Flash
completed_FAST
completed_Illusory_contours
completed_Motor
completed_Resting_state
fsiq
srs2_total_t
mabc_total_ss
cpt_response_style
ados_css
medication
fsiq_dup
srs2_total_t_dup
mabc_total_ss_dup
cpt_response_style_dup
ados_css_dup
medication_dup
```

### Reviewed role mapping

| Column(s) | Role | Structural Engine? | Notes |
| --- | --- | --- | --- |
| `participant_id` | `IDENTITY` | YES, after subject reconciliation | currently blocked for three tree-only subjects |
| `age`, `sex`, `handedness` | `DEMOGRAPHIC_COVARIATE` | NO | downstream Atlas/covariate layer |
| `group` | `CLINICAL_LABEL` | **NO** | ASD / TD / sibling grouping cannot define Engine structure |
| `completed_*` | availability/bookkeeping (`OTHER`) | NO as feature | can audit expected task availability; actual files remain authoritative |
| `fsiq` | `CLINICAL_OUTCOME` / cognitive phenotype | NO | downstream only |
| `srs2_total_t` | `CLINICAL_OUTCOME` | NO | symptom/trait measure downstream |
| `mabc_total_ss` | `CLINICAL_OUTCOME` | NO | behavioral/motor measure downstream |
| `cpt_response_style` | `CLINICAL_OUTCOME` | NO | behavioral phenotype downstream |
| `ados_css` | `CLINICAL_OUTCOME` / diagnostic severity | **NO** | downstream clinical variable |
| `medication` | downstream clinical covariate (`OTHER`) | NO | may be used in sensitivity/covariate analysis after structure is frozen |
| `*_dup` columns | `OTHER / PROVENANCE AUDIT` | NO | duplicated metadata require equality/missingness audit; never treated as independent predictors |

### D3 implication

Even after the subject-count mismatch is resolved or a restricted subset is frozen, the Structural Engine must not see `group`, ADOS, SRS, IQ, motor, CPT, or medication while constructing spectral/modal/scalar/system features.

This creates a hard test of the framework: the architecture must exist in the recordings before ASD/TD/SIB labels are permitted to evaluate it.

### Duplicate-column issue

The participant table contains duplicated versions of multiple fields (`fsiq_dup`, `srs2_total_t_dup`, `mabc_total_ss_dup`, `cpt_response_style_dup`, `ados_css_dup`, `medication_dup`).

Before D3 promotion the join audit must report:
- exact equality count between each base/duplicate pair;
- missingness disagreements;
- non-equal non-missing values;
- authoritative resolution rule from dataset provenance if discrepancies exist.

The project must not choose one copy silently.

## 5. Engine firewall consequence

The executable `MetadataRoleManifest` rejects clinical labels, outcomes, demographics, and unreviewed columns from the Structural Engine input set.

This means a future analysis cannot accidentally improve clinical separation by:
- selecting peaks using ASD/TD labels;
- choosing modal order from diagnosis;
- choosing regions from symptom scores;
- changing scalar-admission thresholds by group;
- giving age/sex or IQ to the structural feature extractor and later calling the resulting separation “neurophysiological architecture.”

Demographic and clinical variables remain scientifically useful, but only in their correct downstream layer.

## 6. D3 completion requirements

A dataset earns `D3_METADATA_JOIN_VERIFIED` only when:
1. every metadata column used anywhere in the task has an explicit reviewed role;
2. join keys and cardinality are audited;
3. unmatched and ambiguous records are quarantined;
4. duplicated columns are reconciled explicitly;
5. Engine-visible fields contain no diagnosis/outcome leakage;
6. covariates are prespecified for the exact Atlas or clinical question;
7. metadata missingness is quantified;
8. the resulting role manifest is versioned and hashed.

The mappings above are the first reviewed pass, not final D3 promotion.