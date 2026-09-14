# GRI Chi_bio B3 matched-network holdout post-result audit

**Date:** 2026-09-13 / workflow completion 2026-09-14 UTC  
**Protocol authority:** `General_Cross_Project_Research_Protocol_v0.7.5_FINAL.md`  
**Holdout freeze:** `GRI_CHI_BIO_B3_MATCHED_NETWORK_HOLDOUT_20260913_V0_1`  
**Workflow run:** `34797932432`  
**Frozen execution head:** `e176d3b28e7a822afdcbc0035af7d5d249418fd6`  
**Artifact ID:** `10330711216`  
**Artifact SHA-256:** `02562ee9f1b47d497529b1e60a3c7df295cbf3b29d8983d1b50271cd189f4298`  
**Chi_bio:** `NOT_ADMITTED`

## 1. Firewall

This audit records the result of the prospectively frozen unseen-seed B3 matched-network holdout. It does not alter:

- the five unseen seeds;
- candidate dimensions `2,3,4,5`;
- the 0.15 primary noise level;
- the 0.30 diagnostic stress level;
- CollecTRI primary / DoRothEA ABC sensitivity roles;
- ULM scoring;
- the 45-degree latent-geometry criterion;
- the 10% spectral-radius recovery criterion;
- predictive-baseline requirements;
- conditioning rules;
- the cross-network requirement;
- the smallest-fully-passing-dimension selection rule.

The qualification job passed before the holdout job executed. Real SCC25/TCGA expression remained closed throughout. No empirical TF activity, normalized G1, biological unity value, or Chi_bio value was computed.

## 2. Machine disposition

The immutable result is:

```text
status: REFUSE_B3_MATCHED_NETWORK_IDENTIFIABILITY
passing_dimensions: []
selected_smallest_fully_passing_dimension: null
promotion_effect: NONE_B3_IDENTIFIABILITY_REFUSED
```

This is a **scientific refusal**, not an execution failure.

The workflow step is red because the runner intentionally returns a nonzero refusal code when no frozen candidate dimension passes. The result artifact was still uploaded successfully as designed.

## 3. Pass-count overview at the primary 0.15-noise gate

Each network/dimension combination had five unseen seeds.

```text
Dimension   CollecTRI passes   DoRothEA ABC passes
2           1 / 5              1 / 5
3           0 / 5              0 / 5
4           1 / 5              1 / 5
5           0 / 5              0 / 5
```

No dimension passed every seed in even one network, much less the required cross-network criterion.

## 4. What did work

The B3 scoring layer is not empty or numerically nonsensical.

Examples of fully passing individual trials include:

### d=2, seed 31007

```text
CollecTRI
median regulator r:                 0.8316
minimum canonical cosine:           0.9493
maximum principal angle:            18.32 degrees
relative rho error:                 1.38%
LOTO NRMSE:                          0.0663

DoRothEA ABC
median regulator r:                 0.9211
minimum canonical cosine:           0.9433
maximum principal angle:            19.38 degrees
relative rho error:                 0.28%
LOTO NRMSE:                          0.0773
```

### d=4 isolated passing trials

```text
CollecTRI, seed 31003:
minimum canonical cosine:           0.9788
maximum principal angle:            11.83 degrees
relative rho error:                 6.99%

DoRothEA ABC, seed 31007:
minimum canonical cosine:           0.9051
maximum principal angle:            25.17 degrees
relative rho error:                 6.46%
```

Therefore the refusal is not based on a universally nonfunctional inference layer. It is based on **lack of robust identifiability across unseen latent realizations**.

## 5. Why d=2 refused

### CollecTRI

Across the five seeds, only one passed all gates.

Failure categories included:

```text
activity median correlation:        1 / 5
activity fraction r>0.5:            1 / 5
latent geometry:                    2 / 5
spectral-radius recovery:           3 / 5
```

Representative failure, seed `31001`:

```text
median regulator r:                 0.6081
minimum canonical cosine:           0.2876
maximum principal angle:            73.29 degrees
relative rho error:                 34.07%
```

### DoRothEA ABC

Only one seed passed all gates.

```text
latent geometry failures:           2 / 5
spectral-radius recovery failures:  4 / 5
```

Seed `31001` similarly produced:

```text
minimum canonical cosine:           0.2954
maximum principal angle:            72.82 degrees
relative rho error:                 35.79%
```

