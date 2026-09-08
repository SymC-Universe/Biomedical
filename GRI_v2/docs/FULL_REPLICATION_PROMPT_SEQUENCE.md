# GRI v2 Full Scientific Replication Prompt Sequence

**Repository:** `SymC-Universe/Biomedical`  
**Active branch:** `gri-v2`  
**Purpose:** preserve the full substantive scientific/computational sequence that led from the historical GRI manuscript to the current frozen static methylation-transcriptomic architecture paper, while excluding mechanical execution failures that do not need to be repeated.

## 0. Read this first

This document is a **reconstruction/reproducibility guide**, not a new scientific freeze and not a replacement for the machine-readable configs, code, audits, or immutable result packages.

### Prompt fidelity

- The approval prompts explicitly marked **EXACT** are preserved verbatim because those approvals changed the scientific contract.
- The other prompt blocks are **canonical full replication prompts** reconstructed from the frozen repository documents, result packages, and project history. They preserve the actual scientific sequence, frozen rules, nulls, thresholds, claim ceilings, failures, and outputs, but they are not presented as byte-for-byte transcripts of historical chat messages.
- Mechanical failures that did not alter science are intentionally omitted. Examples: Windows batch quoting failures, stale launchers, file-picker problems, interrupted runs, Python process termination, checkpoint path bugs, logging gaps, and packaging retries.
- Scientific failures, construction failures, pre-result specification corrections, refusal states, null results, amendments, and outliers are retained because they materially define the evidence.

### Governing principle

The replication target is **the science, not the historical narrative**.

The standing order is:

`observation -> legitimate mathematics -> prospective computation -> adversarial comparison -> bounded interpretation`

not:

`historical claim -> search for confirming evidence`.

---

# 1. Standing invariants for every prompt

These rules apply throughout the sequence.

1. Historical `CV/2` is provenance only. It is never promoted to biological `chi`, damping, or a stability coordinate.
2. No biological `chi` coordinate is admitted unless its own governing model, dimensional construction, calibration, uncertainty, and prospective admission gates justify that name.
3. `chi = 1` is not a universal cancer optimum, healthy state, treatment target, or organization maximum.
4. Preserve three complementary views:
   - **scalar:** compressed coordinates/invariants;
   - **modal/vector:** mode-resolved carrier structure;
   - **conglomeration:** network/module/cross-layer/system organization.
5. Do not collapse the three views into a master score by convenience.
6. Static cross-sectional structure is a landscape/state map. It is not temporal progression, damping, recovery, hysteresis, exceptional-point motion, or substrate inheritance.
7. All biological rules, thresholds, nulls, missingness policies, masks, feature definitions, multiplicity families, and promotion rules must be frozen before the biological result they govern is inspected.
8. Mechanical repairs may preserve and resume a frozen scientific computation. Any scientific-rule change requires an explicit new version and may not retroactively replace the prior contract.
9. Failed, null, refused, and deferred branches remain visible.
10. Every `x/y cancers` statement must identify:
    - the exceptions or denominator exclusions;
    - effect magnitude;
    - technical-track consistency;
    - support/valid-resample count;
    - the strongest evidence-based explanation or hypothesis;
    - a falsification path where possible.
11. Third-party source datasets are not redistributed unless licensing explicitly allows it. Researchers obtain TCGA/MSigDB/GDC sources themselves. Reproducibility is preserved by source identifiers, acquisition instructions, filenames, hashes, transforms, code, configs, seeds, and expected outputs.
12. The paper may succeed without `chi`, damping, substrate inheritance, or any historical GRI mechanism.

Canonical governance documents:

- `GRI_v2/docs/EPISTEMIC_CONSTITUTION.md`
- `GRI_v2/docs/CHI_SCALAR_MODAL_CONGLOMERATION_FIREWALL_20260830.md`
- `GRI_v2/docs/CHI_ADMISSION_RULES.md`
- `GRI_v2/docs/GRI_V2_TOOL_DISCOVERY_CHARTER_20260830.md`
- `GRI_v2/WORKFLOW.md`

---

# 2. Frozen source identities used on the current paper path

A reproducer should acquire the authorized source files and verify these identities before proceeding.

## PanCanAtlas RNA

- Source: PanCanAtlas EB++ batch-adjusted RSEM expression matrix.
- Historical source identity recorded by the Stage A audit: SHA-256 `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`.
- Frozen Stage A profile cache used downstream: SHA-256 `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`.

## MSigDB Hallmarks

- Library: MSigDB Hallmark `v2026.1.Hs`.
- Raw GMT used by completed C1: SHA-256 `eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596`.
- Deterministic processed membership snapshot: SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`.
- The researcher should download the Hallmark data from the authorized MSigDB source under its terms. Do not redistribute it as though it were project-owned data.

## PanCanAtlas methylation

- File: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`
- GDC UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`
- Size: `5,022,150,019` bytes
- MD5: `5cec086f0b002d17befef76a3241e73b`
- SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- Probe rows: `22,601`

## B1 composition covariates

- ABSOLUTE purity SHA-256: `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`
- methylation-derived leukocyte fraction SHA-256: `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`

## C1A annotation products

- probe-gene-region map SHA-256: `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`
- probe flags SHA-256: `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`

## Frozen Stage C1 contract

- approved scientific-contract blob SHA-1: `a39414c5990c234dc513569bd405b0237117d434`
- final completed implementation version after approved amendments: `stage-c1-frozen-v2-exec-20260906.3`

---

# 3. Full substantive prompt sequence

Run the following in order for a clean scientific reconstruction. Parallel/adjacent branches that informed the broader program but are not required to regenerate the current manuscript are marked accordingly.

---

## PROMPT 00 - Establish the truth-first reconstruction posture

**Role in sequence:** program reset before any new biological computation.

```text
We are rebuilding the GRI oncology work from the evidence upward. Do not defend the historical manuscript, preserve its conclusions, or assume its variables are valid because they appeared in the prior paper.

Treat the historical manuscript, supplement, figures, code, and prior outputs as provenance and hypothesis-generating material only.

Create a truth-first reconstruction protocol with these permanent rules:

1. Historical CV/2 remains CV/2 only. Do not call it biological chi, damping, dissipation, or a stability coordinate.
2. Do not assume mean expression is frequency/energy, expression SD is damping, chi=1 is a cancer optimum, gene rank is time, or static cross-sectional structure is a trajectory.
3. Keep scalar, modal/vector, and conglomeration/system-level measurements distinct but complementary. Do not average them into a master score.
4. Any new biological quantity must retain the interpretation earned by its construction.
5. Dynamics, damping, recovery, hysteresis, transition direction, exceptional points, and substrate inheritance require genuine ordered temporal or perturbational evidence.
6. Freeze every scientific rule before inspecting the biological result governed by that rule.
7. Preserve failures, nulls, refusals, amendments, and unexpected subgroup behavior.
8. A final useful method is allowed to contain no chi, no damping language, and no historical GRI terminology.
9. Publication is downstream of validation. The manuscript may not steer thresholds, features, nulls, or interpretation.

Output:
- an epistemic constitution;
- a chi-admission rule set;
- a scalar/modal/conglomeration firewall;
- a failure-retention policy;
- a landscape-versus-trajectory firewall;
- a statement that the theory must be able to lose.

Do not run biological association tests in this step.
```

**Expected repository anchors:**
`EPISTEMIC_CONSTITUTION.md`, `CHI_ADMISSION_RULES.md`, `CHI_SCALAR_MODAL_CONGLOMERATION_FIREWALL_20260830.md`.

---

## PROMPT 01 - Forensic audit of the historical GRI manuscript

**Role in sequence:** identify what can and cannot survive into the new program.

```text
Audit the historical GRI manuscript, supplement, figures, and code as an adversarial reviewer.

For every major claim, equation, figure axis, variable, biological interpretation, therapeutic statement, and temporal/mechanistic statement:

