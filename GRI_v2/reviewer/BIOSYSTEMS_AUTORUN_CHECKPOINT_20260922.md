# BioSystems autonomous continuation checkpoint

**Created:** 22 September 2026
**Status:** ACTIVE
**Branch:** `gri-biosystems-revision-20260922`
**Program authority:** SymC General Operations Manual v0.8.4
**Purpose:** allow future ChatGPT runs to resume BioSystems revision work after polling/session/tool interruptions without user intervention.

## Non-negotiable resume rule

Every continuation run must:

1. read this checkpoint first;
2. verify current branch/head and relevant workflow state;
3. continue from the first incomplete item in **Current execution queue**;
4. perform all safe/mechanical work that does not change a frozen scientific decision;
5. never retune a frozen endpoint, cohort, representation, threshold, seed, null, or comparator in response to a result;
6. update this checkpoint before ending the run;
7. preserve all failures, indeterminate results, and representation dependence;
8. keep working manuscripts private in the Project Library;
9. stop only at a genuine new scientific decision, an external-access boundary that cannot be solved mechanically, or final submission readiness.

A workflow timeout, polling timeout, chat interruption, or tool interruption is **not** a scientific stop. Resume from the latest checkpoint and workflow/artifact state.

## Frozen scientific state

### Tumor-normal reviewer control
**CLOSED.**

Internal biological closeout is frozen in:
- `GRI_v2/reviewer/BIOSYSTEMS_TUMOR_NORMAL_BIOLOGICAL_CLOSEOUT_20260922.md`
- `GRI_v2/reviewer/BIOSYSTEMS_TN_C1_BIOLOGICAL_RESULT_AUDIT_20260922.md`
- `GRI_v2/reviewer/BIOSYSTEMS_TUMOR_NORMAL_PROTOCOL_LINEAGE_AUDIT_20260922.md`

Key result:
- TN-A1 RNA: tumor lower in 12/12 cancers for all three primary RNA architecture coordinates; BH q=0.000488 each.
- TN-P20 paired sensitivity: same direction 13/13, 13/13, 12/13; q<=0.00342.
- TN-C1: H1 lower in tumor 5/5 with all cancer construction intervals below zero; H2/H3a heterogeneous; H3b small upward tendency without q<0.05 resolution.

Supported interpretation:
**tumor-associated reorganization of pre-existing tissue architecture, dominated by loss of within-layer/modular coherence rather than wholesale disappearance of organization.**

Do not upgrade this static result to recovery failure, causality, biological chi, or a universal boundary.

### Biological chi / recovery program
Do **not** reopen the closed historical `Chi_bio` admission cycle inside this BioSystems revision.

Historical disposition remains:
- scalar Chi_bio NOT_ADMITTED for the tested lineage;
- current SCC25 R1/A3 scalar admission refused as representation-dependent;
- normalized empirical G1 blocked by restoration identifiability;
- broader recovery hypothesis remains scientifically compatible with current tumor-normal findings but requires a new lineage and causally/dynamically informative recovery evidence.

BioSystems submission work has priority. Chi_bio/recovery is the next dedicated investigation after this revision is locked. The distance assessment is formalized in `GRI_v2/docs/GRI_CHI_BIO_DISTANCE_TO_ADMISSION_20260922.md` (commit `979cf5e...`): recovery is a focused new dynamical investigation, while scalar chi admission still requires a new lineage with restoration identifiability, scalar derivation, representation robustness, native-baseline incremental value, prospective boundary testing if applicable, and independent transport. Do not delay the current revision for this.

### External validation reviewer gate
This is the **only remaining publication-critical evidence-bearing reviewer gate**.

Frozen source:
- RNA: GSE237995
- 450K methylation: GSE262522
- EPIC methylation sensitivity: GSE262524

