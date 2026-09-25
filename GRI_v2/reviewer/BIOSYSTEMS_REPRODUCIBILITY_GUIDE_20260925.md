# BioSystems Cancer Paper Reproducibility Guide

**Manuscript ID:** BIOSYS-D-26-00267  
**Current manuscript title:** *Genomic Regulatory Instability in Human Cancer: Recurrent Multiomic Stability Architecture Across Tumor Types*  
**Guide date:** 25 September 2026  
**Repository:** `SymC-Universe/Biomedical`  
**Submission evidence branch:** `biosystems-v27-repro-guide-20260925`  
**Scientific parent:** `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`  
**Status:** REVIEWER ENTRY POINT / NO NEW SCIENTIFIC RESULT

## Purpose

This is the shortest reviewer route through the public evidence used by the cancer manuscript. It supersedes older reviewer-navigation prose for this submission only. Historical files remain provenance, but reviewers should not have to reconstruct the paper from repository archaeology.

The editable manuscript and Supplementary Information remain private authoring files. The public repository contains the scientific freezes, source identities, code, workflow provenance, result audits, failure/refusal records, and claim ceilings needed to audit the paper.

## Five-minute reviewer route

1. Read this file.
2. Read `BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md` for the full chronological public record through v26.
3. Read the five result families below only if the corresponding manuscript claim is being audited.
4. For the biological chi qualification, use the separately frozen public lineage at `bio-chi-topdown-pivot-20260924` @ `86463567f5fab783689e30ce21d7b061623fff36`.
5. Do **not** use the active `gri-biochi-bridge-p0q-20260925` branch as evidence for this submission. Its direct same-carrier GRI-to-Bio-Chi bridge remains an active qualification program and is not a manuscript claim.

## Claim-to-record map

| Manuscript claim family | Public record | What it supports | Claim ceiling |
| --- | --- | --- | --- |
| TCGA H1 within-methylation organization | `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_AUDIT_20260923.md` | H1 remains positive in 30/30 composition-complete cancers after nulls preserving measured linear purity/leukocyte structure and TCGA source-site mean structure; median excess +0.0816210492 | Residual covariance above tested floors, not tumor-cell-intrinsic mechanism or complete confound removal |
| TCGA H2/H3 recurrence | C1/post-C1 records indexed in `BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md` | H2 and H3a recur internally across 32/32 cancers; H3b is smaller/support-sensitive | Internal TCGA correspondence, not universal cross-source architecture or causal direction |
| Tumor versus adjacent normal | `BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md`, `BIOSYSTEMS_TUMOR_NORMAL_BIOLOGICAL_CLOSEOUT_20260922.md`, `BIOSYSTEMS_TN_C1_BIOLOGICAL_RESULT_AUDIT_20260922.md` | Primary RNA organization lower in tumor across 12/12 cancers; TN-C1 H1 lower in tumor across 5/5 eligible cancers | Adjacent/non-tumor state contrast; composition-unadjusted where a symmetric adjustment was unavailable; not failed recovery |
| Independent prostate transport | `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`, `BIOSYSTEMS_EXTERNAL_PROSTATE_P1_POSTRESULT_AUDIT_20260922.md` | H1 transports on 450K and EPIC; H2/H3a do not transport detectably; final class `P1_REPRESENTATION_DEPENDENT` | Independent support for H1 only; no rescue of H2/H3a |
| Independent breast H1 corroboration | `BIOSYSTEMS_BREAST_EXTERNAL_H1_P0D_V01_RESULT_AUDIT_20260923.md` | Post-result external breast 450K H1 corroboration, primary deterministic n=30 lane delta S = 0.15019, p = 0.001 | Corroboration, not retroactive confirmation |
| Direct intervention and recovery extensions | `BIOSYSTEMS_HCI005_DECITABINE_INTERVENTION_V01_RESULT_AUDIT_20260923.md`; `BIO_CHI/artifacts/SU2026_SIMPLE_RECOVERY_V01_RESULT_AUDIT_20260923.md` | One breast PDX supports intervention-consistent inverse promoter methylation-RNA coupling; M397 withdrawal supports transcriptomic return toward baseline under the frozen distance | Model-specific post-result evidence; neither explains TCGA cross-sectional architecture |
| Negative/source-limited clinical extensions | `BIOSYSTEMS_SCC25_RESPONSE_DIRECTION_V01_RESULT_AUDIT_20260923.md`; `BIOSYSTEMS_EXTERNAL_PROSTATE_DIAGNOSTIC_LOPO_V01_RESULT_AUDIT_20260923.md` | SCC25 direction test negative/unresolved; prostate diagnostic route failed; prognosis not opened without a verified outcome crosswalk | Treatment-response prediction and diagnostic/prognostic utility remain unestablished |

