# GRI v2 / Cancer Stability Atlas

Status: DEVELOPMENT ARCHITECTURE, NOT A VALIDATED CANCER TOOL

This branch begins after the frozen GRI v1.1.6 scalar experiment. It does not repair or rescue that result.

## Active rules

- `CV/2` is the historical scalar comparator. It is not chi.
- `chi` is reserved for a dynamical coordinate of the form `Gamma/(2*Omega)` and is unavailable until all admission gates are earned.
- Static RNA and multiomic observables remain independent map axes rather than being folded into chi.
- `chi = 1`, if a valid chi is eventually measured, is a balance boundary of the applicable model and not a presumed cancer optimum.
- No feature receives privileged status because it appeared in the historical manuscript.

## Current phase

Stage A0 is complete from the saved v1.1.6 outputs. Stage A1 is the next executable phase: static Hallmark-network organization on the exact PanCanAtlas source matrix, with no chi and no CV/2 in the network definitions.

See `WORKFLOW.md`, `docs/NEXT_PHASE.md`, and `notes/BUILD_STATUS.md`.

## Repository role

GitHub is the durable reproducible spine: code, configs, tests, scientific/epistemic specifications, compact summaries, and milestone hashes. Large raw datasets and bulky derived tables are not duplicated here when they are reproducible from the recorded source artifacts. Full milestone suites are also retained in ChatGPT and recorded by SHA-256 in `artifacts/MILESTONE_ARTIFACTS.md`.