- identify the exact data and computation that support it;
- classify it as directly supported, descriptive only, hypothesis only, unsupported, circular, dimensionally unjustified, or contradicted by the actual computation;
- identify whether the claim depends on CV/2 being renamed as chi;
- identify whether mean expression was treated as a physical frequency/energy coordinate without derivation;
- identify whether SD was treated as damping/dissipation without a dynamical model;
- identify whether gene rank or cohort ordering was interpreted as time;
- identify whether any static TCGA analysis was promoted to damping, recovery, hysteresis, phase transition, exceptional-point crossing, substrate capture/inheritance, treatment response, or clinical utility;
- identify figures whose labels make claims stronger than the revised text;
- preserve observations that remain legitimate even if the historical mechanism fails.

Build a failure ledger. Do not repair claims by changing terminology alone. If a historical mechanism is not earned, close it rather than searching for a favorable substitute.

The output should explicitly separate:
1. observations worth carrying forward;
2. measurements worth rebuilding;
3. mechanisms that failed;
4. therapeutic claims that must be removed;
5. new questions that can be tested prospectively.
```

**Substantive historical failures carried forward:**
- `CV/2` could not support the claimed damping/chi interpretation;
- historical energy/frequency semantics were not provenance-resolved;
- static rank was not time;
- old figure labels such as “Critical Failure” / “Forensic Capture” overclaimed;
- causal substrate capture, exceptional-point treatment logic, and therapeutic rules were not established by cross-sectional RNA.

---

## PROMPT 02 - Build the clean Stage A RNA representation

**Role in sequence:** construct a reusable static RNA source layer independent of historical GRI feature selection.

```text
Using the authorized PanCanAtlas EB++ batch-adjusted RSEM expression matrix, build a clean Stage A RNA representation for unique-patient primary tumors across cancers.

Rules:

- use primary tumors only and one unique patient representation;
- preserve source non-finite expression as missing; never convert source missing values to zero expression;
- for finite expression values use log2(max(expression,0)+1);
- use the externally defined MSigDB Hallmark v2026.1.Hs collection, not historical GRI gene modules, as the primary compact biological module library;
- require exactly 50 Hallmark modules in the acquired library;
- preserve the exact Hallmark-union gene ordering used by downstream code;
- record participant/sample identity and cancer type explicitly;
- build and hash a reusable profile cache containing the transformed Hallmark-union expression representation;
- do not compute or use biological chi, CV/2, a master stability score, damping, an optimum, or temporal progression;
- preserve all source filenames, source hashes, transformations, and eligibility rules.

The output should be suitable for Stage A1 network analysis, B1 composition analysis, B2 cross-assay work, and later C1 methylation/RNA comparison without rereading or redefining the source layer.
```

**Frozen downstream cache identity:** `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`.

---

## PROMPT 03 - Freeze and run Stage A1 static Hallmark network mapping

```text
Freeze a Stage A1 static Hallmark network analysis before inspecting network point estimates.

Use the frozen PanCan RNA profile representation and the exact Hallmark membership snapshot.

For every eligible cancer and Hallmark module:

1. Gene eligibility:
   - >=95% finite within cancer;
   - >=20 finite samples;
   - nonzero finite variance.

2. C_in pairwise:
   - exact Pearson correlations using pairwise finite overlap;
   - require >=80% of cancer samples and >=20 overlapping samples;
   - summarize internal module coherence as the median absolute Pearson correlation among eligible mapped module genes.

3. C_in PC1:
   - z-score finite cells within each gene;
   - standardized missing cells may be set to zero only for SVD/eigengene construction, where zero is the within-gene standardized mean;
   - compute the fraction of standardized module variance explained by PC1;
   - orient PC1 so its correlation with the per-sample mean standardized module expression is nonnegative.

4. C_out:
   - correlate the complete oriented Hallmark eigengene with eligible genes outside that module but inside the same frozen Hallmark-union background;
   - use the same finite-overlap rule;
   - summarize as median absolute Pearson correlation.

5. Require at least 15 mapped genes per Hallmark.
6. Require at least 30 samples per cancer.
7. Run deterministic five-fold patient-hash leave-one-fold-out stability as an uncertainty diagnostic, not a promotion p-value.
8. Do not use chi, CV/2, a composite stability score, historical GRI modules, or an optimum direction.
9. Report C_in and C_out as separate static coordinates.
10. Explicitly test whether cross-cancer raw magnitudes are associated with cohort size before interpreting between-cancer differences.

Output the full module map, uncertainty diagnostics, source/cache hashes, and an audit with a strict static claim ceiling.
```

**Scientific failure retained:** raw absolute-correlation magnitudes showed finite-sample dependence across cancer cohort sizes. This was not ignored or normalized away post hoc.

---

## PROMPT 04 - Stage A1 construction-bias audit

```text
Audit Stage A1 before biological cross-cancer interpretation.

Verify:
- 32 cancer types;
- 50 Hallmarks per cancer;
- source/cache identity;
- missingness policy;
- leave-one-fold-out reproducibility;
- within-cancer relationships among C_in pairwise, C_in PC1, and C_out;
- whether raw cross-cancer magnitudes depend on original cohort size.

If cohort size materially affects absolute-correlation coordinates, do not interpret raw between-cancer magnitude biologically. Instead design a prospective fixed-n calibration that preserves the metric definitions and removes only the sample-size construction artifact.

Do not choose a calibration n from whichever value produces the most favorable biological pattern. Choose a common n that all 32 cancers can support and freeze it before calibration results are inspected.
```

**Observed reason for next stage:** raw n-associations were non-negligible, so Stage A1.1 was required.

---

## PROMPT 05 - Freeze and run Stage A1.1 fixed-n calibration

```text
Freeze the Stage A1.1 construction calibration before inspecting calibrated results.

Purpose: remove finite-sample-size distortion from cross-cancer comparison without changing any Stage A1 network metric.

Rules:
- cancers: all 32 Stage A cancers;
- fixed n = 30;
- 100 deterministic without-replacement resamples per cancer;
- global seed = 20260829;
- sorted cancer types receive deterministic per-cancer seeds drawn once from NumPy default_rng(global_seed), so scheduling order cannot alter the samples;
- recompute unchanged C_in pairwise, C_in PC1, and C_out metrics for all 50 Hallmarks in every resample;
- retain 5th/50th/95th resampling summaries as uncertainty, not p-values;
- do not redefine Stage A1 metrics;
- do not use chi, CV/2, a composite score, or a historical-GRI recovery test.

Audit whether the association between original cancer cohort size and calibrated cancer-level magnitudes collapses toward zero while within-cancer module ordering is preserved.

Close Stage A as a sample-size-calibrated static network map only if the construction artifact is removed without destroying the topology.
```

**Expected closed result:** 32 cancers x 50 Hallmarks x 100 resamples, sample-size association near zero after fixed-n calibration, strong preservation of module ordering.

---

## PROMPT 06 - Freeze Stage B1 composition/context attack

```text
Before testing composition effects, freeze a Stage B1 context-adjustment analysis that asks whether the Stage A Hallmark network map is materially attributable to independently measured tumor purity or leukocyte composition.

Use:
- frozen Stage A profile cache;
- frozen Hallmark membership;
- ABSOLUTE purity source with its exact hash;
- methylation-derived leukocyte fraction with its exact hash.

Matching rules:
- primary tumor sample type 01 only;
- ABSOLUTE must be called and finite;
- primary key is TCGA sample root through vial;
- patient fallback only when exactly one eligible primary measurement exists;
- no recurrent-tumor substitution;
- duplicate leukocyte measurements at the same sample root may be median-collapsed before matching as already specified.

Models:
1. PURITY;
2. LEUKOCYTE;
3. JOINT_INDEPENDENT using purity + leukocyte together.

For every eligible cancer/model:
- fixed n=30;
- 100 deterministic paired resamples;
- on the exact same 30 patients compute baseline Stage A metrics, actual residualized metrics, and a permuted-context residualization null;
- residualize within cancer/resample by OLS after centering/scaling finite covariates for numerical conditioning;
- preserve missing expression as missing;
- mark rank-deficient resamples invalid rather than altering the model;
- keep Stage A network definitions unchanged.

