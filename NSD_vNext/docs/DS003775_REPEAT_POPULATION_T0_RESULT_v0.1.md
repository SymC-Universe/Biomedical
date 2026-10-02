# ds003775 42-Subject Repeat-Population T0 Result v0.1

Date: 18 September 2026  
Status: T0 LABEL-BLIND POPULATION RESULT / DESCRIPTIVE ONLY  
Dataset: OpenNeuro `ds003775`  
Workflow: `NSD ds003775 42-Subject Repeat Population`  
Run: `35304835270`  
Result: SUCCESS  
Head SHA: `3b72a54a4c590f10e5ec1ca43811be639ee72365`  
Population-summary artifact digest: `sha256:00e418aee53b30377799a509db1523bc3ba7f12e18e3e62ad5a190598e16d7fc`

## 1. Scope

This is the first population-scale execution of the frozen label-blind T0 descriptive pipeline on the complete 42-subject repeat-session subset of `ds003775`.

The workflow processed:

- 42 independent subjects;
- two repeat sessions per subject;
- 84 pinned EEG recordings;
- exact D4 identity re-verification before analysis;
- full-recording Welch PSD;
- the frozen descriptive periodic/aperiodic candidate.

The independent unit is the **subject**. Channels are repeated measurements nested within subjects and are not counted as independent participants.

This result does not establish a healthy boundary, trait biomarker, diagnosis, prognosis, damping ratio, or local chi.

## 2. D4 execution result

All 42 subject pairs completed exact pinned-payload verification inside the population workflow before their numerical outputs were generated.

Current scope statement:

`D4_REPEAT_POPULATION_VERIFIED_FOR_FROZEN_42_SUBJECT_SUBSET`

This does not promote all 111 unique subjects in the dataset to D4. It closes D4 for the exact 84-recording repeat subset used in this T0 qualification task.

## 3. Raw Welch repeat structure

Across the 42 subjects:

| Descriptive quantity | N | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Global median log-PSD correlation | 42 | 0.99146 | 0.65910 | 0.99756 |
| Median channel log-PSD correlation | 42 | 0.97946 | 0.64672 | 0.99048 |
| Minimum channel log-PSD correlation | 42 | 0.74840 | -0.80173 | 0.93079 |

Interpretation:

- typical repeat spectral **shape** similarity is high under the frozen Welch representation;
- the broad medians must not hide strong subject/channel outliers;
- the minimum-channel distribution demonstrates that a high global summary does not imply every channel is repeat-stable;
- this layer is therefore useful for the Function Map and simultaneously supplies a real Limit Map.

The correct forward use is subject-aware and channel/region-aware reliability analysis, not conversion of the global correlations into a clinical score.

## 4. Descriptive periodic/aperiodic repeat structure

Across subjects:

| Descriptive quantity | N | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Median absolute aperiodic-exponent difference per subject | 42 | 0.20476 | 0.09570 | 1.41949 |
| Exact same peak-count fraction per subject | 42 | 0.46094 | 0.25000 | 0.89063 |
| Exact same zero-peak-state fraction per subject | 42 | 0.97656 | 0.46875 | 1.00000 |
| Median nearest first-listed-peak center difference, Hz | 42 | 0.28292 | 0.03774 | 2.25170 |

Across the 84 sessions:

| Limit-map quantity | N | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Fixed-vs-knee model-family disagreement fraction | 84 | 0.42188 | 0.12500 | 0.92188 |
| Max-peak-count saturation fraction | 84 | 0.07813 | 0.00000 | 0.51563 |
| Zero-peak channel fraction | 84 | 0.01563 | 0.00000 | 0.60938 |
| Width-boundary hits per channel | 84 | 0.05469 | 0.00000 | 0.29688 |

## 5. Scientific decision

The population result is deliberately mixed.

### What survives

1. Raw Welch spectral shape is highly repeat-similar for the typical subject under this acquisition family.
2. Zero-peak state is often repeat-consistent.
3. The frozen pipeline can execute reproducibly on the whole repeat subset while preserving subject/session hierarchy and pinned D4 identity.

### What does not earn promotion

