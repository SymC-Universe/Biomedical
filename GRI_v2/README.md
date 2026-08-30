# GRI v2 / Cancer Stability Atlas

**Status:** DEVELOPMENT PROGRAM, NOT A VALIDATED CANCER TOOL  
**Active phase:** Stage B2 genomic closure  
**Status date:** 2026-08-29

> **Reviewer navigation:** start at `reviewer/README.md`. The moving `gri-v2` branch is a development branch, not an immutable submission record. Manuscript/data submissions should point reviewers to an exact tagged/released snapshot following `reviewer/SUBMISSION_RELEASE_CHECKLIST.md`.

## Objective

The active objective is to build the most predictive, falsifiable cancer-stability tool supported by the data and by the updated Chemistry and Stability Arc methodology.

The historical GRI manuscript is provenance, not the target model. The new tool is not required to reproduce its variables, mechanisms, gene rankings, or conclusions. A historical component survives only if it earns retention under the current evidence rules.

## Notation used in this program

- **V**: expression-adjusted variability/fluctuation structure. Static, not damping.
- **L**: lineage/context dependence.
- **C_in**: read “C sub in.” Internal Hallmark-module RNA coherence.
- **C_out**: read “C sub out.” Coupling of a Hallmark RNA module to the external Hallmark-union background.
- **LOH**: loss of heterozygosity.
- **RPPA**: reverse-phase protein array, an independent protein/phosphoprotein abundance assay.
- **chi**: reserved for a genuine dynamical balance coordinate `Gamma/(2*Omega)`. No valid biological chi has been admitted in this cancer program.
- **Gamma**: a genuine same-coordinate relaxation/damping/recovery/decay rate if chi is ever admitted.
- **Omega**: a genuine same-coordinate intrinsic response/restoring rate or frequency if chi is ever admitted.

## Active scientific rules

- `CV/2` is the historical scalar comparator. It is not chi.
- Static RNA, genomic, protein, composition, and future methylation observables remain independent map axes unless later model competition justifies another representation.
- `chi = 1`, if a valid chi is eventually measured, is a dynamical response-regime boundary of the applicable model. It is not a presumed cancer optimum, maximum organization point, healthy state, or therapeutic target.
- Higher `C_in`, lower `C_out`, higher protein coherence, or higher/lower genomic burden is not inherently better, healthier, or more stable.
- No feature receives privileged status because it appeared in the historical manuscript.
- Model selection is driven by predictive performance, calibration, robustness, ablation, appropriate baselines, and external validation.
- Failed and null branches are retained.
- Manuscript reconstruction is downstream of a validated tool architecture and does not steer feature selection.

## Completed development layers

### Historical scalar closure

The historical `CV/2` experiment was reconstructed and audited. PanCanAtlas RNA expression contains a pronounced mean/variability geometry, but the frozen construction-aware primary test did not distinguish the scalar pattern from processed-expression mean/standard-deviation structure. `CV/2` therefore remains a historical descriptive comparator only.

### Stage A: static RNA measurement map

Stage A is closed as a development measurement layer.

The retained RNA observables are `V`, `L`, `C_in`, and `C_out`. They are not combined into a master stability score.

Stage A1.1 fixed-sample-size calibration removed finite-sample inflation in absolute-correlation magnitudes while preserving the module topology. This supports the network coordinates as reproducible static observables, not as evidence of a dynamical mechanism.

### Stage B1: composition/context decomposition

Stage B1 is closed.

Independent ABSOLUTE tumor purity and DNA-methylation-derived leukocyte fraction explain a real but concentrated portion of the Stage A network geometry, especially in immune/inflammatory Hallmarks. They do not erase the broader topology.

Under joint independent adjustment, the inverse relationship between pairwise `C_in` and `C_out` remains negative in all 30 jointly eligible cancers. Both unadjusted and context-adjusted information are retained.

See `docs/STAGE_B1_AUDIT_20260829.md`.

### Stage B2 source and analysis preregistration

The pre-reserved B2 sources were audited before biological association testing. The genomic/protein coordinate rules and construction nulls were then frozen before Stage A/B1/B2 association results were calculated.

Primary documented genomic coordinates:

1. `ANEUPLOIDY_AS`: chromosome-arm aneuploidy count;
2. `LOH_SEGMENT_COUNT`: number of LOH segments;
3. `LOH_GENOME_FRACTION`: fraction of genome containing LOH;
4. `SCNA_SEGMENT_COUNT`: copy-number segment count;
5. `SCNA_ALTERED_FRACTION`: fraction of profiled base pairs in altered copy-number segments.

They remain separate even when correlated. No genomic burden composite is tuned from the RNA results.

See `docs/STAGE_B2_SOURCE_AUDIT_20260829.md` and `docs/STAGE_B2_PREREGISTRATION_20260829.md`.

### Stage B2 RPPA orthogonal-assay branch