Frozen protocol:
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`
- `GRI_v2/config/biosystems_external_prostate_p1_v1_0.json`

Primary:
- 30 paired participants from the 32 complete 450K tumor/adjacent pairs;
- P1-H1 `delta_s`;
- P1-H2 `delta_cka`;
- P1-H3a `delta_a_patient`;
- B=999 endpoint-appropriate nulls/permutations;
- BH over H1/H2/H3a;
- outcome classes FULL / PARTIAL / NO TRANSPORT / REPRESENTATION_DEPENDENT / INDETERMINATE.

Mandatory sensitivities:
- full n=32 450K pair set;
- all 26 complete EPIC pairs;
- neither sensitivity may rescue the frozen primary.

Secondary:
- external paired tumor-normal RNA corroboration of `C_in,pair`, `C_in,PC1`, and `C_out`;
- frozen directional hypothesis is tumor < adjacent.

No biological chi, recovery, causal methylation->RNA, treatment-response, or clinical claim is part of this P1 task.

## Last completed external step

Outcome-blind source preflight completed successfully:

- workflow run: `35801003396`
- artifact: `GRI_BIOSYSTEMS_EXTERNAL_PROSTATE_P1_SOURCE_PREFLIGHT_V01`
- artifact ID: `10725064779`
- artifact digest: `sha256:f77168c359135047d01dbd23b1f848e7929a0a2c0ce2a0254dee374c703aa7d1`
- result: SUCCESS
- GRI biological outcome opened: FALSE
- all frozen primary and EPIC participants present in required source headers;
- no source-header participant ambiguity;
- RNA source: 58,037 Ensembl rows;
- 450K source: 485,512 unique CpG rows;
- EPIC source: 865,859 unique CpG rows.

Exact source hashes are preserved in the preflight artifact and must be inherited by the outcome-bearing run.

## Private manuscript state

Private Library folder:
`/Atlas - GRI update v1/Private Working Manuscripts/Oncology`

Current working source:
`GRI_BioSystems_working_v5_2026-09-22.tex`

v5 already:
- integrates the closed tumor-normal result into abstract/methods/results/discussion/limitations/conclusion;
- removes obsolete language saying the post-C1 sensitivity tranche remains pending;
- preserves static-vs-recovery firewall;
- leaves genuine external confirmation as the remaining explicit evidence placeholder.

Do not publish this working manuscript to the public Biomedical repository.

## Current execution queue

### Q1 - external P1 implementation and preflight
**COMPLETE.**

Build the outcome-bearing external prostate runner by transporting the already frozen C1 constructions, not inventing new statistics.

Required before result opening:
- bind exact source hashes from source preflight;
- bind exact 30 primary participants;
- bind the existing C1 450K-compatible probe/gene support and Hallmark source;
- bind deterministic Ensembl->gene-symbol mapping rule;
- implement H1/H2/H3a with B=999 frozen nulls;
- implement full n=32 and EPIC sensitivities;
- implement secondary paired RNA tumor-normal test;
- write tests/known-shape fixtures;
- run an outcome-blind mechanical preflight if needed.

Scientific rules may not change.

### Q2 - execute external P1
**COMPLETE.** Frozen run `35801966289` succeeded; artifact `10726636434`, digest `sha256:1d7bbef7a4f8ea0cb254c139879e8ec53b9498f8d95c9c97fa28f21367075cde`. Primary 450K n=30 = `P1_PARTIAL_TRANSPORT`; full n=32 concordant; EPIC reproduces H1 but reverses H2/H3a signs; final preregistered disposition = `P1_REPRESENTATION_DEPENDENT`. No rescue performed.

Historical instruction retained below for audit:
After Q1 mechanical/identity gates pass, execute the frozen external result.

On completion:
- audit source/config/code/artifact identities;
- report every endpoint, including failures;
- classify FULL/PARTIAL/NO TRANSPORT/REPRESENTATION_DEPENDENT/INDETERMINATE strictly under the frozen contract;
- do not rescue a failed primary with n=32 or EPIC.

### Q3 - manuscript integration
**SUBSTANTIALLY COMPLETE.** Private main manuscript has advanced through `GRI_BioSystems_working_v8_2026-09-22.tex`; supplement through v7. External P1, tumor-normal, AI disclosure, funding/conflict/contribution statements and source citation are integrated. Figure/caption synchronization remains part of release work.

Integrate the external result into the private working manuscript:
- abstract;
- Methods;
- Results;
- Discussion;
- Limitations;
- conclusion;
- relevant tables/figure plan;
- exact external-validation claim ceiling.

If P1 fails or partially transports, narrow the manuscript exactly as required rather than redesigning P1.

### Q4 - reviewer package
**ACTIVE.** Reviewer matrix, claim map and resubmission closeout are synchronized to the completed P1. Private `BioSystems_Response_to_Reviewers_v1_2026-09-22.md` and `BioSystems_Cover_Letter_v1_2026-09-22.md` are drafted. Final prose/cross-reference synchronization remains after figures are frozen.

Update:
- `BIOSYSTEMS_REVIEWER_RESPONSE_MATRIX_20260922.md`
- `BIOSYSTEMS_RESUBMISSION_CLOSEOUT_20260922.md`
- point-by-point reviewer response;
- claim/evidence map;
- non-claim ledger;
- source/result hash manifest;
- figure/table regeneration/provenance map;
- editor-facing author-initiated correction delta.

### Q5 - final submission mechanics
**CURRENT PRIORITY.** All scientific evidence gates are closed. Active blocker is regenerated visual/release packaging under GOM v0.8.4. The completed C1 result archive is not currently accessible, so no heavy scientific rerun is authorized merely to recreate charts; visuals must be regenerated from verified accessible result artifacts/audited aggregates or replaced with evidence-equivalent release visuals.

Complete:
- final figures/tables;
- citation/source verification;
- axis/unit audit;
- current BioSystems policy boilerplate and disclosures;
- data/code availability;
- competing interests/funding/contributions;
- immutable submission tag/release;
- clean-room/reviewer-package audit;
- PDF visual inspection;
- final release checklist.

## Stop conditions

Do **not** stop for:
- polling delays;
- queued/in-progress GitHub jobs;
- a failed mechanical workflow if a scientific rule-preserving repair is available;
- packaging failures;
- stale workflow runs;
- manuscript synchronization chores.

Stop and surface the issue only for:
- a choice that changes the frozen scientific question;
- a source/access defect that makes the frozen P1 scientifically non-evaluable and cannot be repaired without changing the contract;
- a contradiction that invalidates an upstream frozen result;
- a genuine new user decision required by the GOM;
- final submission readiness.

## Final completion condition

This checkpoint is complete when:
1. external P1 is dispositioned under the frozen contract;
2. manuscript and reviewer response are synchronized to that result;
3. all reviewer concerns are either closed or explicitly narrowed/declined;
4. final release/reproducibility package passes;
5. submission-ready files are available privately to the user.

At that point set:
`STATUS: COMPLETE / SUBMISSION READY`
and do not start a new scientific branch automatically.
