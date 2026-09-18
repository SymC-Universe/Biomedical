# NSD P0-Q Qualification Search Ledger v0.1

Date opened: 18 September 2026
Status: ACTIVE
Program authority: SymC General Operations Manual v0.8.0
Scope: substantial iterative qualification work for the label-blind NSD Structural Engine

## Purpose

This ledger satisfies the GOM v0.8.0 requirement that substantial P0-Q iteration preserve the visible search history rather than allowing successful internal qualification to appear as if it came from a single untouched test.

This is not an MFR-14 confirmatory record. All evidence listed here is qualification evidence unless separately frozen and promoted on untouched evidence.

## Global rules

- Clinical or disorder labels do not enter basic Engine structure qualification.
- Previously observed qualification failures may be reused to improve a candidate, but the reused evidence remains qualification evidence.
- A failed qualification test may motivate a new version without erasing the failure.
- No qualification result is allowed to retroactively become untouched confirmation.
- Candidate complexity increases are recorded explicitly.
- The stopping condition is scientific adequacy or scientifically correct refusal, not production of a desired chi value.
- Real-EEG modal damping and local chi remain disabled until the modal route completes the frozen adequacy program.

## Q-SPEC-001 - Descriptive periodic/aperiodic parameterization

Purpose tag: QUALIFICATION

Candidate family:
- Welch PSD as the preserved descriptive spectral base.
- specparam==2.0.0rc7 as an isolated descriptive periodic/aperiodic candidate.

Qualification evidence reused:
- deterministic known-truth spectra;
- fixed-background and knee-background truths;
- no-peak, single-peak, separated two-peak, weak/noisy peak, overlapping-peak, broad-bump, and resolution cases;
- previously observed model-family misspecification;
- label-blind healthy repeat data only after the candidate operating region was frozen.

Material versions / decisions evaluated:

1. Wide 1-45 Hz fixed aperiodic model.
   - Failure targeted: background curvature interpreted as periodic structure.
   - Result: rejected. High global fit quality could coexist with invented peaks.

2. Permissive peak settings.
   - Families included peak_threshold 2.0/2.5/3.0, min_peak_height 0.05/0.10/0.15/0.20, max_n_peaks 3/4.
   - Failure targeted: weak/noisy false positives, peak splitting, boundary saturation.
   - Result: only min_peak_height=0.20 survived the first fixed-background screen; this did not solve knee misspecification.

3. Dual fixed/knee consensus rule.
   - Complexity added: second model family plus agreement gate.
   - Result: rejected because the frozen qualification criteria yielded passing_count=0; criteria were not relaxed after failure.

4. Frequency-range calibration.
   - Candidate ranges: 1-45, 2-40, 3-35, 3-30, 5-35 Hz.
   - Result: only 5-35 Hz passed the frozen candidate-region criteria across fixed and knee truth.

5. Conservative tie-break among materially equivalent passing configurations.
   - Selected: fixed mode, 5-35 Hz, min_peak_height=0.20, peak_threshold=3.0, max_n_peaks=3, peak_width_limits=0.5-12 Hz.
   - Selection rule: prefer the simpler/more conservative configuration when known-truth performance is materially equivalent.
   - Healthy/clinical parameterized spectra were not used to choose the configuration.

Current real-data qualification use:
- label-blind ds003775 repeat-session healthy data;
- 42 independent repeat subjects / 84 recordings;
- descriptive output only.

Observed real-data Limit-Map findings preserved:
- substantial fixed-vs-knee model-family disagreement;
- exact peak count has limited repeat agreement;
- aperiodic exponent has material subject-level outliers;
- zero-peak state can be highly repeat-consistent;
- global Welch shape similarity does not erase channel-level failures.

Current status:
DESCRIPTIVE_SPECTRAL_PARAMETERIZATION = P0-Q RETAINED WITH LIMITS

Current claim ceiling:
- descriptive periodic/aperiodic Atlas and Function/Limit Map input;
- not a trait biomarker;
- no peak-to-mode conversion;
- no bandwidth-to-damping conversion;
- no chi license.

Stopping rationale:
The candidate region is frozen for the current T0 healthy qualification task. Further changes require a new version and a new P0-Q record rather than post-result retuning of the current candidate.

Canonical records:
- SPECTRAL_PARAMETERIZATION_QUALIFICATION_PLAN_v0.1.md
- SPECTRAL_PARAMETERIZATION_OPERATING_REGION_v0.1.md
- DS003775_REPEAT_POPULATION_T0_RESULT_v0.1.md

## Q-MODAL-001 - Direct output-only AR(2)

Purpose tag: QUALIFICATION

Candidate:
M1_AR2_DIRECT

Qualification evidence:
- known-truth damped oscillator grid;
- frequency: 5, 10, 20 Hz;
- damping ratio: 0.10 through 0.95;
- duration: 10, 30, 120 s;
- deterministic seeds;
- additive observation-noise challenges.

Failure explicitly targeted:
Can direct AR(2) pole recovery remain identifiable when the observed signal contains additive measurement noise?

Result:
- clean known truth recovered well over most of the grid;
- modest observation noise caused severe bias and/or refusal;
- higher observation-noise strata produced zero admitted estimates under the current gate.

Complexity decision:
No attempt was made to loosen the gate to force real-data estimates.

Status:
M1_AR2_DIRECT = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED

Stopping rationale:
The candidate is retained as a known-truth comparator and failure demonstration. It is not being iterated toward real-EEG admission because the failure is structural to the output-only/no-observation-model route.

