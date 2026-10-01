# Healthy Baseline Dortmund Native Preflight Result v0.1

**Date:** 2026-10-01  
**Status:** DEVELOPMENT PREFLIGHT COMPLETE  
**Evidence class:** independent healthy native EEG, pipeline/access qualification only  
**Dataset:** OpenNeuro `ds005385`, snapshot `1.0.3`  
**Kaggle kernel:** `symcuniverse/nsd-dortmund-native-preflight-v0-1`  
**NSD quantities computed:** none

## Purpose

Test transport, EDF reading, preprocessing, and native feature extraction before any full healthy-baseline reproduction.

The pilot was prospectively limited to 12 participants selected deterministically by sex and target ages 20, 30, 40, 50, 60, and 70. It was never authorized to define healthy norms.

## Execution result

- expected EDF recordings: 48;
- successfully processed: 48;
- failed: 0;
- four recordings per participant: EC/EO × pre/post, session 1;
- no clinical/disorder data used.

Pilot paired EC/EO summaries:

| Feature | EC mean | EO mean | paired Cohen's d, EC minus EO | Published full-sample reference |
| --- | ---: | ---: | ---: | --- |
| posterior alpha relative power | 0.466887 | 0.179670 | 2.2159 | 0.453 / 0.190 / d=1.553 |
| alpha peak frequency, Hz | 9.6029 | 9.8877 | -0.2903 | 9.946 / 9.702 / d=0.238 |
| theta/beta ratio | 0.9732 | 0.9245 | 0.0712 | 0.862 / 1.157 / d=-0.342 |
| aperiodic exponent | 1.0315 | 1.1289 | -0.3580 | 1.288 / 1.511 / d=-0.761 |

## Interpretation

The pilot establishes transport and implementation feasibility, not normative inference.

The strongest state effect, posterior alpha attenuation with eyes open, reproduced clearly and the absolute means were close to the published full-sample values. Smaller effects did not reproduce direction consistently at n=12. This is preserved rather than tuned away and reinforces the need for the full sample.

The pilot used a broad posterior-channel rule for one feature family and did not implement the artifact-rejection/model pipeline of the later source-complete 2026 normative paper. Therefore it is superseded as the production reproduction design by the source-faithful full-sample plan.

## Failure/outlier record

The Kaggle science kernel completed and generated all result files. A later local `kaggle kernels output` command returned a Windows console `charmap` encoding error while printing log filenames, after the scientific CSV/JSON outputs had already downloaded successfully. Classification: local transport/UI encoding issue; scientific output unaffected.
