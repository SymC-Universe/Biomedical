# GRI current status under protocol v0.7.1 + v0.7.1A

**Content date:** 2026-09-11  
**Status class:** P0-D FUNCTION/SOURCE MAPPING + P0-Q QUALIFICATION  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.1_FINAL_plus_v0.7.1A_Addendum.pdf`  
**Integration branch:** `gri-v071-protocol-integration-20260910`  
**Draft PR:** #3

## 1. Scientific state preserved

Existing GRI results retain their historical epistemic status. v0.7.1A is prospective and does not retroactively promote, demote, rescue, or redefine prior evidence.

Closed internal state:

- F4 = `NARROW`;
- legacy predictive P0 FINAL_HOLDOUT = closed internal test;
- Stage C1 = computationally complete at historical `C1-3` under its preserved preregistered-plus-amended lineage;
- biological chi = `NOT_ADMITTED`;
- static TCGA does not establish temporal inheritance, causality, recovery, treatment response, EP dynamics, clinical utility, or a chi=1 cancer optimum.

PCPG remains a source-qualified rare oncology context selected for GRI follow-up post-result:

```text
research_role = RARE_NATURAL_LIMIT
mode = P0_D
representative_status = NONREPRESENTATIVE_LIMIT_PROBE
confirmatory_weight = NONE
promotion_debt = OPEN
```

## 2. Current heavy computational gate

The next unresolved heavy local compute gate is the already-frozen **post-C1 adversarial sensitivity v2.2** package.

It is P0-Q qualification of already-viewed/internal evidence. It cannot become P1 confirmation of the same evidence. If running locally, it remains the priority heavy job. This repository status does not claim a local process is active unless separately observed.

## 3. Protocol/control architecture now implemented on the integration branch

The branch contains:

- v0.7.1/v0.7.1A D1-D8 migration audit;
- explicit P0-D/P0-Q separation;
- working Function Map and Limit Map;
- open-channel disposition ledger;
- pathway-specific independence ledger;
- four-role coverage registry;
- Regulatory Substrate Atlas v0.1 schema;
- comparator provenance audit and native-comparator survey;
- P2 Engine gap/code-path/negative/mutation/clean-room plans;
- MFR-14 template;
- capability-description index and supersession map;
- machine-readable Tool-output schema;
- executable protocol contract and known-bad tests;
- schema↔validator synchronization tests;
- machine-readable external source-gate ledger;
- external representation-compatibility firewall;
- CI tests that prevent source discovery from silently becoming P1 or a representation adapter from masquerading as confirmation.

## 4. External P0-D source program

Canonical source inventory:

`docs/GRI_EXTERNAL_ATLAS_DATASET_CANDIDATES_P0D_20260910.md`

Machine ledger:

`config/gri_external_source_gate_ledger_20260911.json`

Representation firewall:

`config/gri_external_representation_compatibility_20260911.json`

All candidate scientific GRI outcomes remain unopened and no P1 cohort has been selected.

### Static / near-current bulk representation

**Prostate `GSE262522 + GSE262524 + GSE237995`**

```text
450K = 68
EPIC = 53
methylation union = 121
RNA-seq = 121
methylation↔RNA exact title bijection = 121/121 PASS
450K∩EPIC titles = 0
published shared-probe set = 449,636
```

Current role: strongest source-qualified static/platform-transport candidate. Remaining gate: source files/hashes and independent shared-probe reconstruction.

**LUAD `GSE66836 + GSE66863`**

121 source-declared matched tumor expression/methylation sample numbers. Remaining gate: exact sample table plus RNA-microarray representation reconstruction.

**CGGA `CCell_4083`**

```text
proteomics = 35
phosphoproteomics = 35
methylation = 29
bulk RNA = 19
scRNA = 18 by accession title / 19 samples containing 21 tumors by source description
```

`ALL_FIVE_MODALITIES_COMPLETE_ON_35 = FALSE`. Pairwise intersections remain unresolved and the scRNA count discrepancy stays open.

### Ordered / paired bulk perturbation

**Melanoma `GSE65186`**

```text
shared human patient-states = 61
shared human patient IDs = 19
strict baseline + post-resistance patients = 18
shared cell-model states = 8/8
```

Pt21 is refused from a strict baseline→post paired analysis because no shared baseline exists. Current role: strongest source-qualified bulk ordered perturbation candidate.

**Breast `GSE59000` family**

```text
methylation = 44 matched patient pairs
expression = 36 matched patient pairs
raw title match = 66/72
diagnostic terminal-b crosswalk = 72/72
```

The diagnostic suffix rule is not yet a production identity rule. Full GSM/patient/state export remains the mechanical gate.

**CRC `GSE213402`**

10 paired primary/liver-metastasis patients with RRBS + RNA-seq. Valuable P0-D state-change source but small-N and representation-changing relative to array methylation.

### 2026 longitudinal IDH-glioma sources

Two independent source families now materially improve the v0.7.1A biological perturbation/transition coverage.

**Nomura et al. Nature Genetics 2026 dual-capture cohort**

```text
total tumors = 36
total patients = 19
longitudinally matched tumors = 32
longitudinally matched patients = 15
joint XRBS + Smart-seq2 matched nuclei = 2,117
GSE292025 tumor records = 36
paper 10x retained tumors = 32
GSE292130 current sample records = 31
```

The core strength is direct same-nucleus DNA methylation + RNA capture. The paper/GEO 10x 32-versus-31 discrepancy remains open. This source is representation-changing relative to bulk TCGA and requires a P0-D/P0-Q single-nucleus representation or explicit aggregation model before any GRI outcome is evaluated.

Dedicated audit:

`artifacts/GRI_IDH_GLIOMA_DUAL_CAPTURE_LONGITUDINAL_SOURCE_AUDIT_P0D_20260911.md`

**CARE Nature 2026 longitudinal IDH-mutant cohort**

```text
total tumors = 75
total patients = 35
timepoints = 2 or 3 per patient
main longitudinal pairs = 35
initial at primary diagnosis = 17/35
initial at later surgery = 18/35
treated between main pair = 26/35
no reported adjuvant treatment between main pair = 9/35
Multiome RNA+ATAC tumors = 48
matched Multiome T1/T2 patients = 22
Smart-seq2 tumors = 16
```

The complete `GSE327580` title list independently closes the 22-patient Multiome identity gate: all 22 have T1 and T2, and patients 59, 100, 105, and 111 also have T3, giving `44 + 4 = 48` deposited records.

Bulk DNA methylation is present in the study and in public analysis-code availability categories, but its exact sample count, public accession, and pairwise RNA overlap remain unresolved. No count/accession is inferred.

Dedicated audit:

`artifacts/GRI_CARE_IDH_LONGITUDINAL_MULTIOMIC_SOURCE_AUDIT_P0D_20260911.md`

### Why the two IDH cohorts are not collapsed

- **Nomura:** cleaner direct methylation↔RNA coupling at the same-nucleus level and 15 longitudinal patients.
- **CARE:** larger 35-patient longitudinal cohort, richer treatment/genetic context, and exact 22-patient RNA+ATAC longitudinal subset, but the bulk-methylation source path is unresolved.

Both are high-value P0-D `PERTURBED_FUNCTION` / `BOUNDARY_OR_TRANSITION` sources. Neither is P1.

## 5. Representation firewall

External source qualification no longer implies current-Engine compatibility.

Current source classes include:

- closest bulk match: prostate;
- bulk but RNA-platform-changing: LUAD/breast;
- bulk ordered complex hierarchy: melanoma;
- RRBS methylation-changing: CRC;
- same-nucleus representation-changing: Nomura;
- multi-layer representation-changing with unresolved methylation path: CARE;
- static multi-layer incomplete-overlap: CCell_4083.

Any new adapter developed on an external candidate is P0-D/P0-Q and cannot confirm itself on the same evidence.

## 6. Comparator state

Historical post-FINAL equal-dimensional comparator:

```text
PROTOCOL_INTENT_REFERENCED = YES
EXACT_EXECUTABLE_FREEZE_RECOVERED = NO
RESULT_RECOVERED = NO
HISTORICAL_COMPARATOR_FREEZE_PROVENANCE = UNRESOLVED
```

Repeated repository/File-Library recovery has not located an exact runnable freeze. No filename, hash, design, or result is invented. If unrecoverable, a replacement design is new science-adjacent P0-Q work and requires review before freeze.

## 7. v0.7.1A coverage after source discovery

| Research role | Current state |
|---|---|
| `NOMINAL_FUNCTION` | strong internal static coverage; external bulk source qualification now strong |
| `PERTURBED_FUNCTION` | materially improved: melanoma, breast, CRC, Nomura, CARE source families |
| `BOUNDARY_OR_TRANSITION` | strong method limits plus genuine ordered biological-state source families, not yet GRI-analyzed |
| `RARE_NATURAL_LIMIT` | PCPG post-result P0-D only; no prospectively selected rare-limit P1 test |

The largest previous source-architecture gap, genuine biological ordering/perturbation, is no longer a candidate-discovery vacuum. It is now a **representation and freeze problem**, which is a much better position scientifically.

## 8. Current scientific stop boundaries

Autonomous work still stops where a new result or science/science-adjacent choice is required:

1. post-C1 sensitivity outcome before final supported System Model / Engine scope freeze;
2. new capacity-matched comparator design if the historical freeze remains unrecovered;
3. decisive external P1 task/cohort/comparator selection and MFR-14 freeze;
4. final scientific System Model capability freeze after sensitivity/comparator disposition;
5. authoritative manuscript claim edits after returned evidence and user-authorized scope;
6. biological chi admission, which remains unsupported.

Source-only identity/access/manifest reconstruction, representation triage, protocol-control hardening, provenance recovery, and CI repair remain safe P0-D/P0-Q work.

## 9. Immediate safe next work

- reconstruct the Nomura 36-tumor longitudinal identity/order table and joint-nucleus pairing schema;
- reconstruct CARE's full 75-sample patient/timepoint table and continue the bulk-methylation source search;
- finish breast GSM/patient/state crosswalk;
- build melanoma patient/state/modality/replicate manifest;
- obtain CCell processed manifests for exact modality intersections;
- verify prostate source files/hashes/shared-probe gate;
- reconstruct LUAD exact 121-sample identity table;
- keep current control/status/PR text synchronized and CI green.

## 10. User action

**Repository/source side:** none required right now.

**Heavy local compute:** post-C1 sensitivity v2.2 remains the needed result. If already running, do not start competing heavy local analyses against the same frozen state.

## 11. Next scientific gate

When post-C1 sensitivity returns:

1. verify returned state/provenance before biology;
2. disposition every frozen sensitivity branch without retuning;
3. update Function and Limit Maps;
4. establish the current-paper claim ceiling;
5. resolve comparator/scientific-freeze decisions;
6. then freeze supported System Model scope and proceed toward production Engine consolidation, independent Atlas freeze, MFR-14 external confirmation, and P2 qualification.
