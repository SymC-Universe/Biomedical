# Phase 0B Failure-Boundary Audit and Phase 0C Freeze Decision
Date: 2026-09-08

## Provenance
User-local Phase 0B execution completed under config SHA-256:
`d9358f456563ef18fe7bea45d5cd1e2de62e0bc724b4c7a4cf5c3394ef991fb6`.

The uploaded local `CODE_MANIFEST.sha256` matches the pre-run package manifest byte-for-byte for all 12 frozen code/config/test files.

User-result SHA-256:
- estimated_poles.csv: `d411838c939b1dcc97f862ad7101d0df6f283896f4fdde9115e380a1036ff3b6`
- trial_diagnostics.csv: `3bc68761b948648ea58b43ecf050bb76032b1850df581096ba37c972757b8bbe`
- truth_matches.csv: `6a22dfafe6355b318209b365e4fb8791db272c0c2b3f9b2d630e5d04bd72d505`
- failures.json: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- summary.json: `2cdfab5d8a7f741d507edd74ec7da0eee84953d701453004fbf54c7f75730e15`
- WORKING_STATE.json: `290ef18fb159a5bf995a8dc9fd340b9f821f0a0c7b17506628704dff1827fdf1`
- CODE_MANIFEST.sha256: `4af21d0d0156d279676eb9fec8f4d4cf9d80497412d813fd5582ea22e1773fae`
- RUN_LOG.txt: `b8003bc4cb84f19effa5bcf0edba88b47c19e5844f7a83ed8e4ce271aa1f5083`

Mechanical result: 288/288 condition trials represented; 17,280 estimated-pole rows; 9,072 truth-match rows; 3,456 trial-diagnostic rows; zero failed fits.

## What Phase 0B established
Phase 0B does not admit the estimator to EEG. It is the development/calibration set used to expose failure boundaries and freeze the next prospective rules.

### 1. Observable-order evidence is strong but not identical to latent order
Define the singular-gap diagnostic at candidate order q:
`g_q = S_q / S_(q+1)`, where S are descending singular values from the SSI-COV block covariance decomposition.

Retrospectively on Phase 0B:
- all five strongly observable stationary four-state families had their order-4 gap at least 14.913;
- the 1/f null had no candidate-order gap larger than 6.220;
- the weak-observability family had an order-2 gap at least 121.900 and therefore exposed only the strong observable oscillatory pair.

This is a key identifiability result. SSI-COV can recover an effective observable rank without proving the full latent rank. A hidden/weak mode must not be manufactured because the latent generator happened to contain it.

### 2. Near degeneracy separates eigenvalue recovery from eigenvector recovery
For the near-degenerate family at order 4:
- median individual truth-vs-estimated mode-shape MAC = 0.990235;
- 10th percentile individual MAC = 0.849833;
- median truth-vs-estimated joint observable-subspace similarity = 0.999995;
- 10th percentile subspace similarity = 0.999974.

The pole estimates remained accurate while individual mode vectors became materially less stable. The joint modal subspace remained essentially intact. Therefore Phase 0C must switch from individual-vector claims to subspace claims when modes are spectrally crowded.

### 3. Weak observability is a genuine refusal/reduction boundary
The weak-observability family selected effective order 2 under the development gap rule in all 36 conditions. At order 2, the retained strong complex pair had:
- 90th-percentile normalized pole error = 0.002998;
- 10th-percentile MAC = 0.999989.

The omitted weak pair is not licensed merely because it exists in synthetic latent truth. This supports a reduced-order observable claim, not recovery of the hidden generator.

### 4. Real poles are not yet licensed for individual scalar interpretation
In `mixed_complex_real`, the complex pair was recovered well (90th-percentile normalized pole error 0.006122), but the two real poles were much less reliable:
- median normalized real-pole error = 0.119827;
- 90th percentile = 0.480769.

