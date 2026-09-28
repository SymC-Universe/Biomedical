# Bio Chi Single-Series Uncertainty Method Comparison Plan v0.1

**Status:** APQ-2 SUBSTANTIAL DRAFT  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, uncertainty-method qualification  
**Parent uncertainty map:** `BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_POSTRESULT_v1.0.md`

## Scientific target

The repeated-realization map establishes that C1Q-RS estimator uncertainty is region-dependent under correct C-family specification. Real biological inference, however, will usually begin from one observed series rather than repeated known-truth realizations.

The next question is:

> Which single-series uncertainty diagnostic best reflects the known repeated-realization sampling behavior of local chi without falsely declaring precision in weak or boundary-attracted regions?

The comparison is methodological. It does not create an admission threshold.

## Prior-method control

Prior work supports the following hierarchy:

- profile likelihood is a standard practical-identifiability diagnostic and can reveal open/flat parameter directions missed by local curvature methods [Rau09b, Wie21, Lil19];
- Hessian/Fisher uncertainty is a useful local/asymptotic comparator but can remain finite in practically non-identifiable nonlinear problems [Rau09b, Wie21, Lil19];
- finite-sample likelihood-ratio calibration can differ materially from asymptotic chi-square assumptions [Ton23];
- innovations/parametric bootstrap is established for Gaussian state-space parameter uncertainty and can outperform conventional asymptotics in finite samples [Sto91, Sto04b];
- sampled continuous-time oscillator likelihoods can contain multiple local maxima [Gon18].

No asymptotic LR cutoff or confidence level is frozen in this plan.

## Frozen source truths

Use four cells from the completed uncertainty map, chosen by a rule frozen from the postresult categories rather than by individual-seed outcome:

- cell 0: compact representative;
- cell 1: compact representative with lower latent fraction;
- cell 6: weak-information representative without raw-boundary saturation;
- cell 2: strongest boundary/nonregular representative.

For each cell use the first prospectively frozen uncertainty-map realization seed `989969`, at both 256 Hz and exact-decimated 128 Hz.

This gives eight single-series cases.

The completed 12-realization distributions for those same truth/rate cells are the external known-truth reference for method calibration. They are already viewed and are not confirmation data.

## Methods compared

### M1. Local observed-Hessian curvature

Compute a numerical Hessian of the C1Q-RS negative log-likelihood at the selected optimum in a direct physical parameterization centered on:

- latent fraction A;
- natural frequency (f_n);
- chi;
- g.

Report Hessian eigenvalues, condition number, local covariance if positive-definite/invertible, and delta/local standard error for chi.

This method is diagnostic only. It is not assumed valid near boundaries or nonquadratic profiles.

### M2. Chi profile likelihood

Reparameterize the same C likelihood directly by (A,f_n,chi,g). For a frozen grid of chi values, fix chi and re-optimize (A,f_n,g) with multi-start optimization.

Frozen profile grid:

- 61 chi values uniformly spaced from 0.05 to 0.98;
- additionally include the fitted chi and true chi exactly as profile evaluation points;
- nuisance bounds are the physical image of the current C1Q-RS domain;
- all eight cases use the same grid and optimizer budget.

Report the complete (Delta)NLL profile relative to the global C1Q-RS optimum, number and location of local minima, boundary behavior, and whether the profile remains descending/flat toward either profile edge.

No (Delta)NLL threshold is used to define a confidence interval in this experiment.

### M3. Parametric state-space bootstrap

For each of the eight observed cases:

1. treat the selected C1Q-RS fitted model as the generating model;
2. simulate 32 independent bootstrap realizations with the same duration/rate and observation structure;
3. refit each with unchanged C1Q-RS;
4. preserve full bootstrap distributions of chi, g, and natural frequency.

Bootstrap seeds are frozen as integers `700001` through `700032` for every case. Seed reuse across cases is allowed because cases are analyzed separately; it does not create cross-case independence.

Thirty-two replicates are an exploratory finite-sample calibration sample, not enough to define a final coverage threshold.

## Comparison to repeated-realization source of truth

For each case, compare:

- Hessian chi standard error;
- shape and spread of the full chi profile;
- bootstrap chi SD/MAD/quartiles/range;
- the already-completed 12-realization empirical chi SD/MAD/quartiles/range at that truth/rate.

No single metric is declared the winner by a frozen numerical score. The goal is to detect qualitative calibration failures:

- local curvature tiny while empirical/bootstrapped/profile uncertainty is broad;
- profile flat/open/multimodal while Hessian remains finite;
- bootstrap substantially narrower or shifted than known-truth repeated realizations;
- compact cells where all methods agree reasonably.

## Outcome architecture

**Profile/Hessian agreement in compact cells, profile warning in difficult cells:** supports profile likelihood as primary identifiability diagnostic with Hessian as cheap screen.

**Bootstrap tracks repeated-realization dispersion while profile geometry identifies weak directions:** supports a combined profile + bootstrap uncertainty architecture.

**Bootstrap fails in boundary/nonregular cells:** bootstrap requires a boundary-specific calibration/refusal rule and cannot alone support admission.

**Profile itself is unstable or optimizer-sensitive:** deeper likelihood geometry must be resolved before an uncertainty gate.

**All methods fail to distinguish compact from difficult cells:** no single-series uncertainty gate is currently justified.

## Claim ceiling

This plan can choose or reject an uncertainty *method family* for later qualification. It cannot:

- define an empirical chi admission threshold;
- define a confidence level for real data;
- validate C-family membership;
- promote C1Q-RS to production;
- license real EEG;
- infer biological prevalence.

## Mechanical preflight

Run cell 0 fine and cell 2 coarse only.

Preflight checks implementation, profile completeness, Hessian computation, bootstrap serialization, and design identity. Scientific profile shape or bootstrap spread cannot retune the frozen method set.

## Reproducibility

Exact source cells/rates/seed, profile grid, bootstrap seeds, optimizer budgets, software environment, and output schema are frozen before execution.

## APQ request

`APQ-2 SUBSTANTIAL` because the result will determine which uncertainty method proceeds toward the later admission architecture.
