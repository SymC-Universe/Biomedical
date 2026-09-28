# NSD Combined Structural-Predictive Refusal Postresult v0.1

Status: QUALIFICATION-ONLY KNOWN-TRUTH RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Primary investigation: Bio Chi  
Branch: \`nsd-rebuild-gom-v0.8.0\`

## Provenance

Workflow: \`NSD Combined Structural Predictive Refusal\`  
Run: \`36360088607\`  
Conclusion: SUCCESS  
Source head: \`99e3264cc5eb4a0ca93bcb62b0cbf2ad09b1f95a\`

Artifact: \`nsd-combined-structural-predictive-refusal\`  
Artifact ID: \`10945211948\`  
Digest: \`sha256:a1c4ef424f0c1323e9fd3249621c1c29f17c8c34b8a94cc5b83c5b38d8b633c1\`

Output status: \`PREDECISION_CALIBRATION_ONLY\`  
\`licenses_real_eeg_local_chi=false\`  
\`defines_refusal_threshold=false\`  
\`changes_production_estimator=false\`

## Design

Each known-truth realization contained 60 s at 256 Hz and was split into a 30 s training segment and a 30 s untouched contiguous holdout.

Truth classes:
- C interior: g=0, -0.75, +0.75;
- positive and negative D outside C;
- positive and negative S outside D;
- colored-process extra-pole truth with phi=0.7;
- genuine separated two-mode truth.

C1Q and D1Q were fit only on training data. Fitted parameters and training normalization were frozen. Holdout scoring used the existing cold-start-plus-burn semantics. The same holdout also supplied positive-lag recurrence and Hankel diagnostics. Current A0/A1/A2 training/holdout behavior was retained as a descriptive control.

No threshold was selected.

## Result

The combined diagnostic set did **not** produce a clean finite-sample refusal signature for the colored-process truth.

Against the pooled C-interior reference distribution, threshold-free rank AUC for the colored truth was:

- C1Q held-out NLL per sample: 0.0370;
- C1Q held-out innovation maximum absolute autocorrelation: 0.4444;
- D1Q held-out NLL per sample: 0.0370;
- D1Q held-out innovation maximum absolute autocorrelation: 0.4444;
- D1Q-minus-C1Q held-out NLL per sample: 0.4444;
- Hankel s3/s2: 0.4074;
- normalized order-two recurrence hold-lag RMS: 0.4815.

These values do not support a monotone separator in which the colored truth is consistently more misspecified than valid C interiors.

The colored truth also remained strongly approximable by the one-mode candidates:
- median C1Q held-out innovation max absolute autocorrelation: 0.02381;
- median C1Q held-out NLL per sample: 0.87664;
- median recurrence normalized hold-lag RMS: 0.06126;
- median Hankel s3/s2: 0.03256.

These values overlap the C-interior finite-sample ranges.

Current A0/A1/A2 behavior did detect extra model-order pressure descriptively: A2 was the training and holdout winner for all three colored-process seeds. However, earlier qualification already established that A2 pressure can also arise from valid one-mode C truths when the one-mode nuisance family is misspecified. A2 preference therefore remains a warning, not a physical-mode admission rule.

The genuine two-mode truth also failed to yield a universal multichannel separator. Innovation autocorrelation was relatively discriminating against C interiors (rank AUC approximately 0.963), while held-out NLL, recurrence, and Hankel diagnostics were not uniformly ordered. This reinforces the need for model-specific qualification rather than a generic composite cutoff.

## Root-cause refinement

The exact colored-process law is rank three, but its third population Hankel singular component is weak relative to the leading second-order structure.

Using the frozen analytic colored-process positive-lag decomposition from \`STRUCTURAL_ORDER_REFUSAL_PREFLIGHT_v0.1.md\`, a 6x6 population Hankel matrix gives approximately:

- s1 = 2.0123;
- s2 = 0.7020;
- s3 = 0.001692;
- s3/s2 = 0.002410;
- s3/s1 = 0.000841.

Thus the extra pole is structurally real but weak in the covariance-Hankel spectrum. Finite-sample noise can readily obscure that component. This explains why exact rank theory and finite-sample raw rank diagnostics diverge without invalidating the exact theorem.

## Scientific consequence

The current shortcut is falsified:

\[
\text{several weak diagnostics}
\not\Rightarrow
\text{a reliable structural-order gate}.
\]

The next safe question is explicit recurrence-order or higher-order/memory model comparison on untouched holdout data, with no cutoff tuned on the same rows.

The existing nested recurrence-order preflight and probe are the next qualification rung:

- \`NSD_vNext/docs/NESTED_RECURRENCE_ORDER_COMPARATOR_PREFLIGHT_v0.1.md\`;
- \`NSD_vNext/engine/tools/probe_nested_recurrence_order.py\`.

If that comparator still overlaps materially, the next move is an explicit likelihood-based higher-order/memory candidate rather than threshold tuning.

## Threshold impact

No threshold is frozen, revised, or retired.

The following remain unfrozen:
- finite-data structural-order threshold;
- C-vs-D family-membership threshold;
- predictive-closure tolerance;
- paired-sampling drift cutoff;
- near-critical uncertainty cutoff.

## Interpretation ceiling

This result does not:
- license real-EEG local chi;
- promote C1Q or D1Q;
- change production A0/A1/A2;
- prove that A2 corresponds to two physical modes;
- define a biological memory cutoff;
- open historical ASD/disorder outcomes;
- alter completed GRI/BioSystems or parked cancer/Shaffer.