Construction null:
- single-covariate model: permute the covariate across the 30 patients;
- joint model: permute the two-column purity/leukocyte matrix jointly by row to preserve their internal relationship while breaking association to RNA.

Primary context-specific effect = actual-adjusted minus permuted-null-adjusted, so generic changes from fitting/residualization are not mistaken for biological context effects.

Do not define any direction as healthier, more stable, optimal, or closer to chi. Retain both adjusted and unadjusted coordinates.
```

---

## PROMPT 07 - Audit and close Stage B1

```text
Audit the completed Stage B1 context experiment without changing the frozen design.

For each model, report:
- valid task/resample counts;
- baseline-vs-adjusted Hallmark rank preservation for C_in pairwise, C_in PC1, and C_out;
- context-specific effect magnitudes relative to baseline;
- whether the inverse C_in/C_out topology survives adjustment;
- which Hallmarks carry the strongest reproducible composition sensitivity;
- which cancers are unavailable for a model and why.

Do not describe composition as negligible if immune/inflammatory modules move materially. Do not describe composition as explaining the whole network if the broad module ordering/topology remains strongly preserved.

Retain the bounded conclusion: composition explains a real but concentrated sector of the RNA network geometry, especially immune/inflammatory Hallmarks, while broader topology persists.

Record both the result and the limitations for use as a mandatory composition attack in downstream C1.
```

**Closed B1 finding:** broad topology remained, while immune/inflammatory programs were strongly composition-sensitive.

---

# 4. Parallel program branch: B2 orthogonal multiomic decomposition

The following B2 prompts are part of the scientific sequence and helped establish that multiple molecular layers should remain distinct. They are not required to regenerate the current methylation/RNA C1 manuscript, but they belong in the program lineage.

## PROMPT 08 - Freeze Stage B2 source inventory and integration design

```text
Reserve independent multiomic sources before looking at their biological association with Stage A.

Freeze a Stage B2 integration plan that keeps each source and coordinate separate.

Include:
- an RPPA protein/phosphoprotein branch;
- separately documented genomic coordinates for aneuploidy, LOH, and SCNA burden;
- the frozen Stage A RNA map;
- the frozen B1 composition covariates;
- fixed n=30 resampling where applicable;
- construction-aware patient-permutation or covariate-permutation nulls;
- no master genomic burden score;
- no chi, damping, optimum, causal substrate, or temporal claim.

Do not admit a source because it agrees with Stage A. Source choice and rules must be fixed before biological association.
```

---

## PROMPT 09 - Run/audit Stage B2 RPPA

```text
Run the preregistered RPPA branch to ask whether Hallmark RNA state is patient-aligned with an independently measured protein/phosphoprotein panel beyond a row-permutation construction floor.

Use the frozen common-panel rule: retain RPPA measurements with >=95% finite values across matched primary samples and nonzero finite variance before biological association.

For each eligible cancer:
- fixed n=30;
- 100 deterministic resamples;
- for each Hallmark RNA eigengene, compute the median absolute Pearson correlation across the frozen RPPA panel;
- null = permute RPPA patient rows as a block relative to RNA, preserving protein covariance while breaking patient identity;
- repeat after prespecified purity/leukocyte projection where coverage permits.

Do not interpret stronger coupling as better/worse/stable. Report cancers absent from raw or adjusted branches and why. Preserve context-sensitive cancers rather than correcting them away.

Close only as a static cross-assay coupling layer if patient-aligned coupling exceeds its construction floor reproducibly.
```

**Retained outcome:** broad RNA/RPPA patient-aligned coupling above row-permutation floor; composition did not erase the global effect but changed module ordering in some cancers.

---

## PROMPT 10 - Run/audit Stage B2 genomic decomposition

```text
Run the preregistered genomic branch with the five documented genomic coordinates kept separate:
- ANEUPLOIDY_AS;
- LOH_SEGMENT_COUNT;
- LOH_GENOME_FRACTION;
- SCNA_SEGMENT_COUNT;
- SCNA_ALTERED_FRACTION.

Do not create a genomic master score.

For each eligible cancer-coordinate task:
- fixed n=30;
- 100 deterministic resamples;
- residualize the Stage A RNA representation on the real genomic coordinate;
- create a same-patient permuted-genomic residualization null;
- primary specific effect = actual-genomic-adjusted minus permuted-genomic-null-adjusted;
- separately test incremental genomic effect after preserving Stage B1 purity/leukocyte adjustment where coverage permits;
- keep C_in pairwise, C_in PC1, and C_out separate;
- report module-order preservation and effect magnitude;
- do not introduce a post-result significance threshold.

A weak distributed effect is a valid result. Do not promote small recurrent effects into a causal genomic-substrate claim.
```

**Scientific result retained:** small distributed genomic effects with overwhelming preservation of Stage A topology. This was evidence against collapsing the static architecture into a single genomic master variable.

---

# 5. Tool-feasibility branch before full C1 execution

This branch tested whether the general architecture had enough value to justify a standalone integration-readiness tool. It did not modify the already frozen Stage C1 scientific contract.

## PROMPT 11 - Lock the tool-discovery charter (F0)

```text
Lock the GRI v2 program objective as tool discovery rather than historical-manuscript defense.

The candidate tool should answer:
- is each layer organized beyond a construction-aware null?
- do matched layers share patient geometry?
- is the sharing biologically/semantically specific or merely global?
- how much apparent sharing survives measured-confounder and technical attacks?
- what modes/features carry the result?
- when should the method refuse cross-layer integration?

Keep modal, scalar, and conglomeration views complementary.

Define explicit methodological states such as:
- NO_SHARED_STRUCTURE;
- WITHIN_LAYER_ONLY;
- GLOBAL_SHARED_ONLY;
- SEMANTIC_SHARED_CONFOUNDED;
- SEMANTIC_SHARED_ROBUST.

No biological chi is admitted. Stage C1 remains frozen and unread during feasibility work.
```

---

## PROMPT 12 - Build the assay-agnostic F1 mathematical kernel

```text
Implement and regression-test assay-agnostic primitives for the candidate cross-omic architecture auditor.

Required primitives:
- marginal-preserving within-layer organization tests;
- eigenspectrum/effective-rank/participation diagnostics;
- mode-to-feature contribution tracing;
- linear CKA;
- principal-angle comparisons;
- patient-row permutation nulls;
- semantic/module-label permutation nulls;
- covariate projection;
- same-module coupling;
- cross-validated modal predictability;
- provisional conditional-dependence/regulatory-autonomy quantities;
- explicit refusal outputs.

Use only synthetic or separate benchmark inputs. Do not read C1 beta-value biological results. The functions must be deterministic under fixed seeds and must preserve the scalar/modal/conglomeration firewalls.
```

---

## PROMPT 13 - F2 synthetic ground-truth challenge

```text
Challenge the F1 kernel against a frozen synthetic scenario family before using it as a biological tool.

The test suite must include:
1. independent layers with similar-looking marginals;
2. one genuine shared mode;
3. several shared plus layer-specific modes;
4. false sharing generated by a common confounder;
5. shared global geometry with scrambled biological labels;
6. module-specific sharing with weak global alignment;
7. technical outliers manufacturing false concordance;
8. unequal feature counts and missingness;
9. nonlinear-only sharing that the initial linear method should under-detect or refuse rather than overclaim;
10. high apparent coupling with preserved regulatory autonomy;
11. high apparent coupling with low autonomy from a substrate-conditioned shared driver;
12. confounded apparent autonomy loss that should disappear after correct covariate control.

Score mandatory safety behavior separately from raw sensitivity. A method that confidently misclassifies confounding or nonlinear out-of-scope behavior should fail or be narrowed.

Do not alter Stage C1 from the F2 result.
```

**Scientific failure retained:** the nonlinear-only scenario was outside validated scope and was explicitly excluded rather than repaired into success.

---

## PROMPT 14 - F3 baseline competition

```text
Compare the retained F2 capabilities with strong simple baselines and established multiview/integration approaches.

