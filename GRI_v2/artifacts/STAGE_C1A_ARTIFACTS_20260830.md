# Stage C1A artifact and handoff record

Date: 2026-08-30

## Final verified repository state

- branch: `gri-v2`
- commit: `364d8b85224343055674366ff3d5a34588961700`
- commit role: closes the external C1A source gate, fills exact source provenance, records the source audit, repairs extraction-root hash manifests, and makes the Windows handoff a true one-picker workflow.

## CI verification

General GRI v2 test workflow:

- run: `33318328260`
- conclusion: **SUCCESS**

Final C1A annotation source/handoff workflow:

- run: `33318328284`
- conclusion: **SUCCESS**
- every source acquisition, frozen annotation extraction, portable artifact audit, Windows handoff build, source-artifact upload, and handoff upload step completed successfully.

No methylation beta-value biological association was performed by either workflow.

## Final Windows handoff

- artifact name: `CSA_STAGE_C1A_PROBE_INVENTORY_WINDOWS_20260830`
- GitHub artifact ID: `9734154387`
- SHA-256: `6663ca29588111d3da893257d3f0f67442ba8feb05282cfa3317068fc859b7e5`
- role: exact 22,601-probe local annotation/mask inventory; reuses the already-audited 5.02 GB methylation TSV and prompts only for that one local file.

Independent post-download verification:

- outer ZIP SHA-256 matched the GitHub artifact digest exactly;
- internal `SHA256SUMS.txt` passed for all 8 payload files;
- Windows driver contains one file-picker invocation only: the existing methylation TSV;
- bundled annotation export, Chen cross-reactive ID list, and C1A source summary are selected automatically;
- the local engine streams the full methylation source to verify SHA-256 and recover the first tab-delimited probe-ID field only; beta values are not parsed for biological analysis.

## Final source-gate evidence artifact

- artifact name: `gri-v2-stage-c1a-annotation-source-gate`
- GitHub artifact ID: `9734154208`
- SHA-256: `3d6122516971c642b466c5c82e861304503eb7b36a77a2c4ae979a1c0abbd5d6`

Independent post-download verification:

- outer ZIP SHA-256 matched the GitHub artifact digest exactly;
- corrected extraction-root-relative `SHA256SUMS.txt` passed for all 7 evidence files.

Key evidence hashes:

- annotation tarball SHA-256: `249b8fd62add3c95b5047b597cff0868d26a98862a47cebd656edcd175a73b15`
- Chen source SHA-256: `4e962d36821f6f6fcd8b81cc0558090c028e54fbdb2c039a5712f9b471d9d89e`
- portable annotation export SHA-256: `a7f83233f97c3933752d74b8042e967de88df20eba2cf477a536136631a8da17`
- compact Chen ID export SHA-256: `078e95716af2b20c3515f59d09310d20c43deb5ed8ba8d1b70885810acde2179`
- annotation object inventory SHA-256: `838aee6a51effd979280bfde4bc9aa57c4f629d901aef2b1c0c2700d3166664c`

## Scientific boundary

This milestone establishes source provenance and a tested local annotation/probe-ID gate only. It does not establish methylation biology, cross-assay coupling, causal regulation, substrate inheritance, dynamics, a phase transition, an optimum, or biological chi.

C1 beta-value analysis remains blocked until the local exact-probe inventory passes, is audited, and the full modal + scalar + conglomeration formulas/nulls/seeds/missingness/promotion rules are frozen prospectively.
