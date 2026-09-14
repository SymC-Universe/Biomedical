# GRI Chi_bio G2 short-versus-chronic architecture scaling interpretation

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome identifiability / information-scaling attack  
**Artifact:** GitHub Actions run #625, `gri-chi-bio-g2-architecture-scaling-calibration`  
**Artifact digest:** `sha256:aaddf93006e778ffcafcf2179e6faa2a99c0217e7a7b0b009fb83c78a46c9718`  
**Architectures:** 5+5 versus 10+10 transitions  
**Real SCC25/TCGA molecular files opened by calibration:** NO  
**Chi_bio:** `NOT_ADMITTED`

## 1. Question

The short-term 5+5 transition calibration showed that the treatment-interaction model D2 pays a severe variance/conditioning penalty, especially at `r=3`.

The chronic SCC25 trajectory has approximately twice the transition count:

```text
short-term architecture: 5 PBS + 5 CTX = 10 transitions
chronic architecture:    10 PBS + 10 CTX = 20 transitions
```

This calibration asked whether the extra transition information materially changes the D1-versus-D2 predictive tradeoff before any real molecular trajectory is opened.

## 2. Mechanical result

The full workflow passed. The same synthetic generating families, ranks and noise coordinates were compared under both transition counts.

The synthetic noise levels remain stress coordinates only. They are not estimates of SCC25 assay noise and cannot be used as empirical thresholds.

## 3. Conditioning improves substantially with 10+10 transitions

At synthetic noise `0.01`, median leave-one-transition maximum condition numbers fell markedly when moving from 5+5 to 10+10 transitions.

Examples:

```text
r=2, shared truth:
  D2 short-term median max cond ~8.2e2
  D2 chronic median max cond    ~2.3e2

r=3, shared truth:
  D2 short-term median max cond ~8.6e3
  D2 chronic median max cond    ~5.5e2

r=3, reorganized stable:
  D2 short-term median max cond ~8.1e3
  D2 chronic median max cond    ~6.1e2
```

The extra transitions therefore reduce one major source of numerical fragility rather than merely increasing nominal sample count.

## 4. D2 becomes meaningfully competitive in the chronic architecture at the smallest nonzero stress coordinate

At synthetic noise `0.01`, the fraction of replicates in which D2 had lower leave-one-transition prediction error than D1 changed as follows.

### Reorganized stable truth

```text
r=2: short 0.280 -> chronic 0.692
r=3: short 0.020 -> chronic 0.532
```

### Reorganized above-unit-circle truth

```text
r=2: short 0.208 -> chronic 0.696
r=3: short 0.008 -> chronic 0.484
```

### Reorganized non-normal stable truth

```text
r=2: short 0.140 -> chronic 0.724
r=3: short 0.092 -> chronic 0.872
```

Under shared-operator truth, D2 remained correctly disfavored:

```text
r=2 chronic: D2 lower-error fraction 0.128
r=3 chronic: D2 lower-error fraction 0.052
```

Thus the 10+10 architecture contains materially more information for distinguishing operator reorganization from a shared controlled operator.

## 5. But the chronic architecture does not make D2 automatically safe

At the larger synthetic stress coordinate `0.05`, D2's advantage under true reorganization was weaker or scenario-dependent.

Examples:

```text
reorganized stable:
  r=2 D2 better fraction = 0.324
  r=3 D2 better fraction = 0.132

reorganized above-unit-circle:
  r=2 = 0.472
  r=3 = 0.272

reorganized non-normal:
  r=2 = 0.472
  r=3 = 0.732
```

Therefore doubling the transition count improves identifiability but does not erase the bias-variance problem. D2 still requires prospective stability/model-adequacy gates.

## 6. Scientific consequence: short-term and chronic sources should not be forced into identical model roles

The synthetic evidence supports a source-specific role split while preserving one G2 family:

```text
SHORT-TERM 5+5:
  D1 shared-T controlled operator = primary feasibility architecture
  D2 treatment-interaction        = secondary escalation only

CHRONIC 10+10:
  D1 shared-T controlled operator = restricted/null comparator
  D2 treatment-interaction        = viable primary operator-reorganization candidate,
                                    conditional on frozen conditioning/adequacy gates
```

This is not post hoc selection by real outcomes. The distinction is driven by the pre-outcome information geometry of the two source architectures.

## 7. A3 implication

The result also reinforces A3 rather than weakening it.

At `r=2`, chronic D2 often gains a clearer predictive advantage under reorganization truth. At `r=3`, the advantage is more variable except in the non-normal class. Therefore a real chronic operator-reorganization claim should still require the predeclared material conclusion to survive both ranks or return:

```text
REPRESENTATION_DEPENDENT_NO_TRANSFER
```

No rank should be promoted because it yields the more appealing spectral result.

## 8. Recommended D architecture after the full synthetic sequence

The pre-outcome recommendation is now:

### D-short

```text
primary: D1 shared T + treatment input
purpose: low-order temporal feasibility
D2: escalation only after D1 adequacy and frozen complexity gate
```

### D-chronic

```text
primary candidate: D2 treatment-interaction
restricted/null comparator: D1 shared T + treatment input
stress sensitivity: D3 separate-arm operators only if identifiable
```

For chronic D2, promotion over D1 must be based on a frozen adequacy/model-comparison rule, not merely on a treatment-specific `rho(T)` existing.

## 9. What is still missing before empirical execution

The synthetic scaling study does not supply an empirical cutoff. The following remain to be frozen prospectively:

- RNA transformation/normalization;
- gene feature universe;
- day-0 convention for the short-term source;
- conditioning refusal rule;
- model-adequacy / D1-to-D2 escalation rule;
- non-iid uncertainty/sensitivity rule;
- daily-versus-weekly transport rule;
- exact A3 material-conclusion schema.

## 10. Claim ceiling

The chronic 10+10 architecture is **more capable of supporting a treatment-dependent low-order operator than the short-term 5+5 architecture in the synthetic information attack**. That is not evidence that the real SCC25 chronic trajectory has a treatment-induced stability transition, and it does not admit a biological `Chi_bio` or biological unit-circle boundary.
