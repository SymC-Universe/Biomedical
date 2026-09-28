# Bio Chi C1Q-RS Search-Route Qualification Plan v0.1

**Status:** APQ-2 SUBSTANTIAL DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 15.4  
**Lifecycle stage:** Stage 3, P0-Q estimator/search qualification  
**Parent evidence:** Function Map, likelihood-basin root cause, recurrence-seed rescue

## Scientific target

### Native question

Can the current C1Q likelihood be searched more reliably across its intended continuous-lineage C interior by preserving the full legacy optimized start set and adding one truth-blind recurrence/covariance start when admissible, without changing the model, parameter count, likelihood, or scientific claim ceiling?

### Residual problem

The completed Function Map identified reproducible boundary-collapse fits. The likelihood-basin diagnostic established that many were worse local basins, and the truth-blind recurrence-seed diagnostic reached the better basin in a substantial subset. The unresolved question is whether this repair can be incorporated as a search-route candidate without creating new failures or obscuring existing semantic refusals.

### Smallest live claim

A versioned search candidate, C1Q-RS, may improve optimization of the existing C1Q likelihood. It is not a new biological model and cannot establish that unknown biology belongs to family C.

## Candidate definition

C1Q-RS keeps unchanged:

- the four C1Q parameters \(A,\rho,f_d,g\);
- all transforms and \([-8,8]^4\) raw bounds;
- C-family \(|g|<1\) parameterization;
- steady-state innovations likelihood;
- burn-in;
- frequency bounds;
- parameter count \(k=4\);
- BIC formula;
- all existing legacy start generation and scoring.

For a declared \`max_optimized_starts=N\`, C1Q-RS first identifies the exact same top \(N\) legacy starts that current C1Q would optimize. If the frozen recurrence/covariance seed is admissible, it is added as **one additional forced optimized start**. It does not displace a legacy start. Thus C1Q-RS optimizes \(N\) or \(N+1\) starts.

If the recurrence seed refuses or is invalid, C1Q-RS must fall back to current C1Q behavior without changing the model or start set.

The seed construction is exactly the one frozen in \`BIO_CHI_C1Q_RECURRENCE_SEED_PLAN_v0.1.md\`: lag-12 normalized positive-lag covariance, least-squares second-order recurrence, conditional linear \(A,Ag\) fit, explicit projection record, then raw conversion.

## Foundational mechanical invariant

On the same signal, environment, optimizer settings, and legacy start budget,

\[
\mathrm{NLL}_{\mathrm{C1Q-RS}}
\le
\mathrm{NLL}_{\mathrm{legacy\ C1Q}}
\]

within the declared numerical comparison tolerance, because every legacy optimized start remains available and the recurrence start can only add a candidate basin.

Violation is an implementation defect, not a scientific result.

## Inputs and provenance

Primary Function Map source:
- run \`36368579380\`;
- artifact \`10948327278\`;
- digest \`sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c\`.

Root-cause source:
- run \`36369682759\`;
- artifact \`10948127976\`;
- digest \`sha256:f8d5c1eae3a38d8b8751190767e78e264c91c44a1edacaf85619a781e9e1a105\`.

Recurrence-seed source:
- run \`36370056281\`;
- artifact \`10948891782\`;
- digest \`sha256:95a74a7d757e2f9afd0e37040414e66137a2825dbfa3780b8105a40be06da248\`.

Existing adversarial/family/sampling controls remain already-viewed P0-Q evidence. Re-execution with C1Q-RS is repair qualification, not new confirmation.

## Planned execution

### Gate 0. Mechanical contracts

Before large execution, test:

1. same parameter count and BIC formula as C1Q;
2. exact legacy top-start identity is preserved;
3. admissible recurrence seed adds at most one optimized start and never removes a legacy start;
4. recurrence refusal falls back to the legacy fit path;
5. C1Q-RS NLL is never worse than current C1Q on deterministic fixtures within numerical tolerance;
6. seed provenance, projection/refusal status, legacy start count, total start count, and winning-start origin are returned.

### Gate 1. Complete C-interior Function Map repair

Regenerate the exact 16 cells x 3 seeds x fine/coarse paths from the completed Function Map and fit C1Q-RS using the same primary/rescue budgets.

For all 96 rows report:

- archived C1Q NLL and physical parameters;
- C1Q-RS NLL and physical parameters;
- NLL improvement;
- truth \(\chi,g,f_n\) recovery errors;
- raw-bound proximity;
- recurrence-seed status, unprojected/projected values, and whether it supplied the winning basin;
- practical same-path fine/coarse drift.

No threshold is selected. The whole distribution, including unchanged rows and residual failures, is retained.

### Gate 2. Mandatory Limit Map requalification

Using the exact existing truth generators and seeds, evaluate C1Q-RS on:

- nested isotropic one-mode \(g=0\);
- anisotropic 4:1 white forcing;
- rank-1 axis white forcing;
- colored-process \(\phi=0.7\) extra-pole control;
- genuine separated two-mode truth;
- D\C controls of both signs;
- S\D controls of both signs;
- paired-sampling C, D\C, and S\D semantics.

Where A0/A1/A2 comparisons are scientifically part of the existing control, retain them unchanged and add C1Q-RS to the comparison.

The known semantic facts remain fixed:
- a C1Q-RS BIC win cannot establish truth \(\in C\);
- fitted \(|g|<1\) cannot establish truth \(\in C\);
- paired-rate stability cannot establish truth \(\in C\);
- colored extra-pole and out-of-family truths remain refusal/Limit cases even if C1Q-RS fits them better.

### Gate 3. Post-execution deviation and scope audit

Classify:
- repaired interior search failures;
- residual interior failures;
- recurrence-seed refusals;
- new false model-selection behavior, if any;
- unchanged semantic failures;
- compute/runtime changes.

No candidate promotion occurs from Gate 1 alone.

## Outcome architecture

**Search repair supported:** C1Q-RS removes or materially reduces the known interior boundary-collapse branch while satisfying the strict non-worsening mechanical invariant and without introducing new mechanical defects.

**Partial repair:** substantial improvement occurs but residual interior basin failures remain.

**Search repair falsified:** C1Q-RS does not materially alter the known failures despite admissible recurrence seeds, or violates the non-worsening invariant.

**Regression:** a nested simpler or genuine multimode control changes in a scientifically adverse direction because of the augmented search.

**Semantic limit unchanged:** colored or out-of-C controls remain well fit by C1Q-RS. This does not falsify the search repair, but it preserves the requirement for an independent admission/refusal architecture.

**Need more information:** optimization stochasticity or environment dependence prevents stable comparison.

## Claim ceiling

C1Q-RS is qualification-only. No real EEG, biological prevalence, scientific threshold, estimator promotion, or C-family membership claim can follow directly.

## APQ request

\`APQ-2 SUBSTANTIAL\`. Two isolated first-pass attacks, objection ledger, Plan Delta, shared-premise challenge, revised plan, and freeze are required before implementation/execution.
