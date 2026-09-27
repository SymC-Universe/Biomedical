# NSD Continuous-Lineage Finite-Realization Probe Postresult v0.1

Status: EXPLORATORY KNOWN-TRUTH RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD State-Space Lineage Sampling Contracts`  
Run: `36354816856`  
Conclusion: SUCCESS  
Source head: `f452c97396669c55648d17826b8f9e4705370985`

Artifact: `nsd-continuous-lineage-nonzero-g-probe`  
Artifact ID: `10943760557`  
Digest: `sha256:fbd34354bc034eccc88a585b9317660a51db5c968b3de7e24b55dadf83ec22ad`  
Expiry: 26 December 2026

The same workflow also passed the lineage/sampling, substrate-closure, continuous-lineage truth, and predictive-closure analytic contract suite before running this probe.

## Frozen exploratory setup

Each truth contains one continuous-time underdamped oscillator:

- natural frequency = 10 Hz;
- truth chi = zeta = 0.30;
- A = 0.8;
- fine sampling = 256 Hz;
- deterministic paired decimation to 128 Hz;
- 30 s realization;
- g = -0.75, 0, +0.75;
- seeds = 0, 1;
- unchanged production A0/A1/A2 comparison.

The fine and coarse records within each cell come from the same realized path.

## Results

For g = -0.75, A2 was selected in all four comparisons:

- seed 0 fine: A2, BIC margin 25.106572;
- seed 0 coarse: A2, BIC margin 5.670896;
- seed 1 fine: A2, BIC margin 17.398391;
- seed 1 coarse: A2, BIC margin 9.185251.

This is a false multimodal selection because the truth contains one physical continuous-time mode.

For g = 0, A1 was selected in all four comparisons:

- seed 0 fine: A1, margin 23.188680;
- seed 0 coarse: A1, margin 22.205846;
- seed 1 fine: A1, margin 26.704757;
- seed 1 coarse: A1, margin 20.061441.

For g = +0.75, finite-realization behavior was mixed:

- seed 0 fine: A1, margin 1.761072;
- seed 0 coarse: A1, margin 12.202888;
- seed 1 fine: A2, margin 22.232023;
- seed 1 coarse: A1, margin 0.083656.

The positive-g coarse seed-1 result is effectively near-tied by descriptive BIC margin, but no tie/admission threshold is introduced here.

Current A1 also showed sampling- and realization-dependent chi distortion despite invariant truth chi = 0.30. Examples include:

- g=-0.75 seed 0: fine A1 chi 0.297745, coarse 0.259104;
- g=-0.75 seed 1: fine 0.310241, coarse 0.268725;
- g=+0.75 seed 0: fine 0.264933, coarse 0.304754;
- g=+0.75 seed 1: fine 0.313183, coarse 0.359819.

## Interpretation

The finite-realization probe confirms the analytic spectral result: current A1 can create false A2 model-order pressure inside the intended one-mode continuous-lineage C family when g/H is nonzero.

The result is asymmetric and sample-sensitive at this small exploratory seed count, so it does not define a population error rate or a new threshold. The negative-g cells provide an especially clear constructive failure: one true physical mode is repeatedly represented as two A2 modes at both sampling rates.

Therefore A2 preference cannot be used as evidence of multimodality until a one-mode C-family nuisance-capable candidate has been qualified against these truths.

## Claim boundary

This result supports qualification of the separate one-mode C1Q candidate. It does not:

- promote C1Q into production;
- change A0/A1/A2;
- license real-EEG local chi;
- establish a numerical admission threshold;
- prove that every A2 win is nuisance-driven;
- alter N-B2/N-B3 or completed GRI/BioSystems work.
