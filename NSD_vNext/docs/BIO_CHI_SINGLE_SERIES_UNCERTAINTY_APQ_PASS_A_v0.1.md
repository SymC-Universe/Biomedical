# Bio Chi Single-Series Uncertainty Method APQ Pass A v0.1

**Review lens:** inferential validity, practical identifiability, claim compression  
**Plan reviewed:** `BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_PLAN_v0.1.md` at commit `7da5c43e42a2bf0bec1e93e562d432c786a85563`  
**Isolation:** role-isolated first pass from one cognition; not an independent reviewer.

1. **Strongest feature:** the plan compares single-series diagnostics directly against an already-completed repeated-realization source-of-truth map rather than treating textbook intervals as automatically calibrated.
2. **Strongest assumption:** one fixed observed realization per truth/rate is sufficient to reveal whether a method's geometry is qualitatively appropriate.
3. **Most likely failure:** the chosen realization may itself be unusually favorable or unfavorable, so apparent method performance could be seed-specific.
4. **Dangerous dependency:** parametric bootstrap is generated from the fitted model, so if the observed fit is displaced in a weak region the bootstrap can faithfully reproduce the wrong local geometry rather than truth uncertainty.
5. **Competing explanation:** broad profile or bootstrap spread may reflect nuisance-coordinate coupling rather than uncertainty in chi itself.
6. **Circularity concern:** cells 0/1/2/6 are selected after viewing the uncertainty map, but selection is explicitly by predeclared postresult category. This is exploratory method development, not confirmation.
7. **Missing control:** include the true-generating parameter location on each profile and report its delta-NLL. This shows whether the realized series statistically prefers a displaced chi even before an interval rule is chosen.
8. **Cheaper discriminating test:** Hessian and profile alone should be completed before bootstrapping all eight cases. If profile implementation is mechanically invalid, bootstrap should not run.
9. **Refusal condition:** no method should be promoted if difficult cases show open/disconnected profiles that bootstrap/Hessian summarize as compact, or if compact cases are themselves profile-unstable.
10. **Classification:** A1 MATERIAL, single-seed dependence must be acknowledged; A2 MATERIAL, bootstrap is conditional-on-fit rather than truth-calibrated; A3 MATERIAL, true-chi delta-NLL must be retained; A4 MINOR, stage profile before bootstrap mechanically.