The goal is not to beat every established method at generic data fusion. The candidate must earn a useful role in at least one of:
- construction-aware refusal;
- confounder attack;
- technical attack;
- semantic-specificity decomposition;
- modal traceability;
- calibrated integration-readiness decisions.

If a candidate scalar such as regulatory autonomy is redundant with simpler established quantities, narrow or remove it rather than preserving it for narrative reasons.

Keep all failed comparisons and unavailable benchmark implementations visible.
```

---

## PROMPT 15 - F4 decision

```text
Make a pre-C1 engineering decision from F2/F3 using only GO, NARROW, or STOP.

Do not inspect C1 biological results to make this choice.

Use these rules:
- GO only if the complete architecture adds defensible utility;
- NARROW if only specific components add value;
- STOP if a standalone tool is not justified.

Component-level decisions must be explicit. Keep established primitives without novelty claims, preserve useful guardrails, and remove/reject redundant or failed components.
```

**Actual decision:** `F4_NARROW`.

Retained:
- global geometry as an established primitive, no novelty claim;
- confounder and technical attack tracks;
- semantic-specificity testing;
- modal shared/private traceability;
- integrated refusal architecture for prospective testing.

Narrowed/failed:
- regulatory-autonomy scalar judged redundant;
- nonlinear-only scope excluded.

---

# 6. Predictive P0 branch (scientifically substantive, not required for the current C1 paper)

This sequence explored leakage-controlled predictive use of methylation-to-RNA architecture. It is included because it materially shaped the program and preserved a major negative result: broad geometry replicated much better than Hallmark-label specificity.

## PROMPT 16 - Freeze P0 partitions before eligibility and targets

```text
Freeze a deterministic participant split before opening predictive targets:
- DISCOVERY;
- REPLICATION;
- FINAL_HOLDOUT.

Use the exact one-to-one matched methylation/RNA participant universe. Partition assignment must be deterministic and immutable. Do not rebalance cancers after seeing eligibility or performance.

Freeze a minimum pan-cancer promotion floor before results. Do not lower it later because too few cancers qualify.

No target value may influence partition assignment or sample eligibility.
```

---

## PROMPT 17 - P0 eligibility audit

```text
Using the frozen P0 split and exact primary methylation source, compute only per-sample source eligibility.

Rule:
- a sample is methylation-eligible only if at least 95% of exactly 22,601 PRIMARY_PUBLICATION probes are finite;
- do not read RNA predictive targets;
- do not perform biological association;
- do not reassign partitions;
- preserve every ineligible sample as a QC outcome with cancer, participant, partition, and finite-probe count.

Determine which cancers have at least 30 eligible participants independently in DISCOVERY, REPLICATION, and FINAL_HOLDOUT. Keep the already-frozen pan-cancer promotion floor unchanged even if fewer cancers qualify.
```

**Retained failure/limitation:** only 19 cancers were fully P0-evaluable, below the frozen 24-cancer pan-cancer promotion floor. The floor was not relaxed.

---

## PROMPT 18 - P0 D1 DISCOVERY-only methylation preprocessing

```text
Using DISCOVERY participants only, freeze and compute the source-side methylation transforms for the 19 fully evaluable cancers.

Do not read REPLICATION or FINAL_HOLDOUT methylation values. Do not read RNA targets.

Per cancer:
- retain probes with >=95% finite DISCOVERY values;
- freeze each retained probe's DISCOVERY finite-sample median for later projection/imputation;
- construct PRIMARY_PUBLICATION and fixed MASKED_TECHNICAL tracks;
- preserve the fixed 579-probe technical mask;
- construct TSS200/PROMOTER_CORE gene scores from the frozen annotation map;
- require Hallmark source mapping >=10 mapped genes and >=10 contributing probes;
- fit methylation Hallmark PC1 transforms using DISCOVERY only;
- orient PC1 by nonnegative correlation with the DISCOVERY module mean;
- persist all transform parameters needed for untouched later projection.

Do not rescue source-limited Hallmarks after seeing results.
```

**Retained refusal:** five Hallmarks failed the source mapping floor in every cancer/track and remained refused:
ANGIOGENESIS, HEDGEHOG_SIGNALING, NOTCH_SIGNALING, REACTIVE_OXYGEN_SPECIES_PATHWAY, WNT_BETA_CATENIN_SIGNALING.

---

## PROMPT 19 - P0 D2 DISCOVERY-only RNA target construction

```text
Construct the RNA predictive targets using DISCOVERY only.

Use the frozen Stage A expression representation and Hallmark library. For each cancer/Hallmark:
- apply the frozen RNA gene-eligibility rules;
- fit the RNA Hallmark PC1 transform in DISCOVERY only;
- orient PC1 by nonnegative correlation with the DISCOVERY module mean;
- persist means/loadings/reference statistics for later untouched projection;
- do not generate REPLICATION or FINAL_HOLDOUT target scores;
- compute common Hallmark eligibility as source-eligible AND RNA-evaluable;
- keep the five methylation-source-limited Hallmarks refused even though their RNA targets are evaluable.

Audit all participant identities, transform dimensions, loading norms, centering, and leakage guards before opening the model/audit gate.
```

---

## PROMPT 20 - P0 D3 DISCOVERY audit state and model fitting

```text
Before computing real D3 cross-layer results, freeze:
- global CKA effect floor and permutation count;
- semantic same-Hallmark patient-alignment test;
- Hallmark-label specificity effect floor;
- composition attack;
- technical-track agreement logic;
- discovery decision states/refusal rules;
- ridge-model feature set, alpha grid, CV folds, and comparator models.

Use DISCOVERY only.

Compute:
1. within-layer construction-aware organization;
2. raw global cross-layer CKA and patient-permutation null;
3. composition-adjusted global CKA;
4. same-Hallmark patient-aligned coupling;
5. independent Hallmark-label specificity;
6. technical-track agreement;
7. discovery state and decision class;
8. discovery-only predictive model fitting with deterministic CV.

Persist every transform, composition-projection parameter, target reference, model coefficient, selected hyperparameter, null, and seed required for untouched REPLICATION.

Do not lower semantic thresholds if global geometry passes but Hallmark-label specificity fails.
```

**Scientific result retained:** all 19 cancers passed robust global geometry, but zero passed the frozen full Hallmark-label-specific semantic rule. All 19 therefore remained `GLOBAL_SHARED_ONLY / CAUTION` rather than being promoted.

---

## PROMPT 21 - P0 D4 untouched REPLICATION

```text
Project the already-frozen D1/D2 transforms and D3 model parameters into REPLICATION without refitting.

FINAL_HOLDOUT remains sealed.

Reconstruct and audit:
- replication methylation scores;
- replication RNA scores;
- raw and composition-adjusted global geometry;
- same-Hallmark patient coupling;
- Hallmark-label specificity;
- frozen five-state decision;
- model prediction metrics using discovery-frozen target references;
- comparison against the frozen composition-only baseline.

Do not change thresholds, states, features, transforms, alpha choices, covariate rules, or partition membership in response to replication.

If one cancer disagrees, identify it by name and determine whether the failure is within-layer organization, global geometry, semantic specificity, composition support, technical robustness, or prediction.
```

**Retained result/failure:** 18/19 state agreement. PCPG shifted from `GLOBAL_SHARED_ONLY/CAUTION` to `WITHIN_LAYER_ONLY/REFUSE` and was also the lone cancer where the all-methylation model underperformed the composition-only model. No cancer satisfied full semantic-specificity promotion. This failure was retained.

---

# 7. Methylation C0/C0.1/C1A source-and-identity gates

These are required for the current paper path.

## PROMPT 22 - C0 methylation source audit before biology

```text
Audit the exact PanCanAtlas merged HM27/HM450 methylation source before reading beta values for biological association.

