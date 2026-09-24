# Bio Chi rapid checkpoint - scalar gate frozen

**Branch:** bio-chi-closure-p0q-20260924

## Completed
- NF-kB six-state local observability: PASS and pinned.
- Source-native pulse protocols audited; mixed TR=1/TR=0 pulse responses are excluded as clean tests of the TR=1 equilibrium pole.
- Generator-derived scalar qualification rule frozen:
  BIO_CHI/config/JARUS_CHI_BIO_SCALAR_P0Q_FREEZE_v0_1.json

## Frozen scalar definition
For the unique observable complex-conjugate invariant factor:

chi_bio = -Re(lambda) / |lambda|
gamma = -2 Re(lambda)
omega0 = |lambda|
omega_d = |Im(lambda)|

All values must come from the same pair. Negative chi is retained as local amplification. No chi=1 biological boundary is claimed.

## Scope
The candidate is a local, mode-specific biological scalar in the Jaruszewicz-Blonska NF-kB model. It is not a system scalar and not P1-confirmed.

## Next action
Recompute and adjudicate the scalar from immutable archived eigenvalues, with all three frozen Jacobian steps retained and the native pole pair reported as comparator.

No user intervention required.
