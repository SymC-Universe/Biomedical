# NSD Reproducibility Matrix v0.1

Status: ACTIVE / T0 P0-Q REPRODUCIBILITY INFRASTRUCTURE RUNNING
Date: 18 September 2026

## R1 — Release integrity and regeneration

Required for a release-qualified NSD package:
- canonical commit identified;
- archive/checksum generated;
- dependency/environment lock;
- tests separated into scientific tests, software tests, and drift/integrity checks;
- clean-room extraction verified;
- generated figures/tables regenerated from declared parents;
- stale historical artifacts excluded from the active release path.

### Current R1 progress

Already implemented:
- forward work isolated on `nsd-rebuild-gom-v0.8.0` with draft PR #5;
- `NSD_vNext/` is the canonical forward workspace;
- historical source files are separated from forward evidentiary authority;
- historical TeX/PDF files are hash-recorded in the source audit;
- Engine package has explicit semantic version `0.1.0` in its current scaffold;
- configuration SHA-256 generation is deterministic;
- result JSON serialization is deterministic;
- mechanical contract tests cover scalar lineage, whole-system-chi prohibition, refusal states, hierarchy duplication, metadata-join ambiguity, subject split leakage, and exact oscillator conventions;
- GitHub Actions workflow `.github/workflows/nsd-engine-contracts.yml` runs Engine contract tests on relevant push/PR changes;
- dedicated NSD Engine workflow has completed successfully on the active PR branch.

Not yet release-closed:
- package lock/requirements freeze for scientific dependencies;
- release archive and whole-package checksum;
- clean-room reconstruction from a tagged release;
- figure/table regeneration scripts and parent manifests;
- full release archive and clean-room tagged-release reconstruction;
- figure/table regeneration scripts and parent manifests for the eventual manuscript release;
- mutation tests for every production safeguard;
- release-qualified Atlas lock and external benchmark package.

Current R1 state: `PARTIAL / ACTIVE INFRASTRUCTURE`, not a release claim.

## R2 — Scientific recomputation

Required:
- exact dataset/source identity;
- subject/session/trial hierarchy;
- preprocessing configuration;
- feature extraction version;
- model and threshold versions;
- split definitions;
- subject-level resampling/validation logic;
- deterministic or seeded stochastic steps;
- recomputation of every primary manuscript quantity from preserved inputs where licensing permits.

### Current R2 progress

Completed / active:
- exact classical second-order known-truth convention frozen;
- analytic DHO impulse and transfer-power fixtures implemented;
- estimator licensing rules frozen at the current design level;
- known-truth/adversarial test matrix specified;
- modal estimator interface separated from scalar-admission policy;
- scalar admission mechanically requires explicit model/mode lineage and qualification evidence rather than a descriptive peak alone;
- exact forward healthy dataset identity and 42-subject repeat-session subset manifest established for ds003775;
- all 84 repeat recordings re-verified at D4 inside the population workflow;
- frozen Welch descriptive layer executed population-wide;
- frozen descriptive periodic/aperiodic candidate executed population-wide;
- subject-aware repeatability outputs include channel-wise ICC(A,1) and categorical agreement;
- M1 direct AR(2) and M2 latent-covariance routes have executable known-truth/adversarial qualification records;
- the P0-Q qualification-search history is now explicit in P0Q_QUALIFICATION_SEARCH_LEDGER_v0.1.md.

Blocked before clinical R2 or real-EEG modal-scalar recomputation can begin:
- a qualified and frozen modal adequacy/admission route;
- a locked independent Atlas version appropriate to the downstream claim;
- a frozen clinical task and untouched subject-level evidence;
- standard/native comparator freeze for that task.

Current R2 state: `HEALTHY DESCRIPTIVE RECOMPUTATION ACTIVE / MODAL P0-Q ACTIVE / CLINICAL R2 BLOCKED`.

## R3 — Primary evidence and provenance reconstruction

Required:
- dataset provenance and access route;
- clinical-label provenance;
- acquisition metadata;
- covariate provenance;
- literature source identity for external reference values;
- exact transformations and units;
- Atlas-source independence mapping;
- privacy-safe subject/session identity preservation where raw IDs cannot be redistributed.

### Historical R3 result

For the 2025 paper, source-level provenance reconstruction is now complete for the material supplied by the user:
- main TeX recovered and hashed;
- supplementary TeX recovered and hashed;
- rendered main/supplement PDFs recovered and hashed;
- figure claims classified;
- absence of claim-level inline citation binding documented.

However, the historical package does not contain the code/data provenance needed to reconstruct the displayed values as empirical results. Therefore historical figures remain P0-D architecture/provenance rather than R3-closed empirical evidence.

### Forward R3 state

For the first healthy T0 source, ds003775, the source/release identity, 111-subject public hierarchy, 42-repeat-subject index, 84-recording frozen repeat manifest, metadata-role firewall, subject/session joins, acquisition condition, and exact D4 payload identities are now auditable in the forward package.

Clinical-label provenance and clinical dataset/source reconstruction remain intentionally downstream. The first healthy source is therefore materially ahead of the clinical R3 path and must not be described as if both are still merely pending.

