# Uncertainty and INDETERMINATE Hold

Status: **METHOD ROUTE IDENTIFIED / P0 CALIBRATION REQUIRED / P1 RULE NOT FROZEN**.

Published SSI-COV uncertainty work provides a principled first-order sensitivity/covariance route for uncertainty in poles and modal parameters from output-only data. That literature is method-native but primarily validated in structural/mechanical applications, so direct neural validity is not assumed.

P0 implementation may therefore add an uncertainty object capable of carrying covariance/interval information, plus synthetic known-truth calibration through repeated realizations or Monte Carlo coverage checks.

`INDETERMINATE` must not be defined by an arbitrary fixed gray-zone width. It should arise when supported uncertainty spans incompatible adjudication states, when alternative admissible model orders produce incompatible structural assignments, or when crowding prevents a unique claim at the requested level.

Exact confidence level, simultaneous-versus-marginal coverage, replicate count, multiplicity adjustment and final P1 thresholds remain unfrozen pending P0 calibration.

See `LITERATURE_GATE_CANDIDATES_20260910.md` and `FOUR_HOLD_DECISION_PACKET_20260910.md`.
