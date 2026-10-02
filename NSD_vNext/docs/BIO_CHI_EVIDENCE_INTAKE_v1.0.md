# Bio Chi Evidence and Dataset Intake Record v1.0

**Status:** ACTIVE BACKFILL  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 0.6  
**Investigation:** Bio Chi  
**Repository:** `SymC-Universe/Biomedical`  
**Branch:** `nsd-rebuild-gom-v0.8.0`

## Project-level intake state

**EVIDENCE_INTAKE_STATUS: INTAKE_PASS_WITH_LIMITS**

The current Bio Chi investigation is using three materially different evidence classes: prior literature, synthetic/known-truth qualification evidence, and already-existing descriptive neural data/artifacts. They have different admissibility ceilings and are not pooled into one evidence class.

## E1. Prior-art literature corpus

- **Canonical identifier:** `BIOCHI-LIT-20260927`
- **Source type:** `LITERATURE_DERIVED`
- **Primary location:** Undermind workspace `Chi Bio Investigation 2026`, workspace ID `2313474c-bd7d-42dd-921b-25cc69acff8e`
- **Deep-search sources:** `Native biological generators for chi_bio`; `Biological stability perturbation recovery and state inheritance`; `Cancer same-carrier static RNA to native dynamics B1`; `Bio Chi P0N methodological foundations`
- **Acquisition/review date:** 23-27 September 2026, P0-N reconciliation on 27 September 2026
- **Identity lock:** source title, authors, DOI/link, cite key, deep-search identity, and workspace identity where available
- **Use:** P0-N component extraction, compatibility mapping, novelty reconstruction, A0 prior-art Atlas
- **Evidence tier:** primary-source abstract/metadata unless explicitly recorded as full-text verified. No literature-sourced numerical coordinate is locked from abstract-only, snippet-only, or metadata-only evidence.
- **Rights/access:** literature access through public publisher metadata, abstracts, open-access PDFs where available, or connected research service. Publisher rights remain source-specific.
- **Outcome exposure:** not applicable as a confirmatory dataset; literature is prior-art evidence.
- **Provenance purity:** PASS for source-level bibliographic identity; claims remain source-specific.
- **Intake state:** `INTAKE_PASS_WITH_LIMITS`
- **Limit:** claims requiring exact equations, conditions, or numerical values must satisfy the GOM Section 18.2 evidence tier appropriate to the intended use. The current P0-N novelty synthesis does not lock source-derived numerical coordinates.

## E2. Synthetic / known-truth qualification evidence

- **Canonical identifier:** `BIOCHI-SYNTH-QUAL-BRANCH`
- **Source type:** `SIMULATED` and `DERIVED_INTERNAL`
- **Primary location:** `NSD_vNext/engine/`, qualification workflows, artifacts, and postresult records on branch `nsd-rebuild-gom-v0.8.0`
- **Generating code:** versioned repository code for C/D/S lineage, closure, C1Q/D1Q, structural-order, paired-sampling, and related qualification fixtures
- **System identity:** declared known-truth linear stochastic/state-space systems and adversarial controls
- **Units/conventions:** defined per fixture and test record; no synthetic coordinate is reclassified as measured biology
- **Replicate status:** pseudorandom repeated realizations are computational replicates, not independent biological specimens
- **Outcome exposure:** fully exposed qualification evidence
- **Use:** P0-Q qualification, exact-contract testing, failure/refusal mapping, Function/Limit mapping
- **Intake state:** `INTAKE_PASS`
- **Limit:** synthetic frequency does not estimate biological prevalence. Previously viewed known truths cannot serve as untouched P1 confirmation for an estimator adapted to them.

## E3. Existing neural descriptive data and artifacts

- **Canonical identifiers:** source-specific records including current ds004148 and ds003775 NSD lanes
- **Source type:** `RAW_MEASURED`, `TRANSFORMED`, and `DERIVED_INTERNAL` depending artifact
- **Use ceiling in current Bio Chi work:** descriptive Function/Limit evidence only unless a source-specific intake and independence record licenses stronger use
- **Known limitations:** current real-EEG local (chi) is unlicensed; prior eyes-closed topology audit and ds004148 transport issues remain provenance/infrastructure limitations where documented; historical disorder outcomes are already viewed
- **Outcome exposure:** legacy/descriptive outcomes already exposed and therefore unavailable as untouched confirmation for a newly revised N-B1 estimator
- **Intake state:** `INTAKE_PASS_WITH_LIMITS`
- **Limit:** no empirical neural artifact is admitted as local dynamical (chi) merely because it contains oscillatory, spectral, covariance, or state-space structure.

## Transformation and lineage rule

Every future material transformation that changes the scientific object receives a derivative identity linked to the parent source, generating code/procedure, parameters, and commit/version. Source-origin duplicates and naturally repeated observations are preserved as such. Manufactured replicas remain marked and never acquire false source independence.

## Quarantine / blocked items

No currently used P0-N literature source is quarantined for bibliographic identity. Any future material dataset with unresolved carrier, condition, source, event, or population identity is assigned `QUARANTINED_IDENTITY_CONFLICT` or `BLOCKED_MISSING_PROVENANCE` before claim-bearing aggregation.

## Current claim ceiling imposed by intake

This intake record supports Stage 1 novelty synthesis and P0 qualification work. It does not authorize P1 empirical confirmation, real-EEG local (chi), biological prevalence estimates from synthetic grids, or reuse of already-viewed neural outcomes as untouched confirmation.