The cross-network recurrence of the same poor unseen realization argues against treating this as a CollecTRI-specific accident.

## 6. Why d=3 refused

Neither network had a fully passing seed set.

The dominant problem was transition-spectrum recovery:

```text
CollecTRI rho-error failures:        5 / 5
DoRothEA ABC rho-error failures:     4 / 5
```

There was also one latent-geometry failure per network and one persistence-baseline failure per network.

The regulator-activity correlations were frequently strong, which demonstrates why activity recovery alone is insufficient to admit the state.

## 7. Why d=4 refused

Each network had only one fully passing seed.

CollecTRI failures included latent geometry, spectral-radius recovery and one persistence-baseline failure. DoRothEA ABC was especially limited by spectral-radius recovery, failing that criterion in four of five seeds.

This rules out selecting `d=4` merely because isolated realizations are excellent.

## 8. Why d=5 refused decisively

Every seed in both networks failed the latent-geometry gate.

```text
CollecTRI latent failures:           5 / 5
DoRothEA ABC latent failures:        5 / 5
```

Typical minimum canonical cosines were close to zero, with maximum principal angles commonly above 80 degrees.

The spectral criterion also failed in all five CollecTRI seeds and three of five DoRothEA seeds.

This confirms the nonpromotable pilot's warning: apparently reasonable transition summaries can coexist with collapse of one or more recovered latent directions.

## 9. Scientific interpretation

The current frozen construction:

```text
externally sourced signed regulons
-> ULM t-value activities
-> all eligible regulators retained
-> control-only PCA to d dimensions
-> compact transition/operator inference
```

is **not robustly identifiable under the matched-network known-truth family tested here**.

The refusal does not mean:

- CollecTRI is biologically invalid;
- DoRothEA is biologically invalid;
- ULM carries no regulatory information;
- SCC25 lacks low-dimensional regulatory structure;
- no externally grounded B3 representation can work;
- no effective transition coordinate can be estimated;
- G2 chronic results are invalid;
- a biological Chi does or does not exist.

It means the exact currently tested B3 low-dimensional construction has failed its prospectively frozen admission test.

## 10. Actions that are now forbidden as rescue

Do **not**:

- loosen the 45-degree latent criterion;
- loosen the 10% spectral-radius criterion;
- drop seed 31001, 31009, 31013 or any other unfavorable seed;
- select only the better-performing network;
- choose `d=2` because it looked best in the pilot;
- choose `d=4` because isolated seeds passed;
- replace the primary 0.15-noise condition with the 0.30 diagnostic condition;
- inspect real SCC25/TCGA TF activity and then design a better projection;
- force the primary CollecTRI representation onto the 249-TF cross-network intersection after this refusal merely because the intersection may be easier;
- open normalized empirical G1.

## 11. Lawful next branches

The current ULM-plus-control-PCA B3 construction is closed.

Further B3 investigation is scientifically permissible only as a **new, materially distinct pre-outcome representation candidate** with explicit lineage and multiplicity debt. It must be justified independently of real SCC25/TCGA candidate values and receive its own synthetic known-truth freeze before empirical use.

Examples worth investigating, not yet approved or frozen, include externally defined network/module coordinates that do not rely on recovering an arbitrary expression-derived PCA rotation from overlapping regulons. Any such route must explain why its coordinates have biological/operator semantics rather than merely improving synthetic scores.

The already predeclared G2 temporal comparator remains independently interpretable under its own completed freezes and empirical results. The predeclared G4 stochastic alternative also remains conceptually separate but requires its own state/identifiability work.

Normalized G1 additionally remains blocked by the separate unresolved restoration decomposition.

## 12. Current status after audit

```text
B3 source provenance:                     PASS
B3 identifier mapping:                    PASS
B3 ULM runtime:                           PASS
B3 nonpromotable pilot:                   COMPLETE
B3 unseen-seed matched-network holdout:   REFUSE
current ULM -> control-PCA B3 state:       CLOSED / NOT ADMITTED
real B3 SCC25 TF activity opening:         FORBIDDEN
real B3 TCGA TF activity opening:          FORBIDDEN
G1 restoration:                            UNRESOLVED SEPARATE GATE
normalized G1:                             CLOSED
Chi_bio:                                   NOT_ADMITTED
```
