# NSD v0.2 N-B2/N-B3 Switched Certification Code-Delta Audit v0.1

**Status:** OUTCOME-BLIND POST-FREEZE IMPLEMENTATION PREPARATION  
**Scientific baseline:** `NSD-V02-B01-FROZEN`  
**Execution authority:** false  
**Scientific outcomes opened:** false

This audit records the exact mechanical implementation delta required by the already-frozen switched-versus-surrogate target. It creates no new scientific authority and does not alter any frozen case, threshold, target, operator, switching law, or claim ceiling.

## Frozen target and certificate

The implementation must certify

\[
D(t)=\left\|\Phi(t,0)-e^{\bar A t}\right\|_2,
\qquad 0\le t\le 32,
\]

with a relative enclosure gap no larger than `1e-9 * max(1, |L|)`, where `L` is the current certified lower bound on the maximum.

The horizon is partitioned at every frozen switch boundary. On each switch-free interval `[a,b]` with active generator `A_i`, the implementation may use the Lipschitz consequence

\[
|D(t)-D(a)| \le
\left(
\|A_i\|_2 e^{\max(0,\mu_2(A_i))(b-a)}\|\Phi(a)\|_2
+
\|\bar A\|_2 e^{\max(0,\mu_2(\bar A))(b-a)}
\|e^{\bar A a}\|_2
\right)(t-a).
\]

This produces a conservative endpoint-cone upper bound. Branch-and-bound must fail closed on interval-budget exhaustion, nonfinite bounds, switch-partition mismatch, or failure to close the frozen `1e-9` enclosure.

The target remains the raw operator 2-norm written above. The frozen physical metric input is validated but does not redefine the discrepancy target.

## Required code delta

1. Extend `NSD_vNext/engine/nsd_engine/v02_nb23_peak.py` with a numerical-only `certified_switching_discrepancy_max` routine.
2. Preserve explicit switch partitions and all non-pruned argmax intervals overlapping the frozen tie criterion.
3. Return only numerical evidence with `NUMERICAL_ONLY_NO_SCIENTIFIC_VERDICT`; no representation-sufficiency or recoverability verdict is permitted.
4. Detect the exact identical-generator anchor without tolerance-based scientific equivalence and return an exact zero enclosure.
5. Add an independent reference module that does not call the production certificate or reuse its branch-and-bound state.
6. Add non-confirmatory tests for the exact-zero anchor, explicit partitioning, dense-reference enclosure, fail-closed interval exhaustion, and verdict-namespace separation.

## Outcome-blind numerical sanity check

Before repository mutation, the planned bound was evaluated only on the already-bound non-confirmatory fixture `NB23-REF-SWITCH-DENSE-01`:

- `A0 = diag(-0.2, -0.5)`
- `A1 = diag(-0.4, -0.3)`
- `G = I`
- segment = `0.5 s`
- phase offset = `0.1 s`
- horizon = `2 s`

A standalone implementation of the planned branch-and-bound bound produced a lower maximum estimate of approximately `0.03619590966947828` and upper enclosure approximately `0.03619591066190259`, closing within the frozen `1e-9` relative-to-`max(1,|L|)` criterion after 447 splits. An independently evaluated 20,001-point dense reference attained approximately `0.03619590966947828` at `t = 0.4 s`, inside the enclosure.

These values are non-confirmatory mechanical-fixture evidence only. They do not inspect `NB23B01-M-TV` or any frozen confirmatory suite outcome and do not create scientific execution authority.

## Current transport disposition

A direct repository mutation attempt for the production code remained blocked by the repository connector safety layer. Do not bypass that block and do not weaken the certificate. When code mutation becomes available, implement exactly the frozen delta above, run `NSD Engine Contracts`, retain the independent fixture evidence, and only then advance `PF-NB23-I01` toward final identity binding.
