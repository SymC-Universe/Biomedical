# NSD Predictive Closure Calibration Preflight v0.1

Status: PREDECISION CALIBRATION DESIGN  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

This preflight defines how predictive approximate closure will be calibrated before any real-EEG N-B1 admission rule is frozen.

The design is claim-relative. It does not ask whether a biological mode is isolated from all substrate effects. It asks whether unresolved substrate/interface dynamics materially alter the specific local continuous-time pole-pair and chi claim or materially degrade held-out reduced-model prediction.

## Exact mechanism classes

Calibration keeps four exact known-truth classes separate:

1. exact closed: no P-to-Q leakage and no Q-to-P hidden-state input;
2. leakage only: P drives Q, but Q does not return to P;
3. hidden-input only: Q can drive P, but P does not excite Q;
4. return-memory: bidirectional coupling allows P -> Q -> P feedback.

The exact eliminated equation is

[
p'(t)=L_{PP}p(t)
+L_{PQ}e^{L_{QQ}t}q_0
+\int_0^t L_{PQ}e^{L_{QQ}(t-s)}L_{QP}p(s)\,ds.
]

Therefore hidden-state uncertainty and endogenous memory are calibrated separately.

## Descriptive calibration outputs

No admission threshold is defined here. The exploratory calibration map reports at minimum:

- resolved-subspace reduced-versus-full predictive error;
- hidden-initial-state sensitivity;
- memory-kernel magnitude;
- local-to-embedded pole displacement when matching is unambiguous;
- local-to-embedded chi displacement when both remain on the same licensed branch;
- full-system stability status;
- model-family/refusal behavior in the parallel A0/A1/A2 known-truth probes.

Raw coupling strength is retained as fixture provenance, not used as a universal closure score.

## Required invariants and controls

The calibration must preserve the following exact controls:

- leakage-only can have nonzero P-to-Q coupling while resolved P prediction remains exact;
- hidden-input-only can have zero endogenous memory but nonzero sensitivity to hidden initial state;
- return-memory can perturb resolved P prediction even when hidden initial state is zero;
- N-B1 local chi may remain valid while N-B3 whole-system transient behavior changes;
- exact C-family chi and g remain invariant under alias-safe pure decimation;
- coarse discrete D compatibility cannot be back-projected as evidence of fine-rate D semantics.

## Calibration before thresholding

The calibration stage must map mechanism strength to claim error before selecting any tolerance. It must not choose a threshold by maximizing performance on real EEG or disorder labels.

A later threshold freeze must specify, at minimum:

- the prediction horizon or horizons;
- the error functional used for reduced-versus-full prediction;
- how hidden-state uncertainty is represented;
- the tolerated pole/chi displacement or its uncertainty-relative equivalent;
- held-out predictive degradation criterion;
- near-critical handling;
- multiplicity/coverage policy if multiple modes or horizons are tested;
- refusal behavior when these quantities are nonidentifiable.

Those choices are scientific decisions and are not silently filled in by this preflight.

## Current executable tools

Core mechanism contracts:

`NSD_vNext/engine/tests/test_predictive_closure_contracts.py`

Exploratory mechanism map:

`NSD_vNext/engine/tools/probe_predictive_closure_calibration.py`

Continuous-lineage model-order pressure:

`NSD_vNext/engine/tools/probe_continuous_lineage_nonzero_g.py`

`NSD_vNext/engine/tools/probe_continuous_lineage_spectral_kl.py`

## Interpretation ceiling

This preflight does not:

- license real-EEG local chi;
- define a predictive-closure tolerance;
- define a universal memory threshold;
- promote nonzero-g/H into the production estimator;
- interpret A2 preference as two physical modes;
- alter N-B2 or N-B3;
- alter completed GRI/BioSystems or parked cancer/Shaffer work.
