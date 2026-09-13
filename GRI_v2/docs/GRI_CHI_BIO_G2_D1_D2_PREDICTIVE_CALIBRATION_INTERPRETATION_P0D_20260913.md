# GRI Chi_bio G2 D1-versus-D2 predictive calibration interpretation

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome model-complexity attack  
**Artifact:** GitHub Actions run #622, `gri-chi-bio-g2-model-comparison-calibration`  
**Artifact digest:** `sha256:8164660ed4d1db428768170ea50e5a947cea5cb6f4d01ee73b599017680b1e18`  
**Architecture tested:** 5 PBS + 5 CTX transitions, shared synthetic pre-treatment origin  
**Real molecular data opened:** NO  
**Chi_bio:** `NOT_ADMITTED`

## 1. Question

The first interaction calibration showed that the treatment-dependent D2 model can be formally full rank while remaining highly noise-sensitive.

The next pre-outcome question was therefore:

> Under the exact 10-transition short-term architecture, can leave-one-transition predictive behavior distinguish a parsimonious shared operator from a true treatment-dependent operator strongly enough to justify making D2 the first empirical model?

The compared models were:

```text
D1: x_next = T x + B u + c
D2: x_next = T0 x + u DeltaT x + B u + c
```

D1 cannot represent treatment-induced operator reorganization. D2 can, but spends substantially more degrees of freedom.

## 2. Mechanical result

Both D1 and D2 were leave-one-transition identifiable in all calibration replicates at both `r=2` and `r=3`.

Therefore the comparison is not being driven by formal rank refusal.

## 3. Shared-operator truth

When the true control and treated operators were identical, any preference for D2 is overfitting.

At synthetic noise `0.01`:

```text
r=2:
  D1 median LOTO relative error = 0.0419
  D2 median LOTO relative error = 0.0669
  D2 lower-error fraction       = 0.024

r=3:
  D1 median LOTO relative error = 0.0541
  D2 median LOTO relative error = 0.2282
  D2 lower-error fraction       = 0.012
```

At noise `0.05`, D2 remained worse, especially at `r=3`.

This confirms the expected complexity penalty in the tiny architecture.

## 4. True operator-reorganization truth

More importantly, D1 often still predicted omitted transitions better once noise was added **even when D2 was the true generating family**.

At synthetic noise `0.01`:

### Reorganized stable truth

```text
r=2:
  D1 median LOTO error = 0.0433
  D2 median LOTO error = 0.0526
  D2 lower-error fraction = 0.280

r=3:
  D1 median LOTO error = 0.0553
  D2 median LOTO error = 0.1818
  D2 lower-error fraction = 0.020
```

### Reorganized above-unit-circle truth

```text
r=2:
  D1 median LOTO error = 0.0389
  D2 median LOTO error = 0.0505
  D2 lower-error fraction = 0.208

r=3:
  D1 median LOTO error = 0.0479
  D2 median LOTO error = 0.1687
  D2 lower-error fraction = 0.008
```

### Reorganized non-normal stable truth

```text
r=2 D2 lower-error fraction = 0.140
r=3 D2 lower-error fraction = 0.092
```

At zero noise, D2 correctly won every true-reorganization fixture because it matched the exact generating family. The reversal after adding even the smallest synthetic stress coordinate is therefore a bias-variance/identifiability effect rather than an implementation failure.

## 5. Consequence for the short-term SCC25 source

The 5+5-transition architecture does **not** earn D2 as the first empirical model merely because D2 expresses the more interesting scientific question.

The synthetic result supports the stricter sequence:

```text
SHORT-TERM G2 STAGE 0:
  D1 shared-T controlled operator
  purpose = establish whether a coherent low-order temporal operator is supportable at all

SHORT-TERM G2 STAGE 1:
  D2 treatment-interaction operator
  purpose = exploratory/secondary operator-reorganization test
  only after D1 adequacy and a prospectively frozen complexity-escalation rule
```

D2 should not be promoted because it produces a treatment-specific spectral radius. In the exact short-term sample architecture, its extra freedom can degrade out-of-transition prediction even when operator reorganization is truly present.

## 6. What this does not establish

The synthetic noise coordinates are not calibrated to GSE114446 measurement error.

Therefore this calibration does **not** prove that D2 is unusable on the real source. It establishes a more limited and important point:

```text
with 10 transitions, D2 needs evidence of exceptionally stable state measurement / estimation before its extra operator degrees of freedom can be trusted.
```

The next safe question is whether the **chronic 10+10-transition SCC25 architecture** materially changes that conclusion.

## 7. Revised D recommendation

The pre-outcome recommendation is revised to:

```text
D1 = primary short-term G2 feasibility model
D2 = operator-reorganization escalation, not first-line short-term primary
D3 = stress sensitivity only
```

For the chronic source, D2 remains open pending matched 10+10-transition synthetic calibration.

This is a recommendation, not an empirical freeze.
