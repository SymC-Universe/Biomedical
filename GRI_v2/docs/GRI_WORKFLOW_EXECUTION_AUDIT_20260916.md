# GRI workflow execution audit

**Date:** 2026-09-16  
**Scope:** `.github/workflows` as present on `gri-v071-protocol-integration-20260910-chi-bio`  
**Purpose:** distinguish live scientific execution surfaces from provenance probes, synthetic/tool qualification, historical stage workflows, and general CI so documentation work cannot accidentally be mistaken for a biological computation.

## Executive result

The active branch currently contains **27 workflow definitions**. They fall into four operational classes:

1. current `Chi_bio` scientific/qualification workflows;
2. current `Chi_bio` source/provenance probes;
3. historical `gri-v2` stage/tool workflows retained for reproducibility;
4. broad GRI test CI.

The current `Chi_bio` scientific workflows inspected here are guarded by branch/path filters and/or manual dispatch. A manuscript or status-document edit does **not** match their scientific input paths. Historical stage/tool workflows are branch-scoped to `gri-v2` or a historical stage branch and therefore do not auto-run from the active `Chi_bio` branch.

The one intentionally broad surface is `gri-v2-tests.yml`: its `pull_request` trigger covers `GRI_v2/**`, so documentation/manuscript edits inside the open PR may run the general deterministic GRI test suite. That CI is validation/synthetic qualification, not a new biological outcome analysis. This is conservative but lawful.

## A. Current `Chi_bio` scientific/qualification workflows

These workflows can consume or derive scientific qualification results. They must not be described as running merely because the files exist.

| Workflow | Role | Automatic trigger surface | Documentation-only risk | Current governance interpretation |
| --- | --- | --- | --- | --- |
| `gri-v2-chi-bio-shortterm-g2-empirical.yml` | frozen short-term G2 empirical execution | active Chi branch + exact freeze/runner/preflight/test/workflow paths; manual dispatch | none from manuscript/status edits | historical closed scientific lineage; do not rerun to alter its outcome |
| `gri-v2-chi-bio-chronic-g2-empirical.yml` | frozen chronic G2 empirical execution | active Chi branch + exact scientific paths; manual dispatch | none from manuscript/status edits | historical closed/qualified scientific lineage |
| `gri-v2-chi-bio-chronic-g2-feature-gate-robustness.yml` | bounded chronic feature-gate sensitivity | active Chi branch + exact scientific paths; manual dispatch | none from manuscript/status edits | historical qualification evidence; no post-result retuning |
| `gri-v2-chi-bio-b3-matched-network-pilot.yml` | prospective B3 matched-network pilot | active Chi branch + exact B3 scientific paths; manual dispatch | none from manuscript/status edits | closed precursor within refused compact B3 lineage |
| `gri-v2-chi-bio-b3-matched-network-holdout.yml` | frozen B3 matched-network holdout | active Chi branch + exact B3 scientific paths; manual dispatch | none from manuscript/status edits | decisive compact-lineage refusal evidence; do not dimension-shop afterward |
| `gri-v2-chi-bio-b3-network-overlap.yml` | network-overlap qualification | active Chi branch + exact qualification paths; manual dispatch | none from manuscript/status edits | qualification only |
| `gri-v2-chi-bio-b3-network-dependence.yml` | network-dependence qualification | active Chi branch + exact qualification paths; manual dispatch | none from manuscript/status edits | qualification only |
| `gri-v2-chi-bio-b3-symbol-mapping.yml` | deterministic symbol/namespace qualification | active Chi branch + exact mapping paths; manual dispatch | none from manuscript/status edits | qualification only; fuzzy outcome-driven repair remains disallowed |
| `gri-v2-chi-bio-b3-topology-spectrum.yml` | outcome-free topology/spectrum audit | active Chi branch + exact topology paths; manual dispatch | none from manuscript/status edits | Limit-Map evidence; not a license to choose a favorable mode |
| `gri-v2-chi-bio-b3-ulm-runtime-preflight.yml` | ULM runtime preflight | active Chi branch + exact runtime-preflight paths; manual dispatch | none from manuscript/status edits | mechanical qualification only |
| `gri-v2-chi-bio-g1-restoration-r0-embedding-preflight.yml` | current restoration R0 embedding/inverse-identifiability preflight | active Chi branch + R0 runner/bounds/config/freeze/workflow paths; manual dispatch | none from manuscript/status edits | live scientific lane when intentionally triggered; consumes frozen G2 evidence and must preserve its digest |

### R0 immutability guard

The R0 workflow is especially important because it is the only current restoration workflow in the active workflow directory. It is not a generic always-on calculation. It validates the frozen G2 lineage, downloads the pinned chronic-G2 result artifact, verifies the immutable artifact digest, and only then performs the bounded restoration embedding/preflight. This protects against silently converting a later restoration investigation into a rewrite of G2.

## B. Current `Chi_bio` source/provenance workflows

These workflows establish source identity, namespace, or provenance. They do not by themselves admit a biological state or validate `Chi_bio`.

