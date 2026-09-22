# NSD State-Space Standard-Toolkit Comparator Plan v0.1

Date: 18 September 2026
Status: P0-Q COMPARATOR ACTIVE / FAIRNESS MAPPING FROZEN

## Purpose

The GOM requires comparison with the strongest relevant native/simple toolkit before an incremental-value claim can be made.

State-space neural oscillator modeling is established prior art. NSD therefore does not use direct AR(2) as its only comparator and does not claim that oscillator state-space decomposition, EM fitting, or information-criterion model-order search is new.

## Prior-art anchor

Beck, Stephen, and Purdon:
"State Space Oscillator Models for Neural Data Analysis"
Annual International Conference of the IEEE Engineering in Medicine and Biology Society, 2018.
DOI: 10.1109/EMBC.2018.8513215
PMID: 30441408

That work uses combinations of linear oscillatory state-space models, expectation-maximization parameter learning, and AIC model selection on EEG.

## Native software comparator

Pinned candidate:
- package: SOMATA;
- version: 0.5.6;
- release date: 9 August 2024;
- project: State-space Oscillator Modeling And Time-series Analysis;
- license: BSD 3-Clause Clear;
- PyPI: https://pypi.org/project/somata/0.5.6/;
- repository: https://github.com/mh105/somata.

Relevant SOMATA capabilities include:
- OscillatorModel and AutoRegModel state-space components;
- EM learning;
- iterative and decomposed oscillator-search methods;
- information-criterion/model-knee selection;
- innovations/residual diagnostics;
- switching state-space inference.

The public dOsc implementation also exposes residual autocorrelation and normality diagnostics and allows knee, maximum-likelihood, or EBIC-based model selection.

## Comparator firewall

SOMATA is an isolated comparator lane, not a silent dependency of the NSD Engine.

The comparator receives the same frozen generator families where semantic mapping is legitimate. It is not allowed to tune NSD thresholds, and NSD outputs are not allowed to tune SOMATA settings after outcomes are viewed without recording a new comparator version.

Differences in model definitions or parameter conventions are preserved rather than forced into artificial scalar equality.

## First comparison questions

1. Valid single oscillator:
   - does SOMATA identify one oscillatory component?
   - what frequency/decay errors are obtained?

2. Nonoscillatory AR(1):
   - does the standard toolkit retain a nonoscillatory/AR-like explanation or invent an oscillator?

3. Separated and close two-mode truth:
   - what model order is selected?
   - how does resolvable separation compare with NSD A2?

4. Colored observation noise:
   - does residual diagnosis expose the misspecification?
   - does selected oscillator structure change?

5. Frequency shift:
   - does stationary oscillator search split a temporal transition into multiple components?
   - do switching/time-varying methods resolve the distinction?

6. Finite bursts:
   - how do stationary and switching/state-sensitive methods behave?

7. White noise:
   - does the toolkit avoid a meaningful oscillator claim?

## Outcome classes

The comparison is reported under the GOM standard-toolkit outcome classes rather than as a winner-take-all score:

- ADDS;
- EQUIVALENT;
- SUBTRACTS;
- NOT_COMPARABLE for a specific quantity when definitions do not match.

No overall tool verdict is frozen in P0-Q.

## Novelty ceiling

Even if NSD later adds value, novelty cannot attach to generic:
- Kalman filtering;
- oscillator state-space representation;
- EM learning;
- information-criterion model selection;
- residual whiteness testing.

A defensible residual contribution would have to lie in one or more of:
- explicit qualification/refusal architecture;
- known-truth operating-region and Limit-Map construction;
- separation of local modal identity from embedded/system stability;
- preservation of absent/refused/open-channel states;
- independent Atlas integration;
- cross-layer stability interpretation;
- demonstrable incremental predictive or interpretive value on untouched evidence.

## Activation condition

Execute this comparator after the current A0/A1/A2 optimizer-repair rerun stabilizes the NSD implementation enough that the comparison is not dominated by a known mechanical search defect.


## Mechanical/API preflight closure

Date: 22 September 2026

Pinned SOMATA 0.5.6 installed successfully in GitHub Actions and exposed the required comparator API:
- `IterativeOscillatorModel.iterate`;
- `get_knee_osc`;
- `diagnose_residual_acf`.

Preflight run:
- workflow: `NSD SOMATA Comparator Preflight`;
- run: `35671757551`;
- artifact: `nsd-somata-comparator-preflight`;
- artifact id: `10670958164`;
- artifact ZIP SHA-256: `7957a8b5d0fd98c848961a8481fb1c689c2b399119e5799f591d63232a98b742`.

No EEG or scientific comparator performance was evaluated in that run.

## Matched-information fairness freeze

The first known-truth comparator mapping is now prospectively frozen in:
- `SOMATA_COMPARATOR_FAIRNESS_FREEZE_v0.1.md`;
- `docs/manifests/somata_comparator_fairness_v0.1.json`.

Key rule:
both tools receive the exact same deterministic 120 Hz standardized signal produced from the already-frozen 256 Hz NSD adequacy generator realization. This follows SOMATA's documented recommendation to downsample to 120 Hz or less while preventing NSD from receiving a higher-information-rate signal.

The iOsc lane permits one or two oscillators, whereas NSD A0/A1/A2 includes a nonoscillatory A0 alternative. Therefore zero-oscillator refusal is explicitly `NOT_DIRECTLY_COMPARABLE` in this first iOsc lane rather than being forced into a false equivalence.

The first matched known-truth comparator is now executable under:
`.github/workflows/nsd-somata-known-truth.yml`.

No overall ADDS/EQUIVALENT/SUBTRACTS verdict is authorized by this first P0-Q run.
