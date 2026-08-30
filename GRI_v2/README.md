# GRI v2 / Cancer Stability Atlas

**Status:** DEVELOPMENT PROGRAM, NOT A VALIDATED CANCER TOOL  
**Active phase:** Stage C0 DNA-methylation source gate  
**Status date:** 2026-08-30

> **Reviewer navigation:** start at `reviewer/README.md`. The moving `gri-v2` branch is development history, not an immutable submission record. Manuscript/data submissions will use an exact tagged/released snapshot under `reviewer/SUBMISSION_RELEASE_CHECKLIST.md`.

## Objective

Build a falsifiable cancer-stability and substrate-architecture tool in which every retained coordinate earns its role through prospective tests, appropriate nulls, robustness, prediction, and external validation.

The historical GRI manuscript is provenance, not the target model. `CV/2` is historical only. No valid biological chi coordinate has been admitted.

## Scientific firewall

- **chi** is reserved for a genuine same-coordinate dynamical balance `Gamma/(2*Omega)`.
- Static RNA, methylation, genomic, protein, composition, and organization quantities are not damping rates or chi by interpretation.
- `chi = 1`, if later measured legitimately, is not presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum.
- No master stability score is currently admitted.
- Failed and null branches are retained.
- Publication goals do not steer coordinate definitions, nulls, thresholds, or feature selection.
- **Modal structure + scalar coordinates + conglomeration/system organization are complementary views.** A scalar may compress an empirically licensed structure but may not replace its mode-resolved carrier or whole-system architecture.

Canonical guardrails:

- `docs/EPISTEMIC_CONSTITUTION.md`
- `docs/CHI_ADMISSION_RULES.md`
- `docs/TOOL_OBJECTIVE.md`

## Closed evidence layers

### Stage A: static RNA map

Stage A retains separate static observables `V`, `L`, `C_in`, and `C_out`. Fixed-`n=30` calibration showed that finite-sample inflation can be controlled while the Hallmark topology remains reproducible. These are static network measurements, not a dynamical mechanism.

See:

- `docs/STAGE_A1_AUDIT_20260829.md`
- `docs/STAGE_A1_1_AUDIT_20260829.md`

### Stage B1: composition/context decomposition

Independent ABSOLUTE tumor purity and methylation-derived leukocyte fraction explain a concentrated part of the Stage A network geometry, especially immune/inflammatory structure, without erasing the broader topology. Raw and adjusted maps are both retained.

See `docs/STAGE_B1_AUDIT_20260829.md`.

### Stage B2: orthogonal static multiomic integration

B2 source selection and analysis rules were frozen before the target association results.

The closed layers are:

- five separate genomic coordinates: `ANEUPLOIDY_AS`, `LOH_SEGMENT_COUNT`, `LOH_GENOME_FRACTION`, `SCNA_SEGMENT_COUNT`, and `SCNA_ALTERED_FRACTION`;
- an orthogonal 189-measurement RPPA protein/phosphoprotein panel;
- composition/context sensitivity inherited from B1.

The RPPA branch retains reproducible patient-aligned RNA/protein coupling above its block-permutation construction floor, including after purity/leukocyte adjustment. The genomic branch completed 306/306 frozen tasks and shows small distributed decomposition effects while preserving nearly all Hallmark module ordering.

B2 therefore closes as a **layered static architecture**, not a master score and not substrate inheritance.

See:

- `docs/STAGE_B2_SOURCE_AUDIT_20260829.md`
- `docs/STAGE_B2_PREREGISTRATION_20260829.md`
- `docs/STAGE_B2_RPPA_AUDIT_20260829.md`
- `docs/STAGE_B2_GENOMIC_AUDIT_20260830.md`
- `docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md`

## Active phase: Stage C0 DNA-methylation source gate

The next regulatory-substrate layer is now prospectively frozen **before methylation acquisition or biological association**.

Primary source:

- PanCanAtlas merged HumanMethylation27/HumanMethylation450 beta-value matrix;
- GDC UUID `d82e2c44-89eb-43d9-b6d3-712732bf6a53`;
- expected size `5,022,150,019` bytes;
- expected GDC MD5 `5cec086f0b002d17befef76a3241e73b`;
- expected publication-era shared representation: 22,601 probes.

The 41.54 GB 450K-only matrix remains deferred as robustness-only.

C0 is a **source/schema/coverage audit only**. It may verify file identity, hashes, probe inventory, TCGA sample identity, and Stage A primary-tumor coverage. It may not inspect methylation relationships to RNA, RPPA, genomic burden, clinical outcomes, treatment, or any preferred SymC pattern.

Frozen C0 records:

- `config/stage_c0_methylation_source_plan.json`
- `docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md`
- `src/probe_stage_c0_methylation.py`
- `tests/test_stage_c0_methylation_contract.py`
- `RUN_STAGE_C0_METHYLATION_WINDOWS.bat`

Pre-acquisition CI is closed successfully. GitHub Actions run `33292691811` passed the full 29-test GRI v2 suite, confirmed the live source endpoint reports exactly `5,022,150,019` bytes, and built the tested Windows handoff.

Handoff:

- `CSA_STAGE_C0_METHYLATION_WINDOWS_20260830.zip`
- SHA-256 `69dcaa00e96c9668c97b1b20047d121db3f61533f6e6f5bb55e41f22a11916eb`

## What follows C0

A successful source gate does **not** authorize immediate biological association testing. Before Stage C1, the project must prospectively freeze the annotation/feature-reduction rules and then the full biological protocol.

That protocol must preserve all three complementary views:

1. **modal:** eigenspectrum/mode-resolved structure and participation;
2. **scalar:** compressed coordinates only where empirically justified;
3. **conglomeration:** module-to-module and whole-system organization across independently measured layers.

None of these static methylation quantities is biological chi. Substrate inheritance itself remains downstream of ordered or temporal evidence.

## Where to look

- `reviewer/README.md` - reviewer-facing evidence ladder
- `reviewer/CLAIM_EVIDENCE_MAP.md` - conservative claim-to-evidence map
- `reviewer/REVIEWER_MANIFEST.json` - machine-readable stage map
- `reviewer/SUBMISSION_RELEASE_CHECKLIST.md` - immutable submission packaging rules
- `notes/BUILD_STATUS.md` - canonical live handoff and exact next action
- `artifacts/MILESTONE_ARTIFACTS.md` - milestone hashes/provenance

## Repository role

GitHub is the durable reproducible spine: code, configs, tests, preregistrations, audits, compact results, hashes, and reviewer navigation. Multi-gigabyte raw datasets and bulky reproducible intermediates stay outside Git history and are identified by immutable source identifiers and cryptographic hashes.
