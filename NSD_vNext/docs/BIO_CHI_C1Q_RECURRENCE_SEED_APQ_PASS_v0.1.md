# Bio Chi C1Q Recurrence-Seed Rescue APQ-1 Pass v0.1

**Plan reviewed:** \`BIO_CHI_C1Q_RECURRENCE_SEED_PLAN_v0.1.md\`  
**APQ level:** APQ-1 EXPLORATORY  
**Review limitation:** role-isolated same-cognition review

The strongest feature is that the proposed start is derived from the same observable second-order structure that often remained informative when C1Q collapsed, while using a parameterization distinct from the C1Q likelihood optimizer.

The strongest assumption is that sample positive-lag covariance contains enough information to construct a useful seed at 60 s. The recurrence diagnostic already refused seven rows in the broader Function Map, so refusal must remain a valid outcome.

The main failure risk is circular overfitting of the start to noisy covariance. This does not invalidate the test because the start is evaluated by the independent C1Q likelihood, but a successful start must still be requalified on untouched/expanded known truths before becoming part of C1Q.

The most dangerous hidden dependency is that both recurrence and C1Q assume second-order structure. Therefore this test can repair search inside C but cannot establish that unknown biology belongs to C.

The amplitude fit can produce \(A\) or \(g\) outside the C1Q domain. Projection is acceptable only as an initialization operation, must be recorded row by row, and cannot be interpreted as evidence that the unprojected estimate belongs to C.

**Objections and dispositions:**
- **S1 MATERIAL:** projected seeds could conceal systematic out-of-domain covariance estimates.  
  **Disposition:** \`ACCEPTED_TEST_ADDED\`. Preserve unprojected \(A,g\), projection flags, and refusal reasons.
- **S2 MATERIAL:** success on already-selected pathological rows is post-hoc.  
  **Disposition:** \`DEFERRED_CLAIM_LIMITED\`. Root-cause/discriminating test only; no estimator promotion.
- **S3 MINOR:** one local optimization does not prove the seed is globally optimal.  
  **Disposition:** \`DEFERRED_CLAIM_LIMITED\`. Compare only with the already-frozen selected and truth-seeded basins.

No BLOCKER or unresolved MATERIAL objection remains.
