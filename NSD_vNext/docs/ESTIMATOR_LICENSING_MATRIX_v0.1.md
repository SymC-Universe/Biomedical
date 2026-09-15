# NSD Estimator Licensing Matrix v0.1

Date: 14 September 2026
Status: ACTIVE METHOD CONTROL
Purpose: prevent a measured feature, fitted parameter, proxy, or visualization from silently becoming a dynamical `chi`.

## 1. Admission classes

Every candidate quantity entering the NSD architecture must be assigned one of four classes before clinical analysis:

1. **DYNAMICALLY_DERIVED** — follows from an explicit dynamical model with stated equations, parameter identifiability, fitting assumptions, uncertainty, and validation.
2. **VALIDATED_OPERATIONAL_ESTIMATOR** — not a direct model parameter, but independently validated against a target dynamical quantity across the intended measurement regime.
3. **CHI_LIKE_PROXY** — monotone or conceptually related to stability but not licensed as the dynamical damping ratio.
4. **EMPIRICAL_COORDINATE** — useful measured feature with no claim that it is chi.

Refusal is a valid output.

## 2. Current licensing matrix

| Observable / estimator | Native meaning | May enter architecture? | May be called dynamical chi? | Current decision |
| --- | --- | --- | --- | --- |
| Aperiodic exponent | Broadband spectral slope/exponent after periodic-background parameterization | Yes | No, not by itself | `EMPIRICAL_COORDINATE` |
| Aperiodic offset | Broadband spectral offset | Yes | No | `EMPIRICAL_COORDINATE` |
| Periodic center frequency | Frequency of fitted spectral peak | Yes | Not automatically; center frequency is not automatically undamped natural frequency | `EMPIRICAL_COORDINATE` unless model supplies conversion |
| Periodic peak power | Peak amplitude/power relative to background | Yes | No | `EMPIRICAL_COORDINATE` |
| Gaussian peak bandwidth from SpecParam/FOOOF | Width parameter of a Gaussian peak model | Yes | No; Gaussian width is not a mechanical decay constant | `EMPIRICAL_COORDINATE` |
| Generic half-power bandwidth | Spectral sharpness | Yes | Only under a licensed resonant model with competing broadening bounded | `CONDITIONAL` |
| Quality factor `Q = f0 / BW` | Spectral/resonant sharpness under stated convention | Yes | Only if the underlying resonance model establishes the second-order relation | `CONDITIONAL`; do not use as independent feature beside chi from same mode |
| Damped-harmonic-oscillator parameters estimated directly from time series | Natural frequency, damping/decay, noise terms under a second-order stochastic model | Yes | Potentially yes | `CANDIDATE_DYNAMICALLY_DERIVED`; requires fit qualification and known-truth recovery |
| Neural-mass / state-space complex poles | Local linearized modal decay/growth and oscillation frequency | Yes | Potentially, for a defined mode after mapping convention is stated | `CANDIDATE_DYNAMICALLY_DERIVED` |
| Dynamic Mode Decomposition complex eigenvalues / modes | Data-driven spatiotemporal mode frequency, growth/decay, spatial participation under DMD assumptions | Yes | Potentially only after estimator/model qualification and continuous-time conversion are explicit | `NATIVE_MODAL_CANDIDATE / COMPARATOR` |
| Output-Only Modal Analysis modes | Output-only system-identification modal frequency/decay/damping structure under OMA assumptions | Yes | Potentially, if estimator recovery and physiological scope are qualified | `NATIVE_MODAL_CANDIDATE / COMPARATOR` |
| Autocorrelation decay time | Temporal persistence | Yes | Not by itself | `EMPIRICAL_COORDINATE`; may constrain a dynamical model |
| Oscillation burst duration | Temporal persistence/burst phenotype | Yes | No direct conversion by default | `EMPIRICAL_COORDINATE` |
| Regional spectral differences | Spatial heterogeneity | Yes | No | `CONGLOMERATE/SYSTEM FEATURE` |
| Channel participation / mode shapes | Spatial/modal organization | Yes | No scalar reduction by default | `VECTOR_MODAL FEATURE` |
| Functional connectivity | Statistical interdependence under chosen estimator | Yes | No | `CONGLOMERATE/SYSTEM FEATURE` |
| HRV RMSSD, LF/HF, pNN50 | Autonomic variability summaries | Yes where scientifically relevant | No | `EMPIRICAL_COORDINATE`; historical HRV-to-chi equation retired |
| fMRI BOLD amplitude / variance | Hemodynamic signal property | Yes where justified | No direct dynamical chi | `EMPIRICAL_COORDINATE` |
| Behavioral reaction-time variance | Behavioral variability | Yes | No | `EMPIRICAL_COORDINATE` |
| Whole-head average of a local feature | Global descriptive summary | Yes as comparator | No whole-brain chi without derivation | `DESCRIPTIVE_COMPARATOR` |
| Absence of a detectable peak | Categorical feature state | Yes | No numeric imputation required | `CATEGORICAL_PHENOTYPE` |
| Rejected / poor-fit mode | Model failure or insufficient information | Yes, in open channel | No | `REFUSAL / OPEN_CHANNEL` |

## 3. Aperiodic exponent firewall

The historical NSD source treated the EEG aperiodic exponent as a direct chi proxy and mapped flatter/steeper slopes onto low/high damping states. The forward project does not permit that equivalence.

Reasons:
- the exponent can be associated with excitation/inhibition changes in some settings, but current evidence does not support a universal one-to-one mapping;
- pharmacological manipulations can move the exponent in directions inconsistent with a simple E/I ratio interpretation;
- age, state, frequency range, model form, artifact structure, and fitting choices alter the estimate;
- there is no universal exponent cutoff that defines excitatory, inhibitory, healthy, underdamped, or overdamped neural states.

