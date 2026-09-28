# Bio Chi Single-Series Uncertainty Method Comparison Plan v0.2

**Status:** APQ-2 REVISED / BLOCKER CONTRACT PENDING  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, uncertainty-method qualification  
**Parent uncertainty map:** `BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_POSTRESULT_v1.0.md`  
**APQ ledger:** `BIO_CHI_SINGLE_SERIES_UNCERTAINTY_APQ_LEDGER_v0.1.md`

## Scientific target

Determine which single-series uncertainty diagnostic best reflects the already-known repeated-realization sampling behavior of local chi under correct C-family specification, while refusing false precision in weak or boundary-attracted cases.

This plan compares three established uncertainty families on exactly the same frozen observed series and exact C1Q-RS likelihood:

1. local observed-Hessian curvature;
2. chi profile likelihood;
3. fitted-model parametric bootstrap.

No method is allowed to define a biological or empirical admission threshold in this experiment.

## Prior-method basis

The literature basis is:

- profile likelihood for practical identifiability [Rau09b, Wie21, Lil19];
- local Hessian/Fisher curvature as a cheap asymptotic comparator, with known limitations in nonlinear/non-identifiable settings [Rau09b, Wie21, Lil19, Mat16];
- finite-sample likelihood-ratio calibration concerns [Ton23];
- Gaussian state-space innovations/parametric bootstrap for finite-sample estimator precision [Sto91, Sto04b];
- sampled continuous-time oscillator likelihood multimodality [Gon18];
- Bayesian/full-posterior methods remain a later option if profile/bootstrap are insufficient [Sin17, Swa22].

## Frozen cases

Use four cells from the completed uncertainty map:

- cell 0: compact representative;
- cell 1: compact representative with lower latent fraction;
- cell 6: weak-information representative without raw-boundary saturation;
- cell 2: strongest boundary/nonregular representative.

For every cell use realization seed `989969` at both:

- 256 Hz fine rate;
- exact factor-2 same-path 128 Hz rate.

Selection is by predeclared postresult category, not by the seed-specific outcome of seed 989969.

The full 12-realization distributions for each truth/rate are the external known-truth reference. They are already viewed P0-Q evidence, not untouched confirmation.

## Exact likelihood-equivalence prerequisite

The physical-coordinate wrapper must pass all tests in
`tests/test_continuous_lineage_profile_equivalence.py`
before this plan can freeze.

The contract verifies:

- physical (A,f_n,chi,g) round-trip through the existing C1Q raw parameterization;
- physical-wrapper NLL equals the canonical raw C1Q NLL;
- fitted/raw interior coordinates round-trip without changing the likelihood;
- both 128 and 256 Hz routes.

If that contract fails, execution is held and no profile result may be interpreted.

## M1. Local observed-Hessian comparator

Evaluate numerical second derivatives of the physical-coordinate NLL around the selected C1Q-RS optimum using coordinates:

[
(A,; f_n,; chi,; g).
]

Use central finite differences with frozen relative steps:

- A: max((10^{-4}), (10^{-3}A));
- (f_n): max(0.005 Hz, (10^{-3}f_n));
- chi: max((10^{-4}), (10^{-3}chi));
- g: (10^{-3}).

If a step crosses the admissible physical domain, use the largest symmetric step that stays inside; if no stable symmetric step exists, report `HESSIAN_REFUSED_BOUNDARY`.

Report:

- Hessian matrix;
- eigenvalues;
- condition number;
- positive-definiteness;
- inverse-Hessian covariance when invertible/PD;
- local chi standard error (sqrt{H^{-1}_{chichi}});
- explicit coordinate units.

Hessian results are local coordinate-dependent diagnostics only.

## M2. Chi profile likelihood

Profile the exact existing C1Q likelihood in physical coordinates.

Frozen chi evaluation set:

- 61 uniformly spaced values on ([0.05,0.98]);
- fitted chi inserted exactly if not already present;
- generating true chi inserted exactly if not already present.

At each fixed chi, optimize nuisance (A,f_n,g).

Nuisance search must include:

