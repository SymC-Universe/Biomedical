# Bio Chi C1Q-RS Uncertainty Map APQ Pass B v0.1

**Review lens:** stochastic design, computation, numerical diagnostics, reproducibility  
**Plan reviewed:** `BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_PLAN_v0.1.md` at commit `646410f9f0a82332837ae655465dffd3493a4f58`  
**Isolation:** role-isolated first pass from one cognition; not an independent reviewer.

1. **Strongest feature:** all truth coordinates, seeds, rates, duration, and estimator implementation are frozen before outcome exposure.
2. **Strongest assumption:** twelve realizations per cell are enough to describe useful dispersion without formal interval claims.
3. **Most likely failure:** interpolated 5th/95th percentiles with n=12 may look more precise than they are.
4. **Dangerous dependency:** optimizer boundary counts require an exact numerical definition before execution.
5. **Competing explanation:** a wide fitted distribution may mix estimator variance with occasional optimizer failure or boundary attraction.
6. **Circularity/provenance:** seed list and cell list are cleanly frozen; no issue.
7. **Missing control:** summaries should stratify successful interior fits versus numerical-boundary fits while still preserving the full distribution. Do not drop boundary rows.
8. **Cheaper test:** preflight should verify that all requested row fields are emitted and that repeated seeds are truly independent realizations of the frozen truth generator.
9. **Refusal condition:** if numerical-boundary/optimizer states dominate a cell, classify it as estimator-uncertainty/optimization-confounded rather than summarizing it as ordinary sampling dispersion.
10. **Classification:** B1 MATERIAL, replace 5th/95th with full rows plus quartiles/range for n=12; B2 MATERIAL, freeze boundary diagnostic definition; B3 MATERIAL, preserve optimizer-confounded classification; B4 MINOR, exact repeated-seed provenance must be in artifact.
