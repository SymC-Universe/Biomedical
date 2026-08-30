# GRI v2 / Cancer Stability Atlas

**Status:** DEVELOPMENT PROGRAM, NOT A VALIDATED CANCER TOOL  
**Active phase:** Prospective substrate-extension design  
**Status date:** 2026-08-30

> **Reviewer navigation:** start at `reviewer/README.md`. The moving `gri-v2` branch is a development branch, not an immutable submission record. Manuscript/data submissions should point reviewers to an exact tagged/released snapshot following `reviewer/SUBMISSION_RELEASE_CHECKLIST.md`.

## Objective

The active objective is to build the most predictive, falsifiable cancer-stability and substrate-architecture tool supported by the data and by the updated Chemistry and Stability Arc methodology.

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
- Modal structure, scalar coordinates, and conglomeration/system organization are complementary views. A scalar may compress an empirically licensed structure but may not replace the modal carrier or integrated system architecture by assumption.

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

### Stage B2 genomic decomposition

The genomic branch is computationally closed and audited.

Completed run:

- 306/306 frozen cancer-coordinate-analysis tasks;
- 158 `PRIMARY` tasks and 148 `INCREMENT_B1` tasks;
- fixed `n = 30`;
- 100/100 valid resamples per task;
- 15,300 cancer-module summary rows;
- 1,530,000 raw module-resample rows.

The five genomic coordinates remained separate. The frozen construction null permuted only the tested genomic coordinate within the same 30 patients before residualization.

Across primary tasks, the cancer-level specific shifts are small: median approximately `-0.000481` for pairwise `C_in`, `+0.000688` for `C_in` PC1 variance fraction, and `+0.000948` for `C_out`. Comparable small shifts remain in the prespecified increment-beyond-B1 analysis.

The stronger architectural result is preservation. Across genomic coordinates, median reference-versus-adjusted 50-module rank agreement is approximately 0.993-0.997 for the two `C_in` metrics and approximately 0.984-0.988 for `C_out`. The overwhelming majority of module-level empirical 5th-to-95th resample intervals for the genomic-specific effect cross zero.

The genomic branch therefore earns retention as a weak distributed static decomposition layer. It does not support treating genomic burden as a master organizer, a master score, or a biological chi coordinate.

See `docs/STAGE_B2_GENOMIC_AUDIT_20260830.md`.

### Stage B2 static multiomic integration

The closed component results have now been integrated without fitting a master score.

The supported static architecture contains:

- RNA variability/lineage and Hallmark organization;
- composition/context decomposition;
- separate genomic burden/decomposition axes;
- orthogonal protein/phosphoprotein coupling;
- genome-wide methylation only as a separately prospectively gated extension.

The current cross-layer conclusion is architectural rather than scalar: the Hallmark RNA organization is only partly explained by measured composition and the admitted genomic burden coordinates while carrying detectable patient-aligned information into an independently measured protein/phosphoprotein layer.

This remains cross-sectional and non-causal. It does not establish substrate inheritance.

See `docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md`.

## Current phase: prospective substrate-extension design

The next investigation must be specified before new association, predictive, or dynamic endpoints are inspected.

The next architecture will explicitly preserve:

1. **modal structure**: mode-resolved/eigenstructure and participation information;
2. **scalar coordinates**: compressed summaries only where empirically licensed;
3. **conglomeration**: module-to-module and whole-system organization across measurement layers.

These three views are complementary rather than competing definitions of the state.

Genome-wide methylation remains deferred rather than rejected. The merged PanCanAtlas 27K/450K source is approximately 5.02 GB and uses a preprocessed common-probe representation. A separate prospective feature-reduction/platform-handling specification must be frozen before that source is acquired for association testing.

## What comes next

1. freeze the methylation extension specification or explicitly close the extension without inspecting methylation associations;
2. freeze the next modal + scalar + conglomeration protocol before testing any new endpoint;
3. build and test the corresponding execution machinery and construction nulls;
4. only then acquire/run the next required dataset;
5. advance to genuine ordered perturbation/time-course benchmarking against established dynamic and predictive baselines;
6. test biological chi only if same-coordinate relaxation and intrinsic-response rates satisfy the admission rules.

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
- `docs/STAGE_B2_GENOMIC_AUDIT_20260830.md` - completed genomic audit
- `docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md` - closed B2 multiomic architecture
- `artifacts/MILESTONE_ARTIFACTS.md` - artifact hashes and provenance

## Repository role

GitHub is the durable reproducible spine: code, configs, tests, scientific specifications, compact summaries, audits, milestone hashes, and reviewer navigation. Large raw datasets and bulky derived tables are not duplicated in repository history when they are reproducible from recorded source artifacts.