Current R3 state: `FIRST HEALTHY SOURCE PROVENANCE ACTIVE/CLOSED FOR FROZEN REPEAT SCOPE / CLINICAL PROVENANCE PENDING`.

## Result-by-result matrix

| Result family | R1 | R2 | R3 | Current ceiling |
| --- | --- | --- | --- | --- |
| 2025 NSD architecture figures | source hashes/audit recorded | no auditable empirical regeneration path | manuscript/supplement source reconstructed; plot data/code absent | P0-D provenance / illustration |
| Historical exact disorder chi/threshold claims | source wording recorded | no valid current recomputation | empirical source chain absent | retired / not earned |
| Engine contract safeguards | CI active | mechanically recomputable | code/provenance in branch | locally verified implementation |
| Exact DHO known-truth fixtures | CI active | analytically recomputable | equations/convention explicit | qualification infrastructure, not neural evidence |
| Descriptive spectral layer | CI + frozen configuration + population artifacts active | recomputed on 42 subjects / 84 pinned recordings | ds003775 repeat source and hierarchy audited | P0-Q descriptive layer with explicit limits; no damping/chi license |
| Modal Engine qualification | M1/M2 code, known-truth and adversarial workflows active | M1 and M2 qualification maps reproducible; M2 adequacy still open | synthetic provenance explicit; real EEG modal use prohibited | P0-Q known-truth baseline / real-EEG not admitted |
| Healthy Atlas | release-manifest schema + reference design active | first descriptive population inputs reproducible | ds003775 frozen repeat provenance audited | Atlas-P0-D/P0-Q construction target; not locked confirmatory Atlas |
| ASD phenotype analysis | not frozen | pending | exact forward dataset/source pending | historical/exploratory only |
| Cross-disorder comparison | not frozen | not run | datasets not frozen | hypothesis |
| Comorbidity analysis | not frozen | not run | suitable data pending | hypothesis |
| Predictive clinical endpoint | not frozen | not run | longitudinal evidence not frozen | not tested |

## Release rule

A successful archive hash is not R2. A successfully rerun analysis from local intermediate files is not necessarily R3. A green software CI run is not scientific validation. A known-truth oscillator recovery test is not evidence that a psychiatric EEG signal obeys that oscillator model.

Each reproducibility level and scientific maturity level is reported separately and only after the corresponding evidence is actually reconstructable.

## 18 September 2026 synchronization note

This matrix was updated after the GOM v0.8.0 live-alignment audit because its prior wording lagged the implemented capabilities. The correction changes documentation state only. It does not promote any scientific claim.

The current reproducibility boundary is:

- descriptive healthy spectral/repeatability outputs are reproducible for the frozen ds003775 repeat subset;
- modal known-truth qualification is reproducible, but real-EEG modal damping remains prohibited;
- Atlas schema work exists, but a confirmatory independent Atlas is not yet locked;
- clinical, cross-disorder, comorbidity, longitudinal, and predictive result families remain downstream;
- P1/P2 evidence cannot inherit P0-Q qualification evidence as untouched confirmation.

Capability descriptions should be re-synchronized again whenever the modal adequacy gate, first Atlas artifact, or first clinical task changes state.


## 24 September 2026 GOM v0.8.6 synchronization

The canonical executable verification path is now `REPRODUCIBILITY_GUIDE_v0.1.md`, which uses the GOM v0.8.6 V-section format with visible [CLAIM] markers, exact commands, expected outputs, interpretation ceilings, and a master smoke test. This R1/R2/R3 matrix remains the maturity overview rather than the only reproduction instruction.

The next experiment has been prospectively frozen as `DS004148_DESCRIPTIVE_TRANSFER_FREEZE_v0.1.md`. It uses the six D4-verified ds004148 resting recordings from one subject and reuses the already-frozen ds003775 descriptive representation without ds004148-driven tuning. The suite is required to preserve subject/session/channel hierarchy, report complete same-state pairwise values, compare state medians to the previously committed ds003775 empirical envelopes, retain outside-envelope observations as Limit Map information, and refuse unsupported modal, chi, capital-Chi, clinical, recovery, or population claims.

Current transfer reproducibility state: `FROZEN / EXECUTION SUITE VERSIONED / RESULT NOT PROMOTED UNTIL WORKFLOW AND POST-RESULT AUDIT CLOSE`.


## 24 September 2026 corrected transfer closure

The first ds004148 transfer suite was withheld during post-result audit because its aggregate cross-dataset comparison did not enforce the prospectively frozen exact-label rule. This was corrected without retuning by rebuilding the ds003775 envelopes from the original 42 subject artifacts over the exact 59 shared channel labels.

Promoted workflow run: `36088323374`

Promoted artifact: `nsd-ds004148-descriptive-transfer-suite-v0-2`

Artifact digest: `sha256:f6ce93029c38d72016c2bfd17f4e1b7bdc74bdc5d3ac0fac780896052bf170ce`

Result status: `P0-Q CLOSED / DESCRIPTIVE TRANSFER ONLY`

All 18 state-median transport indicators remained within matched ds003775 empirical envelopes. Two pair-level excursions are retained in the Limit Map and documented in `DS004148_DESCRIPTIVE_TRANSFER_POSTRESULT_v0.2.md`. No scalar, modal, clinical, or population promotion follows from this result.
