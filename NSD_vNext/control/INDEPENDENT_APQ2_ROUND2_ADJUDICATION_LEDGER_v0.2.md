# NSD Independent APQ-2 Round-2 Adjudication Ledger v0.2

**Status:** ROUND-2 COMPLETE / MATERIAL REVISIONS ACCEPTED / v0.5 RE-REVIEW REQUIRED  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum  
**Workspace:** Undermind `b9de6e85-abe4-401b-a922-4a7d3aeebc3f`

No majority vote is used. Every BLOCKER and MATERIAL objection is adjudicated on its own methodological content. No v0.1 scientific result payload was inspected or used in this adjudication.

| Review | ID | Severity | Objection | Disposition | Prospective correction | Re-review |
| --- | --- | --- | --- | --- | --- | --- |
| N-B1 | NB1-R2-B1 | BLOCKER | generating-family contract and per-channel decision rules remain insufficiently operational | ACCEPTED | v0.5 binds generator-defined C semantics, fail-closed channel grammar, truth-class applicability, and packet-level decision-rule requirements | yes |
| N-B1 | NB1-R2-M1 | MATERIAL | operating characteristics need Monte Carlo uncertainty and explicit non-convergence/failure accounting | ACCEPTED | report raw counts plus prospectively fixed binomial uncertainty by truth class; estimator failures remain separate labeled outcomes and never disappear from denominators | yes |
| N-B1 | NB1-R2-M2 | MATERIAL | sampling/observation model and search-failure handling are not explicit enough | ACCEPTED | v0.5 binds alias-safe sampling semantics, same-path decimation, observation mapping rules, deterministic search-reproduction requirements, and fail-closed estimator-route states | yes |
| N-B1 | NB1-R2-M3 | MATERIAL | practical-identifiability channel names a profile method without an executable decision criterion | ACCEPTED_MODIFIED | v0.5 defines a structural, cutoff-free regular-interior profile eligibility screen; nonregular/boundary/multibasin profiles return NEED_MORE_INFO rather than semantic refusal | yes |
| N-B2/N-B3 | NB23-R2-B1 | BLOCKER | exact sufficiency, numerical verification, and recoverability are not operationally separated | ACCEPTED | v0.5 limits exact claims to an exhaustively enumerated frozen suite, defines exact representation-equivalence classes independently of numerical tolerances, and defines observation-conditioned compatible-model sets separately | yes |
| N-B2/N-B3 | NB23-R2-B2 | BLOCKER | primary target functionals are labels rather than executable mathematical objects | ACCEPTED | v0.5 gives formulas/domains for spectral abscissa, physical-metric propagator gain, peak-time/direction sets, response curves, integrated burden, impulse input-output response, observed recovery, and switched propagators | yes |
| N-B2/N-B3 | NB23-R2-M1 | MATERIAL | similarity invariance does not yet bind all transformed objects | ACCEPTED | v0.5 binds A', B', C', G', x0' and invariant comparison rules; coordinate-dependent diagnostics are excluded from invariant claims | yes |
| N-B2/N-B3 | NB23-R2-M2 | MATERIAL | Function/Limit and switched cases lack matched-pair construction semantics | ACCEPTED | v0.5 requires explicit pair identities, held-fixed representations, target agreement/difference question, switching order/phase/continuity, and frozen surrogate construction | yes |
| N-B2/N-B3 | NB23-R2-M3 | MATERIAL | peak and sampling validation need global checks; DMD/Koopman scope is ambiguous | ACCEPTED | v0.5 requires global/adaptive peak verification plus an independent reference check; v0.2 excludes learned DMD/Koopman estimators from the claim scope | yes |
| Integrated | INT-R2-B1 | BLOCKER | unfrozen packet must remain a hard release gate | ACCEPTED | execution_authorized remains false until architecture re-review, exact packet APQ, final code/environment/case freeze, and checkpoint manifest closure | yes |
| Integrated | INT-R2-B2 | BLOCKER | a shared generator/provenance defect could invalidate both lanes | ACCEPTED | add an outcome-blind independent generator/provenance validation stage before evaluation; disjoint confirmatory case identities remain mandatory | yes |
| Integrated | INT-R2-M1 | MATERIAL | exposed-development lineage and cross-lane result access need enforceable firewalls | ACCEPTED | preserve v0.1 quarantine, auditable lineage, disjoint prospective cases, and no cross-lane outcome access before both freezes | yes |
| Integrated | INT-R2-M2 | MATERIAL | qualification and representation sufficiency must never collapse into one decision | ACCEPTED | N-B1 and N-B2/N-B3 retain separate verdict namespaces and separate result packages; no combined PASS exists | yes |
| Integrated | INT-R2-M3 | MATERIAL | checkpoint/resume and workflow authority need immutable scientific identity and a human review boundary | ACCEPTED | final checkpoint binds protocol/code/environment/cases/seeds/artifact hashes; automation stops at SCIENTIFIC_REVIEW_READY and cannot rank/promote; researcher + ChatGPT scientific sign-off is required | yes |
| Integrated | INT-R2-m1 | MINOR | Monte Carlo error, failures, and refusal patterns must remain stratified | ACCEPTED | v0.5 reporting keeps truth-class counts, intervals, failures, and multi-label refusals separate with no aggregate score | no |

## Disposition

Round-2 architecture review found valid blockers. They are not reasons to abandon the program; they identify missing executable semantics between the architecture and the exact packet. Those corrections are incorporated prospectively in N-B1 v0.5 and N-B2/N-B3 v0.5.

Because the accepted changes are material, v0.5 requires isolated re-review before architecture closure. Exact packet-level APQ and final freeze remain downstream gates. Substantive computation is not authorized.
