# NSD Native Comparator Selection Plan

Status: **P0Q1 SPLIT RESULT RECORDED; P1 COMPARATOR NOT FROZEN.**

## Two comparison levels remain separate

### A. Estimator-at-declared-order/rank

Subspace DMD remains the leading independent stochastic structural comparator candidate when the same declared/correct rank is supplied. Its earlier P0 stress performance was strong across random dynamics, observation noise, crowding and weak observability.

### B. Operational truth-blind structural recovery

The first frozen candidate for a common simple rank-signal gate has now been tested prospectively at P0Q1.

Frozen candidate rule v1:

- candidate rank = largest finite method-native adjacent singular gap;
- require gap >= 3.0;
- refuse the grid maximum;
- refuse any unstable selected pole;
- require at least one stable positive-frequency complex mode.

Prospective P0Q1 result:

- **SSI-COV: SURVIVES_P0Q1**, admitting 35/35 oscillatory records and false-admitting 0/40 refusal records with zero mechanical exceptions.
- **Subspace DMD: FAILS_P0Q1**, admitting 35/35 oscillatory records but false-admitting 2/5 real-pole-only controls. Every stochastic/noise null family remained fully refused and there were zero mechanical exceptions.

Therefore the same simple operational gate is **not qualified across the two method families**.

## Consequence

The Subspace-DMD failure cannot be repaired by retuning v1 on P0Q1 records. The next step is a retrospective method diagnostic, not a new threshold.

The key diagnostic question is why the projected-future singular spectrum selected rank 4 for every two-real-mode stochastic control and sometimes generated stable complex eigenpairs at that rank. The investigation must inspect:

- projected singular values across all retained ranks;
- the rank-2 and rank-4 eigenvalues;
- finite-sample versus persistent behavior;
- adjacent-rank mode assignments;
- the authors' retained-mode/rank convention;
- whether stochastic innovation dimension can masquerade as persistent generator dimension in the projected-future object.

Only after that diagnosis may a new method-native Subspace-DMD operational hypothesis be formulated. Such a hypothesis will be explicitly post-P0Q1, separately versioned, and tested on new untouched P0Q2 evidence.

## Current comparator hierarchy

- **Subspace DMD:** leading independent comparator for conditional estimator-at-rank recovery; operational rank selection remains unqualified after P0Q1 failure.
- **SSI-COV:** candidate NSD estimator; the simple rank-signal gate survived one frozen P0Q1 challenge but remains P0 and requires additional untouched qualification before P1.
- **TLS-DMD:** snapshot/sensor-noise assumption control; preserved stochastic mismatch.
- **Exact DMD:** transparent baseline with known observation-noise bias.
- **specparam/FOOOF and PLI/wPLI:** later spectral/connectivity baselines for different target objects.

P1 remains closed. A weak, retuned or assumption-mismatched comparator will not be manufactured to create an added-value result.
