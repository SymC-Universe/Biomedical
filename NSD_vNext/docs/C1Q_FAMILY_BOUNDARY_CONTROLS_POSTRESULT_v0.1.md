# NSD C1Q Family-Boundary Controls Postresult v0.1

Status: QUALIFICATION-ONLY FAMILY-BOUNDARY RESULT  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Provenance

Workflow: `NSD C1Q Family Boundary Controls`  
Run: `36355282570`  
Conclusion: SUCCESS  
Source head: `a1b8e4d8fa8f9921d76abdb3b89f824f4c93fbd0`

Artifact: `nsd-c1q-family-boundary-controls`  
Artifact ID: `10944145699`  
Digest: `sha256:9fb2e8ef80f78ff026b83c161a0bb5f12ff8f8a18e9522ae40e1a80196d90c38`  
Expiry: 26 December 2026

## Frozen truth geometry

The control used one underdamped reference at 128 Hz with:

- A = 0.8;
- natural frequency = 10 Hz;
- truth chi = 0.30;
- L = 0.14726215563702155;
- rho = 0.8630676896963296;
- theta = 0.468263810491061;
- continuous C boundary `H_C = 0.11355130508902342`;
- discrete exact-image D boundary `H_D = 0.11823599286494063`;
- scalar-positive S boundaries approximately -0.1419378809270763 and +0.25832255733921916.

D\C truths were placed halfway between the C and D boundaries. S\D truths were placed halfway between the signed D and scalar-positive S boundaries. Every generated law was strictly scalar-spectral-positive by construction.

## Results

C1Q had the lowest BIC in all eight D\C and S\D finite-realization cells.

Negative D\C truth:
- implied continuous g = -1.0206280666;
- seed 0: C1Q winner by 107.540 BIC, fitted g = -0.9999989924;
- seed 1: C1Q winner by 99.802 BIC, fitted g = -0.9999979707.

Positive D\C truth:
- implied continuous g = +1.0206280666;
- seed 0: C1Q winner by 28.501 BIC, fitted g = +0.9101433648;
- seed 1: C1Q winner by 28.679 BIC, fitted g = +0.8672182108.

Negative S\D truth:
- implied continuous g = -1.1456225606;
- seed 0: C1Q winner by 169.485 BIC, fitted g = -0.9999997749;
- seed 1: C1Q winner by 149.421 BIC, fitted g = -0.9999997749.

Positive S\D truth:
- implied continuous g = +1.6580987330;
- seed 0: C1Q winner by 95.362 BIC, fitted g = +0.9999997749;
- seed 1: C1Q winner by 94.535 BIC, fitted g = +0.9999997749.

## Interpretation

The result establishes a second C1Q refusal boundary.

A constrained C-family candidate can be the best finite-sample approximating model even when the generating law is known to lie outside C and even outside D. Therefore:

[
\mathrm{C1Q\ wins}
\not\Rightarrow
\mathrm{truth\in C}.
]

Boundary proximity is also not a sufficient refusal rule. Three of the four constructed boundary classes drove fitted g essentially to |g|=1, but the positive D\C cells were approximated with fitted g approximately 0.87-0.91, well inside C, while the true law had |g|>1.

Therefore:

[
|\hat g|<1
\not\Rightarrow
\mathrm{truth\in C}.
]

Finite-sample C1Q parameter location cannot substitute for independent continuous-lineage qualification.

## Consequence

C1Q may be used as a nuisance-capable one-mode candidate, but continuous-lineage admission must be established by independent qualification such as paired sampling/metamorphic consistency, structural-order/memory controls, predictive closure, and uncertainty-aware family-boundary calibration.

This result also confirms that C/D/S are semantic/model-scope layers, not ordinary same-dimensional alternatives that can be selected by BIC alone.

## Claim boundary

C1Q remains qualification-only. No production family is changed. No empirical C/D/S refusal threshold is defined. Real-EEG local chi remains unlicensed. N-B2 and N-B3 remain separate.
