# NSD Continuous-Lineage Spectral Adequacy Postresult v0.1

Status: PREDECISION ANALYTIC RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD Continuous-Lineage Spectral Adequacy`  
Run: `36354717604`  
Conclusion: SUCCESS  
Artifact: `nsd-continuous-lineage-spectral-kl`  
Artifact ID: `10943149187`  
Artifact digest: `sha256:b918ab342b3884681b0ad0cb2633582127eb4aa4a773504d042b5b6ded1a9246`  
Artifact expiry: 26 December 2026

Source head for the successful result: `1508ff7389fc144c69c7785249b2db9915842b52`.

## Frozen analytic setup

The probe used one exact underdamped continuous-lineage C truth with:

- sampling rate: 256 Hz;
- standardized latent fraction A = 0.8;
- natural frequency = 10 Hz;
- truth chi = zeta = 0.30;
- effective likelihood sample count = 7552;
- current optimizer-reachable A1/A2 parameter box;
- g cells = -0.75, 0, +0.75.

The truth is one physical continuous-time oscillator in every cell. Only the licensed C-family covariance-phase/nuisance coordinate g changes.

## Results

For g = 0, current A1 contains the truth exactly within numerical precision:

- A1 KL rate approximately 0;
- fitted chi approximately 0.300000000;
- descriptive expected BIC preference: A1.

For g = -0.75:

- H = -0.04377612255528212;
- best A1 KL rate = 0.005762739413465506;
- best A1 fitted chi = 0.28632115634972;
- best A2 KL rate = 0.0027848211294710557;
- expected A1-to-A2 NLL improvement at n_eff=7552 = 22.489238880726088;
- expected BIC(A2)-BIC(A1) = -18.189774637976164;
- descriptive expected BIC preference: A2.

For g = +0.75:

- H = +0.04377612255528212;
- best A1 KL rate = 0.004392205903574285;
- best A1 fitted chi = 0.2729775635912047;
- best A2 KL rate = 0.0016092986440856484;
- expected A1-to-A2 NLL improvement at n_eff=7552 = 21.016515623658186;
- expected BIC(A2)-BIC(A1) = -15.244328123840361;
- descriptive expected BIC preference: A2.

## Interpretation

The result establishes a model-family misspecification pressure inside the scientifically intended continuous-lineage C family.

A valid one-mode C truth with nonzero g/H is outside current A1 because A1 fixes H=0. Under the declared 30-s-equivalent effective sample count, A2 can improve the scalar spectral approximation enough to overcome its three-parameter BIC penalty even though the generating truth contains only one physical mode.

Therefore:

[
A2\text{ preference}
\not\Rightarrow
\text{two physical modes}
]

even when the truth is inside the intended continuous-time biological-lineage family.

The current A1 restriction can also bias the local chi estimate. In the two nonzero-g cells above, the best A1 chi shifts downward from the true 0.30.

This result strengthens the existing anisotropic/rank-1 process-noise finding. The failure is not confined to discrete arbitrary-Q truths outside the preferred biological family; it occurs inside C itself when the allowed covariance-phase coordinate is nonzero.

## Claim boundary

This result justifies qualification of a one-mode C-family nuisance extension capable of representing nonzero g/H before A2 selection can be interpreted as multimodality.

It does not by itself:

- promote such an extension into the production estimator;
- license real-EEG local chi;
- define an admission threshold;
- establish that every A2 win is caused by nonzero g/H;
- alter N-B2 or N-B3;
- alter completed GRI/BioSystems or parked cancer/Shaffer work.

A finite-realization known-truth probe remains separately required to confirm that the analytic spectral pressure appears in the existing numerical fitting pipeline rather than only in the asymptotic spectral calculation.
