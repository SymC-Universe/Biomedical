# Bio Chi C1Q-RS Untouched Interior Qualification Plan v0.1

**Status:** APQ-2 SUBSTANTIAL DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, prospective P0-Q qualification  
**Purpose:** untouched known-truth generalization test of the C1Q-RS search repair

## Scientific target

C1Q-RS was engineered from already-viewed C1Q search failures. This plan asks whether its search advantage appears on previously unexecuted C-family truths and previously unused realizations within the same intended qualification envelope.

The question is deliberately narrow:

> Does the recurrence-augmented search route generalize as a more complete optimizer of the unchanged C1Q likelihood on unseen valid C truths, without creating a new recovery or numerical failure mechanism?

This plan does not retest whether biology belongs to C. The existing semantic Limit Map remains separate and unchanged.

## Claim ceiling

P0-Q search-route qualification only. A successful result may support superseding legacy C1Q with C1Q-RS as the **preferred qualification search implementation**. It cannot:

- promote C1Q-RS to a production Bio Chi estimator;
- establish C-family membership in real data;
- license real EEG;
- define an empirical admission threshold;
- estimate biological prevalence;
- erase colored-process, D\\C, S\\D, multimode, closure, alias, or sampling Limit results.

## Outcome exposure

At plan freeze, no C1Q or C1Q-RS fit has been executed on the coordinates or realization seeds below.

The coordinate generator is frozen as SciPy Sobol dimension 4, \`scramble=True\`, seed \`20260928\`. The listed coordinates, not the generator, are the authoritative design identity.

Realization seeds are \`314159\`, \`271828\`, and \`161803\`, none used in the development Function Map.

## Untouched qualification envelope

The ranges match the intended C-interior envelope used during development:

- latent fraction \(A\in[0.20,0.90]\);
- natural frequency \(f_n\in[3,25]\) Hz;
- true \(\chi=\zeta\in[0.15,0.85]\);
- \(g\in[-0.80,0.80]\).

| Cell | A | f_n Hz | chi | g |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.688150539 | 20.201612910 | 0.551117689 | -0.020547418 |
| 1 | 0.336642675 | 13.188539490 | 0.377758221 | 0.028267951 |
| 2 | 0.528666673 | 16.642470066 | 0.682941012 | -0.560485229 |
| 3 | 0.887143663 | 5.759101400 | 0.158522118 | 0.589873901 |
| 4 | 0.759569973 | 18.659578890 | 0.435244692 | 0.728151667 |
| 5 | 0.418348405 | 3.740129625 | 0.613944070 | -0.720637715 |
| 6 | 0.216579191 | 22.308349485 | 0.303208497 | 0.289988850 |
| 7 | 0.564855985 | 11.081272740 | 0.833566780 | -0.260393216 |
| 8 | 0.635893316 | 14.425340595 | 0.276149426 | -0.658955383 |
| 9 | 0.276813467 | 8.013827052 | 0.805831470 | 0.691468263 |
| 10 | 0.434784128 | 21.081338726 | 0.495778490 | -0.322123064 |
| 11 | 0.786905533 | 12.346410183 | 0.673786919 | 0.326719342 |
| 12 | 0.816036363 | 24.560055207 | 0.731768850 | 0.191559513 |
| 13 | 0.468545259 | 8.867165821 | 0.208024861 | -0.158838145 |
| 14 | 0.320309133 | 17.820472134 | 0.512522389 | 0.426626757 |
| 15 | 0.660755691 | 4.616835512 | 0.339855204 | -0.422238585 |

Sampling is frozen at 60 s, 256 Hz fine rate, and exact factor-2 same-path decimation to 128 Hz. Each fine/coarse pair is one metamorphic unit.

Total frozen output rows: \(16\times3\times2=96\).

## Estimators

Compare unchanged current C1Q and frozen C1Q-RS.

Both use the same likelihood, four parameters, transforms, bounds, burn, frequency domain, BIC penalty, primary budget, and rescue budget. C1Q-RS differs only by adding one admissible recurrence/covariance start without removing any legacy start.

Primary:
- \`optimizer_maxiter=80\`;
- \`max_optimized_starts=18\`.

Conditional rescue:
- \`optimizer_maxiter=160\`;
- \`max_optimized_starts=24\`.

Rescue activation follows the legacy-only primary result as frozen in the C1Q-RS plan.

## Mechanical preflight

Before full execution, run cells 0, 5, 10, and 15 at seed \`314159\`.

The preflight may stop only for:
- invalid C truth covariance;
- alias-safety violation;
- C1Q/C1Q-RS execution failure caused by implementation/runtime;
- strict containment failure;
- design identity mismatch;
- artifact/schema failure.

Scientific recovery magnitude may not retune the design.

## Outputs

For every rate-level row preserve:

- truth \(A,f_n,\chi,g\);
- C1Q NLL/BIC and parameters;
- C1Q-RS NLL/BIC and parameters;
- strict non-worsening status;
- NLL improvement;
- absolute \(\chi,g,f_n\) recovery error for each route;
- recurrence-seed status/projection/winner origin;
- optimizer start/convergence metadata;
- same-path fine/coarse drift for C1Q and C1Q-RS.

Summaries report the whole distribution, per-rate distribution, and per-cell distribution. No outcome-derived pass threshold is introduced.

## Outcome architecture

**Generalized search utility:** untouched rows contain reproducible lower-likelihood basins found by C1Q-RS that legacy C1Q misses, with strict containment intact and without a new recovery-failure mechanism.

**No added utility in this envelope:** C1Q-RS mostly ties C1Q on untouched truths. This does not make RS wrong, but weakens the case that its extra computation should become the default qualification route.

**Likelihood improvement with recovery tension:** RS obtains lower NLL on some untouched rows while truth-coordinate recovery degrades. This indicates objective/identifiability tension and blocks simple canonicalization until characterized.

**Regression:** strict containment fails, numerical instability appears, or the augmented route creates a reproducible new failure class.

**Partial generalization:** some unseen search failures are rescued while important unresolved rows remain. Full distributions determine scope; no arbitrary count becomes a scientific threshold.

## Promotion rule

No numerical success fraction is frozen.

If the untouched evidence shows lower-NLL rescue on more than a single isolated realization, strict containment holds throughout, and no new reproducible failure mechanism appears, the search-route evidence is sufficient to consider C1Q-RS the preferred **qualification search implementation** for future C-family work. This is an implementation-level supersession only. The semantic admission architecture remains independently required.

If the result is ambiguous because lower-NLL rescue systematically conflicts with truth recovery, promotion is held for a scientific decision.

## Reproducibility

The grid and seeds are frozen before outcome exposure. Numerical/decision-equivalent repeatability is required in the declared environment. Cross-platform bitwise identity is not required.

## APQ request

\`APQ-2 SUBSTANTIAL\` because the result can change the canonical qualification search implementation.
