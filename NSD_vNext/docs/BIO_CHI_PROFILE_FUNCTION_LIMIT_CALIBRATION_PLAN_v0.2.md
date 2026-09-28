# Bio Chi Profile Function/Limit Calibration Plan v0.2

**Status:** APQ-2 QUALIFIED CANDIDATE  
**Date:** 28 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle stage:** Stage 3, P0-Q profile/refusal qualification  
**Parent method result:** \`BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_POSTRESULT_v1.0.md\`  
**APQ ledger:** \`BIO_CHI_PROFILE_FUNCTION_LIMIT_APQ_LEDGER_v0.1.md\`

## Scientific target

Profile likelihood is qualified as the primary single-record **practical-identifiability** diagnostic for local chi. This experiment calibrates its proper scope across a balanced Function/Limit known-truth map.

The central question is not whether profile likelihood can become a universal semantic gate. It is:

> Which uncertainty/refusal questions can profile geometry answer reliably, and which semantic failures remain invisible even when the imposed C1Q likelihood is locally well determined?

A compact profile can establish only local determination within the imposed likelihood family. It cannot by itself establish that the C family is the correct scientific representation.

## Claim ceiling

P0-Q known-truth Function/Limit calibration only.

No result may:

- define an admission cutoff;
- infer biological prevalence;
- promote C1Q-RS to production;
- establish C-family membership from profile/fit quality;
- license real-EEG local chi;
- replace C/D/S family semantics, model-order, or closure/memory gates.

## Frozen Function Map truths

All paths are generated at 256 Hz for 60 s and exactly decimated by factor 2 for paired 128 Hz records.

| ID | GOM coverage role | A | natural f Hz | chi | g | Purpose |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| C0 | NOMINAL_FUNCTION | 0.80 | 10.0 | 0.30 | 0.00 | regular interior |
| C1 | NOMINAL_FUNCTION | 0.65 | 12.0 | 0.45 | 0.55 | regular nonzero-g interior |
| C2 | PERTURBED_FUNCTION | 0.28 | 19.0 | 0.50 | -0.72 | weak-observation / low-latent-information |
| C3 | BOUNDARY_OR_TRANSITION | 0.80 | 10.0 | 0.93 | 0.20 | near-critical valid C |
| C4 | BOUNDARY_OR_TRANSITION | 0.80 | 10.0 | 0.30 | 0.95 | near-g-boundary valid C |
| C5 | BOUNDARY_OR_TRANSITION | 0.70 | 42.0 | 0.25 | 0.20 | high-frequency estimator-edge valid C |

C3-C5 remain semantically valid C truths regardless of whether their profiles are flat, boundary-directed, or otherwise nonregular.

## Frozen Limit Map truths

Canonical second-order C/D/S geometry uses A=0.8, natural frequency 10 Hz, zeta=0.30 at 256 Hz.

- **L0 D_NOT_C_POS:** positive D\C midpoint between continuous-C and exact-discrete-D nuisance boundaries.
- **L1 D_NOT_C_NEG:** negative D\C counterpart.
- **L2 S_NOT_D_POS:** positive S\D midpoint between exact-D and scalar-positive boundary.
- **L3 S_NOT_D_NEG:** negative S\D counterpart.
- **L4 COLORED_MEMORY:** established phi=0.7 colored-process control on the qualified 10 Hz / zeta=0.30 base oscillator.
- **L5 GENUINE_TWO_MODE:** established separated 10 Hz / 20 Hz two-mode control.

These use the existing qualified repository generators. For L0-L5, fitted C1Q-RS chi is an imposed candidate coordinate only. No generating continuous-C true-chi error is reported.

## Frozen seeds and sampling

Seeds:

\`301103, 509203, 811223\`

Sampling:

- 60 s;
- 256 Hz fine path;
- exact factor-2 same-path 128 Hz record;
- 12 truth classes x 3 seeds x 2 rates = 72 profile/Hessian cases.

The 50/50 Function/Limit composition is a qualification design choice, not biological prevalence.

## Frozen profile method

Use unchanged:

- C1Q-RS likelihood, bounds, parameterization, multistart search, and budgets;
- qualified physical-coordinate profile implementation;
- 61-point chi grid over [0.05, 0.98] plus exact fitted chi;
- exact generating chi inserted for C0-C5 only;
- qualified nuisance multistart recipe;
- local physical-coordinate Hessian as regular-only secondary diagnostic.

No bootstrap is run.

## Mechanical preflight

- C0, seed 301103, fine;
- L4, seed 301103, coarse.

Preflight is mechanical only. It checks generator execution, exact decimation, C1Q-RS fitting, fitted-chi profile/global-NLL reproduction, full serialization, Hessian compute-or-refusal, and semantic-label schema.

Scientific profile shape cannot stop or retune the full plan.

## Frozen row outputs

Every row preserves:

- truth ID, generator identity, Function/Limit role, seed, rate;
- semantic C-membership truth YES/NO;
- whether a generating continuous-C chi is scientifically defined;
- C1Q-RS fitted A, natural frequency, chi, g, NLL, BIC, raw parameters, winner origin;
- fitted raw-box edge distance and g-boundary distance;
- Hessian status, eigenvalues/condition, local chi SE when valid;
- complete profile point set;
- profile nuisance optimum at every point;
- winning nuisance start at every point;
- count of profile points whose nuisance optimum touches the raw optimization box within 1e-6;
- fitted-chi/global-NLL reproduction;
- true-chi delta NLL for valid C truths only;
- number and grid locations of local minima;
- left/right edge delta NLL;
- full profile delta-NLL range;
- lowest-profile grid location;
- whether lowest point is a profile-grid edge;
- same-path fine/coarse fitted-chi drift.

For C0-C5 additionally preserve chi/g/natural-frequency recovery errors.

For L0-L5 all “true continuous-C chi recovery” fields are \`NOT_APPLICABLE\`.

## Descriptive morphology

The full profile points are the source of truth. Derived labels are secondary descriptive summaries only.

Permitted labels:

- interior minimum;
- low-chi edge minimum;
- high-chi edge minimum;
- multiple grid-local minima;
- Hessian regular;
- Hessian refused/non-positive-definite;
- nuisance-boundary contact present.

No hidden delta-NLL, width, or edge cutoff converts these labels into admission/refusal.

## Frozen scientific questions

1. Do nominal C cases generally show reproducible interior profile geometry?
2. How do weak-information, near-critical, g-boundary, and high-frequency valid C cases degrade while remaining semantically valid?
3. Can D\C or S\D truths produce compact/interior C profiles despite semantic incompatibility?
4. Can colored-memory or genuine multimode truths also look practically identifiable under the imposed one-mode C likelihood?
5. Which failures therefore require independent family/order/closure gates even when profile likelihood is well behaved?

## Outcome architecture

### A. Practical-identifiability / semantic-orthogonality result

Profiles distinguish well- versus weakly-determined estimates inside C, but some semantic Limit truths remain compact. Profile becomes a practical-identifiability gate only; independent family/order/closure gates remain mandatory.

### B. Additive semantic sensitivity

Some Limit classes systematically show nonregular profile geometry. Retain profile as additive evidence but not a universal semantic test.

### C. Profile method fails on nominal C

If nominal C profiles are not mechanically reproducible or are generally nonregular across seeds/rates, re-open profile calibration before further admission design.

### D. No useful morphology structure

If Function and Limit classes show no interpretable profile structure, do not freeze a profile-based refusal component.

### E. Need more information

If seed/rate variability prevents stable class-level description, expand known-truth replication prospectively rather than select a threshold.

## Reproducibility

Each of 72 cases is a separate workflow job. Existing profile search/grid/budgets are unchanged. Runtime failures may receive only mechanical workflow repair; no scientific simplification or reduced grid is allowed after outcomes.

All case artifacts are merged only after every frozen case has a valid terminal artifact.

## APQ closure

Two role-isolated passes completed. All MATERIAL objections are resolved. The plan is eligible for prospective freeze.
