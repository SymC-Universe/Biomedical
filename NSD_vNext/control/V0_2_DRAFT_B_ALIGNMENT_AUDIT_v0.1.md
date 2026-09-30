# NSD v0.2 Draft-B / v0.5 / Packet-APQ Alignment Audit v0.1

**Status:** PREFREEZE / OUTCOME-BLIND / NO EXECUTION AUTHORITY  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum  
**Scope:** mechanical and semantic consistency audit only. No v0.1 scientific outcome values were inspected.

This audit compares `FRESH_UNTOUCHED_V0_2_DRAFT_B.json` against the revised v0.5 architecture authorities and `V0_2_PACKET_LEVEL_APQ_CHECKLIST_v0.2.md`. It does not freeze final cases, seeds, tolerances, or execution authority.

## N-B1 alignment

Already aligned:

- generator-defined C membership is separate from fit quality;
- P/S/T/F/O/M/R/N/I/U namespaces are represented;
- candidate seeds are explicitly non-final;
- Function and Limit classes remain separated;
- two retention controls are named;
- Wilson intervals are reporting-only;
- v0.1 scientific values are excluded as design inputs;
- real-EEG local chi remains unlicensed.

Must close before exact packet APQ/freeze:

1. **U applicability mismatch.** Draft-B `applicability_contract.default_required` still includes U, while v0.5 makes U conditional and non-licensing unless a separate quantitative U rule is prospectively APQ-qualified and frozen. The exact packet must remove U from the default required set and enumerate U applicability explicitly by truth class.
2. **Per-truth applicability not exhaustive.** Draft-B uses a default map plus special R cases. v0.5 requires applicability to be declared by truth class before generation. The exact packet must carry an explicit P/S/T/F/O/M/R/N/I/U map for every final truth identity.
3. **Final seed/replicate identity not frozen.** Draft-B seeds derive from a superseded v0.4 blob and are candidate-only. Final replicate count, seed-generation rule, RNG identity, and final seeds remain packet-level APQ items.
4. **Numerical-only N/I tolerances absent.** Exact optimizer reproduction, objective equality, profile-optimum reproduction, tied-minimum equality, and profile-domain edge rules require frozen numerical identities and provenance.
5. **Generator/source identity incomplete.** Generator names and parameters exist, but final source implementation identity, parameter-domain contract, and analytical proof/validator for preserving observation transforms are not yet bound.
6. **Observation/reference transforms incomplete.** Gain and mixture examples are named, but exact transform functions, latent/observed object semantics, and preservation/refusal validator rules must be explicit.
7. **Sampling/alias rule incomplete.** Rates and same-path intent exist, but exact decimation/filter semantics, continuous-lineage alias-safety calculation, and failure state must be bound.
8. **Search/profile procedure incomplete.** Multistart set/order, deterministic rerun rule, profile grid/domain/source identity, and complete serialization contract remain to be frozen.
9. **FRAMEWORK_NOT_OPERATIONAL not yet machine-bound.** v0.5 defines the scientific rule; the exact packet/schema must encode all four triggers without adding a post-result threshold.
10. **Row/refusal grammar needs final schema binding.** Multi-label provenance, NEED_MORE_INFO precedence, failure retention, and denominator accounting must be mechanically explicit.

## N-B2/N-B3 alignment

Already aligned:

- exact sufficiency and recoverability are separate namespaces;
- primary recovery is deterministic/noiseless;
- stochastic recovery is excluded unless separately qualified;
- physical metric and similarity transformation law are declared;
- autonomous/input/observed/time-varying target families remain distinct;
- switching phase and stationary-surrogate semantics are represented;
- learned DMD/Koopman is excluded from v0.2 claim scope;
- conclusions remain suite/target/observation-contract specific.

Must close before exact packet APQ/freeze:

1. **Suite is not exhaustively enumerated.** Draft-B contains component systems/operators but not the final case list, equivalence classes, held-fixed representation, queried target, Function/Limit role, and expected mathematical equality/difference for every case.
2. **x0 contracts are missing.** v0.5 target and similarity semantics require explicit initial-condition identities and normalization rules where x0-dependent targets are used.
3. **Observation-compatible-set rule is descriptive only.** `K_O(y)` membership must be executable for each primary recoverability case using only declared observations.
4. **Aliasing control is not instantiated.** Draft-B records `REQUIRED_IN_EXACT_PACKET_BEFORE_FREEZE`; the exact packet must contain an explicit pair/set of distinct continuous models compatible with the same sampled information unless extra information resolves them.
5. **Peak-search fields conflict in specificity.** The older `peak_refinement` field says to refine the best grid neighborhood, while v0.5 requires a global/adaptive search over all candidate maxima plus an independent dense/reference check. The exact packet must use one unambiguous global procedure.
6. **Target formulas/domains need packet binding.** Target names are present, but formula, norm, time domain, tie/degeneracy rule, and numerical verification identity must be attached to each target.
7. **Numerical identity tolerances need role provenance.** Current matrix/spectrum/invariant tolerances are candidate numerical values only. Packet APQ must justify their computational role and freeze exact use without turning them into scientific-effect thresholds.
8. **Matched B/C recipes are not enumerated.** Exact same-A/different-B and same-A,B/different-C case identities and target applicability must be declared.
9. **Partial-observation and misspecification cases are not fully instantiated.** Required architecture classes need final model/observation identities and compatible-set expectations.
10. **Generator/provenance validator and final implementation are not yet bound.** The v0.1 conveyor is not final v0.2 implementation authority.

## Cross-lane and identity closure

- Actual final case-ID disjointness must be proven after final IDs are generated; a policy flag alone is insufficient.
- Final architecture blobs must be the versions that clear independent re-review.
- Packet/config, code, dependency, environment, RNG/seed identities, evidence schemas, checkpoint schema, and result-landing audit must be bound in one final identity manifest.
- Resume must refuse any identity mismatch.
- GitHub remains mechanical and terminal state remains `SCIENTIFIC_REVIEW_READY`.

## Disposition

Draft-B remains a useful preparatory scaffold but is not internally sufficient for packet freeze. The listed items are predeclared closure debt, not failures. Architecture re-review remains the current scientific gate. None of these items grants execution authority or licenses substantive compute.
