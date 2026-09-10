# Stage D Execution Handoff v0.1

Status: ACTIVE EXECUTION GUIDE UNDER FROZEN STAGE-D SCIENCE
Branch: gri-stage-d-perturbation-recovery

## Project-control protocol

At every checkpoint report:
1. current status;
2. next scientific/computational step;
3. work that can proceed mechanically without scientific reinterpretation;
4. exact user action, if any;
5. expected success artifact.

Mechanical failures are repaired without changing frozen scientific assumptions. Any proposed change to dataset role, primary endpoint, feature universe, null, detector family, promotion rule, or interpretation requires an explicit amendment committed before the affected biological results are inspected.

## Active execution sequence

### Gate 0A - Existing GRI post-C1 v2.1
Continue the already-frozen post-C1 sensitivity independently. Stage D does not wait for it to define its acquisition metadata, but Stage D cannot rewrite its outcome.

Expected artifact: `Post_C1_Adversarial_Sensitivity_v2_1_Result.zip`.

### Gate D0.1 - Public-data acquisition inventory
Purpose: collect authoritative file identities and sample metadata for D1-D4 without biological contrast analysis.

Required output per dataset:
- `ACQUISITION_MANIFEST.json`
- `FILES_SHA256.csv`
- `SAMPLE_MANIFEST_RAW.csv`
- `SAMPLE_MANIFEST_NORMALIZED.csv`
- `MANIFEST_AUDIT.json`
- `RUN_LOG.txt`

Pass conditions:
- accession identity matches the frozen registry;
- every retained file has size + SHA-256;
- all samples have source accession, assay, biological condition, time point if present, treatment, replicate identifier if recoverable, and platform;
- ambiguous samples are marked `UNRESOLVED`, never guessed;
- no outcome contrast, clustering, differential analysis, or feature selection has been performed.

### Gate D0.2 - Assay-overlap and design audit
Purpose: determine exactly which samples/layers can support each prespecified question.

Required output:
- layer-by-sample overlap table;
- condition/timepoint/replicate counts;
- paired-versus-unpaired status;
- missingness matrix;
- batch/platform fields;
- explicit list of unresolved design ambiguities.

No biological effect values are computed here.

### Gate D0.3 - Final analysis freeze
Only after D0.1/D0.2 are known, freeze:
- exact feature universes;
- mapping/annotation versions;
- scaling/imputation rules;
- matched-control definitions;
- norm for `Q_residual`;
- modal/subspace construction;
- conglomeration construction;
- linear detector;
- nonlinear secondary detector and bandwidth rule;
- empirical null replicate count;
- capacity-matched controls;
- model-family competition for D2 time courses;
- minimum support/evaluability rules;
- multiple-testing families;
- refusal states.

This freeze must precede any Stage-D biological outcome inspection.

### Gate D1 - Primary perturbation-withdrawal-recovery
Dataset: GSE216989 / GSE216986.

Questions:
1. Did decitabine measurably perturb methylation under the frozen representation?
2. What fraction/direction of that displacement remains after withdrawal/recovery?
3. Does acute methylation state predict later RNA and/or 3D-regulatory persistence better than generic/scrambled/capacity-matched controls?
4. Which scalar/modal/conglomeration views agree or disagree?

Do not fit a recovery time constant if only acute + endpoint recovery are available.

### Gate D2 - Temporal recovery replication
Dataset: GSE20945.

Questions:
1. Is a recovery trajectory identifiable across the available time points?
2. Which candidate trajectory family wins under the frozen model-competition rule?
3. Do D1-defined directions/features predict D2 recovery behavior without refitting against D2 outcome labels?

### Gate D2.5 - Freeze recovery-associated signatures
Freeze only signatures that meet the D1/D2 criteria defined in D0.3.

Record rejected/failed candidates too.

The D3/D4 files may be downloaded/hash-locked earlier, but their biological outcomes must not be used to choose D1/D2 signatures.

### Gate D3 - Independent malignant-transformation challenge
Dataset: GSE231780 / GSE231778.

Question: do D1/D2-frozen recovery-associated signatures change in the prespecified direction across the experimentally ordered transformation sequence?

This is not treated as longitudinal recovery and does not prove recovery failure causes transformation.

### Gate D4 - Transformation-resistance contrast
Dataset: GSE91071 / GSE91069.

Question: do the same frozen signatures distinguish transformable from refractory/resistant states under the supported detector class?

A negative linear result is `NO_DETECTABLE_RELATIONSHIP_UNDER_LINEAR_DETECTOR`, not `NO_RELATIONSHIP`, because the upstream synthetic suite already retained a nonlinear-only failure.

### Gate D5 - Specificity and robustness
Run every predeclared:
- sample shuffle;
- feature/Hallmark scramble;
- size-matched shuffled Hallmark membership;
- equal-dimensional unsupervised compression;
- technical/platform attack;
- regulatory-context depth diagnostic;
- linear/nonlinear detector comparison;
- uncertainty/refusal propagation.

### Gate D6 - Manuscript integration
Every outcome is incorporated before claim promotion.

Allowed outcomes include:
- broad success;
- influence only;
- recovery association without transformation generalization;
- transformation association without recovery prediction;
- nonlinear-only support;
- context-sensitive support;
- nonidentifiable/refusal;
- complete failure of the resilience hypothesis.

## Compute routing

### GitHub
Use for:
- frozen protocols/configs;
- tests;
- metadata-only/small jobs;
- result validation;
- compact reproducibility artifacts;
- figure/table regeneration.

Do not place multi-gigabyte third-party datasets in GitHub.

### Kaggle
Use for:
- D1-D4 public dataset download/caching;
- EPIC/WGBS/RNA/PCHi-C matrix preprocessing;
- large eigendecompositions and repeated-null workloads;
- checkpointed jobs benefiting from the available RAM.

Kaggle notebooks are launchers only. Scientific code must be imported from the authoritative GitHub branch/commit.

### PowerCell
Use for:
- long/restart-sensitive runs;
- independent reruns;
- jobs exceeding comfortable Kaggle session duration;
- verification of Kaggle outputs from the same frozen code.

## User-facing rule

Do not manually edit scientific JSON/configs after results begin. If a run fails mechanically, return the complete `RUN_LOG.txt` plus the generated `RETURN_TO_CHAT` or checkpoint package. Mechanical repairs will be supplied as a new version with the frozen science preserved.