Limit this stage strictly to:
- source identity;
- remote/local size and hash verification;
- schema/header inventory;
- exact probe inventory;
- primary-tumor sample coverage;
- Stage A sample-root/patient coverage.

Expected source:
- file jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv;
- GDC UUID d82e2c44-89eb-43d9-b6d3-712732bf6a53;
- size 5,022,150,019 bytes;
- MD5 5cec086f0b002d17befef76a3241e73b;
- SHA-256 5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77;
- 22,601 unique probes.

Do not inspect beta-value associations, select samples by methylation values, or test methylation/RNA coupling.

If duplicate primary sample roots are discovered, stop before biology and freeze a separate sample-identity rule rather than choosing or averaging replicates from their values.
```

**Retained source-schema issue:** 41 duplicated primary sample roots required the separate C0.1 gate.

---

## PROMPT 23 - C0.1 one-to-one sample identity

```text
Resolve Stage A-to-methylation sample identity prospectively without reading methylation beta-value rows for biological analysis.

Primary rule:
- admit a Stage A tumor only when exactly one eligible primary methylation source column maps to the exact TCGA sample root through vial;
- allow patient-level fallback only when the source contains exactly one eligible primary measurement for that patient;
- if a Stage A sample root has multiple methylation columns, exclude it from primary C1;
- do not average duplicates;
- do not select by platform, order, completeness, or beta values;
- do not rescue samples to increase cancer coverage.

Report:
- exact unique-root matches;
- patient-fallback matches;
- duplicate-root exclusions;
- no-source samples;
- per-cancer retained n;
- whether all 32 cancers remain >=30.

No biological association, chi, substrate-inheritance, or composite-score analysis is allowed in this stage.
```

**Closed result:** 9,460 one-to-one matched Stage A tumors; 34 duplicate-root Stage A samples excluded; 52 with no eligible source match; all 32 cancers remained above n=30.

---

## PROMPT 24 - C1A freeze and exact-probe annotation inventory

```text
Before any methylation beta-value biological analysis, freeze the exact annotation, mapping, regulatory-stratum, and technical-mask rules.

Requirements:
- exact annotation coverage for all 22,601 source probes;
- preserve exact probe-gene-accession-region tuples;
- do not invent nearest genes for unmapped probes;
- retain annotation-supported multi-gene mapping;
- define PROMOTER_CORE as TSS200 primary;
- preserve secondary strata only as context/decomposition;
- build a prespecified technical-mask robustness track independently of biological results;
- primary publication-faithful track remains all exact source probes;
- masked robustness track removes the fixed technical-mask union only;
- beta values must not be parsed for biological association during this gate.

Audit exact source-probe overlap, tuple integrity, stratum counts, unmapped-probe handling, and technical-mask overlap. Fail the gate if source/annotation identity or mapping integrity is inconsistent.
```

**Closed C1A identities:**
- exact annotation overlap 22,601/22,601;
- PROMOTER_CORE/TSS200 3,999 probes;
- technical-mask union 579 probes;
- masked track 22,022 probes;
- 132 unmapped probes retained in all-probe modal space but not assigned invented genes/Hallmarks.

---

# 8. Frozen Stage C1 scientific contract

## PROMPT 25 - Draft and freeze C1 v2 before biological results

```text
Design the complete Stage C1 methylation/RNA architecture test now, before any C1 beta-value biological result is inspected.

Freeze all of the following together:

INPUTS AND ELIGIBILITY
1. shared sample eligibility derived once from the PRIMARY_PUBLICATION 22,601-probe track and inherited unchanged by MASKED_TECHNICAL;
2. publication-era beta scale; no M-value discovery branch;
3. 95% sample completeness;
4. 95% probe completeness;
5. within-cancer probe-median imputation only after eligibility;
6. fixed n=30;
7. 100 deterministic without-replacement resamples per cancer;
8. cancer, not resample, is the inferential unit;
9. seed namespace GRI_V2_C1_20260830 with SHA-256-derived deterministic seeds.

MODAL / SCALAR METHYLATION ARCHITECTURE
10. center probe columns without variance scaling;
11. construct the all-probe patient Gram matrix G = X X^T / p;
12. retain the complete 29-position normalized eigenspectrum for n=30 plus top-five mode contributions;
13. define primary scalar S_spec = 1 - H_norm;
14. define S_PR = 1 - r_PR/29 as secondary only;
15. explicitly state neither scalar is biological chi;
16. H1 null = independently permute each probe column within the same draw, preserving probe marginals while destroying patient-aligned covariance.

FULL-MODAL CROSS-LAYER BRIDGE
17. use the exact frozen RNA feature ordering on the same patients;
18. compute linear centered-kernel alignment between methylation and RNA patient geometries;
19. H2 null = deterministic RNA-patient permutation relative to methylation;
20. retain top-five principal-angle diagnostics as a modal cross-check.

CONGLOMERATION / HALLMARK BRANCH
21. primary regulatory stratum = PROMOTER_CORE/TSS200;
22. unique-probe median gene methylation aggregation;
23. preserve annotation-supported multi-gene mapping;
24. no nearest-gene invention;
25. methylation Hallmark PC1 with deterministic orientation;
26. minimum 10 mapped genes and minimum 10 contributing probes;
27. minimum 25 evaluable common Hallmarks for primary conglomeration resample;
28. RNA Hallmark PC1 uses the already-frozen Stage A missingness/eligibility rules;
29. same-Hallmark statistic = median absolute Spearman correlation between matched methylation and RNA Hallmark PC1 scores;
30. H3a null = patient permutation, asking whether the same patients carry corresponding pathway states;
31. H3b null = Hallmark-label permutation, asking whether matching biological labels add specificity beyond generic cross-layer state.

COMPOSITION AND TECHNICAL ROBUSTNESS
32. mandatory joint B1 ABSOLUTE-purity + methylation-derived-leukocyte projection for the highest promotion tier;
33. run PRIMARY_PUBLICATION and MASKED_TECHNICAL tracks;
34. no favorable-mask selection.

INFERENCE
35. raw family H1, H2, H3a, H3b with BH FDR q<0.05 separately by technical track;
36. adjusted family H2_adj, H3a_adj, H3b_adj with BH FDR q<0.05 separately by technical track;
37. minimum 24 eligible cancers for promoted pan-cancer adjusted claim;
38. cancer-level effect = median across valid resamples;
39. exact sign test across eligible cancers, ties excluded;
40. mandatory direction/significance agreement across both technical tracks for promotion.

PROMOTION LADDER
C1-1: H1 passes both tracks -> organized static methylation geometry beyond exact probe marginals only.
C1-2: C1-1 + H2/H3a/H3b both tracks -> specific patient- and Hallmark-aligned static methylation/RNA architecture only.
C1-3: C1-2 + adjusted H2/H3a/H3b both tracks with >=24 eligible cancers -> composition-robust specific static methylation/RNA architecture only.

PERMANENT CLAIM CEILING
Even C1-3 does not establish causality, substrate inheritance, temporal progression, memory, irreversibility, damping, recovery, critical slowing, an exceptional point, a phase transition, a cancer optimum, treatment response, a master stability score, biological chi, or chi=1 as a cancer boundary.

FAILURE RETENTION
Do not post-result retune the primary stratum, scalar, scaling, missingness, mask, nulls, direction, multiplicity family, n, or resample count. Scientific changes require explicit versioned amendments and cannot retroactively replace this contract.

Before real execution, bind this contract by hash and make the code/tests prove exact agreement with it.
```

**Frozen contract blob:** `a39414c5990c234dc513569bd405b0237117d434`.

---

## PROMPT 26 - Implement C1 against the frozen contract before opening results

```text
Implement Stage C1 exactly as frozen. Treat the preregistration as executable law.

