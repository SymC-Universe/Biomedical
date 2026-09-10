# NSD Phase 0D v0.2 P0 Artifact Identity

Date: 2026-09-10

Two independently identified artifacts exist for this P0 reconciliation milestone and must not be described as byte-identical.

## Downloadable local validation package

Filename: `NSD_Phase0D_v0_2_Protocol_Reconciliation_P0_20260910.zip`

SHA-256: `0700897c98e13a99cca468e131d11834e3afabd545603a5825fba8fa4b901c07`

The extracted local package was verified in the development environment with 36 passing tests, successful P0 development-runner execution, Python compilation, JSON parsing, and a fail-closed confirmatory runner that exited before scientific generation because no P1 readiness record exists.

## GitHub source snapshot

Branch: `neural-stability-dynamics-phase0d-v0.2-protocol-v0.7.1`

Milestone source commit: `7f5c65d332ba260c68b21dd71fa524dd71da2620`

Workflow-addition commit: `db1405b8540bfc99017caeb01d1b46a4ea2ee8bb`

The GitHub tree is a source snapshot of the same P0 reconciliation design, but some files were serialized/reformatted through the repository connector while being written. Therefore the local ZIP manifest must not be used to claim byte identity with GitHub source files. Git commit identity authenticates the GitHub tree; the ZIP SHA-256 authenticates the downloadable package.

No GitHub CI pass is claimed here unless and until an actual workflow run is observed and audited.

This distinction is intentional compliance with the rule that hashes authenticate bytes while semantic checks authenticate meaning.