Canonical record:
- MODAL_ESTIMATOR_QUALIFICATION_v0.1.md

## Q-MODAL-002 - Latent oscillator covariance route

Purpose tag: QUALIFICATION

Candidate:
M2_LATENT_COVARIANCE

Reason for version:
M1 failed under observation noise, motivating an explicit latent-state/observation-noise separation.

Complexity added:
- two-dimensional latent damped rotation;
- explicit white observation-noise contribution through the zero-lag variance fraction;
- nonlinear covariance fitting.

Qualification evidence reused:
- the M1 observation-noise failure region;
- known-truth frequency/damping/duration grid;
- additive observation-noise ratios;
- deterministic seeds.

First result:
The route recovered single-oscillator truth under additive white observation noise substantially better than direct AR(2).

Observed difficult region:
Short, low-frequency, highly damped signals retained materially larger damping/frequency error despite mechanical admission.

Status after first map:
PROMISING_KNOWN_TRUTH_ROUTE / REAL_EEG_NOT_YET_ADMITTED

Stopping rationale after first map:
Do not apply to real EEG until misspecified alternatives and an error-aware operating region are mapped.

Canonical record:
- MODAL_ESTIMATOR_QUALIFICATION_v0.1.md

## Q-MODAL-003 - M2 adversarial model-adequacy challenge

Purpose tag: QUALIFICATION

Candidate under challenge:
The Q-MODAL-002 single-oscillator covariance route.

Previously observed failure explicitly targeted:
Mechanical convergence/admission might not distinguish a true single stationary oscillator from plausible non-single-oscillator generators.

Adversarial generators:
- valid single oscillator;
- two close oscillatory modes;
- two separated oscillatory modes;
- colored observation noise;
- mid-record frequency shift;
- finite bursts;
- nonoscillatory AR(1);
- white noise.

Result:
All tested generator families were mechanically admitted. A close two-mode generator achieved covariance fit quality at least as strong as the valid single-mode truth.

Scientific consequence:
M2_MECHANICAL_ADMISSION != M2_SCIENTIFIC_MODEL_ADEQUACY

Status:
M2_LATENT_COVARIANCE = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED

The failure is preserved and is not repaired by a post-hoc R-squared threshold.

Canonical record:
- M2_MODEL_ADEQUACY_PLAN_v0.1.md

## Q-MODAL-004 - Interim adequacy diagnostics

Purpose tag: QUALIFICATION

Implementation:
engine/tools/probe_latent_oscillator_adversaries.py

Reason for this iteration:
Probe whether alternative-model competition and within-record stability contain enough information to design the proper adequacy route without yet changing production admission.

Complexity added for diagnosis only:
- nonoscillatory AR(1)-like covariance alternative;
- two-oscillator covariance alternative;
- split-half frequency and damping stability;
- explicitly labeled pseudo-BIC diagnostics.

Important limitation:
Autocorrelation lags are correlated. The pseudo-BIC values are qualification diagnostics, not formal likelihood-based BIC and are not eligible to become a production admission threshold merely because they separate selected cases.

Observed diagnostic behavior:
- valid single oscillator strongly preferred the single oscillator over AR(1) in the pseudo-BIC comparison;
- nonoscillatory AR(1) strongly preferred the AR(1) alternative;
- the two-oscillator diagnostic improved fit for the two-mode adversaries, but also improved the diagnostic criterion for the valid single-oscillator truth;
- the mid-record frequency-shift adversary showed large split-half frequency disagreement;
- finite bursts and colored-noise cases were not cleanly solved by split-half frequency stability alone;
- white noise remained an obvious poor-fit case but cannot define the general adequacy rule.

Decision:
No production threshold is frozen from Q-MODAL-004.

Next exact action:
Implement the frozen A0/A1/A2 model-adequacy program using a proper state-space innovations/Kalman likelihood or another statistically justified equivalent, plus residual/innovation, stationarity, identifiability, held-out, and operating-region qualification.

Final P0-Q stopping condition for the modal route:
A frozen modal candidate may face untouched/label-blind real-data adequacy only after:
1. known-truth recovery is acceptable in its declared operating region;
2. nonoscillatory alternatives are correctly refused or preferred where appropriate;
3. multimode/model-order alternatives are distinguished at a prespecified error rate;
4. nonstationary/bursty/colored-noise failure regions are mapped and refusal behavior is explicit;
5. uncertainty/identifiability is quantified;
6. the production admission/refusal rules are frozen before the next untouched gate.

Until then:
- no M2-derived real-EEG modal damping ratio;
- no M2-derived local chi;
- no biological interpretation of an M2 fitted mode;
- no clinical feature selection from M2 outputs.

## P0-Q search-family accounting

Current major Engine qualification families represented in this ledger:

- descriptive spectral parameterization: 1 primary candidate family with multiple prespecified operating-region/calibration families;
- direct AR(2) modal route: 1 candidate, retained only as baseline;
- latent covariance modal route: 1 candidate with successive known-truth and adversarial qualification passes;
- adequacy wrapper/model-order program: active, not yet frozen.

This ledger is updated when a material candidate version, estimator family, qualification dataset, targeted failure, complexity increase, or stopping rationale changes.

## Promotion firewall

Nothing in this ledger is P1 evidence by itself.

Any future P1 claim must:
- freeze its exact claim and decision rule;
- satisfy the full MFR-14 floor;
- use genuinely untouched decisive evidence;
- preserve the qualification search history;
- compare against the strongest relevant native/simple toolkit;
- and accept failure without retuning the frozen claim on the decisive evidence.
