# NSD state-space sampling/process-noise extension freeze v0.1

Date: 22 September 2026  
Status: FROZEN BEFORE RESULT  
Program authority: SymC General Operations Manual v0.8.3  
Maturity: P0-Q qualification only

## Purpose

Close two remaining pre-real-EEG adequacy gaps that were already named in the frozen modal qualification plan:

1. sampling-rate dependence of A0/A1/A2 recovery;
2. sensitivity to process-noise structure beyond the current isotropic white-drive truth.

This extension does not change the A0/A1/A2 scientific models or admission rules.

## Part A: sampling-rate extension

The existing 256 Hz map remains the reference. New rows use the same continuous-time latent oscillator construction at:

- 128 Hz;
- 512 Hz.

Frozen truth grid:
- natural frequency: 5, 10, 20 Hz;
- damping ratio: 0.20, 0.50, 0.80;
- duration: 30 s;
- observation-noise SD / latent SD: 0.50;
- seeds: 0, 1, 2.

A0/A1/A2 use the same physical frequency band, 1-45 Hz, at every sampling rate. This keeps the scientific target fixed while changing discrete sampling density.

Required outputs:
- BIC winner/margin;
- A1 natural-frequency relative error;
- A1 damping absolute error;
- innovation autocorrelation;
- latent fraction;
- full fit diagnostics.

No result from 128 or 512 Hz may be treated as a replacement for the prior 256 Hz map. The question is sampling robustness/limit behavior.

## Part B: process-noise misspecification challenge

All process-noise scenarios share:
- natural frequency 10 Hz;
- damping ratio 0.30;
- 256 Hz sampling;
- 30 s duration;
- observation-noise SD / latent SD 0.50;
- seeds 0, 1, 2.

The latent transition matrix is the same damped rotation in every scenario. Only the driving process changes.

Frozen process families:

1. `isotropic_white`
   - current matched-model baseline;
   - independent equal-variance white innovations on both latent quadratures.

2. `anisotropic_white_4_to_1`
   - white innovations;
   - first-quadrature innovation SD is four times the second before stationary rescaling.

3. `rank1_white_axis_drive`
   - white innovations drive only the first latent quadrature.

4. `colored_process_phi_0_7`
   - each latent innovation channel follows an independent AR(1) process with phi=0.7 before entering the latent state equation.

For the misspecified process families, no claim is made that the resulting process has the exact stationary covariance assumed by the NSD fitting model. That mismatch is the point of the challenge.

Each generated latent trace is burned in for 5 s. Observation noise is added after burn-in at 0.50 times the realized latent standard deviation.

## Frozen model/search settings

Unchanged:
- A0 nonoscillatory latent relaxation;
- A1 one latent damped oscillator;
- A2 two latent damped oscillators;
- steady-state Kalman innovations likelihood;
- BIC;
- hardened deterministic multistart search;
- fmin=1 Hz;
- fmax=45 Hz;
- optimizer_maxiter=80.

## Interpretation firewall

This run may map:
- sampling-density robustness;
- process-noise-model sensitivity;
- candidate refusal needs.

It may not:
- retune A0/A1/A2 on viewed rows;
- define a production threshold from the same rows;
- convert process-noise misspecification into a biological interpretation;
- license real-EEG modal damping/local chi;
- define a universal neural stability boundary.

If a specific misspecification is not distinguishable by the current candidate set, the correct result is an unresolved Limit-Map region, not a forced model label.
