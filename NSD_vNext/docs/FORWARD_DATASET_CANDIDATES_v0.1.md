# NSD Forward Dataset Candidates v0.1

Date: 14 September 2026
Status: ACTIVE SOURCE-CANDIDATE AUDIT / FIRST D2 HIERARCHY GATES COMPLETE
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

## 2. Highest-priority healthy reliability candidate — SRM Resting-state EEG / OpenNeuro ds003775

### Verified public identity and hierarchy

- OpenNeuro accession: `ds003775`
- repository Dataset DOI: `doi:10.18112/openneuro.ds003775.v1.2.1`
- BIDS version: `1.6.0`
- license: CC0
- participants.tsv rows: **111**
- BIDS subject directories: **111**
- duplicate participant IDs: **0**
- participant/tree mismatches: **0**
- explicit sessions: **153**
- subjects with more than one session: **42**
- task label: `resteyesc`
- EEG recording files represented in the metadata checkout: **153**
- channels TSV files: **153**
- EEG JSON sidecars: **153**
- session-table inconsistencies: **0**

Current structural result:

`D2_HIERARCHY_VERIFIED`

The important count is therefore not “153 participants.” It is **111 subjects, 153 sessions, with 42 subjects contributing repeated sessions**.

### NSD value

This is the preferred first real-data qualification source because it can test:
- label-blind spectral and modal adequacy;
- test-retest behavior in the repeat subset;
- no-peak/refusal reproducibility;
- subject/session separation;
- preliminary Function/Limit mapping;
- eventual comparison of raw versus cleaned representations where provenance permits.

### Current NSD disposition

`PRIORITY A — FIRST HEALTHY ENGINE-QUALIFICATION / RELIABILITY DATASET`

Next gate:
- D3 reviewed metadata-role/join manifest;
- D4 actual EEG payload readability and signal-level identity checks.

It is not yet analysis-ready and is not the final lifespan Atlas by itself.

## 3. Strong adult Atlas candidate — Dortmund Vital Study / OpenNeuro ds005385

### Verified public identity and hierarchy

- OpenNeuro accession: `ds005385`
- current repository Dataset DOI: `doi:10.18112/openneuro.ds005385.v1.0.3`
- BIDS version: `1.9.0`
- license: CC0
- participants.tsv rows: **608**
- BIDS subject directories: **608**
- participant/tree mismatches: **0**
- explicit sessions: **816**
- subjects with more than one session: **208**
- task labels: `EyesClosed`, `EyesOpen`
- EEG recording files represented in the metadata checkout: **3264**
- events TSV files: **3264**
- channels TSV files: **3264**
- EEG JSON sidecars: **3264**
- sessions TSV files: **608**
- session-table inconsistencies: **0**

Current structural result:

`D2_HIERARCHY_VERIFIED`

This independently recovers the expected large longitudinal structure: **608 unique subjects, 816 sessions, 208 repeat participants**.

### NSD value

This dataset is unusually strong for the adult Function Map because it supports:
- broad adult age structure;
- eyes-open versus eyes-closed state effects;
- pre/post cognitive-load state effects;
- approximately five-year repeated measurement in the repeat subset;
- trait versus immediate-state versus long-term-change analysis;
- ordinary spectral and modal reliability before clinical labels enter.

### Current NSD disposition

`PRIORITY A — ADULT NEUROSTABILITY ATLAS / FUNCTION-MAP DATASET`

Next gate:
- D3 metadata-role/join audit;
- D4 signal-payload verification.

It is not age-matched to the pediatric SFARI cohort and must not be used as that cohort's disease-specific reference.

## 4. Highest-priority clinical candidate with provenance quarantine — SFARI_EEG / OpenNeuro ds006780

### Public identity

- OpenNeuro accession: `ds006780`
- Dataset DOI in `dataset_description.json`: `doi:10.18112/openneuro.ds006780.v1.0.0`
- dataset name: `SFARI_EEG multi-paradigm dataset (BIDS)`
- dataset type: raw
- license: CC0
- acquisition: BioSemi ActiveTwo, 64 channels
- sampling rate: 512 Hz
- README cohort description: 66 ASD, 44 typically developing (TD), 28 unaffected siblings (SIB), total **138**
- README age range: 8–13 years
- README resting-state description: 1-minute eyes-open blocks, maximum six blocks, potentially spanning **two recording sessions on different days**.

### Hard provenance findings from the actual public tree

The first programmatic audit did **not** pass this dataset through D2.

Current public counts disagree:
- README-described cohort total: **138**
- `participants.tsv` rows: **136**
- `sub-*` directories in the public tree: **139**

Three tree subjects have no row in `participants.tsv`:
- `sub-10708`
- `sub-10931`
- `sub-10950`

There are no duplicate participant IDs in the participant table, so this is not explained by simple duplicate rows.

A second metadata discrepancy is also present:
- `dataset_description.json` declares BIDS `1.9.0`;
- the current README text states BIDS `1.10.1`.

### Session-boundary problem

The README says resting data may span two physical recording days, but the checked public hierarchy contains:
- no `ses-*` directories for the dataset;
- no `*_sessions.tsv` hierarchy establishing those two days.

Per-subject `*_scans.tsv` files were inspected for both orphan subjects and a matched participant. They contain a `session` column and acquisition-time column, but sampled records use `n/a` for those fields. Therefore the physical day/session boundary cannot currently be reconstructed from the inspected scans metadata either.

This means:

