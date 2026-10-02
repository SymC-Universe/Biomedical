# NSD C1Q Paired-Sampling Semantics Postresult v0.1

Status: PREDECISION CALIBRATION RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD C1Q Paired-Sampling Semantics`  
Run: `36355594966`  
Conclusion: SUCCESS  
Source head: `982040dd6e6041a0034e5e946e5135941ad95623`

Artifact: `nsd-c1q-paired-sampling-semantics`  
Artifact ID: `10943546777`  
Digest: `sha256:dadea7ad96f6be13bc693c2b39561ead555223e25146b71997fadf29992d19dc`  
Expiry: 26 December 2026

## Design

Each 30 s fine-rate realization at 256 Hz was deterministically decimated by two and the same qualification-only C1Q candidate was fit independently at 256 and 128 Hz.

Truth families:
- C interior, g = -0.75 and +0.75;
- D\C second-order laws;
- S\D scalar-positive second-order laws.

No cross-rate acceptance threshold was defined.

## Results

C-interior controls showed finite-sample paired-rate shifts rather than exact fitted invariance:

- g=-0.75: absolute chi shifts 0.00095 and 0.00778; absolute g shifts 0.0314 and 0.0195.
- g=+0.75: absolute chi shifts 0.00626 and 0.00650; absolute g shifts 0.1515 and 0.1978.

The positive-g seed-1 coarse fit reached practical g-boundary proximity despite the generating truth being a valid C interior point.

D\C controls did not separate cleanly from C by paired-rate stability:

- negative D\C: chi shifts 0.00573 and 0.00159; g shifts 0.04397 and approximately 4.3e-7;
- positive D\C: chi shifts 0.00253 and 0.00186; g shifts 0.1218 and 0.0988.

S\D controls were asymmetric:

- negative S\D: chi shifts 0.00191 and 0.00731 with both rates pinned near g=-1;
- positive S\D: larger chi shifts 0.03074 and 0.02251 with both rates pinned near g=+1.

## Interpretation

Paired deterministic resampling remains a valid metamorphic qualification tool, but finite-sample fitted-parameter consistency is not by itself a reliable C-membership test at 30 s.

A constrained C1Q fit can approximate out-of-C second-order laws at both sampling rates while preserving apparently stable fitted chi/g. Conversely, valid C truths can show noticeable fitted-g drift because of finite-sample uncertainty and boundary behavior.

Therefore:

[
\mathrm{paired\ C1Q\ stability}
\not\Rightarrow
\mathrm{truth\in C},
]

and

[
\mathrm{finite\ fitted\ drift}
\not\Rightarrow
\mathrm{truth\notin C}
]

without prospective uncertainty calibration.

## Consequence

The next family-scope control must estimate the broader discrete exact-image one-mode law without forcing |g|<=1. That D-family control can determine whether the data-supported one-mode solution itself lies outside continuous embeddability, rather than asking a constrained C fit to reveal its own misspecification through parameter drift.

No sampling-consistency cutoff is frozen. C1Q remains qualification-only. Real-EEG local chi remains unlicensed.