- continuation start from the best neighboring profile point where available;
- physical coordinates corresponding to the global C1Q-RS optimum projected onto the fixed chi;
- recurrence-derived start if admissible;
- at least six fixed interior nuisance starts spanning A/g and frequency neighborhood.

Retain the lowest finite nuisance-optimized NLL across starts.

Mechanical profile contracts:

- the fitted-chi profile point must reproduce the global C1Q-RS NLL within relative tolerance (10^{-5});
- the true-chi delta-NLL must be preserved;
- every profile point records winning start and nuisance optimum;
- nonfinite/no-solution points remain explicit.

Report the complete profile and:

- (Delta)NLL relative to the global optimum;
- true-chi (Delta)NLL;
- fitted-chi (Delta)NLL;
- number and locations of local minima on the evaluated grid;
- whether the profile is still decreasing toward either grid edge;
- whether distinct low-profile basins are separated by higher-NLL regions.

No LR/confidence cutoff is applied.

## M3. Fitted-model parametric bootstrap

For each of the eight cases, simulate from its selected C1Q-RS fitted model using the same duration and sampling rate.

Frozen bootstrap seeds:

`700001` through `700032`.

For each of 32 replicates, refit unchanged C1Q-RS and preserve:

- chi, g, natural frequency;
- signed difference from the original fitted coordinates;
- optimizer/boundary diagnostics.

Report full bootstrap values and mean, median, SD, MAD, quartiles, and range.

The bootstrap is explicitly conditional on the fitted model. It is compared against the known-truth repeated-realization distribution and cannot by itself establish truth coverage.

## Comparison against known-truth repeated realizations

For each truth/rate compare:

- local Hessian chi SE;
- full chi profile geometry;
- bootstrap chi distribution;
- full completed 12-realization known-truth chi distribution.

Also preserve A, (1-A), true frequency, true chi, true g, cycles observed, and the single-series point estimate.

Qualitative failure patterns of interest are frozen as:

- Hessian compact while profile is open/multibasin and known-truth dispersion is broad;
- fitted-model bootstrap compact while known-truth dispersion is broad or shifted;
- profile exposes weak/boundary geometry in cells 2/6 while remaining compact in cells 0/1;
- all methods compact in cells 0/1;
- profile nuisance search itself fails mechanical reproducibility.

No one-seed coverage probability or winner score is defined.

## Staged execution

### Stage A: mechanical profile preflight

Cases:

- cell 0 fine;
- cell 2 coarse.

Requirements:

- physical-likelihood equivalence contracts already PASS;
- fitted-chi profile point reproduces global NLL;
- full profile grid serializes;
- Hessian serializes or explicitly refuses;
- no scientific profile shape changes the method set.

### Stage B: eight-case profile + Hessian execution

Run all four cells at both rates.

### Stage C: bootstrap execution

Only after Stage A/B complete mechanically. Bootstrap runs all eight cases with 32 frozen seeds.

No scientific outcome from profile/Hessian may alter bootstrap seed count, cases, or method.

## Outcome architecture

**Profile is the clearest identifiability discriminator:** compact cases have closed/steep profiles while difficult cases have flat, boundary-directed, disconnected, or multimodal profiles; Hessian may understate this. Proceed to prospectively calibrate profile-based refusal with finite-sample resampling.

**Profile + bootstrap complement each other:** profile shows geometry and bootstrap roughly tracks repeated-realization dispersion. Proceed with combined architecture.

**Bootstrap conditionality fails materially in difficult cases:** bootstrap is not adequate as standalone calibration and remains secondary.

**Profile implementation/optimization is unstable:** hold uncertainty architecture and resolve profile search before proceeding.

**No method distinguishes compact from difficult truth:** no current single-series uncertainty gate is justified.

## Claim ceiling

This method comparison can select an uncertainty method family for later P0-Q calibration only. It cannot define confidence levels, empirical admission thresholds, production promotion, model membership, biological prevalence, or real-EEG local chi.

## Reproducibility

Exact cases, observed seed, profile grid, nuisance search recipe, Hessian steps, bootstrap seeds, software environment, and source repeated-realization artifact are frozen before execution.

## APQ status

All non-blocking APQ objections are incorporated. APQ closure remains pending only the physical-likelihood equivalence contract (B1).
