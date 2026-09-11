# GRI current status under protocol v0.7.1 + v0.7.1A

**Content date:** 2026-09-11  
**Status class:** P0-D FUNCTION/SOURCE MAPPING + P0-Q QUALIFICATION  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.1_FINAL_plus_v0.7.1A_Addendum.pdf`  
**Integration branch:** `gri-v071-protocol-integration-20260910`  
**Draft PR:** #3

## 1. Scientific state preserved

Existing GRI results retain their historical epistemic status. v0.7.1A applies prospectively and does not retroactively promote, demote, rescue, or redefine prior results.

Closed internal evidence:

- F4 = `NARROW`;
- legacy predictive P0 FINAL_HOLDOUT = closed internal test;
- Stage C1 = computationally complete at historical `C1-3` under its preserved preregistered-plus-amended lineage;
- biological chi = `NOT_ADMITTED`;
- temporal inheritance/causality/recovery/EP dynamics = not established by static TCGA.

PCPG is independently source-qualified as a rare oncology context but was selected for GRI follow-up post-result. Current role:

```text
research_role = RARE_NATURAL_LIMIT
mode = P0_D
representative_status = NONREPRESENTATIVE_LIMIT_PROBE
confirmatory_weight = NONE
promotion_debt = OPEN
```

## 2. Current heavy computational gate

The next unresolved heavy-compute gate remains the already-frozen **post-C1 adversarial sensitivity v2.2** package.

Under v0.7.1A this is P0-Q qualification of already-viewed/internal evidence. It cannot become P1 confirmation of the same evidence.

No claim is made here that a local process is currently executing. If it is running, it remains the priority heavy local job. If not, launching the frozen package against the completed C1 state is the priority user-side compute action.

## 3. Protocol migration / control architecture now present

The integration branch contains:

- v0.7.1/v0.7.1A audit and D1-D8 migration;
- P0-D/P0-Q separation;
- working Function Map and Limit Map;
- open-channel disposition ledger;
- pathway-specific independence ledger;
- four-role coverage registry;
- Regulatory Substrate Atlas v0.1 schema;
- external source candidate inventory;
- native-comparator survey;
- comparator-provenance recovery audit;
- P2 Engine gap and code-path inventory;
- negative/mutation/refusal test specification;
- clean-room R1/R2/R3 plan;
- MFR-14 template;
- capability-description index and supersession map;
- draft machine-readable Tool-output schema;
- executable protocol contract and known-bad tests;
- schema↔validator synchronization tests;
- machine-readable external source-gate ledger plus CI firewalls;
- PR CI.

Protocol-control tests explicitly guard biological-chi prohibition, P0/P1 status separation, MFR-14 P1 requirements, Atlas independence, rare-natural selection/representativeness/base-rate rules, all eight independence dimensions, and source-discovery non-promotion.

## 4. Current external P0-D source gates

Machine-readable source of record:

`config/gri_external_source_gate_ledger_20260911.json`

Detailed candidate inventory:

`docs/GRI_EXTERNAL_ATLAS_DATASET_CANDIDATES_P0D_20260910.md`

No external candidate has been evaluated for GRI scientific performance, selected as P1, or frozen as a decisive confirmation cohort.

### Prostate `GSE262522 + GSE262524 + GSE237995`

Source identity gate closed:

```text
450K = 68
EPIC = 53
methylation union = 121
RNA-seq = 121
450K∩EPIC titles = 0
methylation∩RNA titles = 121
methylation-only = 0
RNA-only = 0
EXACT_CROSS_MODALITY_TITLE_BIJECTION = PASS
```

Published methods retain 449,636 probes shared across 450K/EPIC after harmonization.

Dedicated audit:

`artifacts/GRI_PROSTATE_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

Current use: very-high-priority P0-D static external / platform-transport candidate, not P1.

### Breast primary -> regional metastasis `GSE58999 + GSE57968 / GSE59000`

Source declares 44 methylation-profiled matched patient pairs and RNA for 36 of those pairs.

```text
methylation samples = 88
expression samples = 72
raw title intersection = 66/72
terminal-b diagnostic title crosswalk = 72/72
```

The six raw discrepancies are a narrowly documented terminal-`b` naming asymmetry. Multiple cases were verified directly at patient/state level. The diagnostic normalization is **not yet a production identity rule**; full 72-row GSM/patient/state crosswalk remains the final mechanical identity gate.

Dedicated audit:

`artifacts/GRI_BREAST_PAIRED_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

Current use: high-priority paired `PERTURBED_FUNCTION` / `BOUNDARY_OR_TRANSITION` P0-D candidate.

### Melanoma acquired MAPKi resistance `GSE65186`

Source structure:

```text
methylation arrays = 144
expression-array samples = 4
RNA-seq samples = 70
unique human methylation states = 63
unique human transcriptome states = 64
shared human patient-states = 61
shared human patient IDs = 19
strict shared baseline+post patients = 18
shared cell-model states = 8/8
```

Explicit asymmetries are preserved. Pt21 has resistant-state overlap but no shared baseline and is refused from a strict baseline→post paired analysis unless a different rule is prospectively justified.

Dedicated audit:

`artifacts/GRI_MELANOMA_MAPKI_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

