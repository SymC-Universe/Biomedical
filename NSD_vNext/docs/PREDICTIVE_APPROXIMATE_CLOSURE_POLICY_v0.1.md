# NSD Predictive Approximate Closure Policy v0.1

Status: PROSPECTIVE SCIENTIFIC POLICY / PRE-CALIBRATION  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Decision

N-B1 will use predictive approximate closure rather than requiring exact or near-exact Markovian isolation.

A local continuous-time mode may remain admissible when measurable substrate/interface memory or hidden-state dependence exists, provided prospective known-truth and held-out qualification demonstrates that those omitted effects do not materially change the specific local claim being made.

This policy keeps continuous-time modal lineage C as the prospective N-B1 family. It does not license real-EEG local chi and does not authorize a production estimator-family change.

## Scientific meaning

Predictive closure is claim-relative rather than isolation-relative.

For local biological chi, the reduced modal description must be sufficiently closed that unresolved dynamics do not materially alter:

1. the licensed continuous-time pole-pair lineage;
2. the inferred local chi derived from that pole pair;
3. held-out predictive behavior of the reduced model over the prospectively defined evaluation horizon;
4. refusal behavior under known out-of-family or nonclosed truths.

Measurable memory is therefore not automatically disqualifying. Memory or substrate dependence becomes disqualifying when it materially changes the claimed local dynamics or causes the reduced model to lose prospective predictive adequacy.

## Structural decomposition retained

For a P/Q split of a full generator L,

[
L =
\begin{bmatrix}
L_{PP} & L_{PQ}\\
L_{QP} & L_{QQ}
\end{bmatrix},
]

the qualification program keeps separate:

- P-to-Q leakage: `L_QP`;
- Q-to-P hidden-state input: `L_PQ`;
- return-memory/self-energy:
  `Sigma(z)=L_PQ(zI-L_QQ)^{-1}L_QP`.

No single raw coupling norm is treated as a universal closure score.

## Prospective admission architecture

A future N-B1 local-chi admission requires all of the following classes of evidence:

- C-family continuous-time lineage is supported;
- structural identifiability is retained;
- alias-safe sampling invariance is supported;
- predictive closure criteria are satisfied under the frozen calibration;
- known refusal controls behave correctly;
- uncertainty on the pole pair and chi remains within the prospectively frozen claim tolerance.

The exact numerical tolerances are not defined in this policy. They must be calibrated using known truths and held-out prediction, frozen before real-EEG outcomes are opened, and then applied without retuning.

## Calibration rules

The closure calibration must be constructed without real EEG and must include at minimum:

- exact closed controls;
- hidden-input-only controls;
- leakage-without-return controls;
- bidirectional return-memory controls;
- continuous-lineage C interiors with both signs of g;
- near-critical cells;
- sampling/decimation controls;
- A2 pole-collision controls;
- colored-process out-of-family controls.

Calibration outputs must separately report:

- reduced-versus-full predictive error;
- memory/self-energy magnitude or an equivalent mechanism-specific diagnostic;
- pole-pair displacement where a comparison is mathematically licensed;
- chi displacement where chi remains identifiable on the same branch;
- held-out likelihood/prediction degradation;
- refusal status.

No criterion may be tuned against real-EEG disorder outcomes.

## Interpretation firewall

Predictive approximate closure does not mean that substrate effects are biologically unimportant. It means only that, for the local N-B1 claim being made, unresolved substrate effects have been prospectively shown not to materially alter the claimed local dynamical coordinate within the frozen qualification contract.

N-B2 and N-B3 remain separate. A mode can fail N-B1 predictive closure while still contributing to modal/vector architecture or system-level perturbation/recovery structure.

## Current non-claims

This policy does not:

- license real-EEG local chi;
- define a universal memory cutoff;
- define a production refusal threshold;
- add a production refusal code;
- choose a nonzero-g/H nuisance estimator;
- reinterpret previous A2 wins as closure failures;
- alter completed GRI/BioSystems or parked cancer/Shaffer work.

## Exact elimination identity and claim-relative consequence

For
[
p' = L_{PP}p + L_{PQ}q,\qquad
q' = L_{QP}p + L_{QQ}q,
]

eliminating q gives
[
p'(t)
=
L_{PP}p(t)
+
L_{PQ}e^{L_{QQ}t}q_0
+
\int_0^t
L_{PQ}e^{L_{QQ}(t-s)}L_{QP}p(s)\,ds.
]

This separates two distinct non-Markovian risks for the local claim:

- hidden-state forcing: `L_PQ exp(L_QQ t) q0`;
- endogenous return-memory kernel: `K(t)=L_PQ exp(L_QQ t)L_QP`.

A nonzero P-to-Q leakage term `L_QP` is therefore not, by itself, sufficient reason to refuse local chi. If `L_PQ=0`, the resolved P trajectory remains exactly governed by `L_PP` even though the full state leaves P. Under the approved predictive-closure policy, refusal is tied to material effect on the claimed local dynamics, not to raw leakage alone.

Likewise, `L_PQ!=0` with `L_QP=0` produces hidden-state sensitivity without endogenous return memory. Predictive qualification must therefore distinguish hidden-state uncertainty from memory rather than folding both into one closure score.
