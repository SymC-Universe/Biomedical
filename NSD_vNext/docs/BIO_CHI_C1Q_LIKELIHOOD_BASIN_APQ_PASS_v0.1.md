# Bio Chi C1Q Likelihood-Basin APQ-1 Adversarial Pass v0.1

**Plan reviewed:** \`BIO_CHI_C1Q_LIKELIHOOD_BASIN_PLAN_v0.1.md\`  
**APQ level:** APQ-1 EXPLORATORY  
**Review status:** role-isolated same-cognition adversarial pass; not independent review

## Strongest feature

The plan reuses immutable source rows and evaluates the existing likelihood directly, so it can separate a search defect from the realized objective surface without introducing a new estimator or new biological evidence.

## Strongest assumption

The population generating coordinates remain a meaningful reference after finite-realization standardization. They need not be the finite-sample MLE, so lower selected-fit NLL than truth is not itself a defect. The plan must interpret that difference as finite-sample objective geometry rather than "truth losing."

## Most likely failure mode

A single truth-seeded L-BFGS-B run may remain in a local truth-near basin and fail to reveal a continuous path to the boundary branch. That would establish multimodality but not fully characterize the likelihood topology.

## Most dangerous hidden dependency

The diagnostic imports the same C1Q likelihood implementation used to generate the original result. It can diagnose search versus objective geometry inside that implementation, but it cannot independently validate the likelihood formulation.

## Competing explanation

Large parameter displacement with a small NLL gap could arise from practical nonidentifiability rather than a pathological optimizer or a scientifically meaningful second regime.

## Circularity / leakage / provenance concern

The boundary-collapse cells are selected after viewing the Function Map. This is appropriate for P0-Q root-cause work but forbids confirmatory or prevalence language. Including all rows within the eight cells reduces cherry-picking of only the most extreme realizations.

## Missing control

The source-artifact NLL reproduction check is essential. Without it, a regenerated path or software mismatch could masquerade as likelihood geometry.

## Cheaper discriminating test

No cheaper test preserves the exact selected solution and known truth while separating search failure from objective geometry. Numerical gradients or Hessians should wait until the basin comparison shows they are needed.

## Refusal condition

Refuse scientific interpretation if source NLL cannot be reproduced, if truth raw coordinates fall outside the declared model domain, or if the regenerated realization does not match the frozen source construction.

## Objection classification and disposition

- **R1 MATERIAL:** truth-coordinate NLL must not be interpreted as the expected finite-sample optimum.  
  **Disposition:** \`ACCEPTED_MODIFIED\`. The plan now explicitly treats truth as a population reference, not the finite-sample MLE.
- **R2 MATERIAL:** post-hoc cell selection could inflate claims.  
  **Disposition:** \`DEFERRED_CLAIM_LIMITED\`. P0-Q root-cause only; all 48 rows within the eight identified cells are retained.
- **R3 MATERIAL:** source reproduction must be verified.  
  **Disposition:** \`ACCEPTED_TEST_ADDED\`. Frozen mechanical NLL reproduction gate added.
- **R4 MINOR:** one truth-seeded local start does not map the full surface.  
  **Disposition:** \`DEFERRED_CLAIM_LIMITED\`. The experiment distinguishes immediate next routes; Hessian/profile mapping follows only if scientifically necessary.

No BLOCKER remains. No unresolved MATERIAL objection remains.
