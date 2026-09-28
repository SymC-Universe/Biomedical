# Bio Chi C1Q-RS Repeated-Realization Uncertainty Map Postresult v1.0

**Status:** COMPLETE / REGION-DEPENDENT ESTIMATOR UNCERTAINTY  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** `NSD_vNext/docs/BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_PLAN_v0.2.md`  
**Freeze:** `NSD_vNext/docs/BIO_CHI_C1Q_RS_UNCERTAINTY_MAP_FREEZE_v1.0.md`

## Provenance

- Workflow: `NSD C1Q-RS Uncertainty Map`
- Run: `36372559076`
- Source head: `f70751773eb03e88e4f1c01c5458fa854fbc6d79`
- Complete artifact: `nsd-c1q-rs-uncertainty-complete`
- Artifact ID: `10949349324`
- Digest: `sha256:7331b6781838d3cd4f97f68ecb8dbc301035bfa7cd0f16454ddd80169c16d194`

Both frozen preflight cells passed. All eight full uncertainty cells passed and the merge completed successfully.

The complete artifact contains exactly 192 rate-level fits and 96 same-path fine/coarse pairs.

## Overall sampling behavior

All 192 C1Q-RS fits returned successfully.

Across the full frozen envelope:

- absolute chi error: median **0.01874**, interquartile range approximately **0.01014 to 0.05434**, maximum **0.31418**;
- absolute g error: median **0.09815**, interquartile range approximately **0.04249 to 0.21134**, maximum **0.91326**;
- absolute natural-frequency error: median **0.35167 Hz**, interquartile range approximately **0.15499 to 0.88494 Hz**, maximum **42.61224 Hz**.

Only 3/192 selected fits reached the prospectively defined numerical raw-boundary flag. Those three rows were all in cell 2.

The recurrence seed was admissible in 177/192 rows and supplied the winning C1Q-RS basin in 72/192.

These counts are estimator diagnostics, not biological frequencies or scientific thresholds.

## Rate structure

At 256 Hz:

- median absolute chi error: **0.01724**;
- median absolute g error: **0.07217**;
- median absolute natural-frequency error: **0.27532 Hz**;
- one numerical raw-boundary fit.

At exact-decimated 128 Hz:

- median absolute chi error: **0.02371**;
- median absolute g error: **0.12834**;
- median absolute natural-frequency error: **0.44638 Hz**;
- two numerical raw-boundary fits.

The coarse rate therefore increases estimator uncertainty descriptively, especially for g and natural frequency, but does not create uniform failure.

Across 96 same-path pairs, median rate drift was:

- chi: **0.01709**;
- g: **0.09021**;
- natural frequency: **0.22881 Hz**.

Maximum rate drift was much larger because a small number of cells were unstable:

- chi: **0.30324**;
- g: **1.39782**;
- natural frequency: **32.36628 Hz**.

## Function-map heterogeneity

The repeated-realization result is clearly region-dependent.

Cells 0, 1, 3, and 4 were comparatively compact at both rates. Their median absolute chi errors were approximately 0.008 to 0.015, with no numerical-boundary fits.

Cell 5 showed moderate dispersion, with median absolute chi error about 0.044 at 256 Hz and 0.050 at 128 Hz.

Cell 7 remained broadly recoverable but showed wider g and natural-frequency dispersion, especially after decimation.

Cell 6 showed a clearer weak-information region. Its truth has low latent fraction (Aapprox0.292), high natural frequency (approx18.95) Hz, (chiapprox0.496), and (gapprox-0.720). Median absolute chi error increased from about 0.053 at 256 Hz to 0.081 at 128 Hz, with a coarse-rate maximum of 0.314. No raw-boundary fit occurred, indicating broad sampling variability rather than a simple optimizer-boundary artifact.

Cell 2 was the strongest instability. Its truth is (Aapprox0.504), natural frequency (approx22.10) Hz, (chiapprox0.757), and (gapprox0.087). At 128 Hz:

- median absolute chi error: **0.15397**;
- median absolute g error: **0.91010**;
- median natural-frequency error: **4.58668 Hz**;
- maximum natural-frequency error: **42.61224 Hz**.

All three prospectively flagged raw-boundary rows occurred in cell 2, including fits near (chiapprox1) with severely distorted frequency and g.

The same cell also showed the largest same-path rate instability, with median chi drift about 0.123, median g drift about 0.751, and median natural-frequency drift about 3.30 Hz.

## Scientific interpretation

The uncertainty map supports **region-dependent estimator sampling uncertainty**, not uniform estimator failure.

Most of the frozen C interior tested here shows compact repeated-realization recovery with no recurring numerical-boundary pathology. A minority of truths show substantially weaker finite-sample recovery, and those weak regions are not explained by the old C1Q search defect because C1Q-RS is already active.

Two distinct difficult patterns are visible:

1. cell 2 combines high chi and high frequency and shows a severe likelihood/identifiability instability with repeated g/frequency distortion and three raw-boundary fits;
2. cell 6 combines low latent fraction, high frequency, and strongly negative g and shows broad chi dispersion without raw-boundary saturation.

This distinction matters. Cell 2 appears partly nonregular/boundary-attracted in finite samples, whereas cell 6 looks more like weak information with ordinary interior solutions.

Because only eight truth coordinates were frozen, these observations do not establish causal parameter dependence or a general biological operating boundary.

## Claim consequences

- **C1Q-RS preferred qualification search implementation:** retained.
- **C1Q-RS production promotion:** no.
- **Real-EEG local chi:** unlicensed.
- **Biological prevalence:** not estimated.
- **Scientific admission threshold:** none.
- **Uniform uncertainty assumption:** rejected for the tested qualification envelope.
- **Region-dependent uncertainty:** supported descriptively.
- **Need for uncertainty-aware admission/refusal:** strengthened.

## Post-execution deviation audit

The frozen plan was followed.

- exact eight truth cells retained;
- exact twelve seeds retained;
- 60 s, 256 Hz, and exact factor-2 decimation retained;
- all 192 rows retained;
- no boundary or outlier row excluded;
- numerical raw-boundary definition remained (10^{-6}) from the raw box edge;
- no confidence interval or admission threshold was inferred from the 12-realization summaries;
- no biological or semantic claim was promoted.

No material plan deviation occurred.

## Next scientific requirement

The next question is no longer whether estimator uncertainty exists, but **how it should be quantified prospectively on a single observed series** so that unstable local coordinates can be refused rather than reported with false precision.

Before choosing that method, compare established uncertainty toolkits for state-space/continuous-time maximum likelihood, especially profile likelihood, parametric bootstrap, information/Hessian approximations, and practical-identifiability methods near boundaries and weakly identified modes.

A later plan should test candidate uncertainty methods against the repeated-realization source-of-truth map, with particular attention to cells 2 and 6 and to representative compact cells. No empirical admission threshold should be chosen before that method-comparison step.
