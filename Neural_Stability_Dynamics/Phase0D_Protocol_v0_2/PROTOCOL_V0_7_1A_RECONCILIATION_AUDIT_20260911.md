# NSD Reconciliation Audit: General Protocol v0.7.1 + v0.7.1A

Date: 2026-09-11
Protocol basis: **General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum**
Status: **P0 RECONCILIATION AUDIT. PROSPECTIVE GOVERNANCE UPDATE ONLY. NO HISTORICAL RESULT IS REWRITTEN.**

## Bottom-line disposition

NSD remains a developing System Model + Structural Engine. P1 remains closed.

The v0.7.1A addendum does not invalidate the existing v0.7.1 reconciliation, P0Q1 freeze, P0Q1 result, or current scientific holds. It changes the prospective organization of P0 work by requiring an explicit distinction between P0-D discovery/mechanism mapping and P0-Q qualification, and by requiring Function Map and Limit Map to be treated as coequal scientific targets.

The existing P0Q1 result is preserved exactly:

- SSI-COV: `SURVIVES_P0Q1` for the frozen rank-signal qualification;
- Subspace DMD: `FAILS_P0Q1` because of 2/5 false admissions in the real-pole-only family;
- P0Q1 is not retuned or rescued;
- Phase 0C remains official FAIL / FAIL / FAIL;
- Phase 0D v0.1 remains unexecuted and superseded;
- no P1 or EEG execution is opened by this reconciliation.

## A.1 - Research-mode separation

**Previous state: PARTIAL.** The repository already used `P0Q1` language and separated prospective qualification from post-result diagnosis in practice, but the top-level protocol pointer and project-state language still treated P0 as a single generic mode.

**Required change: IMPLEMENT NOW.**

Use:

- `P0-D` for exploratory discovery, mechanism/rank diagnosis, response-surface mapping, already-viewed P0Q1 diagnostics, alternative estimator inspection, and Function/Limit landscape discovery;
- `P0-Q` for controlled estimator qualification on known-truth, known-bad, sensitivity, identifiability, and independently generated prospective qualification families;
- `P1` only after the complete MFR-14 and all existing v0.7.1 freeze requirements are satisfied.

Current classification:

- P0Q1 itself: historical **P0-Q prospective qualification**.
- Subspace-DMD P0Q1 failure diagnosis: **P0-D post-result mechanism/method mapping**.
- pyOMA2 point-estimator/uncertainty compatibility: **P0-Q external-reference qualification**, with derivational exploration retained as P0-D where rules are still being developed.
- new function/limit landscape: **P0-D**.

## A.2 - Function Map and Limit Map

**Previous state: BLOCKER / imbalanced.** Recent work was appropriately adversarial but increasingly failure-dominated: null stress, rank-gate refusal, P0Q1 failure diagnosis, and uncertainty compatibility. The repository did not yet expose a coequal Function Map.

**Required change: IMPLEMENT NOW.**

Create a P0-D landscape that maps, on known-truth synthetic systems, both:

### Function Map

- regions where each estimator recovers planted/observable structure;
- how recovery changes with mode count, decay, frequency separation, observability, noise, duration, channel count, conditioning, and crowding;
- all-rank singular spectra and cross-rank persistence;
- pole and carrier/subspace recovery against truth where truth exists;
- model-adequacy/open-channel diagnostics;
- whether different internal organizations yield similar observable behavior.

### Limit Map

- loss of identifiable rank signal;
- instability or false complexification;
- crowding/subspace-only transitions;
- weak-observability collapse;
- model-adequacy degradation;
- refusal or unresolved regions;
- estimator disagreement and ambiguity.

No single aggregate pass score will replace these maps.

## A.3 - Rare natural testbeds

**Current synthetic stage: NOT_APPLICABLE.** No natural event should be manufactured merely to fill this role.

Before real EEG, a `RARE_NATURAL_TESTBED` may be introduced only with domain-native rarity evidence, authenticity/confounding checks, base-rate context, and a selection rule independent of the NSD Engine output. Previously viewed rare cases may be P0-D/P0-Q evidence but may not independently confirm a rule developed from them.

