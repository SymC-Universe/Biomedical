# GRI v2 build status

Status date: 2026-08-28

## Scientific status

The historical scalar branch is closed. `CV/2` remains a historical comparator only and is not chi. No valid biological chi coordinate has yet been identified.

The active project is the Cancer Stability Atlas: a multidimensional predictive-tool development program whose static axes remain separate from any future dynamical chi coordinate.

The development target is not the historical manuscript and not preservation of prior GRI claims. The target is the best falsifiable model supported by the data. Old components may survive only if they earn retention under the new architecture.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static primitives completed from saved v1.1.6 outputs: 20,309 genes, 638,693 within-cancer rows, 32 cancer types.
- Chi admission firewall defined and regression-tested.
- Stage A1 network definitions fixed before network results.
- MSigDB Hallmark v2026.1.Hs chosen as the first external module universe.
- `gri-v2` GitHub development branch established from `main`.
- Project objective explicitly reset to predictive-tool discovery rather than defense or resubmission of the historical manuscript.

## Development sequence

1. Static map: quantify independently defined variability, lineage, and network-organization coordinates.
2. Multiomic map: add independently measured substrate/context layers without folding them into chi.
3. Dynamic benchmark: test ordered perturbation/time-course systems against DNB and ordinary network baselines.
4. Candidate dynamical coordinate: only if the data support admissible `Gamma` and `Omega`, test whether chi adds predictive information.
5. Freeze the selected model before external validation.
6. External validation and calibration determine whether a predictive tool has been earned.
7. Only after that point is a replacement manuscript or resubmission strategy constructed around the validated result.

## Current blocker

Stage A1 requires the exact PanCanAtlas expression matrix and the Hallmark v2026.1.Hs gene-symbol GMT on the local Windows machine. The source expression matrix must match the frozen provenance hash in `inputs/SOURCE_RUN.json`.

## Exact next scientific/computational step

Run Stage A1 to compute `Cin_pairwise`, `Cin_pc1`, and `Cout` across eligible cancer types and Hallmark modules, with five-fold deterministic patient-hash leave-one-fold-out stability diagnostics.

No chi, criticality, tipping-point, historical GRI recovery, or composite stability claim is allowed at Stage A1. Stage A1 is a map-building measurement pass.

## User action

Download the Hallmark v2026.1.Hs symbols GMT if not already present, then run the Stage A1 local launcher from the latest milestone suite. Return the four named Stage A1 output files for audit.
