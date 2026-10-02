# NSD Predictive Closure Calibration Postresult v0.1

Status: EXPLORATORY KNOWN-TRUTH RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD State-Space Lineage Sampling Contracts`  
Run: `36354816856`  
Conclusion: SUCCESS  
Source head: `f452c97396669c55648d17826b8f9e4705370985`

Artifact: `nsd-predictive-closure-calibration-probe`  
Artifact ID: `10943920300`  
Digest: `sha256:5e4a29c6e8025cfc99dc6bf54561910e8682462337cce943cbd79ff7fc09ad60`  
Expiry: 26 December 2026

## Exploratory setup

Resolved local mode:

- natural angular frequency = 2*pi*10 rad/s;
- local chi = zeta = 0.30.

Hidden mode:

- natural angular frequency = 2*pi*18 rad/s;
- zeta = 0.40.

The exploratory horizon was 2.0 s with 401 evaluation samples. Coupling fractions were 0, 0.05, 0.10, and 0.20 relative to the resolved-mode omega^2 scale. These are exploratory map coordinates, not admission thresholds.

Four exact mechanism classes were evaluated separately: closed, P-to-Q leakage only, Q-to-P hidden-input only, and bidirectional return memory.

## Results

Closed controls retained numerical-zero resolved prediction error, hidden-state sensitivity, memory, pole displacement, and chi displacement.

P-to-Q leakage-only controls retained effectively exact resolved prediction despite nonzero leakage at every nonzero coupling cell. Resolved relative operator RMS error remained approximately 2e-13, memory remained zero, and chi displacement remained numerical zero.

Q-to-P hidden-input-only controls also retained exact P-only resolved propagation and zero endogenous memory, but hidden-state sensitivity increased with coupling:

- fraction 0.05: hidden-state operator RMS 0.170183197;
- fraction 0.10: 0.340366394;
- fraction 0.20: 0.680732788.

Bidirectional return-memory controls produced nonzero predictive error, memory, pole displacement, and chi displacement:

- fraction 0.05: prediction RMS 0.197626680, memory RMS 18.076754072, chi displacement 0.000370231;
- fraction 0.10: prediction RMS 0.808170105, memory RMS 72.307016290, chi displacement 0.001480745;
- fraction 0.20: prediction RMS 4.928003851, memory RMS 289.228065158, chi displacement 0.005920262.

## Interpretation

The result directly supports the approved predictive approximate-closure policy.

Raw P-to-Q leakage is not a valid universal refusal criterion because substantial one-way leakage can coexist with exact resolved local prediction and unchanged local chi when no return path exists.

Hidden-state sensitivity and endogenous return memory are also not interchangeable. One-way Q-to-P influence can create sensitivity to hidden initial state without shifting the autonomous resolved pole pair, whereas bidirectional coupling creates return memory that perturbs resolved prediction and the embedded modal coordinate.

Therefore the future N-B1 closure gate should be tied to the effect of unresolved dynamics on the claimed pole/chi lineage and held-out prediction, not to a raw coupling norm or a universal memory magnitude.

## Claim boundary

This exploratory map does not define the numerical predictive-closure tolerance. The horizon, prediction-error functional, hidden-state uncertainty model, pole/chi tolerance, and coverage policy remain prospective calibration choices that must be frozen before real EEG is opened.

N-B1 real-EEG local chi remains unlicensed. N-B2 and N-B3 remain separate.