## A.4 - Coverage architecture

**Previous state: PARTIAL / implicit.** Existing synthetic work contains ordinary, perturbed, boundary-like, and refusal cases, but their research roles were not explicitly registered.

**Required change: IMPLEMENT NOW.** Maintain `registries/COVERAGE_ARCHITECTURE.json` with:

- `NOMINAL_FUNCTION`;
- `PERTURBED_FUNCTION`;
- `BOUNDARY_OR_TRANSITION`;
- `RARE_NATURAL_LIMIT`.

At the current synthetic stage, the first three are active and `RARE_NATURAL_LIMIT` is `NOT_APPLICABLE_CURRENT_SYNTHETIC_STAGE`.

## A.5 - Claim-specific gates and partial results

**Status: PASS / strong alignment.** NSD already reports scalar, modal/carrier, participation, relational geometry, and system status separately; supports partial admission, refusal and unresolved states; and preserves the P0Q1 distinction between conditional estimator recovery and operational rank selection.

**Action:** preserve. Do not allow an unrelated full-system gate to suppress a narrower claim that does not logically depend on it.

## A.6 - Pathway-specific independence

**Previous state: PARTIAL.** The Atlas plan recorded several dependence sources but collapsed them into a single overall grade.

**Required change: IMPLEMENT NOW.** Record, where applicable, independence separately for:

- data;
- cohort/system;
- outcome/label;
- parameter/tuning;
- method/estimator;
- Atlas;
- source/literature;
- temporal/decisive-evidence timing.

The controlling test is whether shared information on that pathway could force the agreement being presented as evidence.

## A.7 - Scope is earned

**Status: PASS IN INTENT, formalization needed.** NSD currently avoids broad empirical claims and keeps the current ceiling at method development.

**Required change: IMPLEMENT NOW.** Use bounded scope labels such as:

- `SUPPORTED_IN_TESTED_REGIME`;
- `CROSS_REGIME`;
- `CROSS_SYSTEM`;
- `ROBUST_ACROSS_TESTED_LIMITS`;
- `REGIME_LIMITED`;
- `DOMAIN_LIMITED`;
- `UNRESOLVED_BEYOND_TESTED_RANGE`.

`UNIVERSAL` is not an allowed target scope.

## A.8 - Standard-output extension

**Current maturity: NOT YET REQUIRED AS P2 TOOL OUTPUT.**

**Safe P0 action: scaffold now.** P0 mapping records may already distinguish:

- `WORKS_HERE`;
- `STOPS_WORKING_HERE`;
- `NOT_KNOWN_HERE`.

This is descriptive mapping, not a release/tool qualification claim.

## A.9 - Milestone balance check

**Current verdict: FAILURE/LIMIT-DOMINATED.** Recent NSD work learned a great deal about refusal and failure boundaries but has not mapped the supported interior with equal depth.

**Required work-order change:** the next substantial P0 computation should prioritize Function-Map/mechanism mapping while the already-justified uncertainty and P0Q1 diagnostic work continues in parallel. A new failure-only P0Q2 should not be the sole next milestone.

## v0.7.1 safeguards that remain unchanged

The addendum does not weaken:

- MFR-14;
- frozen-holdout integrity;
- no retuning of P0Q1;
- native-model-first derivation;
- label/Atlas leakage firewall;
- uncertainty/INDETERMINATE requirement before P1;
- multiplicity accounting;
- comparator-selection freeze for P1;
- semantic and byte-integrity separation;
- known-bad production qualification;
- epistemic classification;
- smaller-claim preference.

## Current gate after reconciliation

`P0-D Function/Limit mapping + P0-D P0Q1 failure diagnosis + P0-Q uncertainty/reference qualification -> milestone balance audit -> only then evaluate whether a new P0-Q version/family is ready to freeze.`

P1 remains closed until the existing v0.7.1 requirements and the balanced evidence architecture introduced by v0.7.1A are satisfied.