## Biological chi qualification used by the manuscript

The manuscript's connection to the wider chi representation hierarchy comes from a **separately frozen biological qualification**, not from reinterpreting static TCGA variables as dynamics.

Public source-of-record for this qualification:

- branch: `bio-chi-topdown-pivot-20260924`;
- frozen completion head: `86463567f5fab783689e30ce21d7b061623fff36`;
- primary closure: `BIO_CHI/control/ONCOLOGY_P0Q_CLOSURE_20260924.md`;
- generator result pin: `BIO_CHI/config/SU2026_ONCOLOGY_GENERATOR_V01_RESULT_PIN.json`;
- uncertainty/native-comparator result pin: `BIO_CHI/config/SU2026_NATIVE_COMPARATOR_SEM_LIMIT_V01_RESULT_PIN.json`;
- held-out behavior result pin: `BIO_CHI/config/SU2026_CROSS_CELL_BEHAVIOR_TRANSPORT_V01_RESULT_PIN.json`.

The three representation levels are kept distinct:

| Object | Submission disposition |
| --- | --- |
| scalar `chi_bio` | **REFUSED** in the Su oncology lineage because nominal complex carriers were not robust to reported +/-1 SEM eigenvalue-class stress and the defined scalar was algebraically redundant with native 2D invariants |
| modal/vector `Chi_bio` | **QUALIFIED MODEL-SPECIFICALLY** as the complete uncertainty-aware Su two-state generator/eigenstructure. Three of eight nominal source scenarios (`ON_PP`, `OFF_PN`, `OFF_NN`) contain stable complex-conjugate modes and therefore support a nominal damped/oscillatory modal description, but all three cross the real/complex boundary somewhere in the frozen +/-1 SEM stress. |
| whole-system biological chi | **NOT ADMITTED FROM SU CROSS-CELL TRANSPORT** because the frozen M397 generator failed the HCC827 constant-state baseline; HT-29 failed the frozen carrier-coverage gate |

These outcomes connect the cancer work to the same scalar/modal/system representation hierarchy while preserving refusal. They do **not** establish a universal cancer scalar, a chi=1 boundary, or a direct same-carrier bridge from static GRI architecture to realized biological chi behavior.

## Damping and oscillation scope

The revision does **not** discard damping or oscillation as biological dynamical questions. It separates the carrier on which those terms are licensed.

- The historical cross-sectional RNA quantity `chi_GRI = sigma/(2 mu) = CV/2` is preserved in the Supplementary Information as an operational fluctuation-to-signal/stability proxy and research-lineage quantity. It is not identified with a physical damping coefficient or oscillator frequency, and it does not inherit a `chi=1` critical-damping boundary.
- Static TCGA gene rank is not time and is not used to infer oscillation, relaxation class, hysteresis, or temporal progression.
- In the source-native longitudinal Su M397 two-state generator, three of eight nominal scenarios contain stable complex-conjugate modes. At the nominal source parameters these are legitimate damped/oscillatory linear modes of that model.
- All three nominal complex scenarios cross the real/complex eigenvalue-class boundary somewhere within the frozen +/-1 SEM parameter stress. The oscillatory classification is therefore uncertainty-sensitive, the scalar `chi_bio` remains refused, and no universal cancer oscillator or universal damping boundary is claimed.
- The complete modal/vector representation remains qualified model-specifically because retaining the full generator/eigenstructure preserves the uncertainty and mode information that scalar compression would discard.

This scope restores the dynamical question without back-projecting it onto cross-sectional TCGA statistics.

## Active bridge work is not a submission dependency

