# Research Structure Report Example — ds003775 sub-069 / ses-t1

Status: **RESEARCH_STRUCTURE_ONLY**  
Clinical use: **DISABLED**  
Diagnostic model: **NONE**  
Prognostic model: **NONE**  
Atlas context: `ds003775-repeat-p0d-v0.1` (exploratory, non-independent for Engine validation)

## 1. Data identity

- Dataset: OpenNeuro `ds003775`
- Pinned release: OpenNeuro v1.2.1 / NEMAR `on003775 v1.0.0`
- Subject/session: `sub-069 / ses-t1`
- Task: resting eyes closed
- Acquisition: 17 October 2017, 10:33:20
- EEG channels: 64
- Sampling rate: 1024 Hz
- Duration: 240 s
- Exact payload MD5: `656b7184b5ed01e36601b79a3bf38c52`
- D4 payload identity/readability: **PASS**

Signal-quality status remains **PARTIALLY_USABLE** rather than fully usable because the population workflow did not run the complete artifact/QC stack required for a clinical-quality admission decision.

## 2. Descriptive spectral state

Frozen descriptive parameterization:

- fixed aperiodic model;
- 5–35 Hz;
- peak-width limits 0.5–12 Hz;
- minimum peak height 0.20 log10;
- peak threshold 3 SD;
- maximum 3 peaks.

Across 64 channels in this session:

- median aperiodic exponent: **1.5534**;
- exponent range: **0.6588–1.9180**;
- mean descriptive peak count: **1.3594**;
- zero-peak channel fraction: **0.0000**;
- median first-listed peak center: **10.2240 Hz**;
- first-listed peak-center range: **8.9692–10.4722 Hz**;
- median first-listed descriptive bandwidth: **2.2799 Hz**.

The bandwidth is descriptive. It is **not** converted to damping.

## 3. Limit / open-channel state

This session also contains reasons not to overcompress the result:

- fixed-vs-knee aperiodic-model disagreement: **34 / 64 channels (53.125%)**;
- channels reaching the maximum allowed peak count: **7 / 64**;
- total descriptive width-boundary hits: **3**.

The current Atlas-P0-D repeat reference provides context that, across 64 channels:

- median aperiodic-exponent ICC(A,1): **0.65882**;
- median exact peak-count agreement: **0.53571**;
- median exact zero-peak-state agreement: **0.90476**.

These are reliability/Limit-Map quantities, not health thresholds.

## 4. Modal / dynamical state

**No modal damping ratio is reported.**

The current real-EEG modal route remains disabled because known-truth adversarial testing showed that a single-oscillator fit can mechanically admit multi-mode, nonstationary, colored-noise, burst, and nonoscillatory alternatives.

Therefore this report contains:

- no admitted local modal damping ratio;
- no local chi;
- no whole-system chi;
- no project-branded system scalar.

## 5. Atlas comparison status

An individual abnormality score is **not available**.

The current `ATLAS_P0_D` artifact is a first exploratory repeatability/reference serialization from the same source cohort used during T0 qualification. Its evidence-path grade is:

`NON_INDEPENDENT_FOR_ENGINE_VALIDATION`

It is useful for Function/Limit discovery and tool/report development but does not yet license a clinical percentile, reference deviation, or healthy/pathological cutoff.

## 6. Clinical modules

| Module | Status |
| --- | --- |
| Screening | DISABLED |
| Differential diagnosis | DISABLED |
| Longitudinal clinical monitoring | DISABLED |
| Prognosis / forecasting | DISABLED |

No placeholder probability is emitted for a disabled module.

## 7. What this report demonstrates

This is the first end-to-end human-readable rendering of a **real pinned EEG recording** through the current qualified descriptive layer into the future tool's reporting architecture.

It demonstrates the intended product behavior:

1. establish data identity;
2. report only measurements that are currently licensed;
3. preserve channel/model limitations;
4. attach reference context without manufacturing an abnormality score;
5. refuse unqualified modal/scalar interpretation;
6. keep diagnosis and prognosis visibly disabled until they are earned.

Machine-readable companion:

`sub-069_ses-t1_research_structure_report_v0.1.json`