1. Exact peak count is not highly repeat-stable at the population level. The median same-count fraction is only about 0.46.
2. Fixed-versus-knee model-family disagreement is substantial, with a median near 0.42 of channels per session and a maximum above 0.92.
3. Aperiodic-exponent differences have a long upper tail, including large subject-level outliers.
4. First-listed-peak center differences also contain substantial outliers.
5. Global PSD similarity cannot be used to erase channel-specific instability.

Current disposition:

`RAW_WELCH_DESCRIPTIVE_LAYER = POPULATION-USEFUL_WITH_LIMITS`

`SPECPARAM_DESCRIPTIVE_LAYER = RETAIN_FOR_ATLAS/LIMIT_MAP; NOT_A_STANDALONE_TRAIT_BIOMARKER`

No settings are retuned after seeing this population result.

## 6. Channel-wise subject-aware repeatability result

The frozen aggregation was extended and re-run without changing the spectral parameterization.

Qualification workflow:

- `NSD ds003775 42-Subject Repeat Population`
- run `35337659470`
- result: **SUCCESS**
- population-summary artifact digest: `sha256:0859c127ca1cac7f2789fb12b7e66b1453f9ec6fb250e20f11eed6e84b9e0bb2`

The continuous repeatability statistic is **ICC(A,1)**: two-way mixed, absolute-agreement, single-measure, with subjects as independent rows and the two repeat sessions as columns. Channels are summarized separately rather than treated as independent participants. Negative ICC values would be retained rather than clipped.

Across the 64 channels:

| Channel-wise repeatability quantity | N channels | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Aperiodic exponent ICC(A,1) | 64 | 0.65882 | 0.40278 | 0.83557 |
| Exact peak-count agreement fraction | 64 | 0.53571 | 0.30952 | 0.71429 |
| Exact zero-peak-state agreement fraction | 64 | 0.90476 | 0.78571 | 1.00000 |

Additional distribution facts:

- all 64 aperiodic-exponent ICC values were non-negative in this sample;
- the 10th/25th/75th/90th percentiles of exponent ICC(A,1) were approximately 0.4864 / 0.5681 / 0.7389 / 0.7876;
- peak-count exact agreement remained limited even after changing the aggregation view from subject-wise to channel-wise;
- zero-peak-state agreement remained substantially more repeat-consistent than exact peak count, but was not perfect.

The spatial pattern is heterogeneous. For example, exponent ICC(A,1) ranged from about 0.403 at FT8 and 0.412 at AF8 to about 0.816 at FC2 and 0.836 at F2. These are **descriptive channel differences only**. They are not interpreted as neurobiological regional effects because reference/montage, peripheral artifact susceptibility, and other acquisition factors have not yet been excluded as explanations.

Peak centers are **not** assigned a channel-wise ICC at this stage because a first-listed peak is not guaranteed to preserve mode identity across sessions. A peak-matching/identity rule must be frozen before that question can be asked.

### Repeatability decision

The population result supports three separate treatment classes rather than one spectral-trait label:

1. **Aperiodic exponent:** potentially useful reference feature with material channel and subject heterogeneity; retain with uncertainty and Limit-Map context.
2. **Exact peak count:** descriptive/state-sensitive feature; current repeat agreement is insufficient to promote it as a stable person-level trait coordinate.
3. **Zero-peak state:** promising categorical reference feature because repeat agreement is high across many channels, but it remains acquisition/model dependent and requires external/reference transfer before any clinical use.

No repeatability cutoff was selected from these observed values.

## 7. Consequence for the future tool

The first reference-assessment tool should not report one spectral number as “brain stability.”

Instead this population result supports a report architecture that can distinguish:

- highly repeatable descriptive structure;
- quantities that are state/configuration/model sensitive;
- categorical absence;
- model-family disagreement;
- channel/region outliers;
- explicit uncertainty and refusal.

That is exactly the behavior needed before a downstream diagnostic model is allowed to consume these features.

## 8. Interpretation ceiling

This result is a label-blind T0 measurement/reliability result only.

Still prohibited:

- diagnostic classification;
- prognosis;
- healthy versus pathological cutoffs;
- descriptive bandwidth-to-damping conversion;
- descriptive peak-to-mode conversion;
- local modal damping ratios from this layer;
- whole-brain chi;
- claims that repeat similarity by itself proves stable biological trait identity.
