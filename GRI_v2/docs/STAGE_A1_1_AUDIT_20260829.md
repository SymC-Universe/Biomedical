# Stage A1.1 Fixed-n Calibration Audit - 2026-08-29

Status: PASS as a construction-bias closure. Claim ceiling remains a sample-size-calibrated static network map only.

## Purpose

Stage A1 showed that raw absolute-correlation coordinates had a finite-sample-size dependence across cancer cohorts. Stage A1.1 therefore froze a pre-result calibration in which every cancer was repeatedly subsampled to n=30 and the unchanged Stage A1 metrics were recomputed 100 times per cancer.

This calibration does not compute chi, does not use CV/2, does not create a composite stability score, and does not define an organization optimum.

## Integrity

- 32 cancer types.
- 50 Hallmark modules per cancer.
- 1,600 cancer-module calibration rows.
- 100 valid resamples for every cancer-module cell.
- 160,000 complete resample rows.
- No missing metric values in the resample or calibration tables.
- Maximum median PC1 imputation fraction: 0.0.
- Cache SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`.
- Hallmark membership SHA-256: `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`.

## Construction-bias result

Before fixed-n calibration, cancer-level median raw coordinates retained moderate association with cohort size:

- median pairwise Cin vs original n: Spearman rho approximately -0.4783;
- median PC1 fraction vs original n: rho approximately -0.3010;
- median Cout vs original n: rho approximately -0.4279.

After every cancer is evaluated at the same n=30, the corresponding associations collapse to near zero:

- calibrated median pairwise Cin vs original n: rho = -0.0317;
- calibrated median PC1 fraction vs original n: rho = -0.0880;
- calibrated median Cout vs original n: rho = -0.0563.

Conclusion: the cross-cancer finite-sample floor detected in Stage A1 is effectively removed by the frozen calibration.

## Topology preservation

The calibration removes the cohort-size artifact without erasing the network ordering.

Median within-cancer rank agreement between original A1 module values and fixed-n calibrated module medians:

- pairwise Cin: rho approximately 0.9893;
- PC1 fraction: rho approximately 0.9904;
- Cout: rho approximately 0.9199.

Minimum agreement across any cancer remains high:

- pairwise Cin: rho approximately 0.9602;
- PC1 fraction: rho approximately 0.9726;
- Cout: rho approximately 0.8292.

Within the fixed-n map:

- pairwise Cin vs PC1 fraction: median rho approximately 0.9427 across cancers;
- pairwise Cin vs Cout: median rho approximately -0.5710;
- PC1 fraction vs Cout: median rho approximately -0.6715;
- the Cin-Cout and PC1-Cout relationships are negative in all 32 cancer types.

Interpretation: the two internal-coherence measures are largely redundant descriptions of one static organization axis, whereas external coupling captures a distinct and opposing aspect of the transcriptomic network map.

## Uncertainty

The 5th-95th percentile widths from n=30 resampling are retained as calibration uncertainty, not p-values. Relative uncertainty is larger for some modules and especially for PC1/Cout, so individual cancer-module magnitudes must not be promoted without their resampling intervals.

## Scientific interpretation ceiling

Stage A1.1 supports the following only:

1. reproducible static Hallmark network topology exists in PanCanAtlas;
2. internal module coherence and external coupling are separable static coordinates;
3. the original cross-cancer sample-size distortion can be removed without destroying the module ordering;
4. no direction of these coordinates is defined as more optimal, healthier, more stable, or closer to a preferred state;
5. no chi, damping, regime, transition, phase, or dynamic claim follows from Stage A.

## Closure decision

Static Stage A is closed as a development measurement layer. The active map retains independent static coordinates for variability, lineage/context dependence, internal network coherence, and external network coupling.

The next branch is Stage B: add independently measured multiomic/context layers and determine which add non-redundant information. Dynamic interpretation remains deferred to genuine ordered perturbation/time-course data.

## Output hashes

- `STAGE_A1_1_SUMMARY.json`: `95f8b34fdb0e6aaf24897a318613a645ad3511303bdef95fc54e50f8249a7406`
- `stage_a1_1_fixed_n_calibration.csv`: `b4a260662f7f63bd0485b5e49182608efbd7d8fb897b7414f0a0e2576f108ac3`
- `stage_a1_1_cancer_level_diagnostic.csv`: `48bff6ca6e6dd557353db2bad51f4c6d2db7b0ec5ab355d90c75f21755bb52ee`
- `stage_a1_1_resample_metrics.csv.gz`: `b7aaefd1a0f961f053cceaa989acbc7311bbd452c6588f77d8bc7b13547fcb39`
