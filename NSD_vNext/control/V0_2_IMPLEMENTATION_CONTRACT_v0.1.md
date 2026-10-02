# NSD v0.2 Implementation Contract Skeleton v0.1

**Status:** PREFREEZE MECHANICAL DESIGN / NO EXECUTION AUTHORITY  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum

This document translates the v0.5 scientific authorities and the implementation-gap audit into mechanical requirements. It does not choose final scientific parameters, thresholds, case identities, or verdicts.

## General interface

The final executable must accept only a frozen packet plus a frozen code/dependency/environment manifest. Every consumed scientific field must be explicit in the packet. Unknown or missing fields cause a contract refusal rather than a default scientific choice.

The executable may generate, fit, compute, serialize, validate identity, checkpoint, resume, hash, merge, and package raw evidence. It may not assign scientific PASS/REFUSE states, rank representations, choose thresholds, alter a generator/metric/target, combine lane verdicts, or promote a claim.

## N-B1 implementation requirements

The final generator registry must implement every frozen N-B1 generator identity exactly. Draft-B-only names are not considered implemented until covered by tests.

Observation/reference transforms must be explicit functions with their own frozen identity and must not be folded silently into the base generator.

Same-path paired-rate data must be generated from one frozen fine-path identity followed by the exact frozen transform. Sampling metadata and alias-safety inputs must be serialized.

Search integrity must record every required start, terminal status, objective value, selected optimum, deterministic reproduction check, and numerical-only tolerance identity.

Profile evidence must use the frozen profile implementation and serialize the full profile points needed for later structural I-channel adjudication. No profile cutoff may be invented in code.

Every failure/non-convergence produces a row with failure provenance. Rows are never silently omitted.

## N-B2/N-B3 implementation requirements

Configuration parsing must use the final packet field names directly. No v0.1 key alias may silently substitute for a missing v0.2 field.

The implementation must support the frozen A/B/C/G/x0 identities and the full similarity transformation contract.

Stationary targets must expose raw curves and target values separately. Time-varying targets must consume the frozen switch order, phase, boundaries, and continuity semantics.

Peak computation must implement the final frozen global/adaptive algorithm plus an independent reference check. A base-grid maximum alone is insufficient.

Exact-sufficiency evidence and observation-conditioned recoverability evidence must use separate namespaces. The recovery path may access only information present in the frozen observation contract and may not read hidden exact descriptors.

The primary v0.2 recovery path is deterministic/noiseless unless a later separately qualified stochastic extension changes that contract.

## Generator/provenance preflight

Before any target evidence is produced, the executable must run the frozen generator/provenance validator and refuse execution on truth-label, held-fixed, similarity, switch, sampling, case-disjointness, packet/config, code/dependency, or environment mismatch.

## Checkpoint and resume

Each checkpoint binds:

- lane and stage;
- authority and packet/config hashes;
- final code/dependency/environment identity;
- final case and RNG/seed identity where applicable;
- completed case IDs and artifact hashes;
- incomplete case IDs;
- active run identity;
- next exact mechanical action;
- stop/refusal reason.

Resume refuses any identity mismatch. A completed case is not recomputed unless its artifact is absent or hash-invalid.

## Required tests before final execution authority

1. every frozen packet field is consumed or explicitly declared metadata-only;
2. unsupported generator/config values fail closed;
3. observation transforms are explicit;
4. same-path sampling lineage is reproduced;
5. similarity invariants reproduce under transformed metric/operators;
6. switching phase and chronological order are honored;
7. global peak/reference checks agree within numerical-only tolerance;
8. recoverability code cannot access hidden exact descriptors;
9. generator/provenance mismatches stop before outcome evaluation;
10. lane case IDs are disjoint;
11. checkpoint mismatch refuses resume;
12. GitHub output schemas cannot encode a scientific verdict or combined lane PASS;
13. terminal automation state is SCIENTIFIC_REVIEW_READY.

The final implementation cannot be written against unresolved scientific fields. v0.5 architecture re-review and exact packet-level APQ/freeze remain prior gates.