Therefore Phase 0C will not use individual real-pole values as admitted scalar measurements. Real poles may contribute to selected observable order, but their individual rates remain `REFUSE_REAL_POLE_SCALAR` until a dedicated calibration licenses them.

### 5. Split-record pole stability detects the stationary-model boundary
For all selected stationary families, the largest observed median first-half vs second-half normalized complex-pole-set distance was 0.013389.
For the long nonstationary-switch records that span both regimes, the smallest corresponding distance was 0.063014.

The development-derived prospective boundary is therefore frozen at 0.03 for Phase 0C. It is not rescored on Phase 0B as a pass criterion.

### 6. Cross-order persistence provides a second observable check
For stationary selected models, the largest median selected-order to next-higher-order complex-pole distance was 0.010003.
Phase 0C freezes a maximum of 0.02. A selected order at the edge of the candidate grid is refused because it cannot receive higher-order confirmation.

## Frozen Phase 0C selector/refusal rules
These rules are development-derived and become prospective only in Phase 0C.

1. Candidate observable order q is the smallest tested q with `S_q / S_(q+1) >= 10`.
2. If no candidate satisfies rule 1: `REFUSE_NO_ORDER`.
3. If q is the maximum candidate order: `REFUSE_EDGE_ORDER`.
4. If any selected full-record pole has nonnegative real part: `REFUSE_UNSTABLE`.
5. Complex-pole stationarity: median normalized Hungarian distance between first-half and second-half complex pole sets must be <= 0.03, otherwise `REFUSE_NONSTATIONARY`.
6. Cross-order persistence: median normalized distance between selected-order and next-higher-order complex pole sets must be <= 0.02, otherwise `REFUSE_ORDER_UNSTABLE`.
7. Individual complex mode shapes require split-record MAC >= 0.95.
8. A spectrally crowded pair is defined by `|omega_i-omega_j|/(alpha_i+alpha_j) <= 1`, with `lambda=-alpha+i omega`. Crowded modes are not assigned individual eigenvector claims; the joint observable subspace is primary.
9. Crowded/subspace claims require split-record subspace similarity >= 0.99.
10. Individual real-pole scalar values remain refused in Phase 0C.
11. No damping ratio, chi, diagnosis, phenotype, treatment variable, or whole-system scalar participates in selection.

## Frozen Phase 0C synthetic admission targets
The untouched holdout is passed only if all of the following hold:
- no mechanical/fit failures;
- >=90% model-admission rate on strongly observable stationary holdout trials;
- >=90% correct effective observable-order rate on those trials;
- >=90% refusal rate on off-model/null and intentionally nonstationary holdout trials;
- >=90% coverage of strong observable true complex modes;
- <=5% spurious admitted complex-mode rate;
- among admitted true complex modes, 90th-percentile normalized pole error <=0.02;
- 90th-percentile absolute frequency error <=0.10 Hz;
- 90th-percentile relative decay-rate error <=0.30;
- for admitted noncrowded individual mode shapes, 10th-percentile truth MAC >=0.95;
- for subspace-only crowded clusters, 10th-percentile truth subspace similarity >=0.99;
- the selector produces no clinical or whole-system scalar output.

If any target fails, the estimator is not admitted to EEG under this version. The failure is preserved and the next action is method revision or narrower scope, not threshold retuning on Phase 0C.

## Claim ceiling after Phase 0B
Supported:
- SSI-COV is a viable candidate for recovering observable complex modal structure in the tested stationary synthetic class.
- observable rank can be lower than latent rank under weak observability;
- individual eigenvectors can lose identifiability before the joint modal subspace does;
- real-pole scalar estimation is a current failure boundary;
- 1/f and nonstationary alternatives require explicit refusal gates.

Not supported:
- EEG validity;
- diagnosis or treatment organization;
- universal model order;
- recovery of hidden latent modes;
- universal eigenvector stability;
- reliable individual real-pole rates;
- any whole-system chi or preferred chi value.