Before running the full biological computation:
- verify every input hash;
- verify the sample identity map;
- verify C1A probe flags and mapping hashes;
- verify both technical tracks;
- unit-test Gram/eigenspectrum/S_spec calculations;
- unit-test within-probe null preservation;
- unit-test linear CKA and patient permutation;
- unit-test Hallmark mapping, PC1 orientation, same-Hallmark coupling, and label permutation;
- unit-test purity/leukocyte projection;
- unit-test exact sign-test/BH family logic;
- unit-test deterministic seed construction;
- unit-test output schemas and promotion ladder;
- include negative tests proving historical CV/2/chi cannot enter the C1 computation;
- make implementation failure explicit rather than silently falling back to an alternate rule.

Do not inspect biological effect values until the implementation passes the frozen contract tests.
```

---

# 9. C1 scientifically consequential missingness amendments

The runtime problems themselves do not need to be replicated. The scientific issue they exposed does, because it determined how legitimate source missingness enters the frozen full-modal RNA bridge.

## PROMPT 27 - Diagnose source RNA non-finite values before changing science

```text
The C1 worker encountered non-finite values in the frozen Stage A RNA representation. Do not replace them with zero expression, drop genes, rescale features, or choose a repair based on which option helps the biological result.

Perform a read-only diagnostic before inspecting C1 effect values:
- quantify non-finite entries by cancer, sample, and gene;
- determine whether non-finites were already legitimate Stage A source missingness;
- identify whether completed cancers were all-finite or partially missing;
- determine exactly where the full-modal C1 implementation assumes all-finite input;
- compare the proposed handling with the frozen Stage A missingness policy;
- do not inspect effect directions, p-values, global inference, or promotion results while choosing the rule.

Propose the narrowest scientifically explicit amendment that binds source missingness without feature selection, variance scaling, zero-expression imputation, or result-dependent filtering.
```

---

## PROMPT 28 - EXACT v2.1 approval

```text
Approve C1 v2.1 missingness amendment.
```

### v2.1 scientific rule to preserve

```text
Retain all frozen RNA features. Within each frozen n=30 draw, if a gene has at least one finite observation, compute its finite within-draw mean, use that value only as the completion point for centering, and set source-missing centered coordinates to 0. Then perform the already-required column centering. Do not select/drop features and do not variance-scale. This 0 is the centered mean coordinate, not zero expression. All-finite draws must reproduce the pre-amendment arithmetic exactly. If a gene has zero finite observations in the entire draw, do not silently invent a value; fail and require a separate explicit scientific decision.
```

**Version after v2.1 implementation:** `.2`.

---

## PROMPT 29 - Preflight the zero-finite-gene failure across all cancers

```text
A later cancer contains RNA genes with zero finite observations across the entire frozen n=30 draw. Do not patch this locally and continue.

Run a read-only all-cancer preflight under the exact frozen deterministic memberships:
- for every cancer and all 100 draws, count genes with zero finite observations;
- list the affected gene symbols;
- distinguish partial source missingness from entire-draw zero-information genes;
- identify all cancers in which the issue occurs;
- verify whether previously completed cancers would have been numerically equivalent under any proposed rule;
- do not inspect C1 effect values or inferential direction while selecting the rule.

Propose the narrowest representation that preserves the ordered feature universe and introduces no invented positive/negative RNA signal.
```

**Observed preflight:** only ESCA, OV, and STAD had zero-finite genes in all 100 draws; 44 zero-information genes per affected draw.

---

## PROMPT 30 - EXACT v2.2 approval

```text
Approve C1 v2.2 full-modal zero-information amendment.
```

### v2.2 scientific rule to preserve

```text
For the full-modal RNA bridge:
- if a gene has at least one finite observation in the frozen n=30 draw, use the approved v2.1 finite-mean completion + centering rule;
- if a gene has zero finite observations in the entire draw, preserve its position in the exact frozen ordered RNA feature universe but represent its centered column as the all-zero vector under the explicit status NO_FINITE_IN_DRAW_ZERO_CENTERED;
- this column contributes exactly zero to the RNA Gram matrix;
- it is not zero-expression imputation;
- do not substitute a pan-cancer mean, external mean, neighboring cancer value, alternate gene, or result-dependent feature filter;
- do not change scaling, thresholds, nulls, multiplicity, promotion rules, or claim ceiling;
- record every affected cancer/draw/gene in the result audit.
```

**Final implementation version:** `stage-c1-frozen-v2-exec-20260906.3`.

---

# 10. Complete Stage C1 execution and closure

## PROMPT 31 - Run C1 to completion without interpretive peeking

```text
Execute the final approved C1 v2 + v2.1 + v2.2 implementation across all 32 cancers.

Requirements:
- 100 frozen n=30 resamples per cancer;
- both PRIMARY_PUBLICATION and MASKED_TECHNICAL tracks;
- exact frozen H1/H2/H3a/H3b and adjusted H2/H3a/H3b families;
- checkpoint safely without changing deterministic memberships;
- migrate prior checkpoints only when exact arithmetic equivalence under the approved amendments can be proven;
- preserve source-missingness and zero-information audit records;
- package raw compact outputs, cancer-level effects, global inference, resample summaries, Hallmark detail, mode contribution strata, eligibility, zero-information draws, local heavy-output manifest, and SHA-256 manifest.

Do not reinterpret partial checkpoints. Open biological inference only after the complete output package is closed and hash-bound.
```

---

## PROMPT 32 - Independent C1 result audit

```text
Audit the completed Stage C1 result independently before manuscript interpretation.

Verify:
- status STAGE_C1_COMPLETE;
- 32 cancers;
- 100 resamples per cancer;
- 2 technical tracks;
- 6,400 resample-summary rows = 32 x 100 x 2;
- no duplicate cancer/track/resample keys;
- every patient draw contains exactly 30 patients;
- eigenspectra have 29 positions, are nonnegative/ordered as defined, and normalize correctly;
- S_spec reproduces exactly from the stored eigenspectrum;
- top-five eigenvector diagnostics satisfy orthonormality where stored;
- CKA and principal-angle values remain in mathematical domains;
- observed-minus-null effects reproduce from source columns;
- exact sign-test and BH global inference reproduce independently;
- all returned output hashes match the result manifest;
- v2.1/v2.2 provenance is present;
- biological chi, historical GRI, causality, temporal inheritance, EP, and clinical claims remain absent.

Report the promotion level strictly from the frozen ladder. Do not invent a stronger claim because effect sizes are large.
```

**Closed result:** highest level `C1-3`.

---

## PROMPT 33 - Name and investigate every C1 exception/outlier

```text
Apply a mandatory named-outlier rule to every pan-cancer fraction and extreme effect in C1.

For each statement such as x/y cancers:
1. list the non-positive or excluded cancers by name;
2. give their effect sizes;
3. show whether PRIMARY_PUBLICATION and MASKED_TECHNICAL agree;
4. report the valid-resample/support count;
5. distinguish biological non-positivity from coverage/evaluability exclusion;
6. inspect whether the broad H2/H3a architecture remains when H3b fails;
7. investigate known cancer subtype, histology, composition, or source-coverage explanations using literature only as hypothesis support;
8. propose a direct falsification analysis for each strong hypothesis;
9. apply the same scrutiny to extreme positive outliers, not only negative cases;
10. do not turn low-support negatives into mechanistic stories.

Explicitly investigate raw H3b non-positive cancers and adjusted H3b non-positive cancers, plus the five cancers absent from the adjusted denominator.
```

### Named C1 deviations to preserve

Raw primary H3b non-positive:
- CHOL;
- READ;
- UCS.

Raw masked H3b non-positive:
- READ;
- UCS.

Adjusted denominator exclusions:
- COAD;
- DLBC;
- KIRC;
- OV;
- THYM.

Primary adjusted H3b non-positive:
- CHOL;
- KICH;
- KIRP;
- MESO;
- READ;
- UVM.

Masked adjusted H3b non-positive:
- CHOL;
- LIHC;
- LUAD;
- MESO;
- PAAD;
- TGCT.

Important support distinction:
- CHOL is the clearest well-supported cross-track adjusted exception with 100/100 valid adjusted draws;
- MESO is negative on both tracks but has only 3 valid adjusted draws, so the correct conclusion is insufficient support rather than a cancer-specific mechanism.

Extreme positive cases requiring subtype/histology scrutiny include TGCT, THYM, and ESCA.

---

## PROMPT 34 - Post-C1 v2.2 sensitivity

```text
After the frozen C1 result is complete, run a robustness-only sensitivity that excludes ESCA, OV, and STAD entirely because those are the cancers affected by the v2.2 zero-information rule.

