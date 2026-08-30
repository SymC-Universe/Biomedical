# Stage C0 methylation source-gate handoff record

Date: 2026-08-30

## Frozen protocol

Stage C0 freezes the source identity, publication-era platform representation, sample-matching rules, and allowed source/schema operations before any DNA-methylation biological association is inspected.

Canonical records:

- `config/stage_c0_methylation_source_plan.json`
- `docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md`
- `src/probe_stage_c0_methylation.py`
- `tests/test_stage_c0_methylation_contract.py`
- `RUN_STAGE_C0_METHYLATION_WINDOWS.bat`

## Pre-acquisition CI

- Workflow: `GRI v2 Stage C0 methylation source gate`
- Successful handoff-build run: `33292691811`
- Tested commit: `009245507d8fc22740bc24f57f878a1fd73d5eb4`
- Full GRI v2 test suite: 29/29 PASS
- Live GDC metadata probe: PASS
- Frozen source UUID: `d82e2c44-89eb-43d9-b6d3-712732bf6a53`
- Endpoint content length: `5,022,150,019` bytes, exactly matching the preregistered source
- Biological association performed by CI: no

## Windows handoff

- File: `CSA_STAGE_C0_METHYLATION_WINDOWS_20260830.zip`
- SHA-256: `69dcaa00e96c9668c97b1b20047d121db3f61533f6e6f5bb55e41f22a11916eb`
- GitHub Actions artifact ID: `9726452527`
- Role: exact tested Windows local-execution package for Stage C0 source acquisition and source/schema/coverage audit.

The handoff contains an internal `SHA256SUMS.txt` for its payload. It intentionally does not contain the approximately 5.02 GB methylation matrix or the Stage A profile cache. The launcher asks the user to select the existing frozen Stage A `hallmark_profile_cache.npz` and acquires the exact methylation source from the frozen GDC UUID.

## Claim ceiling

This handoff can establish source identity, integrity, schema, probe inventory, sample identity, and primary-tumor coverage only. It cannot establish methylation-RNA/protein/genomic association, causality, substrate inheritance, dynamics, damping, criticality, an optimum, treatment response, a master stability score, or biological chi.
