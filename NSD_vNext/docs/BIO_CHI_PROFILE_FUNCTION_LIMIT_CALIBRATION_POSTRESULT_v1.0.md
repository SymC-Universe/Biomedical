# Bio Chi Profile Function/Limit Calibration Postresult v1.0

**Status:** COMPLETE P0-Q FUNCTION/LIMIT CALIBRATION  
**Date:** 28 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Frozen plan:** `NSD_vNext/docs/BIO_CHI_PROFILE_FUNCTION_LIMIT_CALIBRATION_PLAN_v0.2.md`  
**Freeze:** `NSD_vNext/docs/BIO_CHI_PROFILE_FUNCTION_LIMIT_CALIBRATION_FREEZE_v1.0.md`  
**Workflow:** `NSD Profile Function Limit Calibration`  
**Run:** `36498024951`  
**Head commit:** `8261cc6ed282a20aa4b7854c465a0de6e065a0bc`  
**Complete artifact:** `11004679194`  
**Artifact digest:** `sha256:07e87df10b3994c28d4740c43dde2ed7f82924545b92d31e56fc2c0d71acab81`  
**Merged output:** 72 frozen rows and 36 exact fine/coarse same-path pairs

## Result

The frozen experiment completed without scientific retuning. Both mechanical preflights passed, all 72 full cases completed successfully, and the merge produced the prospectively specified 72-row / 36-pair output.

The primary frozen outcome is **A, practical-identifiability / semantic orthogonality**, with **B, additive semantic sensitivity**, also present.

Profile likelihood is useful for determining whether a local chi estimate is well or weakly determined **inside the imposed C1Q-RS likelihood family**. It is not sufficient to establish that the C family is the correct scientific representation.

Some semantically invalid Limit truths produced compact, regular, sampling-stable C profiles. Conversely, a semantically valid near-critical C truth produced boundary-attracted and nonregular profile behavior in a subset of realizations. Therefore neither compactness nor nonregularity can be converted into a universal semantic C-membership rule.

## Frozen Function Map behavior

| Truth | Role | Hessian computed | Raw-boundary fits | Profile-edge minima | Median fine/coarse fitted-chi drift | Median absolute chi error |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| C0 | nominal regular interior | 6/6 | 0/6 | 0/6 | 0.0050 | 0.0118 |
| C1 | nominal nonzero-g interior | 6/6 | 0/6 | 0/6 | 0.0120 | 0.0328 |
| C2 | weak-observation / low-information | 6/6 | 0/6 | 0/6 | 0.0660 | 0.0744 |
| C3 | near-critical valid C | 3/6 | 2/6 | 2/6 | 0.0282 | 0.0533 |
| C4 | near-g-boundary valid C | 6/6 | 0/6 | 0/6 | 0.0030 | 0.0088 |
| C5 | high-frequency estimator-edge valid C | 6/6 | 0/6 | 0/6 | 0.0132 | 0.0074 |

C0 and C1 provide the expected nominal-function reference: all profiles were interior and all Hessians were regular.

C2 remained semantically valid and mechanically regular, but its recovery error and paired-rate drift were larger than the nominal cases. This preserves the distinction between a mathematically regular profile and strong finite-sample information.

C3 is the strongest Function-side warning against semantic overreach. It is a valid C generator, yet two of six fits landed on a raw boundary, two of six profile minima reached the high-chi grid edge, and only three of six Hessians were admissible. Nonregular uncertainty geometry therefore cannot be interpreted as evidence that the generating system is outside C.

C4 and C5 show the complementary fact. Boundary-adjacent or estimator-edge valid C truths can still retain compact local chi profiles. Nuisance-boundary contact can be substantial even while the chi profile itself remains regular.

## Frozen Limit Map behavior

| Truth | Semantic role | Hessian computed | Raw-boundary fits | Profile-edge minima | Median fine/coarse fitted-chi drift | Median fitted chi |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| L0 | positive D outside C | 6/6 | 0/6 | 0/6 | 0.0047 | 0.3021 |
| L1 | negative D outside C | 1/6 | 1/6 | 0/6 | 0.0042 | 0.3180 |
| L2 | positive S outside D | 0/6 | 5/6 | 0/6 | 0.0313 | 0.2786 |
| L3 | negative S outside D | 0/6 | 4/6 | 0/6 | 0.0048 | 0.2868 |
| L4 | colored-memory control | 6/6 | 0/6 | 0/6 | 0.0027 | 0.2824 |
| L5 | genuine separated two-mode control | 3/6 | 3/6 | 0/6 | 0.0293 | 0.4676 |

L0 and L4 are the decisive semantic-orthogonality controls. Both are outside the licensed one-mode C interpretation, yet all six realizations in each class had regular Hessians, no raw-boundary fit, no profile-edge minimum, and small fine/coarse fitted-chi drift. A stable and compact imposed C coordinate can therefore exist even when the scientific representation is wrong.

L1-L3 and L5 show additive semantic sensitivity. Several invalid classes often produced boundary or Hessian-refusal behavior, so profile geometry can contribute useful warning information. That contribution is class dependent and cannot replace explicit family, model-order, memory/closure, stationarity, or representation checks.

## Joint interpretation

The result separates two questions that must remain distinct:

1. **Practical identifiability:** is a candidate local chi numerically determined within the imposed C model?
2. **Semantic admissibility:** is C the scientifically licensed representation of the observed dynamics?

Profile likelihood addresses the first question. It does not answer the second.

The current Bio Chi admission architecture must therefore remain conjunctive. A future local chi can be considered only after independent model-family, order/multiplicity, memory/closure, stationarity/sampling, and uncertainty checks are satisfied. A compact profile can support local-coordinate precision after those gates, but cannot self-license the coordinate.

This result also strengthens the program-wide chi/Chi distinction. A well-determined local scalar can coexist with a scientifically inadequate representation, so broader modal and system architecture remains necessary even when local chi is numerically precise.

## Failure and outlier disposition

The most conspicuous Function-side failure, C3 near-critical nonregularity, is retained as a boundary-region limitation and not treated as representative prevalence. The most important Limit-side deceptive successes, L0 and L4, are retained because they falsify any universal rule equating profile regularity with semantic validity. Their designed frequency in this packet is not a biological prevalence estimate.

No row was removed for being inconvenient, and no cutoff was chosen from the observed morphology.

## Claim and threshold impact

No scientific threshold was frozen, revised, or retired.

This result does **not**:

- establish C-family membership from profile shape;
- promote C1Q-RS beyond qualification use;
- establish biological prevalence;
- license real-EEG local chi;
- replace C/D/S semantics, model-order, memory/closure, or stationarity gates;
- license a whole-system chi scalar.

## Next action

The next N-B1 step is to construct and adversarially qualify a prospective **integrated admission/refusal architecture** in which profile likelihood is restricted to practical-identifiability evidence and semantic family/order/closure checks remain independent.

In parallel, N-B2/N-B3 work should proceed without waiting for N-B1 scalar admission. The existing coupled-system known-truth result already establishes that local damping, embedded spectrum, transient gain, and recovery are non-interchangeable. The next safe system-side step is a novelty-first representation-sufficiency map that tests which combinations of modal and system descriptors preserve or lose perturbation/recovery information across a broader coupled known-truth region.

Neither next lane opens real EEG local chi.