Current use: strongest source-qualified ordered `PERTURBED_FUNCTION` candidate found so far, ranked by source architecture only.

### CGGA `CCell_4083`

The public portal's `35 samples` does **not** represent 35 complete cases across all listed modalities.

Verified source-deposit counts:

```text
proteomics = 35
phosphoproteomics = 35
methylation = 29
bulk RNA-seq = 19
scRNA = 18 by accession title / 19 samples containing 21 tumors by source description
```

Therefore `ALL_FIVE_MODALITIES_COMPLETE_ON_35 = FALSE`.

The scRNA count discrepancy remains open. Public analysis code confirms `Cohort_ID` crosswalks were used between protein-defined metadata and methylation/scRNA layers, but exact pairwise modality intersections require processed/controlled manifests.

Dedicated audit:

`artifacts/GRI_CGGA_CCELL4083_MODALITY_AUDIT_P0D_20260911.md`

Current use: high-value external multi-layer Atlas/Function candidate with unresolved exact pairwise intersections.

### Other candidates retained

- LUAD `GSE66836 + GSE66863`: 121 source-declared matched tumor cross-omic subset;
- CRC `GSE213402`: 10 paired primary/liver-metastasis patients, RRBS + RNA-seq;
- ALK resistance `GSE139388` family: cell-model perturbation candidate;
- CGGA legacy methylation/expression families: overlap unresolved;
- ICGC ARGO: exact paired methylation/expression program not yet source-qualified.

Failures/access gaps remain in the ledger rather than being silently replaced.

## 5. Comparator status

Structural comparator work is meaningful and already narrows novelty: AJIVE/MOFA2/simple baselines constrain structural claims; CKA/modal decomposition remain established primitives.

Historical post-FINAL equal-dimensional predictive control:

```text
PROTOCOL_INTENT_REFERENCED = YES
EXACT_EXECUTABLE_FREEZE_RECOVERED = NO
RESULT_RECOVERED = NO
HISTORICAL_COMPARATOR_FREEZE_PROVENANCE = UNRESOLVED
```

A fresh repository/File-Library recovery search did not locate an exact runnable freeze. No filename, hash, design, or result is invented.

If unrecoverable, a replacement capacity-matched comparator is a new science-adjacent P0-Q design and requires review before freezing.

## 6. Current protocol coverage balance

| Role | Current state |
|---|---|
| `NOMINAL_FUNCTION` | strong internal static coverage; external source qualification advancing |
| `PERTURBED_FUNCTION` | now materially improved by melanoma/breast paired/ordered source qualification |
| `BOUNDARY_OR_TRANSITION` | strong method/representation limits; biological state-change candidates now source-qualified but not yet analyzed |
| `RARE_NATURAL_LIMIT` | PCPG source-qualified for post-result P0-D only; no prospectively selected P1 rare-limit test |

The new protocol therefore changed the program from failure-only pressure testing into paired:

`P0-D FUNCTION/SOURCE MAPPING + P0-Q QUALIFICATION`

without weakening the adversarial safeguards.

## 7. Current scientific stop boundaries

Autonomous work stops only where a new result or science/science-adjacent decision is required:

1. **post-C1 sensitivity result** before final supported System Model / production Engine capability freeze;
2. **new capacity-matched comparator design** if the historical freeze remains unrecovered;
3. **decisive external P1 task/cohort/comparator selection** and completed MFR-14;
4. **final System Model scientific scope freeze** after sensitivity/comparator disposition;
5. **authoritative manuscript claim edits** after returned evidence and user-authorized scope;
6. **biological chi admission**, which remains unsupported.

Source-only identity/access/manifest reconstruction remains safe P0-D work and continues independently of those stops.

## 8. Immediate safe next work

Repository-side:

- keep CI green and repair mechanical failures;
- finish breast GSM/patient/state crosswalk if source metadata permits;
- reconstruct full melanoma patient/state/modality/replicate manifest;
- obtain/inspect CCell_4083 processed manifests for a `Cohort_ID x modality` matrix;
- verify prostate downloadable file identities/hashes and shared-probe reconstruction route;
- continue archive recovery for the historical comparator without redesigning it;
- keep source-gate ledger, Function Map, Limit Map, and current status synchronized.

## 9. User action

**Repository-side:** none.

**Heavy local compute:** post-C1 sensitivity v2.2 remains the needed result. Do not start competing heavy local analyses against the same frozen state while it is running.

## 10. Next gate

When post-C1 sensitivity returns:

1. validate returned state/provenance before biology;
2. disposition every sensitivity branch without retuning;
3. update Function and Limit Maps;
4. establish the current-paper claim ceiling;
5. resolve comparator/scientific-freeze decisions;
6. then freeze supported System Model scope and proceed into production Engine consolidation, independent Atlas freeze, MFR-14 external confirmation, and P2 qualification.
