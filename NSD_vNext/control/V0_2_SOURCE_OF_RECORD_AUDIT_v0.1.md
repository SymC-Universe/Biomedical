# NSD v0.2 Source-of-Record Supersession Audit v0.1

**Status:** ACTIVE PREFREEZE AUTHORITY MAP  
**Date:** 29 September 2026

## Current prospective authorities

- N-B1 planning authority: `BIO_CHI_INTEGRATED_NB1_ADMISSION_ARCHITECTURE_PLAN_v0.4.md`.
- N-B2/N-B3 planning authority: `BIO_CHI_NB2_NB3_REPRESENTATION_SUFFICIENCY_PLAN_v0.4.md`.
- Round-1 independent APQ adjudication: `INDEPENDENT_APQ2_ADJUDICATION_LEDGER_v0.2.md`.
- Fresh packet candidate: `FRESH_UNTOUCHED_V0_2_DRAFT.json`, prefreeze only, execution unauthorized.
- Lane checkpoints: `LANE_CHECKPOINT_NB1_v0.2.json` and `LANE_CHECKPOINT_NB23_v0.2.json`.
- GOM audit: `GOM_V1_0_CONVEYOR_AUDIT_2026-09-29.md`.
- Exposure authority: `LONG_RUN_EXPOSURE_LEDGER_v0.1.json`.

## Superseded or development-only authorities

- N-B1 v0.3 is superseded for prospective planning by v0.4.
- N-B2/N-B3 v0.3 is superseded for prospective planning by v0.4.
- Same-cognition APQ ledgers for v0.2/v0.3 remain useful internal adversarial history but are not independent APQ-2 closure.
- `LONG_RUN_PACKET_v0.1.json` and its generated outputs are P0-D exposed development evidence only and cannot serve as untouched qualification.
- v0.1 long-run checkpoint/run IDs are historical and must not be used as v0.2 resume identities.
- Historical WORKING_INVESTIGATION entries that used the phrase APQ_CLOSURE for same-cognition review are superseded by the later GOM_AUDIT entry and this authority map.

## Stale-reference prohibitions

No controller, workflow, plan, or reproducibility instruction may:
- treat v0.3 as the active prospective plan;
- treat v0.1 long-run output as confirmatory;
- treat same-cognition review as independent APQ-2;
- resume a v0.1 scientific checkpoint into v0.2;
- reuse stale v0.1 active-run IDs;
- infer real-EEG local chi from any qualification-only result.

## Current gate

Round-2 full-text independent APQ on v0.4 remains required. Provider transport is temporarily rate-limited; authorized prefreeze work continues through the gate-side queue.
