# Bio Chi C1Q-RS APQ First Pass B v0.1

**Lens:** optimizer mechanics, reproducibility, fairness, regression risk  
**Plan:** \`BIO_CHI_C1Q_RS_QUALIFICATION_PLAN_v0.1.md\`  
**Isolation:** role-isolated first pass; not independent cognition

1. **Strongest feature:** forcing the recurrence start in addition to, rather than instead of, the legacy optimized starts creates a testable non-worsening invariant.
2. **Strongest assumption:** duplicating the legacy-start selection code will remain exactly synchronized with current C1Q.
3. **Most likely failure mode:** implementation drift could cause C1Q-RS to select a different legacy subset, invalidating the strict containment argument.
4. **Most dangerous dependency:** archived Function Map C1Q rows used primary/rescue logic; candidate comparison must reproduce that same route rather than compare a single RS fit against a rescued legacy fit.
5. **Competing explanation:** apparent RS gains could arise from a larger compute budget alone rather than the recurrence information specifically.
6. **Circularity/provenance concern:** if an arbitrary extra random/legacy start is not compared, recurrence-specific information gain is not isolated.
7. **Missing control:** include a compute-matched extra-start control on a bounded subset, using one additional predeclared legacy/spectral start without recurrence information.
8. **Cheaper test:** mechanical unit tests can prove legacy start containment and fallback equivalence before simulations.
9. **Refusal condition:** violation of strict non-worsening or fallback equivalence blocks scientific interpretation.
10. **Classification:** B1 BLOCKER, B2 MATERIAL, B3 MATERIAL.

**B1 BLOCKER:** start-set containment must be proven mechanically, not assumed from duplicated code.  
**Recommended repair:** factor the legacy start-selection operation into a shared helper or explicitly unit-test identical legacy raw starts returned by both routes.

**B2 MATERIAL:** primary/rescue route must be mirrored exactly.  
**Recommended repair:** RS Function Map wrapper uses identical primary and conditional rescue budgets, with the recurrence start added to each budget.

**B3 MATERIAL:** extra compute alone is a plausible explanation.  
**Recommended repair:** on the previously identified boundary-collapse rows, compare recurrence augmentation with one compute-matched additional generic legacy start drawn from the next-ranked scored legacy candidate, where available. This control is P0-Q diagnostic only.
