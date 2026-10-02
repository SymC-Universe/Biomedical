# NSD joint local-chi / embedded-system known-truth post-result audit v0.1

Date: 22 September 2026  
Status: COMPLETE P0-Q KNOWN-TRUTH RESULT  
Program authority: SymC General Operations Manual v0.8.3  
Workflow: `NSD Chi-vs-System Coupled Known Truth`  
Run: `35759456553`  
Artifact: `nsd-chi-system-coupled-known-truth-v0-1`  
Artifact ID: `10710185979`  
Artifact ZIP SHA-256: `b58c3e84194d6e303dcc1b1763b87466bf1364e2d5d4ffa832d0c687220cfd8b`

## Result

The exact coupled-second-order fixtures passed all six regression tests.

The result directly establishes, within the frozen linear known-truth systems, that the local modal damping-ratio vector is not sufficient to determine embedded system behavior.

### Same local damping ratios, same full eigenvalues, different transient behavior

Both systems had:
- local natural frequencies: (1, 1) rad/s;
- local damping ratios: (0.2, 0.2);
- identical full eigenspectra;
- spectral abscissa: -0.2.

The uncoupled reference had:
- numerical abscissa: 0;
- maximum transient gain: 1.0;
- sustained return under the fixture gain criterion: 0.

The feed-forward coupled system had:
- numerical abscissa: ~0.8198;
- maximum transient gain: ~2.3422 at t~4.84;
- sustained return time under the same fixture criterion: ~13.65;
- extreme eigenvector conditioning, consistent with the deliberately defective/non-normal repeated-eigenvalue construction.

Therefore:
`same local zeta_i + same asymptotic eigenspectrum != same transient behavior or recovery`.

This is the strongest exact result so far for the GOM v0.8.3 joint chi/Chi requirement because it rules out both a local-scalar-only description and an eigenspectrum-only description for the transient/recovery question.

### Same local damping ratios, different embedded modal organization

The reciprocal-coupling fixture preserved:
- local natural frequencies (1,1);
- local damping ratios (0.2,0.2);
- isolated local stability.

But the full embedded frequencies reorganized from the uncoupled repeated pair near |Im lambda|~0.9798 to coupled pairs near ~1.32665 and 0.4.

The coupled system remained asymptotically stable with spectral abscissa ~-0.2, yet became reactive and reached transient gain ~1.4065 with sustained return time ~4.48 under the fixture diagnostic.

Therefore:
`same local modal chi != same embedded modal spectrum or response organization`.

### Locally stable, globally unstable

Both isolated modes remained stable with local damping ratios 0.2.

Reciprocal coupling produced a positive embedded eigenvalue:
- spectral abscissa ~+0.28990;
- embedded system asymptotically unstable.

Therefore:
`all local modal chi stable != embedded system stable`.

## What this earns

For the NSD Stability Architecture, local/modal damping ratios and embedded/system descriptors are now mathematically proven to be non-interchangeable in explicit second-order fixtures.

The joint research target therefore has at least four distinguishable layers:
1. local modal damping;
2. embedded eigenspectrum/asymptotic stability;
3. transient amplification/reactivity;
4. recovery/return behavior.

A single whole-system scalar is not licensed by this result.

## What this does not earn

This result does not show:
- that sensor EEG identifies any of these system matrices;
- that human neural dynamics instantiate these exact fixtures;
- that one native system descriptor is sufficient for NSD;
- that a whole-brain chi exists;
- that recovery can be inferred from static/repeat EEG;
- diagnosis, prognosis, treatment guidance, or clinical classification.

## Forward consequence

Once a real-EEG local modal route is qualified, the empirical program must not stop at local `zeta_i`.

The next legitimate system-level question is whether reproducible neural data support identifiable coupling/operator structure and whether that structure adds independent information about embedded response beyond the local modal vector.

Until then, this result belongs in the Function/Limit architecture as exact known truth, not as a biological result.
