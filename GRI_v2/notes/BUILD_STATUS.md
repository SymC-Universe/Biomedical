# GRI v2 build status

Status date: 2026-08-28

## Scientific status

The historical scalar branch is closed. `CV/2` remains a historical comparator only and is not chi. No valid biological chi coordinate has yet been identified.

The active project is the Cancer Stability Atlas: a multidimensional map whose static axes remain separate from any future dynamical chi coordinate.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static primitives completed from saved v1.1.6 outputs: 20,309 genes, 638,693 within-cancer rows, 32 cancer types.
- Chi admission firewall defined and regression-tested.
- Stage A1 network definitions fixed before network results.
- MSigDB Hallmark v2026.1.Hs chosen as the first external module universe.
- `gri-v2` GitHub development branch established from `main`.

## Current blocker

Stage A1 requires the exact PanCanAtlas expression matrix and the Hallmark v2026.1.Hs gene-symbol GMT on the local Windows machine. The source expression matrix must match the frozen provenance hash in `inputs/SOURCE_RUN.json`.

## Exact next scientific/computational step

Run Stage A1 to compute `Cin_pairwise`, `Cin_pc1`, and `Cout` across eligible cancer types and Hallmark modules, with five-fold deterministic patient-hash leave-one-fold-out stability diagnostics.

No chi, criticality, tipping-point, or composite stability claim is allowed at Stage A1.

## User action

Download the Hallmark v2026.1.Hs symbols GMT if not already present, then run the Stage A1 local launcher from the latest milestone suite. Return the four named Stage A1 output files for audit.