Do not replace the frozen inference with this sensitivity.

Recompute the frozen-direction pan-cancer sign-test/BH summaries on the remaining cancers and report whether H1/H2/H3a/H3b and adjusted H2/H3a/H3b conclusions remain directionally intact.

If the result survives, state only that v2.2 is not what creates the promoted C1 architecture. Do not claim that missingness is irrelevant.
```

**Observed sensitivity:** C1-3 conclusions remain significant after excluding all three v2.2-affected cancers.

---

# 11. Integrated PanCan + methylation interpretation

## PROMPT 35 - Compare the two layers without collapsing them

```text
Interpret the completed RNA and methylation results together under the scalar/modal/conglomeration firewall.

Do not say “methylation is the scalar and RNA is the vector.” Instead ask, for each layer:
- what is its modal/vector structure?
- what scalar summaries are derived from that structure?
- what system/module/conglomeration measurements describe within-layer organization?
- what cross-layer measurements compare the two independently structured systems?

For methylation, explicitly distinguish the full eigensystem from S_spec, which is only a scalar compression of spectral concentration.

For RNA, preserve Hallmark/network structure plus scalar summaries such as C_in/C_out/PC1 fractions without claiming that any one scalar is the RNA state.

Use CKA and Hallmark coupling as cross-layer/conglomeration measurements, not as a biological chi.

Ask whether broad patient-state geometry is stronger than one-to-one same-Hallmark specificity and whether composition affects these levels differently.
```

**Data-supported integrated picture:** broad patient-level cross-layer geometry is much stronger and more technically stable than exact Hallmark-label specificity.

---

## PROMPT 36 - Test whether current scalar and modal/integrated measures are redundant

```text
Post-C1, perform an explicitly exploratory analysis asking whether the current scalar and modal/conglomeration measurements collapse onto one another.

Compare cancer-level primary effects representing:
- methylation scalar spectral concentration delta S_spec;
- full-modal cross-layer delta CKA;
- patient-specific Hallmark coupling delta A_patient;
- Hallmark-label specificity delta A_label.

Also examine within-cancer/resample relationships where the stored outputs allow it.

Do not promote these exploratory correlations into the frozen C1 family.

Interpret:
- near-perfect relationships would suggest redundancy;
- moderate/weak relationships suggest complementary information and compression loss;
- disagreement is evidence to preserve, not average away.
```

**Observed direction:** S_spec related moderately to broad cross-layer measures but did not subsume them, and was weakly related to label specificity. This argues against a single current observed scalar being the complete architecture.

---

## PROMPT 37 - Formulate the latent-state/chi hypothesis without promoting it

```text
Given that each molecular layer contains both modal structure and scalar summaries, and that cross-layer conglomeration measures add information not captured by a single scalar, formulate the strongest hypothesis that is compatible with the data without calling it a discovery.

Candidate hypothesis:
modal structure, scalar stability/organization coordinates, and system-level conglomeration may be complementary observational resolutions of a richer latent organizational state rather than three unrelated biological entities.

Do NOT say C1 discovered biological chi.

If the symbol chi is discussed, restrict it to a future candidate latent-state concept or to a generator-specific dynamical scalar when separately licensed. State that a valid scalar chi, where one exists, would be a compressed coordinate of the richer state rather than the entire ontology.

Give explicit failure conditions:
- a unified latent representation fails to generalize out of sample;
- separate-coordinate models predict held-out structure equally well or better;
- the apparent integration disappears under subtype/composition control;
- modal, scalar, and integrated representations do not move coherently under ordered perturbation/time-course data;
- the latent-state model cannot outperform or add interpretability beyond simpler established alternatives.

Keep this in the hypothesis/discussion tier, not the frozen Results tier.
```

---

# 12. Manuscript reconstruction

## PROMPT 38 - Rebuild the paper from the validated architecture rather than patching the old narrative

```text
Rebuild the oncology paper around the evidence that survived GRI v2 reconstruction.

The current paper is a static multiomic architecture paper, not a damping/criticality paper.

Main Results order:
1. execution/provenance closure;
2. methylation organization beyond probe-marginal null (H1);
3. full-modal methylation/RNA patient alignment (H2);
4. Hallmark patient-specific coupling (H3a);
5. smaller/heterogeneous Hallmark-label specificity (H3b), naming all exceptions;
6. composition-adjusted hierarchy, naming denominator exclusions and low-support cases;
7. cancer-specific deviation hypotheses with explicit support/falsification paths;
8. v2.2 exclusion sensitivity;
9. post-C1 exploratory scalar/modal/conglomeration complementarity.

Discussion order:
- what the two molecular layers say together;
- why neither RNA nor methylation is intrinsically “the scalar” or “the vector”;
- methylation as a structural-substrate candidate only;
- substrate inheritance reserved for temporal/perturbational evidence;
- latent-state/modal+scalar+conglomeration hypothesis as a falsifiable future idea;
- failures and limitations;
- exact claim ceiling.

Remove or replace all historical figure labels and axes that make unsupported dynamical/energetic claims.

Do not use historical CV/2 as biological chi. Do not infer gene rank as time. Do not claim cancer damping, exceptional points, therapeutic control rules, or clinical utility.

Every x/y cancer statement must name the exceptions/exclusions and characterize their support.
```

---

## PROMPT 39 - Build the reproducibility package

```text
Create a reviewer-facing reproducibility package that lets an independent researcher reconstruct the analysis without redistributing third-party source datasets that are not ours to redistribute.

Include:
- exact source acquisition instructions and citations;
- filenames, source IDs, sizes, hashes, and expected schemas;
- frozen configs;
- executable source;
- deterministic seed logic;
- regression tests;
- amendment documents;
- failure ledger;
- result archive and output hash manifest;
- report script that independently reconstructs the global inference from returned artifacts;
- figure/table provenance;
- outlier/deviation register;
- explicit non-claims;
- current hypothesis document distinguishing data-derived findings from future tests.

Do not require that TCGA or MSigDB source data be redistributed inside the project archive. The researcher should download authorized source data from the official provider and verify identity before running.
```

---

## PROMPT 40 - Cold adversarial submission audit

```text
Review the finished manuscript and reproducibility package as a skeptical external referee who did not participate in the project.

Check for:
- circularity;
- post-result rule changes presented as preregistration;
- hidden dependence on historical CV/2/chi;
- mismatch between text and figures;
- overclaim from static to dynamic/causal interpretation;
- unreported denominator changes;
- x/y cancer statements without named exceptions;
- low-support outliers being overinterpreted;
- subtype/composition confounding;
- missing source/provenance information;
- calculations that cannot be independently reconstructed;
- unbounded latent-state/chi language;
- claims in Abstract/Title stronger than the Results;
- failure records that were omitted because they were inconvenient.

Classify issues as:
- submission blocker;
- important revision;
- optional polish.

Do not invent more experiments simply to enlarge the paper. Recommend new computation only if it closes a real scientific/reproducibility gap or materially changes claim validity.
```

---

## PROMPT 41 - Freeze the submission baseline

```text
Once the paper, supplement, figures, reproducibility files, failure ledger, and QA pass are mutually consistent, freeze an immutable baseline package before title/wording iteration.

Record:
- exact ZIP SHA-256;
- exact manuscript PDF/source hashes;
- exact result archive hash;
- code/config/test hashes;
- amendment lineage;
- figure hashes;
- current claim ceiling;
- unresolved but non-blocking future hypotheses.

