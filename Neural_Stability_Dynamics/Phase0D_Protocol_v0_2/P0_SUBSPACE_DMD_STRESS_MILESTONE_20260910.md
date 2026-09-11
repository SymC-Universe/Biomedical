# NSD P0 Subspace-DMD Stress Milestone

Date: 2026-09-10/11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL
Status: **P0 COMPARATOR STRESS MILESTONE COMPLETE. P1 REMAINS CLOSED.**

## Verified execution

Commit: `3c45e3847d908a6dece46c80c2dce62713b978c4`
GitHub Actions run: `34562566099`
Result: **SUCCESS**
Regression/protocol tests: **53 passed**
Artifact: `nsd-phase0d-v02-p0-qualification`
Artifact SHA-256: `c7c776a765bb7c02c7d807d2212c9c4da2fd8ba2693925685bb2f686b9aedac8`
P1 execution guard: **PASS, fail-closed before scientific data generation**

The Subspace-DMD addendum used the same condition generator, replicate identities, oracle state rank, truth objects and scoring code already committed for the prior SSI-COV / exact-DMD / TLS-DMD matrix. No challenge was redesigned after observing the earlier TLS result.

## Subspace-DMD result

Across six P0 conditions with six replicates each, Subspace DMD completed all **36/36** records with no method exception. Median unstable-pole fraction was `0.0` in every condition and median known-truth positive-complex-mode coverage was `1.0` in every condition.

| Condition | Subspace-DMD median relative pole error | Frequency MAE (Hz) | Relative decay MAE | Carrier-subspace similarity |
|---|---:|---:|---:|---:|
| baseline stochastic | 0.0038679 | 0.01426 | 0.08724 | 0.999981 |
| white sensor 10% | 0.0051353 | 0.01000 | 0.15542 | 0.999962 |
| colored sensor 10%, rho=0.8 | 0.0103981 | 0.01369 | 0.34346 | 0.999958 |
| weak second mode 5% + white 5% | 0.0135513 | 0.07097 | 0.30420 | 0.998425 |
| crowded modes + white 5% | 0.0047409 | 0.01340 | 0.18883 | 0.999986 |
| condition number 25 + white 5% | 0.0056476 | 0.01391 | 0.15926 | 0.999983 |

## Comparison with SSI-COV on the same oracle-order P0 records

This section is descriptive only. It is not a superiority test and no multiplicity-adjusted confirmatory comparison was preregistered.

- **Baseline stochastic:** SSI-COV and Subspace DMD were very similar. SSI-COV had slightly lower median pole error (`0.00316` vs `0.00387`); Subspace DMD had slightly lower median decay error (`0.0872` vs `0.0967`).
- **White sensor 10%:** Subspace DMD had lower median pole and frequency error (`0.00514`, `0.0100 Hz`) than SSI-COV (`0.00693`, `0.0154 Hz`), while SSI-COV had slightly lower decay error (`0.144` vs `0.155`).
- **Colored sensor 10%:** SSI-COV had lower pole and decay error (`0.00525`, `0.173`) than Subspace DMD (`0.0104`, `0.343`); frequency errors were similar.
- **Weak observability:** the earlier matrix showed severe degradation for SSI-COV at the supplied oracle order (`0.343` median pole error, `2.678 Hz` frequency MAE, carrier-subspace similarity `0.654`). Subspace DMD remained much closer to truth (`0.0136`, `0.071 Hz`, `0.9984`). This is a major P0 finding, but the mechanism must be investigated before any method-level claim because the current SSI observable-order gate was bypassed by the oracle-order comparison.
- **Crowding:** both remained accurate; SSI-COV had lower pole/decay error while Subspace DMD had lower frequency MAE.
- **Condition-number 25:** Subspace DMD had lower median pole, frequency and decay errors in this construction; both preserved near-unity carrier-subspace similarity.

## Interpretation

The earlier TLS-DMD failure on process-driven stochastic data is preserved. It was not an implementation excuse: Subspace DMD, which is specifically designed for random dynamics with observation noise, remained stable and accurate on the same families. That materially strengthens the conclusion that **assumption matching matters to comparator fairness**.

The current leading direct independent structural comparator candidate is therefore:

`SUBSPACE_DMD`

for the present stochastic/output-only P0 target class.

This is **not** an MFR-05 freeze. The current comparison supplied the known state rank/order to every method to isolate estimator behavior. That leaves a separate operational-comparator question unresolved:

> Can SSI-COV and Subspace DMD be compared under fair, predeclared, truth-blind model-order/rank selection rules without handicapping either family?

## New comparator firewall

Future records must distinguish two claims:

1. **Estimator-at-declared-order comparison:** known/fixed order or rank is supplied to both methods and only conditional recovery is compared.
2. **Operational-engine comparison:** each method must select admissible structure without truth access using a predeclared and fairly qualified order/rank route.

Success on claim 1 does not imply success on claim 2.

## Weak-observability warning

The striking weak-observability contrast does not license the statement that Subspace DMD solves observability. The current SSI-COV P0 comparison forced the latent/oracle state order instead of using NSD's observable-order/refusal logic. The next analysis must separate:

- estimator failure at forced order,
- correct refusal due to insufficient observability,
- lower observable-rank recovery,
- and genuine recovery of a weakly expressed mode.

No method receives credit for hallucinating an unobservable latent mode merely because its pole lands near truth.

## Next gate

1. build a truth-blind rank/order **sweep and stability ledger** for SSI-COV and Subspace DMD without yet selecting a winning rule;
2. map observable-rank/refusal behavior explicitly in the weak-mode family;
3. identify candidate method-native order/rank selection routes from the literature;
4. qualify candidate rules on P0 known-truth/known-bad systems;
5. preserve analytical SSI uncertainty as a separate open hold;
6. audit before freezing MFR-05 or any P1 challenge.

No P1 seed, P1 system list, comparator winner, selection threshold, neural boundary, chi coordinate, phenotype or mechanism is frozen by this milestone.