Therefore:

`aperiodic exponent != E/I ratio != gamma != dynamical chi`

unless a specific experiment/model separately validates the chain.

## 4. Periodic-width firewall

A spectral peak can broaden because of several distinct mechanisms:
- true lifetime/decay broadening;
- frequency nonstationarity across time;
- frequency heterogeneity across sources;
- burst-duration variability;
- source mixing/volume conduction;
- finite-window spectral leakage;
- noise and low signal-to-background ratio;
- model misspecification;
- multiple unresolved neighboring modes.

A width-to-damping conversion is therefore licensed only after the relevant alternatives are bounded or explicitly modeled.

### Gaussian versus Lorentzian

SpecParam commonly uses Gaussian periodic peaks. A Gaussian width parameter is a descriptive spectral width and is not the linewidth of a damped second-order resonance by default.

For a damped resonance, Lorentzian-like relationships may arise under specific assumptions. Even then, the neural system must be shown to satisfy the model sufficiently for the parameter to be interpreted dynamically.

## 5. Frequency-identity firewall

The initial NSD known-truth convention is:

`x'' + 2 zeta omega_0 x' + omega_0^2 x = u(t)`.

Even in this simplest licensed second-order case, three frequency quantities differ:

- undamped natural frequency: `f_0 = omega_0/(2 pi)`;
- damped free-oscillation frequency: `f_d = f_0 sqrt(1-zeta^2)`;
- forced displacement-resonance frequency, when present: `f_r = f_0 sqrt(1-2 zeta^2)`.

Therefore:

`measured peak center != f_0 by default`

and

`measured peak center != f_d by default`.

A further important edge case is that a system can remain underdamped in the pole sense, `zeta < 1`, while having no displacement-resonance maximum when `1/sqrt(2) <= zeta < 1`.

Consequences for neural analysis:
- no detected resonance peak does not prove an overdamped pole structure;
- a peak center cannot be substituted for the natural frequency without specifying the generator and observation model;
- scalar admission cannot depend on a simplistic peak/no-peak or narrow/broad rule.

The exact frozen fixture is documented in `DHO_CONVENTION_NOTE_v0.1.md` and implemented in the Engine known-truth module.

## 6. Evidence that dynamical oscillator models are plausible in restricted neural settings

The forward project should not conclude that oscillator-based neural damping is merely metaphorical. There is genuine literature showing model-specific cases where damped-oscillator dynamics fit neural signals:

- Hindriks et al. (2011), *Dynamics underlying spontaneous human alpha oscillations: A data-driven approach*, NeuroImage, DOI `10.1016/j.neuroimage.2011.04.043`: spontaneous human MEG alpha was modeled as a noise-perturbed damped harmonic oscillator, with parameters estimated from data.
- Spyropoulos et al. (2022), *Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise*, Nature Communications, DOI `10.1038/s41467-022-29674-x`: macaque V1 gamma dynamics and spectra were reproduced by a noise-driven damped harmonic oscillator equivalent to a linear E-I circuit.
- Moran et al. (2007), *A neural mass model of spectral responses in electrophysiology*, NeuroImage, DOI `10.1016/j.neuroimage.2007.05.032`: neural-mass transfer functions use complex poles whose real and imaginary components encode decay/growth and oscillatory frequency around a fixed point.
- Brunton et al. (2016), *Extracting spatial-temporal coherent patterns in large-scale neural recordings using dynamic mode decomposition*, Journal of Neuroscience Methods, DOI `10.1016/j.jneumeth.2015.10.010`: DMD recovers coupled spatiotemporal neural modes and is a mature native comparator/candidate implementation rather than an NSD invention.
- Published Output-Only Modal Analysis/DMD comparisons in EEG establish another native system-identification route to modal structure.

These sources support **model-conditional routes** to neural modal and damping-related parameters. They do not license converting every scalp EEG peak or aperiodic slope into chi.

## 7. Required qualification for a mode-specific chi

A mode-specific dynamical chi may be admitted only when all applicable checks pass:

1. a stated second-order or equivalent modal generator is identified;
2. the fitted signal contains sufficient information to identify the mode;
3. the estimator recovers known truth in simulation across realistic SNR, duration, sampling, nonstationarity, and artifact conditions;
4. the fitted mode is not simply a Gaussian decomposition artifact;
5. center frequency is converted to the model’s natural-frequency quantity correctly;
6. decay/width parameter convention is explicit;
7. non-damping broadening is bounded or included in the model;
8. uncertainty is propagated into chi;
9. failure/absence produces refusal rather than fabricated values;
10. the same estimator is evaluated label-blind before clinical use;
11. estimator identifiability is demonstrated in the intended data regime;
12. an established native modal method such as state-space oscillator modeling, DMD, OMA, or another justified comparator is not silently reinvented under different notation.

## 8. Algebraic redundancy control

For a true second-order mode, quality factor and damping ratio can be algebraically linked under the chosen convention. If chi is derived from Q, or both are derived from the same center-frequency/linewidth pair, they are not independent predictors.

The feature pipeline must record dependency lineage so that derived duplicates cannot inflate apparent multivariate information.

## 9. Current preferred architecture

The default NSD feature path is:

`raw/preprocessed signal`

-> `native spectral/time-domain representation`

-> `periodic + aperiodic decomposition`

-> `candidate modal extraction using explicit named methods`

-> `model qualification, identifiability, and refusal checks`

-> `mode-specific dynamical quantities only where licensed`

-> `spatial/modal/conglomerate organization`

-> `clinical comparison only after structural qualification`

This preserves the useful part of the original NSD intuition while preventing visual or numerical convenience from determining the physics.