From this point forward, make only explicit, agreed deltas. Never silently replace the baseline.
```

**Current frozen manuscript-package baseline SHA-256:** `2342acd236483c0499280817c7aecbc8dba604a3d53e82dd00bace60ecadd5a8`.

---

# 13. Scientific failures and null results that MUST remain in the lineage

These should not be removed from a replication/reviewer history even though they are not “successful” outcomes.

## Historical mechanism failures

- `CV/2` did not earn a biological damping/chi interpretation.
- mean expression did not earn the role of physical frequency/energy.
- expression SD did not earn the role of dissipation rate.
- gene rank was not time.
- static TCGA did not establish bandwidth collapse, substrate capture/inheritance, exceptional-point crossing, or therapeutic control rules.
- historical overclaiming figures were replaced rather than cosmetically relabeled.

## Stage A construction failure

- raw cross-cancer absolute-correlation magnitudes depended on cohort size.
- response: prospectively freeze fixed n=30 / 100-resample A1.1 calibration.
- result: construction artifact collapsed while topology remained.

## Stage B1 result that limits interpretation

- composition is not negligible, especially for immune/inflammatory Hallmarks.
- composition also does not explain the entire RNA network topology.

## Stage B2 genomic weak result

- genomic coordinates produced small distributed changes and preserved most Hallmark ordering.
- this did not support a master genomic substrate or strong network reorganization claim.

## Tool-feasibility failures/narrowing

- nonlinear-only synthetic scope failed the validated linear architecture and was excluded.
- provisional regulatory-autonomy scalar was judged redundant and narrowed.
- F4 outcome was NARROW, not GO.

## P0 predictive limitations/failures

- only 19 cancers satisfied fully evaluable frozen split coverage, below the 24-cancer pan-cancer promotion floor; the floor was not lowered.
- five Hallmarks were source-mapping refusals and remained refused.
- D3 full Hallmark-label-specific semantic promotion failed in all 19 cancers despite strong global shared geometry.
- D4 replication state disagreed for PCPG, which became WITHIN_LAYER_ONLY/REFUSE.
- PCPG was also the lone cancer where the all-methylation predictor underperformed the composition-only comparator.
- FINAL_HOLDOUT was not opened in the sequence covered by the current repo state summarized here.

## C0/C0.1 source-schema failure/closure

- 41 duplicate primary methylation sample roots prevented immediate biological analysis.
- they were excluded by a pre-result one-to-one identity rule rather than averaged/selected from beta values.

## C1 missingness amendments

- legitimate Stage A source non-finites required v2.1.
- entire-draw zero-information RNA genes in ESCA/OV/STAD required v2.2.
- neither amendment was chosen after inspecting C1 effect direction/p-values/promotion.

## C1 biological deviations

- H3b was smaller and more heterogeneous than H1/H2/H3a.
- raw primary H3b non-positive: CHOL, READ, UCS.
- adjusted H3b included several negatives, with CHOL the strongest well-supported cross-track exception and MESO too low-support for a strong mechanistic story.
- five cancers were absent from composition-adjusted denominator due to covariate coverage/evaluable-draw rules, not because of biological failure.
- extreme positives TGCT, THYM, ESCA require subtype/histology scrutiny rather than automatic celebration.

## Current chi-state hypothesis remains unproven

The idea that modal, scalar, and conglomeration views may be observational resolutions of one richer latent organizational state is a **future falsifiable hypothesis**, not a C1 result and not an admitted biological chi.

---

# 14. Mechanical failures intentionally NOT reproduced

A clean reproducer does not need to repeat these execution problems:

- broken Windows nested `for /f` file-picker quoting;
- stale BAT entry points;
- launcher/file-picker UX problems;
- pandas `DataFrame.resample` name collision during B1 postprocessing;
- checkpoint path/migration mechanics where the scientific state was already complete;
- Python process shutdowns unrelated to scientific definitions;
- worker stderr not being captured in early launchers;
- retry loops caused by runner mechanics;
- partial heavy-file allocation before checkpoint creation;
- packaging/manifest housekeeping failures;
- temporary download/transport quirks when source identity was independently verified.

A reproducer **must** retain the scientific consequences revealed by failures, but may use the final corrected implementation and clean workflow.

---

# 15. Current paper-specific replication path in one line

For the current static methylation-transcriptomic manuscript, the minimum substantive path is:

`historical audit -> epistemic/chi firewall -> Stage A RNA cache -> Stage A1 -> A1.1 fixed-n -> B1 composition -> C0 methylation source -> C0.1 identity -> C1A annotation -> freeze C1 v2 -> implement/test -> v2.1 missingness rule -> v2.2 zero-information rule -> complete C1 -> independent closure audit -> named outlier investigation -> scalar/modal/conglomeration exploratory integration -> manuscript reconstruction -> cold audit -> immutable freeze`

B2, F0-F4, and P0 are scientifically relevant program lineage and should remain documented, but they are not required to regenerate the exact C1 inferential family used by the current paper.

---

# 16. Reviewer-facing replication expectations

A reviewer/researcher attempting reproduction should be able to answer yes to all of the following:

- I know exactly which third-party sources to download and from where.
- I can verify the expected source identities/hashes.
- I understand that project redistribution of TCGA/MSigDB data is not required.
- I can reconstruct the Stage A RNA representation and exact Hallmark membership used downstream.
- I can reproduce the Stage A1/A1.1 and B1 definitions without historical chi/CV2 assumptions.
- I can independently verify the methylation source, sample identity, annotation, and technical masks before biology.
- I can see the exact pre-result C1 v2 contract and its hash.
- I can see why v2.1 and v2.2 were scientifically necessary and that they were approved before C1 effect inference inspection.
- I can reproduce C1 outputs and global inference from the returned artifacts.
- I can identify every cancer behind the reported pan-cancer exceptions/denominator changes.
- I can distinguish frozen C1 results from post-C1 exploratory analysis.
- I can distinguish data-supported methylation structural-substrate candidacy from unproven substrate inheritance.
- I can distinguish the modal+scalar+conglomeration latent-state hypothesis from an admitted biological chi.
- I can find the failed/null/narrowed branches rather than only the successful ones.

---

# 17. Future prompt required to actually test the latent-state / biological-chi idea

This prompt is **not part of the current paper result**. It records the next decisive hypothesis test rather than pretending the question is already closed.

```text
Design a prospective test of whether modal structure, scalar coordinates, and cross-layer conglomeration are complementary observational resolutions of one latent biological organizational state rather than merely correlated summaries.

Before looking at the new data, freeze:
- the candidate latent-state model;
- separate-coordinate baseline models;
- subtype/composition covariates;
- held-out prediction targets;
- identifiability and uncertainty criteria;
- mapping from modes to scalar summaries and cross-layer structure;
- perturbational or temporal endpoints if ordered data are available;
- criteria for coherent movement across modal, scalar, and integrated representations;
- failure/refusal conditions;
- external replication dataset.

The unified-state hypothesis should fail if:
- it does not improve held-out prediction/calibration/interpretability over separate-coordinate models;
- apparent unity vanishes after subtype or composition control;
- mappings are unstable across cohorts;
- modes and scalars reorganize independently under perturbation;
- cross-layer geometry changes without corresponding scalar/modal movement or vice versa;
- a simpler established model explains the same observations.

Only after prospective out-of-sample and ordered-data support may the program consider whether any scalar compression deserves the symbol chi. If a dynamical chi is proposed, its Gamma and Omega must be genuine same-coordinate dynamical quantities with compatible units and a boundary derived from the governing generator rather than fitted to a preferred value.
```

---

# 18. Final preservation rule

Do not rewrite this history into a smooth success story.

The research became stronger because several attractive ideas failed, were narrowed, or were moved to hypothesis status. A faithful replication should reproduce the **decision sequence and evidentiary constraints**, not the incidental runtime bugs.

The core surviving architecture is:

**within-layer modal structure + scalar summaries + cross-layer/system conglomeration, with disagreement preserved and dynamics deferred until ordered evidence exists.**

That architecture is the current evidence-supported framework. A unified latent `chi`-state remains a falsifiable future possibility, not a present result.
