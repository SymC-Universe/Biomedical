# GRI Chi_bio G2 treatment-interaction synthetic calibration interpretation

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome identifiability / numerical-stability attack  
**Calibration artifact:** GitHub Actions run #617, `gri-chi-bio-g2-interaction-calibration`  
**Artifact digest:** `sha256:363c85d9c95d56c6d6d3ade515c3e4e5f34976d6f8f56ddd852be73022a77127`  
**Real SCC25/TCGA molecular files opened by calibration:** NO  
**Chi_bio:** `NOT_ADMITTED`

## 1. Mechanical result

After correcting a regression test that incorrectly equated full rank with machine-exact recovery, the full CI suite passed and the 500-replicate-per-cell treatment-interaction calibration completed successfully.

The calibration used only synthetic known-truth systems at:

```text
rank: r=2, r=3
truth classes:
  stable treated operator
  near-unit-circle treated operator (rho=0.98)
  above-unit-circle treated operator (rho=1.05)
  non-normal but asymptotically stable treated operator
synthetic state-noise coordinates:
  0, 0.01, 0.05, 0.10
```

The noise values are synthetic stress coordinates. They are not estimates of SCC25 measurement noise and must not be used as empirical thresholds.

## 2. First important result: formal full rank was not protective

Every calibration cell reported:

```text
full_rank_fit_fraction = 1.0
```

Yet the designs could still be severely ill-conditioned and noise-sensitive.

Even at zero injected noise, the median design condition number was already approximately:

```text
r=2: 8e2 to 1.5e3 across truth classes
r=3: 2.5e4 to 6.4e4 across truth classes
```

The non-normal `r=3` zero-noise fixture reached a maximum condition number above `1e13`.

Therefore:

```text
full column rank != adequate empirical identifiability
```

This directly strengthens the need for conditioning and perturbation/refit stability gates before real G2 interpretation.

## 3. Zero-noise known truth

When no measurement noise was added, both ranks preserved the mathematical unit-circle side in all synthetic classes:

```text
treated_unit_circle_side_accuracy = 1.0
```

The independent random-design unit tests also verify exact algebraic recovery of the implemented treatment-interaction model.

The small nonzero spectral perturbations seen in a few zero-noise sequential `r=3` fits were numerical consequences of extreme conditioning, not a model-code error. They are preserved in the artifact rather than erased by an arbitrary test tolerance.

## 4. Noise-stress result

The important result is how quickly the tiny treatment-interaction design degraded under even the smallest nonzero synthetic stress coordinate.

At synthetic noise `0.01`:

| Truth class | r=2 treated-side accuracy | r=3 treated-side accuracy |
| --- | ---: | ---: |
| stable (`rho=0.90`) | 0.866 | 0.570 |
| near boundary (`rho=0.98`) | 0.802 | 0.570 |
| above boundary (`rho=1.05`) | 0.364 | 0.524 |
| non-normal stable (`rho=0.90`) | 0.796 | 0.678 |

At the same stress level, median absolute treated-`rho` error was approximately:

```text
r=2: 0.077 to 0.122 across classes
r=3: 0.059 to 0.202 across classes
```

The non-normal warning itself was also difficult to recover reliably once noise was introduced.

These numbers are **not** estimates of expected SCC25 accuracy. Their role is structural: with only 10 transitions and a treatment-interaction design containing `2r+2` predictor columns, apparently modest state perturbations can produce large spectral uncertainty.

## 5. Scientific consequence for operator-model choice

Before this calibration, the leading operator recommendation was:

```text
D2 treatment-interaction primary
D1 shared-T additive-input restricted/null
D3 separate-arm stress sensitivity
```

The calibration weakens that recommendation.

D2 remains the minimal linear model that can represent treatment-associated operator reorganization in one frozen state basis. But the synthetic evidence shows that its short-term SCC25 architecture is too parameter-hungry to treat formal rank as sufficient qualification, especially for `r=3`.

A safer staged design is now:

```text
G2 feasibility stage:
  D1 shared-T + additive treatment input
  -> ask whether a coherent low-order operator is identifiable at all

operator-reorganization escalation:
  D2 treatment-interaction
  -> only if predeclared stability/conditioning/model-comparison criteria support the added degrees of freedom

D3 separate-arm operators:
  -> stress sensitivity only, not default primary
```

This changes the recommended **sequence**, not the approved A3 rank architecture and not the definition of G2 itself.

## 6. Why D1 is not a substitute for treatment-specific G2

D1 has one shared `T`:

```text
x_next = T x + B u + c
```

Therefore D1 cannot establish that cetuximab changes `rho(T)`.

Its proper role is narrower and important:

> determine whether this tiny transcriptomic trajectory supports a coherent low-order controlled transition model before spending scarce information on a treatment-dependent operator.

If D1 itself is unstable under A3/refit diagnostics, promoting to D2 would not solve the identifiability problem.

If D1 is stable and D2 adds reproducible predictive value without violating the frozen stability gates, then operator reorganization becomes a qualified secondary question.

## 7. New required safe test

The next pre-outcome synthetic task is therefore a **D1-versus-D2 leave-one-transition predictive calibration** under both shared-operator and known-reorganization truth.

Its purpose is not to pick a model from real SCC25 results. It is to determine whether, under the exact 5+5 transition architecture, a prospectively fixed model-escalation rule can distinguish:

```text
shared operator + treatment forcing
from
true treatment-dependent operator reorganization
```

before any real candidate trajectory is opened.

## 8. Claim ceiling

This calibration does not show that SCC25 G2 fails, because the synthetic noise coordinates are not calibrated to SCC25 measurement error. It does show that the short-term D2 design is intrinsically fragile enough that **full rank alone cannot license interpretation** and that the first empirical stage should earn operator complexity rather than assume it.
