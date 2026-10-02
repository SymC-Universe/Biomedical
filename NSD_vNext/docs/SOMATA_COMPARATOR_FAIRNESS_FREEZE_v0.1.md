# NSD SOMATA comparator fairness freeze v0.1

Date: 22 September 2026  
Status: FROZEN BEFORE KNOWN-TRUTH COMPARATOR PERFORMANCE  
Program authority: SymC General Operations Manual v0.8.3  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

Freeze the information and preprocessing mapping for the first isolated standard-toolkit comparison between the NSD A0/A1/A2 qualification lane and SOMATA 0.5.6 before any SOMATA known-truth performance result is opened.

This is P0-Q qualification/comparator evidence. It does not analyze EEG and cannot license real-EEG damping, local chi, diagnosis, prognosis, or a biological mode.

## Comparator identity

- package: SOMATA
- version: 0.5.6
- class: `somata.oscillator_search.IterativeOscillatorModel`
- search: iOsc+
- maximum oscillator count: 2
- selected model: package-native knee selection through `get_knee_osc()`
- residual diagnostic: package-native `diagnose_residual_acf()`
- manual post-result model selection: forbidden

The first lane uses package defaults unless explicitly frozen below.

## Shared information budget

The source generator realization is created once from the existing NSD P0-Q adequacy generator at 256 Hz using the same scenario and seed already defined in `probe_state_space_model_adequacy.py`.

That realization is then transformed once into a **shared comparator signal**. Both NSD and SOMATA receive the exact same array.

Neither tool receives a higher-resolution or differently filtered realization.

## Shared sampling-rate mapping

The shared comparator sampling rate is frozen at **120 Hz**.

Reason:
1. SOMATA documentation recommends downsampling to 120 Hz or less for oscillator search.
2. 120 Hz is the highest documented recommended rate and therefore avoids deliberately handicapping the standard toolkit.
3. The existing NSD adversarial truth content is below 20 Hz, so the comparator lane retains a wide guard band below the 60 Hz Nyquist frequency.
4. NSD is run on the same 120 Hz signal in this comparison, so no information-rate advantage is given to NSD.

The exact transformation is deterministic polyphase resampling from 256 Hz to 120 Hz using `scipy.signal.resample_poly(up=15, down=32)`.

This comparator lane does **not** replace the existing 256 Hz NSD qualification results. It is a matched-information comparison task.

## Shared normalization

After resampling, the signal is:
1. demeaned;
2. divided by its population standard deviation.

The resulting standardized array is passed unchanged to both tools.

NSD also performs its own shared nuisance standardization internally; passing an already standardized signal therefore does not add information or alter the relative information budget.

No scenario-specific filtering, denoising, window shortening, or manual frequency initialization is allowed.

## Frequency scope

For NSD:
- `fmin_hz = 1`
- `fmax_hz = 45`

For SOMATA:
- `noise_start_hz = 40`, which is the package default implied by 120 Hz sampling (`Nyquist - 20 Hz`);
- `freq_res_hz = 1`;
- `osc_range = 2`.

SOMATA's internal oscillator search is not forced to use the NSD 1-45 Hz model bounds because doing so would alter the native comparator algorithm. Native differences are retained and reported.

## Search settings

SOMATA:
- `reiterate = False`
- `sigma2_method = eig`
- `freq_hp = 0`
- `R_hp = 0.1`
- `Q_hp = None`
- `R_sigma2 = constant`
- `Q_sigma2 = MLE`
- `no_priors = False`
- 50 EM iterations per package implementation
- no interactive judgement
- no per-scenario tuning

NSD:
- existing A0/A1/A2 equations unchanged;
- optimizer search unchanged;
- `optimizer_maxiter = 80`;
- BIC winner retained only as the NSD within-family diagnostic;
- no new admission/refusal threshold.

## Semantic comparability rule

The tools do not expose identical model families.

NSD includes:
- A0 nonoscillatory latent relaxation;
- A1 one oscillator;
- A2 two oscillators.

The iOsc comparator starts with at least one oscillator. Therefore:
- single- and two-oscillator model-order behavior is directly comparable at the level of oscillator count and modal parameter recovery;
- a zero-oscillator/nonoscillatory refusal decision is **not directly comparable** in this iOsc lane;
- nonoscillatory AR(1) and white-noise scenarios are still run, but SOMATA results are reported as behavior under an oscillator-only search plus residual diagnostics, not as a fair zero-vs-one oscillator model-selection test.

No artificial equivalence is created by relabeling a low-frequency oscillator as A0.

## Modal parameter mapping

For a SOMATA component with discrete damping radius `a`, reported damped frequency `f_d`, and sampling rate `F_s`:

`decay_rate = -ln(a) * F_s`

`omega_d = 2*pi*f_d`

`omega_n = sqrt(decay_rate^2 + omega_d^2)`

`damping_ratio = decay_rate / omega_n`

`natural_frequency_hz = omega_n / (2*pi)`

This is the same discrete-pole-to-continuous second-order mapping used by the NSD qualification code. It is a reporting transform only; it does not change SOMATA fitting or model selection.

## Frozen first-pass scenarios

Exactly the existing eight adequacy generators and seeds 0, 1, 2:

- single_valid_truth
- two_modes_close
- two_modes_separated
- colored_observation_noise
- frequency_shift_mid_record
- finite_bursts
- nonoscillatory_ar1
- white_noise

No scenario may be added or removed after the first comparator result is viewed without creating a new comparator version.

## Output ceiling

The first result reports:
- NSD A0/A1/A2 BIC winner on the matched signal;
- SOMATA selected oscillator count;
- SOMATA selected frequencies/damping radii and mapped modal values;
- package-native residual diagnostics;
- valid-single and two-mode parameter errors where truth mapping is unambiguous;
- environment/package identities;
- explicit NOT_COMPARABLE flags where model families differ.

It does **not** produce:
- an overall winner;
- an ADDS/EQUIVALENT/SUBTRACTS verdict;
- a production admission threshold;
- a frozen biological operating region;
- real-EEG modal values;
- chi.

## Post-result rule

After the first run:
1. preserve all results, including failures;
2. do not manually retune either tool on a scenario;
3. classify structural non-comparabilities explicitly;
4. use the result to decide whether a second comparator lane is necessary, such as SOMATA dOsc, AutoReg/nonoscillatory competition, or switching-state-space methods;
5. any such lane becomes a new prospectively frozen comparator version.