The RPPA branch is computationally closed.

The frozen common panel contains 189 protein/phosphoprotein measurements across 6,887 Stage-A-matched primary RPPA cases. The primary cross-assay coordinate is the median absolute correlation between each Hallmark RNA eigengene and the fixed protein panel in the same patients. The construction null permutes RPPA patient rows as a block, preserving protein covariance while breaking patient-level RNA/protein alignment.

Completed run:

- 31 primary cancer tasks;
- 29 purity/leukocyte context-sensitivity tasks;
- 100/100 resamples for every task;
- 300,000 module-resample rows.

Primary fixed-n result:

- median patient-aligned RNA/RPPA coupling approximately `0.17664`;
- median row-permutation null approximately `0.12794`;
- median aligned-minus-null approximately `+0.04768`;
- all 31/31 cancer-level median specific-coupling values positive.

After purity + leukocyte adjustment:

- median adjusted coupling approximately `0.16820`;
- median adjusted null approximately `0.12736`;
- median adjusted aligned-minus-null approximately `+0.03989`;
- all 29/29 eligible cancer-level median specific-coupling values positive.

This earns retention of a static orthogonal protein layer and a global RNA/protein cross-assay coupling coordinate for later predictive model competition. It does not establish causality, a pathway-specific protein mechanism, an optimum, dynamics, or chi.

See `docs/STAGE_B2_RPPA_AUDIT_20260829.md`.

## Current phase: Stage B2 genomic closure

The remaining B2 computation tests the five genomic coordinates against the frozen RNA network map.

For each eligible cancer-coordinate combination the run uses fixed `n = 30`, 100 deterministic resamples, unchanged Stage A network metrics, a same-patient permuted genomic construction null, and a separate `INCREMENT_B1` branch that asks whether the genomic coordinate contributes map information after purity and leukocyte composition are already accounted for.

The full frozen design contains 306 eligible cancer-coordinate-analysis tasks. Partial results are not interpreted.

The execution engine is restart-safe: every 100-resample task is written atomically, hash-registered, and validated before reuse. An interrupted Windows run resumes only unfinished tasks.

Current execution handoff:

- `CSA_STAGE_B2_GENOMIC_RESUMABLE_20260829.zip`
- SHA-256 `a153f54ac0d0ac5d48cb8951a5aff8e8914e0652ce73f9e1c6183e63eaf09b2a`
- clean-room manifest PASS;
- clean-room test suite 10/10 PASS.

The latest GitHub GRI v2 test workflow also passes after the Stage B2 execution code was added.

## Deferred methylation layer

The merged 27K/450K PanCanAtlas DNA-methylation matrix is approximately 5.02 GB. The 450K-only robustness matrix is approximately 41.54 GB.

Neither is casually acquired. Genome-wide methylation remains behind an independent feature-reduction/platform-harmonization gate. Its admission or deferral is not determined by whether the genomic or RPPA results look favorable.

## What comes after Stage B2

After the complete genomic run is audited, the B2 genomic and protein layers will be integrated without constructing a master stability score. The methylation extension will then be explicitly closed or carried as a separately justified static extension.

The next major branch is genuine ordered perturbation/time-course benchmarking against established dynamic and predictive baselines. Only after same-coordinate relaxation and intrinsic-response rates satisfy the admission gates may a biological chi coordinate be tested.

## Where to look

- `reviewer/README.md` - reviewer-facing navigation and evidence ladder
- `reviewer/CLAIM_EVIDENCE_MAP.md` - conservative claim-to-evidence map
- `reviewer/REVIEWER_MANIFEST.json` - machine-readable repository/stage map
- `reviewer/SUBMISSION_RELEASE_CHECKLIST.md` - immutable submission/review packaging rules
- `notes/BUILD_STATUS.md` - canonical current handoff and exact next action
- `docs/TOOL_OBJECTIVE.md` - predictive-tool objective
- `docs/EPISTEMIC_CONSTITUTION.md` - scientific guardrails
- `docs/CHI_ADMISSION_RULES.md` - conditions required before chi may be used
- `docs/STAGE_A1_AUDIT_20260829.md` - Stage A1 audit
- `docs/STAGE_B1_AUDIT_20260829.md` - Stage B1 composition/context audit
- `docs/STAGE_B2_SOURCE_AUDIT_20260829.md` - B2 source/coverage audit
- `docs/STAGE_B2_PREREGISTRATION_20260829.md` - B2 frozen integration design
- `docs/STAGE_B2_RPPA_AUDIT_20260829.md` - completed RPPA audit
- `artifacts/MILESTONE_ARTIFACTS.md` - artifact hashes and provenance

## Repository role

GitHub is the durable reproducible spine: code, configs, tests, scientific specifications, compact summaries, audits, milestone hashes, and reviewer navigation. Large raw datasets and bulky derived tables are not duplicated in repository history when they are reproducible from recorded source artifacts.
