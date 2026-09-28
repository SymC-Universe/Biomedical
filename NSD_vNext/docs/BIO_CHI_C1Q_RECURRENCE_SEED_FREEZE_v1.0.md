# Bio Chi C1Q Recurrence-Seed Rescue Freeze v1.0

**Status:** APQ-1 QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**Plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_RECURRENCE_SEED_PLAN_v0.1.md\`  
**APQ pass:** \`NSD_vNext/docs/BIO_CHI_C1Q_RECURRENCE_SEED_APQ_PASS_v0.1.md\`

Frozen rows: all 48 rate-level rows in cells \`0,5,7,8,9,11,12,15\`.

Frozen recurrence/covariance seed:
- normalized positive-lag covariance through lag 12;
- least-squares order-two recurrence;
- stable underdamped recurrence required;
- least-squares \(A,Ag\) amplitude fit under fixed recurrence poles;
- numerical-domain projection recorded explicitly;
- one local C1Q optimization from the seed.

Frozen comparisons:
- source-selected NLL from Function Map;
- truth-seeded local NLL from completed likelihood-basin diagnostic;
- recurrence-seeded local NLL.

No estimator code is modified by this test. No scientific threshold is defined.