The branch `gri-biochi-bridge-p0q-20260925` is an ongoing post-manuscript qualification program asking whether frozen static architecture can be joined to independently licensed dynamics on a defensible same carrier.

For this paper:

- Harmange direct same-carrier bridge is a source-materialization refusal, not supporting manuscript evidence.
- Shaffer is source-qualified/preanalysis work and has not been promoted into this manuscript.
- No B2/B3 bridge result is required to reproduce or interpret any submitted claim.
- Reviewers therefore do not need to inspect that moving branch unless they are auditing future work beyond the submitted paper.

## What the paper does not claim

The manuscript does not claim that the historical cross-sectional `chi_GRI = CV/2` is a physically identified damping ratio, does not infer oscillations or temporal progression from static TCGA gene rank, and does not claim a universal cancer chi value or chi=1 health/treatment boundary. It also does not claim static-to-dynamic equivalence, a universal methylation-to-RNA causal direction, a direct same-carrier GRI-to-Bio-Chi relationship, a general cancer recovery law, or validated diagnostic/prognostic/treatment-response utility. Model-specific damping/oscillation language is retained only where source-native longitudinal dynamics license it and remains bounded by the reported uncertainty.

A failed, refused, unresolved, or source-limited branch remains part of the public evidence record and is not converted into supporting evidence after the fact.

## Minimal reproduction path

A reviewer does not need to download all third-party raw data or run every historical script.

For an audit-only reproduction:

1. checkout this submission evidence branch;
2. inspect the freeze/result-audit pair for the claim being checked;
3. verify the workflow run ID, artifact ID/digest, source accession/hash, and code/config path recorded in that audit;
4. inspect the corresponding implementation under `GRI_v2/src/` or `BIO_CHI/src/`;
5. use the original provider accession for large third-party data rather than expecting redistributed raw data in Git.

For full recomputation, use the source identities and frozen configs named in the relevant audit. The repository intentionally preserves exact identities and transformations rather than duplicating multi-gigabyte third-party datasets.

## Key workflow identities

Independent prostate P1:
- run `35801966289`;
- artifact `10726636434`;
- digest `sha256:1d7bbef7a4f8ea0cb254c139879e8ec53b9498f8d95c9c97fa28f21367075cde`.

H1 composition + source-site attack:
- run `35815819898`;
- artifact `10731877118`;
- digest `sha256:d8d953f7803e8dd048a85a6bb96298315dcfd4c9eff38bd3b400731386cb4e70`.

External P1 precision extension:
- run `35815566680`;
- artifact `10731477329`;
- digest `sha256:c4a54434de5584be0f2d42defc10b82f5c3af4c9584a941ed6391f01bdaa6c65`.

The complete workflow/artifact chronology is retained in `BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md`.

## Repository navigation

| Path | Purpose |
| --- | --- |
| `GRI_v2/reviewer/` | submission freezes, result audits, claim maps, reviewer navigation |
| `GRI_v2/config/` | frozen analysis contracts |
| `GRI_v2/src/` | executable analysis code |
| `GRI_v2/tests/` | contract/regression tests |
| `GRI_v2/artifacts/` | source/provenance and larger-result identities |
| `BIO_CHI/config/` | biological chi source/model freezes and result pins |
| `BIO_CHI/control/` | biological chi checkpoints, closures, refusal records |
| `BIO_CHI/src/` | biological chi analysis implementations |

## Submission-source hierarchy

For this paper, read records in this order:

`biosystems-v27-repro-guide-20260925`  
-> scientific parent `biosystems-v26-final-substantive-20260923` @ `509c4f3335d9020ea8e910579d6d98cb2fa9e58d`  
-> biological chi qualification `bio-chi-topdown-pivot-20260924` @ `86463567f5fab783689e30ce21d7b061623fff36`.

The active `gri-biochi-bridge-p0q-20260925` branch is explicitly outside the submission evidence spine.

## Reviewer stop rule

A reviewer should not need to infer the current manuscript claim from historical README files. If an older file conflicts with this guide for the submitted paper, use this guide plus the dated freeze/result audit for the specific claim. Historical records remain valid only for the stage they document.

**Guide disposition:** submission evidence is navigable from one entry point; no new scientific claim is created by this file.