| Workflow | Role | Trigger pattern | Scientific ceiling |
| --- | --- | --- | --- |
| `gri-v2-chi-bio-collectri-probe.yml` | frozen human CollecTRI export/source fingerprint | path-scoped PR + manual dispatch | representation-prior provenance only |
| `gri-v2-chi-bio-dorothea-probe.yml` | DoRothEA source/provenance qualification | active-branch path-scoped push + path-scoped PR + manual dispatch | representation-prior provenance only |
| `gri-v2-chi-bio-geo-source-probe.yml` | GEO source and identity probing | path-scoped PR + manual dispatch | source qualification only, no P1 outcome |
| `gri-v2-chi-bio-chronic-source-probe.yml` | chronic SCC25 source qualification | active-branch/path-scoped scientific provenance trigger + manual dispatch | source identity/provenance only |
| `gri-v2-chi-bio-gse98812-gene-namespace.yml` | GSE98812 identifier namespace diagnosis | active-branch exact-path push + manual dispatch | identifier qualification only |

A source probe may access an external file or resource, but that does not transform its output into independent biological confirmation. Source independence and outcome independence are separate properties.

## C. Historical `gri-v2` stage/tool workflows

These workflows remain useful reproducibility machinery but their automatic push triggers are tied to `gri-v2` and, where applicable, a historical stage branch. They do not auto-run from ordinary edits on the active Chi branch.

| Workflow | Historical role | Branch behavior on current Chi branch |
| --- | --- | --- |
| `gri-v2-stage-b0.yml` | Stage B0 | no automatic current-branch execution |
| `gri-v2-stage-b2-source-probe.yml` | Stage B2 source qualification | no automatic current-branch execution |
| `gri-v2-stage-c0-1-sample-identity.yml` | C0 sample-identity gate | no automatic current-branch execution |
| `gri-v2-stage-c0-methylation.yml` | C0 methylation source gate | `gri-v2` / historical C0 branch only; manual dispatch remains possible |
| `gri-v2-stage-c1a-annotation-source.yml` | C1A annotation/source gate | `gri-v2` only; manual dispatch remains possible |
| `gri-v2-tool-feasibility-f2.yml` | synthetic F2 feasibility challenge | `gri-v2` only; manual dispatch remains possible |
| `gri-v2-tool-feasibility-f3-established.yml` | established-comparator F3 qualification | `gri-v2` only; manual dispatch remains possible |
| `gri-v2-tool-feasibility-f3-simple.yml` | simple-baseline F3 qualification | `gri-v2` only; manual dispatch remains possible |
| `gri-v2-tool-feasibility-f3-smoke.yml` | dependency smoke for established methods | `gri-v2` only; manual dispatch remains possible |
| `gri-v2-tool-prediction-p0-split-manifest.yml` | historical P0 holdout split packaging | `gri-v2` only; manual dispatch remains possible |

Manual dispatch is not a defect. It is an execution capability. Under current governance, however, manual availability does not constitute authorization to reopen a historical scientific branch to improve a present result.

## D. General test CI

`gri-v2-tests.yml` deserves separate treatment.

Its relevant triggers are:

- push to `gri-v2` when `GRI_v2/**` changes;
- pull requests when `GRI_v2/**` changes;
- manual dispatch.

Because PR #4 changes files under `GRI_v2/**`, manuscript/status/governance edits can legitimately trigger this workflow. The jobs run repository tests and deterministic calibration/adversarial checks, including synthetic known-truth/known-null fixtures. They may consume CI time, but they do not open a new cancer outcome, choose a new biological representation, or change a frozen scientific threshold.

**Classification:** `AUTOMATIC_VALIDATION_CI`, not `ACTIVE_BIOLOGICAL_COMPUTATION`.

## E. Trigger-coverage findings

### Finding 1: documentation edits cannot silently launch the current empirical lanes

The short-term, chronic, B3, and R0 empirical/qualification workflows are scoped to their own code/config/freeze/workflow inputs. The new manuscript, status, Function/Limit, and continuity documents are outside those trigger paths.

### Finding 2: current source probes are bounded

Source probes are either manual or path-scoped to the probe implementation/configuration. They do not wake up because the manuscript changes.

### Finding 3: old pipelines remain executable but not current

Historical workflows retain `workflow_dispatch`. This is useful for reproducibility/recovery but creates a governance obligation: a manually dispatched historical workflow must be described by its actual role and may not be mistaken for continuation of the current scientific program.

### Finding 4: broad PR tests are intentional validation, not scientific progress

A queued/running `GRI v2 tests` workflow after a documentation commit should not be reported as if the GRI experiment itself is running. Conversely, a green general test run does not mean G1 restoration, B3, Stage C1, or external validation is scientifically complete.

## F. Monitor and liveness rule

For any status report:

1. inspect live Actions state;
2. identify the workflow by name and run/commit;
3. classify it as biological computation, source/provenance probe, deterministic validation/synthetic CI, or historical/manual execution;
4. only then use present-tense language such as running, queued, failed, or complete.

A watchdog/monitor or queued generic test does not count as progress in the scientific computation it watches.

## G. No workflow change required by this audit

No trigger is changed in this document. The existing current-science path scoping is appropriate and the broad pull-request test suite is conservative but defensible. Changing those surfaces merely to reduce CI noise is not necessary for scientific closure and could reduce protection.

If workflow behavior later becomes a material bottleneck, any trigger edit should preserve the distinction between scientific execution and validation rather than simply disabling tests.
