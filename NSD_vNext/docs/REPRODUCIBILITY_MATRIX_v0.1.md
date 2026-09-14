# NSD Reproducibility Matrix v0.1

Status: ACTIVE / EARLY R1 INFRASTRUCTURE RUNNING
Date: 14 September 2026

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
- scientific estimator fixtures beyond exact known-truth infrastructure;
- mutation tests for every production safeguard.

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

Completed before empirical recomputation:
- exact classical second-order known-truth convention frozen;
- analytic DHO impulse and transfer-power fixtures implemented;
- estimator licensing rules frozen at the current design level;
- known-truth/adversarial test matrix specified;
- modal estimator interface separated from scalar-admission policy;
- scalar admission now mechanically requires explicit model/mode lineage and qualification evidence rather than a descriptive peak alone.

Blocked before current clinical R2 can begin:
- exact forward empirical dataset manifests;
- implemented/described spectral adapter;
- qualified modal estimator(s);
- frozen first empirical task.

Current R2 state: `KNOWN-TRUTH INFRASTRUCTURE ACTIVE / EMPIRICAL RECOMPUTATION PENDING`.

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

The dataset-provenance schema is frozen at design level, but actual healthy/clinical dataset identities and subject/session maps must still be populated from the forward empirical sources.

Current R3 state: `HISTORICAL SOURCE TEXT RECONSTRUCTED / FORWARD DATASET PROVENANCE PENDING`.

## Result-by-result matrix

| Result family | R1 | R2 | R3 | Current ceiling |
| --- | --- | --- | --- | --- |
| 2025 NSD architecture figures | source hashes/audit recorded | no auditable empirical regeneration path | manuscript/supplement source reconstructed; plot data/code absent | P0-D provenance / illustration |
| Historical exact disorder chi/threshold claims | source wording recorded | no valid current recomputation | empirical source chain absent | retired / not earned |
| Engine contract safeguards | CI active | mechanically recomputable | code/provenance in branch | locally verified implementation |
| Exact DHO known-truth fixtures | CI active | analytically recomputable | equations/convention explicit | qualification infrastructure, not neural evidence |
| Descriptive spectral layer | interface/design only | not implemented | target datasets pending | not active |
| Modal Engine qualification | interface + test plan active | qualification not run | target datasets pending | candidate method layer |
| Healthy Atlas | specification only | pending | dataset audit pending | design target |
| ASD phenotype analysis | not frozen | pending | exact forward dataset/source pending | historical/exploratory only |
| Cross-disorder comparison | not frozen | not run | datasets not frozen | hypothesis |
| Comorbidity analysis | not frozen | not run | suitable data pending | hypothesis |
| Predictive clinical endpoint | not frozen | not run | longitudinal evidence not frozen | not tested |

## Release rule

A successful archive hash is not R2. A successfully rerun analysis from local intermediate files is not necessarily R3. A green software CI run is not scientific validation. A known-truth oscillator recovery test is not evidence that a psychiatric EEG signal obeys that oscillator model.

Each reproducibility level and scientific maturity level is reported separately and only after the corresponding evidence is actually reconstructable.