> `run != session`, and the public run labels cannot be silently reinterpreted as the two physical recording days.

The new scans-session audit has been added to the Engine so this problem is measured rather than hand-waved.

### Multi-paradigm value remains high

The public tree contains task labels including:
- `ASSR`
- `Audiosocial`
- `AvsRT`
- `Beepflash`
- `FAST`
- `Restingstate`

The dataset remains scientifically attractive for:
- ASD versus TD architecture;
- unaffected sibling comparison;
- spatial/modal organization;
- controlled-task Function Map analyses;
- no-peak/refusal phenotypes;
- comparison against already-published analyses.

But its provenance defect changes the order of operations.

### Current NSD disposition

`PRIORITY A CLINICAL SCIENCE / D2 PROVENANCE QUARANTINE`

Current gate state:
- subject-level public hierarchy: **fails clean D2 reconciliation**;
- physical session/day identity: **not recoverable from the audited public hierarchy yet**;
- run identity: recoverable;
- clinical metadata may not enter the Structural Engine in any case.

Permissible future paths are:
1. find an authoritative release/update mapping that reconciles the 136/138/139 discrepancy and physical sessions; or
2. define a frozen, explicitly restricted analysis subset using only participant-table subjects and only hierarchy that is actually recoverable, while **forgoing between-day claims** unless day identity can be established independently.

No silent repair is allowed.

## 5. Complementary adult reference — LEMON / MPI Leipzig Mind-Brain-Body

Current public material reports approximately:
- 215 participants with EEG data in the relevant EEG release;
- younger and older adults;
- 62 EEG channels;
- BrainVision actiCHamp;
- 2500 Hz sampling;
- approximately 16 minutes of alternating eyes-open/eyes-closed blocks.

Published descriptions use slightly different cohort denominators depending on recruitment versus EEG availability, so version-specific participant reconciliation is required before quoting N in an NSD result.

Current disposition:

`PRIORITY B — EXTERNAL ADULT TRANSFER / ACQUISITION-ROBUSTNESS CANDIDATE`

No D2 promotion has yet been made for this source in the NSD Engine audit.

## 6. Large pediatric/transdiagnostic source — Healthy Brain Network EEG releases

Current public releases describe:
- thousands of pediatric/adolescent participants across multiple releases;
- high-density EEG;
- resting and active tasks;
- extensive behavioral/psychopathology metadata;
- BIDS organization.

Critical naming caveat:

**Healthy Brain Network is not equivalent to a healthy-control-only cohort.** Healthy/reference membership must be defined from authoritative metadata, not inferred from the project name.

Current disposition:

`PRIORITY B — LARGE PEDIATRIC/TRANSDIAGNOSTIC TRANSFER SOURCE`

Release-by-release provenance and hierarchy audit is still required.

## 7. Updated forward data sequence

### Phase D-A — healthy Engine qualification

Use `ds003775` first.

Why:
- D2 hierarchy is already clean;
- manageable 64-channel dataset;
- 42 repeat participants permit immediate subject/session discipline testing;
- no disease labels are needed to qualify structure.

### Phase D-B — adult Function/Limit Atlas

Use `ds005385` next.

Why:
- D2 hierarchy is clean;
- large sample;
- 208 repeat participants;
- EO/EC and longitudinal structure;
- ideal for trait/state/age/Limit mapping.

### Phase D-C — pediatric ASD/TD/SIB only after provenance decision

Keep `ds006780` as the highest-value pediatric clinical candidate, but do **not** promote it to analysis-ready status while the subject-count and physical-session discrepancies are unresolved.

If a restricted run-level subset is later used, that restriction must be frozen in the task protocol before outcome inspection.

### Phase D-D — external transfer

Use LEMON and/or HBN after the first Engine/Atlas configuration is frozen enough that transfer can genuinely test it rather than help tune it.

## 8. Why this is scientifically better than rescuing the old plots

The forward NSD program no longer depends on reconstructing the untraceable 2025 figure inputs.

The public-data route already does something the old workflow could not: **it can fail a dataset before the science is allowed to use it.**

The first real audit has produced both outcomes:
- `ds003775` and `ds005385` pass clean structural hierarchy checks;
- `ds006780`, despite being the most clinically tempting dataset, currently fails clean hierarchy admission.

That refusal is evidence that the new safeguards are functioning, not an inconvenience to be patched around.

## 9. Current dataset gate status

| Dataset | D0 discovered | D1 provenance | D2 hierarchy | D3 metadata roles/joins | D4 signal input | D5 analysis ready |
| --- | --- | --- | --- | --- | --- | --- |
| `ds003775` | YES | VERIFIED FOR CURRENT PUBLIC RELEASE METADATA | **VERIFIED** | PENDING REVIEWED MANIFEST | PENDING | NO |
| `ds005385` | YES | VERIFIED FOR CURRENT PUBLIC RELEASE METADATA | **VERIFIED** | PENDING REVIEWED MANIFEST | PENDING | NO |
| `ds006780` | YES | **CONFLICTED / QUARANTINED** | **FAIL / BLOCKED** | PENDING | PENDING | NO |
| LEMON / nm000179 | YES | PARTIAL | PENDING | PENDING | PENDING | NO |
| HBN EEG releases | YES | PARTIAL | PENDING RELEASE-BY-RELEASE | PENDING | PENDING | NO |

No dataset is promoted to D4 until the actual EEG payload identity/readability is verified. No dataset is promoted to D5 merely because its metadata hierarchy is clean.