# Phase 0C Untouched Synthetic Holdout Preregistration v0.1

Frozen before any Phase 0C scientific execution.

## Role
Phase 0C is the first prospective synthetic admission test for the SSI-COV structural estimator after Phase 0B development/calibration.

Sequence:

`Phase 0A easy in-model -> Phase 0B adversarial development -> freeze selector/refusal rules -> Phase 0C untouched holdout -> label-blind EEG adequacy only if Phase 0C passes`

No Phase 0C result may be used to retune the Phase 0C thresholds and then be rescored as a pass.

## Primary object
The primary object is observable dynamical structure:
- effective observable order;
- stable complex poles;
- observable mode shapes when individually identifiable;
- joint observable subspaces when mode crowding makes individual vectors unstable.

No diagnosis, phenotype, treatment outcome, historical neuro-spectrum coordinate, damping target, whole-system chi, or preferred chi value is present.

## Frozen selector
The machine-readable authority is `configs/frozen_rules.json`.

The selector sees only decomposition singular values and estimated poles/mode shapes across order and record segments. Synthetic truth is withheld from selection and is used only after decisions are made to score the holdout.

### Observable order
For candidate order q, define:

`g_q = S_q / S_(q+1)`

where S are descending singular values of the SSI-COV block covariance decomposition.

Choose the smallest tested q with `g_q >= 10`. Refuse if none exists or if q is the maximum tested order.

### Stationarity and persistence
- all selected full-record poles must be stable;
- median first-half vs second-half normalized complex-pole distance must be <= 0.03;
- median selected-order vs next-higher-order normalized complex-pole distance must be <= 0.02.

Distance between poles a and b is:

`|a-b| / max(|a|, |b|)`.

### Mode shape versus subspace
For individually reported complex modes, split-record mode-shape MAC must be >= 0.95.

For positive-frequency modes i,j, define crowding ratio:

`c_ij = |omega_i-omega_j| / (alpha_i+alpha_j)`

with `lambda=-alpha+i*omega`.

If `c_ij <= 1`, individual mode-vector interpretation is suppressed and the joint observable subspace is primary. A subspace claim requires split-record subspace similarity >= 0.99.

Individual real-pole scalar values remain refused.

## Holdout design
Phase 0C uses a new random seed, new system parameters, new durations, stronger noise levels, an order-6 three-mode family, new weak/moderate observability challenges, stronger non-normality, a new near-degenerate family, a mixed complex/real family, a 1/f null, and a fixed-time nonstationary switch.

Candidate orders: 2,4,6,8,10.

The holdout configuration is frozen in `configs/phase0c_design.json`.

## Strong-observability truth used only for scoring
After automatic decisions, a true state counts as strongly observable if its true observable mode-shape norm is at least 0.20 of the maximum true observable mode-shape norm in that system realization. This scoring rule is not available to the selector.

## Pass/fail
All targets in `configs/frozen_rules.json` must pass. A failed target yields `HOLDOUT_FAIL_PRESERVE_DO_NOT_RETUNE`.

Passing Phase 0C licenses only a move to label-blind EEG model-adequacy testing. It does not license diagnostic, treatment, causal, disease-mechanism, or whole-system-scalar claims.
