# Meneses 2026 E. coli PMF recovery Bio Chi preflight

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC RAW-TIME-SERIES ANALYSIS  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct experimental qualification

## Status

The next Bio Chi experiment is a direct experimental perturbation/recovery system rather than another model-only test. The source is Meneses et al. (2026), with curated motor-speed, TMRM, and cell-area time series committed directly in the authors' GitHub repository at upstream commit `d14d0caaa07299f13d1b1121d1e4630454fd724b`.

The publication and repository summaries were inspected during qualification, so the qualitative outcomes are known. This is not a blinded discovery experiment. The frozen analysis asks a different question: what minimum representation is required for the measured collapse-and-recovery event, and does the source support a legitimate scalar `chi_bio` carrier?

## Whole event first

The frozen whole event is hyperosmotic shock at 200, 300, 400, or 500 mM sucrose followed by energetic and physical displacement and recovery.

Three source-native readouts are retained:

- flagellar motor speed as the high-time-resolution PMF reporter;
- TMRM as an independent membrane-potential assay;
- cell area as a physical shrinkage/recovery observable.

The motor and fluorescence/area cells are not paired. Cross-assay inference therefore occurs only at the condition level; cell counts do not inflate the number of independent cross-assay conditions.

## Representation hierarchy

- **Bio Chi:** whole dose-conditioned energetic/physical collapse-and-recovery relation.
- **Chi_bio:** the minimum multicoordinate representation required to preserve that event.
- **chi_bio:** not opened. The source explicitly treats fitted sigmoid/exponential timescales as response summaries rather than mechanistic motor models, so a fitted tau is not silently renamed as biological chi.

## Cross-project reason for this test

The HOG1 model gate showed that a fixed network and parameterization can require multicoordinate response organization when input context changes. Kizilirmak showed that a pre-stimulus global scalar does not determine later dynamics across inputs. Chemistry and Foundations independently warn that local coordinates need not determine embedded recovery. The present E. coli system tests the next missing piece: **directly measured recovery with orthogonal energetic and physical observables**.

Those earlier projects constrain the test design only. They do not count as evidence for the E. coli result.

## Frozen primary questions

1. Can the authors' source-native motor fit parameters and orthogonal TMRM/cell-area summaries be reproduced from the committed time series?
2. Does perturbation depth change strongly while the source-native response timescales remain comparatively dose-robust under the frozen criterion?
3. Does a one-coordinate condition representation preserve the full energetic/physical recovery event?
4. Is any source-native scalar dynamically licensed as `chi_bio`?

## Stop rule

Any source, schema, fit, or reproduction failure is preserved. No coordinate will be removed after result inspection to improve scalar compression. A descriptive tau remains a descriptive tau unless an independently justified dynamical carrier is established.
