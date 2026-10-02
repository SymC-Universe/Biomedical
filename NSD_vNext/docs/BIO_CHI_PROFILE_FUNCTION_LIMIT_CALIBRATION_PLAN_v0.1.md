# Bio Chi Profile Function/Limit Calibration Plan v0.1

**Status:** APQ-2 SUBSTANTIAL DRAFT  
**Date:** 28 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, P0-Q profile/refusal qualification  
**Parent method result:** \`BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_POSTRESULT_v1.0.md\`

## Scientific target

Profile likelihood is qualified as the primary single-record practical-identifiability diagnostic for local chi. The remaining question is whether profile geometry behaves differently across:

1. valid, practically identifiable C-family modes;
2. valid C-family modes that are weak, near-critical, near-family-boundary, or frequency-edge cases;
3. second-order observable laws outside continuous family C;
4. higher-order or memory-contaminated truths.

The purpose is **not** to discover a numerical likelihood cutoff. It is to determine which parts of a future admission/refusal architecture can legitimately be carried by profile geometry and which semantic failures require independent gates.

## Claim ceiling

P0-Q known-truth Function/Limit calibration only.

This plan cannot:

- establish biological prevalence;
- define a profile-likelihood admission threshold;
- promote C1Q-RS to production;
- prove C-family membership from fit/profile quality;
- license real-EEG local chi;
- replace C/D/S family semantics, structural-order controls, or closure/memory tests.

## Frozen truth classes

All paths are generated at 256 Hz for 60 s and exactly decimated by 2 for the paired 128 Hz record. The fine/coarse pair is one metamorphic unit.

### Function Map: valid C-family truths

| ID | Role | A | natural f Hz | chi | g | Scientific purpose |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| C0 | NOMINAL_FUNCTION | 0.80 | 10.0 | 0.30 | 0.00 | regular interior reference |
| C1 | NOMINAL_FUNCTION | 0.65 | 12.0 | 0.45 | 0.55 | regular nonzero-g interior |
| C2 | PERTURBED_FUNCTION | 0.28 | 19.0 | 0.50 | -0.72 | weak-observation / low-latent-information case |
| C3 | BOUNDARY_OR_TRANSITION | 0.80 | 10.0 | 0.93 | 0.20 | near-critical underdamped C case |
| C4 | BOUNDARY_OR_TRANSITION | 0.80 | 10.0 | 0.30 | 0.95 | near-C-family nuisance boundary |
| C5 | BOUNDARY_OR_TRANSITION | 0.70 | 42.0 | 0.25 | 0.20 | high-frequency / estimator-frequency-edge case |

All six remain strictly within the intended underdamped C family. C3-C5 are deliberately non-nominal and are not treated as biological prevalence samples.

### Limit Map: semantically incompatible truths

Canonical second-order C/D/S geometry uses A=0.8, natural frequency 10 Hz, zeta=0.30 at 256 Hz.

- **L0 D_NOT_C_POS:** positive D\C midpoint between continuous C and exact discrete D nuisance boundaries.
- **L1 D_NOT_C_NEG:** negative D\C counterpart.
- **L2 S_NOT_D_POS:** positive scalar-positive S\D midpoint between exact D and scalar-positive boundary.
- **L3 S_NOT_D_NEG:** negative S\D counterpart.
- **L4 COLORED_MEMORY:** established colored-process truth with phi=0.7 and the qualified 10 Hz / zeta=0.30 base oscillator.
- **L5 GENUINE_TWO_MODE:** established separated 10 Hz / 20 Hz two-mode truth with observation noise.

D\C and S\D signals use the existing exact ARMA spectral-factor constructors already qualified in the repository. Colored and two-mode signals use the existing qualified adversarial-control generators.

For L0-L5, a fitted C1Q-RS chi is an **imposed candidate coordinate**, not a generating biological/continuous-C truth coordinate. No “true chi error” is reported for these semantic Limit cases.

## Frozen realization seeds

\`301103, 509203, 811223\`

The same seed index is used for fine-path generation and paired exact decimation. Generator-specific deterministic offsets already present in the established fixtures remain unchanged.

## Frozen fitting and profile method

Use unchanged:

- C1Q-RS likelihood, parameterization, bounds, multistart logic, and optimization budgets;
- physical-coordinate chi profile implementation qualified by run \`36373236094\`;
- profile grid of 61 uniformly spaced chi values on [0.05, 0.98], with fitted chi inserted exactly;
- generating true chi inserted exactly only for C0-C5;
- nuisance optimization recipe from the completed single-series method plan;
- local physical-coordinate Hessian diagnostic as regular-only secondary evidence.

No bootstrap is run in this experiment. The goal is profile morphology and semantic comparison, not another finite-sample bootstrap calibration.

## Planned execution

Total frozen cases:

\[
12\ \text{truth classes} \times 3\ \text{seeds} \times 2\ \text{rates}
=72\ \text{profile/Hessian cases}.
\]

### Mechanical preflight

- C0, seed 301103, fine rate;
- L4 colored-memory, seed 301103, coarse rate.

Preflight passes only if:

- source truth generator executes;
- paired decimation identity is valid;
- C1Q-RS fit executes;
- fitted-chi profile point reproduces global NLL within the existing mechanical tolerance;
- full profile serializes;
- Hessian computes or explicitly refuses;
- semantic truth labels and output schema serialize correctly.

Scientific profile shape cannot retune or stop the plan.

### Full execution

After mechanical preflight, run all 72 cases independently and merge only after all case artifacts exist.

## Frozen outputs

For every case preserve:

- truth class and Function/Limit role;
- seed and rate;
- generator identity;
- semantic C-membership truth: YES/NO;
- whether a generating continuous-C chi is defined;
- C1Q-RS fitted A, natural frequency, chi, g, NLL, BIC, raw parameters, winning start;
- raw-boundary and g-boundary diagnostics;
- Hessian status, eigenvalues/condition if available, local chi SE if valid;
- complete chi profile;
- fitted-chi profile reproduction status;
- true-chi delta NLL for C cases only;
- number/location of profile local minima;
- left-edge and right-edge delta NLL;
- profile delta-NLL range;
- grid location of lowest profiled point;
- whether the lowest profiled point is an edge;
- same-path fine/coarse fitted-chi drift.

For C0-C5 additionally preserve signed/absolute chi, g, and natural-frequency recovery errors.

For L0-L5 explicitly set recovery error against “true C chi” to \`NOT_APPLICABLE\`.

## Descriptive profile morphology

No feature becomes an admission rule in this experiment.

The merged artifact may describe:

- closed interior-looking profile;
- shallow/open-to-low-chi profile;
- shallow/open-to-high-chi profile;
- edge-minimum profile;
- multimodal/multiple-local-minimum profile;
- Hessian regular or refused/non-positive-definite;
- numerical-boundary-attracted fit.

These are descriptive morphology labels derived from exact recorded geometry, not pass/fail thresholds.

## Frozen questions

1. Do nominal/regular C cases generally show closed, interior profile geometry?
2. Do weak/near-critical/boundary/frequency-edge C cases preserve semantic validity while showing weaker or nonregular profile geometry?
3. Do D\C and S\D truths sometimes produce deceptively regular C1Q-RS profiles despite semantic incompatibility?
4. Do colored-memory and genuine multimode truths expose profile nonregularity, or can they also masquerade as practically identifiable one-mode fits?
5. Which failure classes therefore require independent family/order/closure gates even when profile likelihood is regular?

A finding that a Limit truth has a compact profile is **not** a failed experiment. It would establish that practical identifiability and semantic admissibility are orthogonal.

## Outcome architecture

**Profile morphology separates practical information but not semantics:** regular/weak C distinctions are visible, while some D/S or higher-order Limit truths retain compact profiles. Profile remains a practical-identifiability gate only; independent semantic gates are mandatory.

**Profile morphology also reacts to some semantic failures:** retain that as additive evidence, but do not promote it to a universal family/order test.

**Profile morphology fails even for regular C truths:** re-open profile implementation/calibration before any admission architecture.

**All classes look alike:** profile is insufficient as a useful refusal component; do not freeze any profile-based gate.

**Need more information:** seed-to-seed morphology is too unstable for class interpretation.

## Function/Limit balance

This packet contains six valid C truths and six Limit truths by design. The 50/50 synthetic composition is a qualification design choice and **must not** be interpreted as biological prevalence.

Nominal/interior success, degraded-but-valid C behavior, and semantic failures are all reported together in the same merged result.

## Reproducibility

- Python 3.11 environment captured by workflow;
- exact truth table and seed list frozen here;
- all 72 row artifacts preserved;
- no failed/unfavorable row removed;
- same-path fine/coarse relationship preserved;
- no scientific threshold introduced.

## APQ request

\`APQ-2 SUBSTANTIAL\`.

The plan must receive role-isolated adversarial review before execution because it will determine the division of labor between practical-identifiability and semantic refusal gates in the future Bio Chi admission architecture.
