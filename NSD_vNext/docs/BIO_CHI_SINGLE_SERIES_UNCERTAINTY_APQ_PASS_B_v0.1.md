# Bio Chi Single-Series Uncertainty Method APQ Pass B v0.1

**Review lens:** computation, parameterization, profile geometry, bootstrap reproducibility  
**Plan reviewed:** `BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_PLAN_v0.1.md` at commit `7da5c43e42a2bf0bec1e93e562d432c786a85563`  
**Isolation:** role-isolated first pass from one cognition; not an independent reviewer.

1. **Strongest feature:** all methods operate on the same exact likelihood and frozen observed series, avoiding estimator-family confounding.
2. **Strongest assumption:** a 61-point uniform chi grid is dense enough to expose relevant profile structure over 0.05 to 0.98.
3. **Most likely failure:** profile nuisance optimization may miss lower basins at some chi values, manufacturing artificial profile bumps or closure.
4. **Dangerous dependency:** direct physical parameterization must map exactly to the C1Q likelihood domain; any mismatch makes the profile incomparable with the fitted optimum.
5. **Competing explanation:** Hessian ill-conditioning may be a coordinate artifact rather than practical non-identifiability.
6. **Circularity/provenance:** no hidden outcome selection beyond the explicitly viewed uncertainty map.
7. **Missing control:** profile each point from both neighboring continuation start and recurrence/legacy-derived starts, then retain the lowest NLL. Also verify the profile at fitted chi reproduces global NLL within a mechanical tolerance.
8. **Cheaper discriminating test:** preflight should require the fitted-chi profile point to reproduce global NLL and the direct physical parameterization to match the original likelihood at several random admissible coordinates.
9. **Refusal condition:** stop method interpretation if profile implementation cannot reproduce original C1Q-RS NLL or if nuisance optimization is visibly start-dependent under the frozen multistart rule.
10. **Classification:** B1 BLOCKER until physical-parameter likelihood equivalence is mechanically tested; B2 MATERIAL, profile needs continuation plus multistart protection; B3 MATERIAL, Hessian coordinate dependence must be reported; B4 MINOR, 32 bootstrap replicates are descriptive only.
