# GRI Chi_bio chronic G2 bounded feature-gate robustness audit

**Date:** 2026-09-13  
**Primary frozen result:** `GRI_CHI_BIO_CHRONIC_G2_R1_A3_20260913_V1`  
**Robustness workflow run:** `34770059647`  
**Artifact:** `10321991562`  
**Artifact SHA-256:** `7a6a289d14ac7129cce979f340cb54fbbde7b3e767d411c243af76af1c7afed2`  
**Role:** post-result bounded diagnostic only  
**Chi_bio:** `NOT_ADMITTED`

## 1. Why this audit is allowed

Before chronic CTX dynamics were opened, the PBS-only design-input probe recorded two nonprimary feature thresholds in addition to the frozen primary threshold `1.0`:

```text
0.1 and 10.0 source-value units
```

Both used the same requirement of presence in at least `6/11` PBS states. They were explicitly ineligible to replace the primary threshold after inspection. The post-result audit therefore reports **both** as bounded feature-universe perturbations while leaving the primary result unchanged.

All other choices remain fixed: transform, PBS-only basis, r=2/r=3 A3 structure, 20 weekly transitions, D1/D2 models, numerical conditioning, baselines, 12/20 D2-win rule, sensitivity envelope, unit-circle semantics, and no biological Chi.

## 2. Broad gate: threshold 0.1

Retained genes:

```text
15,830
```

### r=2

```text
D1 LOTO NRMSE:             0.924464686717397
persistence baseline:      1.0730502970657534
arm-mean baseline:         0.94948807985357
D1 adequacy:               PASS
D1 rho envelope:           0.667116531933523 .. 0.9137923234268975
D1 unit-circle side:       BELOW
D1 non-normal warning:     ABSENT
D2 LOTO NRMSE:             0.9907690767464589
D2 wins over D1:           7/20
D2 support:                NOT_SUPPORTED
```

D1 improves on the arm-mean baseline by approximately `2.64%` and on persistence by `13.85%`.

### r=3

```text
D1 LOTO NRMSE:             0.9565506925458438
persistence baseline:      1.1723032016670458
arm-mean baseline:         0.976142731540388
D1 adequacy:               PASS
D1 rho envelope:           0.6482928271352838 .. 0.9602684169103565
D1 unit-circle side:       BELOW
D1 non-normal warning:     INDETERMINATE
D2 LOTO NRMSE:             1.24785760331142
D2 wins over D1:           4/20
D2 support:                NOT_SUPPORTED
```

D1 improves on the arm-mean baseline by approximately `2.01%` and on persistence by `18.40%`.

### Broad-gate disposition

The complete primary **core** reproduces:

```text
r=2 D1 adequacy:            PASS
r=3 D1 adequacy:            PASS
D1 unit-circle side:        BELOW at both ranks
D2 reorganization support:  NOT_SUPPORTED at both ranks
```

The pre-existing non-normal-warning rank dependence also reproduces. Machine overall disposition remains `REPRESENTATION_DEPENDENT_NO_TRANSFER` for the same narrow reason as the primary result.

## 3. Stringent gate: threshold 10

Retained genes:

```text
12,865
```

### r=2

```text
D1 LOTO NRMSE:             0.8982294049900018
persistence baseline:      1.0732372634978213
arm-mean baseline:         0.9166563835850106
D1 adequacy:               PASS
D1 rho envelope:           0.7211025155051819 .. 0.884205996159414
D1 unit-circle side:       BELOW
D1 non-normal warning:     ABSENT
D2 LOTO NRMSE:             0.9808728140257125
D2 wins over D1:           7/20
D2 support:                NOT_SUPPORTED
```

D1 improves on the arm-mean baseline by approximately `2.01%` and on persistence by `16.31%`.

### r=3

```text
D1 LOTO NRMSE:             0.9580841499683717
persistence baseline:      1.1427047081662545
arm-mean baseline:         0.9398117721039323
D1 adequacy:               REFUSE
D1 rho envelope:           0.7493800419419584 .. 0.9576847420184863
D1 unit-circle side:       BELOW
D1 non-normal warning:     INDETERMINATE
D2 LOTO NRMSE:             1.2413017306263534
D2 wins over D1:           5/20
D2 support:                NOT_SUPPORTED
```

At `r=3`, D1 remains approximately `16.16%` better than persistence but is approximately `1.94%` **worse** than the stronger arm-specific mean-next-state baseline, so it correctly fails the frozen adequacy rule.

### Stringent-gate disposition

The stringent low-abundance pruning introduces a material rank dependence in D1 predictive adequacy:

```text
r=2: PASS
r=3: REFUSE
```

Therefore the primary predictive shared-operator result is **not fully robust to the complete predeclared feature-gate envelope**.

## 4. What remains robust across all three feature gates

Across thresholds `0.1`, `1.0`, and `10.0`:

1. D2 treatment-specific operator reorganization is `NOT_SUPPORTED` at both A3 ranks.
2. The complete D1 mathematical spectral-radius sensitivity envelope remains `BELOW` the discrete-time unit circle at both ranks.
3. r=2 D1 predictive adequacy remains `PASS`.
4. The r=3 transient/non-normal warning remains sensitivity dependent rather than a stable point-fit feature.

These are the strongest feature-universe-robust statements available from the R1/A3 chronic test.

## 5. What is not robust

The statement

```text
D1 predictive adequacy PASS at both r=2 and r=3
```

holds at the primary `1.0` gate and the broader `0.1` gate, but fails at the stringent `10.0` gate because r=3 no longer beats the arm-specific mean baseline.

This fragility cannot be repaired by selecting the favorable threshold. The primary result remains exactly as originally frozen, and the robustness audit remains a limitation on its generality.

## 6. Interpretation

The data provide no predictive support for a treatment-specific low-dimensional weekly operator under any of the three predeclared feature universes. A shared-operator description has modest positive predictive evidence at the primary and broad gates, but that evidence is sensitive to aggressive pruning of lower-abundance genes in the higher-dimensional A3 representation.

The consistent below-unit-circle mathematical classification is more robust than the predictive adequacy claim, but it remains a property of the fitted weekly operators and is **not** a biological `chi=1` result.

## 7. Closure of R1/A3 optimization lane

No additional feature-threshold search is licensed. The bounded feature-universe audit is complete.

The next scientific move is an **independent representation/functional lane**, specifically the already reserved R2/B3 regulatory-module and relational-functional program. That next lane must use its own prospective construction/admission rules and must not be tuned to rescue the R1/A3 result.
