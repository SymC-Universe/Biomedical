# GRI Final v0.7.5 delta audit

**Date:** 2026-09-13  
**Status:** CURRENT-STATE DELTA AUDIT  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.pdf`  
**Prior delta audit:** `GRI_V074_DELTA_AUDIT_20260912.md`  
**Retroactive status changes:** NONE

## Purpose

This record captures only the GRI-relevant delta introduced by Final v0.7.5. All v0.7.4 controls remain in force. Existing Stage C1 and post-C1 evidence retain their earned historical status; v0.7.5 does not upgrade P0-Q qualification into untouched P1 confirmation.

## 1. New Section 11.3 control

A passed upstream result may be inherited downstream only at the support level actually earned. Before a result becomes a material upstream dependency, a bounded robustness challenge is considered when all three conditions apply:

1. substantial downstream inference, expense, or difficult-to-reverse design materially depends on it;
2. a scientifically legitimate stronger test could plausibly alter admissibility, interpretation, or selected specification;
3. the challenge is feasible at cost proportionate to the downstream risk.

Allowed outcomes are `ROBUSTNESS_SUPPORTED`, `FOUNDATION_REOPENED`, `INDETERMINATE`, and `INVALID_CHALLENGE`.

When the need is identified after the original result was already inspected, the work is a **post-result robustness audit**. It may improve the next dependency decision but cannot be represented as prospectively predeclared evidence.

## 2. Immediate GRI trigger

The completed Stage C1 / post-C1 lineage now matters as a read-only foundation for the Chi_bio admission-or-falsification program. That makes provenance and restart semantics material even though no rerun is needed.

The post-C1 v2.2 implementation used resumable per-cancer pickle checkpoints. Inspection of the historical worker identified a provenance weakness: resume checkpoints are not themselves cryptographically bound to the final result archive as evidentiary objects. This is an implementation-level vulnerability in future inheritance if a recovery checkpoint were allowed to stand in for a final result.

This observation does **not** establish that the completed post-C1 result is wrong. The final returned result archive has a separate integrity and reconstruction record.

## 3. Bounded post-result challenge

The bounded challenge is recorded in:

`docs/GRI_POST_C1_V22_FOUNDATIONAL_ROBUSTNESS_AUDIT_20260913.md`

The challenge asks whether the **final returned result package**, rather than a recovery checkpoint, is sufficiently authenticated and internally reconciled to remain the P0-Q foundation for downstream read-only dependency analyses.

Outcome: `ROBUSTNESS_SUPPORTED` for the final result package at its existing P0-Q support level.

Dependency effect:

- final hashed post-C1 result remains admissible as read-only P0-Q source evidence;
- `WORKING_STATE` is restricted to recovery/provenance explanation and may not satisfy downstream evidentiary identity requirements;
- no historical p/q value, promotion state, claim ceiling, or Chi_bio status changes;
- biological Chi remains `NOT_ADMITTED`.

## 4. Export-schema consequence

`config/gri_Chi_bio_internal_export_schema_v0_1.json` used the field `source_working_state_or_result_identity`, which could blur recovery-state identity and result-output identity despite the schema's broader semantic-identity rules.

Version 0.2 replaces that ambiguity with explicit, non-interchangeable roles:

- required final post-C1 result SHA-256 and `RESULT_OUTPUT` identity;
- optional recovery checkpoint identity tagged `RECOVERY_PROVENANCE_ONLY`;
- explicit prohibition on using `WORKING_STATE` to satisfy final result provenance.

The v0.1 file is retained as historical control-plane lineage.

## 5. Stopping rule

The bounded challenge is closed once the final result identity, package integrity, canonical reconstruction, worker-lineage equivalence, and S2 correction status are all reconciled and downstream export semantics exclude recovery checkpoints from evidentiary substitution.

No additional C1 or post-C1 rerun is authorized by this audit. Further robustness escalation requires a new scientific reason under v0.7.5 Section 11.3.

## 6. Current project control

**STATUS:** Stage C1 and post-C1 v2.2 remain valid at their earned support levels; post-C1 final-result inheritance is robustness-supported; Chi_bio remains not admitted.

**CURRENT GATE:** finish pre-outcome Chi_bio source/provenance and D-L freeze hardening without opening real SCC25 outcomes under an incomplete empirical freeze.

**NEXT ACTION:** continue CollecTRI provenance qualification and pre-outcome G2/B3/D-L hardening; retain final C1/post-C1 archives read-only.

**WHY:** the completed TCGA foundation no longer requires another internal rerun. The next scientific value lies in independent temporal/perturbational architecture and properly frozen external evidence.

**USER ACTION:** NONE.
