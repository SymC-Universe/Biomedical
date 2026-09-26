# E. coli PMF recovery Bio Chi qualification freeze v0.1

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct-measurement representation qualification

## Source

Meneses et al. (2026), *Biophysical Journal*, "Osmotic stress triggers fast and reversible PMF collapse in Escherichia coli."

Pinned upstream repository:

- repository: `wadhwalab/2026-Meneses-Osmotic`
- upstream commit: `d14d0caaa07299f13d1b1121d1e4630454fd724b`
- bead manifest blob: `115688c62927e8491f0b85134b89d40209110e0d`
- manuscript source blob: `d7f6f03c355854b3feb0fe7b7cad8383ee5469a1`
- adaptation notebook blob: `86f8ce55d39681e769b6b3390e11c95da6359ac8`
- shock-fit notebook blob: `6cd23893cf951db3893ef34b7b69e6ccd634f049`
- TMRM summary blob: `52c0a1957da75819e0d670a1013f3fe6b0552290`
- cell-area summary blob: `66e8d49b3d65e7f0304f0b8c33854e580f9292f5`

The source publication and repository were inspected during candidate selection. Therefore the qualitative facts that motor speed and TMRM fall after hyperosmotic shock and later recover are literature-open. No directional result from this experiment is presented as blinded confirmation.

## Whole biological event

A hyperosmotic perturbation drives a rapid energetic and mechanical displacement in *E. coli*, followed by recovery or adaptation. The frozen target is the organization of that perturbation-recovery event, not any one fitted parameter.

Primary measured carrier:
- single-cell flagellar-motor rotation speed from curated bead-assay Parquet traces.

Independent supporting observables:
- TMRM fluorescence as a membrane-potential readout;
- cell area as a mechanical state readout.

## Frozen primary lineage

Use the source "Sucrose" bead assay at 200, 300, 400, and 500 mM for reversible shock/removal dynamics.

For each single-cell motor trace:
1. normalize to the pre-shock mean over all finite samples at time <= 175 s;
2. fit the source-native collapse model on 175-240 s:
   `S(t)=A/[1+exp((t-175-t0)/tau_dec)]+C`;
3. fit the source-native removal-recovery model on 270-360 s:
   `S(t)=B[1-exp(-(t-270)/tau_inc)]+D`;
4. compute nonparametric response coordinates from the normalized trace:
   - minimum during 180-270 s;
   - collapse amplitude = 1 - minimum;
   - mean early post-removal recovery over 330-350 s;
   - recovery fraction = (mean_330_350 - minimum)/(1 - minimum), when defined.

Fits that fail, hit nonphysical values, or lack sufficient finite samples are retained as failures and excluded only under the frozen source-fit validity rules below.

## Frozen sustained-adaptation lineage

Use the source "Adaption" sucrose assay at 200, 300, 400, and 500 mM.

For each single-cell trace:
1. normalize to the pre-shock mean for time < 180 s;
2. preserve the source-native 1 s median filtering semantics;
3. fit 250-600 s with
   `S(t)=B[1-exp(-(t-200)/tau_adapt)]+D`,
   bounds `B in [0,2]`, `tau_adapt in [0.1,500]`, `D in [0,1.5]`;
4. retain `tau_adapt` and plateau `B+D`.

## Frozen representation hierarchy

- **Biological chi:** the whole perturbation-recovery relation linking osmotic context to energetic displacement, recovery/adaptation, and supporting membrane/mechanical observables.
- **Chi_bio:** candidate multicoordinate dynamic organization of the motor response. Initial frozen coordinates are collapse amplitude, `tau_dec`, `tau_inc`, and removal-recovery fraction for the reversible-shock lineage, with `tau_adapt` and sustained plateau analyzed as a separate adaptation projection.
- **chi_bio:** not licensed at freeze. A single scalar may be admitted only if a one-coordinate representation predicts the held-out multicoordinate motor response across concentrations without materially degrading reconstruction and without post hoc feature selection.

## Primary representation test

Construct one row per successfully fitted reversible-shock cell using the four frozen coordinates:
`[collapse_amplitude, log(tau_dec), log(tau_inc), recovery_fraction]`.

Standardize each coordinate using training-fold statistics.

Compare:
- R1: one latent coordinate, PCA rank 1;
- R2: two latent coordinates, PCA rank 2;
- Rfull: direct standardized four-coordinate representation.

Use leave-one-concentration-out cross-validation. In each fold, fit PCA only on the three training concentrations and reconstruct the held-out concentration.

Primary loss is mean squared standardized reconstruction error across all held-out cells and coordinates.

Frozen adequacy rules:
- R1 is **adequate** only if its total held-out MSE is <= 0.25 AND no individual coordinate has held-out RMSE > 0.75.
- R2 is **required** if R1 fails and R2 improves total held-out MSE by >= 25% while meeting the same per-coordinate RMSE ceiling.
- otherwise disposition is **MULTICOORDINATE_UNRESOLVED_P0Q** and the full representation is retained.

This comparison is a representation test, not a mechanistic model-selection claim.

## Independent observable triangulation

Recompute the source-native population summaries for TMRM and cell area from the committed Parquet files for 0, 200, 300, 400, and 500 mM using the source-defined 5 s frame interval, shock frame 35, ten-frame baseline, and committed shock/recovery windows.

The independent-observable check asks only whether:
1. both TMRM and cell area show non-control perturbation under the same concentration series;
2. recovery-window means are not numerically identical functions of shock strength;
3. the motor representation result is not relabeled as a membrane-potential or morphology mechanism.

## Scalar gate

A damping-style scalar `chi_bio` is not licensed merely because the source contains fitted time constants. The source models are sigmoidal/exponential summaries, not an identified second-order oscillator. A scalar result may therefore be:
- `NOT_LICENSED_SOURCE_MODEL_NONOSCILLATORY`;
- `ONE_COORDINATE_COMPRESSION_ADEQUATE_BUT_NOT_CHI_BIO`;
- or, only if an independently identifiable dynamical scalar carrier is found before result inspection, a separately frozen scalar test.

No `chi_bio=1` boundary is used.

## Failure and outlier rules

Every failed fit or source/retrieval failure is preserved with cell identity, condition, failure class, and root-cause text.

A failed fit may be excluded from the representation matrix only if:
- the optimizer fails to converge;
- fitted `tau` is nonfinite or <=0;
- fewer than 20 finite samples exist in the frozen fit window;
- baseline is nonfinite or zero.

No outlier is removed solely for being numerically extreme.

## Claim ceiling

This experiment can establish only a P0-Q direct-measurement representation result in the released curated data. It cannot establish a universal biological chi law, a universal scalar, a causal PMF mechanism, or a pan-bacterial boundary.
