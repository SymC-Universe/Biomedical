# General Protocol v0.7.7 Adoption Note

Date: 2026-09-14
Status: **ACTIVE GOVERNANCE POINTER FOR CURRENT NSD WORK**

## Authoritative baseline
The current authoritative General Cross-Project Research Protocol is **v0.7.7, dated 13 September 2026, status `Active Baseline`**. It supersedes v0.7.6 and therefore supersedes the v0.7.4 baseline previously referenced by this branch.

The existing branch name ending in `protocol-v0.7.1` is retained only as a historical/execution identifier. It is not a statement of current protocol currency.

No historical run, gate, score, result, failure, survival status, hold, or evidence tier is rescored by this adoption.

## Adopted controls material to NSD
The project continues to inherit the complete protocol. In addition to previously integrated controls, current work now explicitly carries:

1. **Foundational-dependency robustness (v0.7.5 layer).** A result that becomes a material inherited foundation receives a proportional bounded robustness challenge when the protocol activation conditions are met. This cannot rescue a failed gate, retune a threshold, or convert qualification evidence into untouched confirmation.
2. **Active-run monitoring and monitor-coverage audit (v0.7.6 layer).** Liveness and scientific progress are distinct; recovery/checkpoint/supersession state must be verified for material active dependencies; retry loops require a circuit breaker.
3. **Current-protocol/source-of-record bootstrap (v0.7.7 layer).** New research sessions load the current GP and current repository/run state before inheriting active work, and duplicate work is not launched merely because conversational context is incomplete.
4. **Reader-first communication (v0.7.7 layer).** Status and research reports prioritize clear prose and real information over decorative formatting.
5. **Bounded scope language.** Scope is earned across tested systems and regimes. Universality is not a protocol target.

## Current monitor-coverage determination
The present P0-D21 through P0-D23 workloads are short-lived GitHub Actions push workflows with direct Actions status, step status, logs, artifact creation, artifact digests, and branch-wide validation. They do not currently depend on an external multi-hour process, remote human action, or long-lived mutable compute state.

Accordingly, a separate persistent watchdog is **not presently proportionate or scientifically useful** for these short runs. This is an explicit monitor-coverage determination, not an absence of monitoring.

Coverage for the current class is:

`push event -> dedicated workflow status/steps -> artifact + digest -> branch-wide validation -> source-of-record result note`

A persistent watchdog/recovery controller becomes expected if a later workload acquires a long runtime, external dependency, mutable checkpoint state, nontrivial restart path, or credible silent-stall mode. That determination must be revisited when the dependency class changes.

## Scientific state preserved
- NSD System Model v1.0 remains locked.
- Historical Phase 0C remains `FAIL / FAIL / FAIL`.
- Phase 0D v0.1 remains superseded before execution, not failed.
- Frozen P0Q1 remains source-of-record: SSI-COV `SURVIVES_P0Q1`; Subspace DMD `FAILS_P0Q1`.
- P1 remains CLOSED.
- Atlas remains independent of Engine construction and current P0-D interpretation.
- No recovery threshold, `chi_system` definition, empirical Atlas zone, final comparator, confidence rule, MFR-14 completion, or P1 scoring design is frozen by this adoption.

## Current execution consequence
P0-D exploratory falsification may continue without additional user approval where it does not alter frozen science. After the remaining null-floor and deliberate-refusal challenges, the project must perform a v0.7.7 milestone/foundational-dependency/monitor-coverage audit before proposing any recovery-related P0-Q promotion.
