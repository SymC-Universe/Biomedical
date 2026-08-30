# GRI v2 tool prediction and prospective-validation objective amendment

**STATUS: LOCKED PROGRAM-OBJECTIVE AMENDMENT BEFORE STAGE C1 BETA-VALUE BIOLOGICAL RESULTS**

Date: 2026-08-30

This amendment refines the tool-discovery objective without changing the already frozen Stage C1 v2 biological analysis and without retroactively changing the frozen F2 or F3 evaluation rules.

## 1. Primary objective

The primary development target is the **tool as an integrated predictive system**, not methodological novelty of any individual statistic, decomposition, coordinate, null, or mathematical ingredient.

The decisive question is:

> Does the completed tool make prospectively correct and scientifically useful predictions on held-out or independent data, with useful calibration and refusal behavior, compared with appropriate existing baselines?

Novelty may emerge at the level of the complete tool, workflow, decision architecture, or predictive capability. It is welcome but is not an optimization target by itself.

## 2. Priority order

Development priorities are now explicitly ordered as:

1. **prospective predictive utility**;
2. **generalization to held-out and independent data**;
3. **calibration, uncertainty, and refusal / abstention quality**;
4. **traceability and scientific interpretability**;
5. **robustness to construction, confounding, technical, semantic, and alignment failures**;
6. **component-level novelty only if it arises naturally and survives comparison**.

A familiar mathematical component is retained if it materially improves the tool's prospective predictive performance, calibration, robustness, refusal behavior, or interpretability.

A mathematically novel component is narrowed or removed if it does not improve a prospectively defined scientific task.

## 3. Relationship to F3 baseline competition

The frozen F3 plan remains unchanged for provenance.

F3 is an **engineering and redundancy audit**, not the final novelty gate. It asks what each component adds beyond CKA, principal angles, ordinary prediction, CCA-like association, AJIVE, MOFA2, DIVAS, and naive semantic correlation.

F3 may show that individual ingredients are already available in established methods. That does not by itself defeat the tool.

Likewise, F3 may show a component-level distinction. That does not establish a useful tool.

The relevant downstream question is whether the integrated system improves prediction, prediction reliability, selective prediction, or prospective reproducibility.

## 4. Tool-level prediction must be tested in more than one sense

The tool will be evaluated on three distinct predictive functions before any clinical promotion.

### P1 - direct cross-layer prediction

Given one measured molecular layer and allowed covariates, predict prospectively frozen target-layer quantities in held-out patients.

Candidate targets may include target-layer modal scores, fixed module-level summaries, or another independently defined target representation. Target definitions must be frozen before held-out values are inspected.

All preprocessing, dimensionality reduction, feature selection, and model fitting must occur inside the training partition. Held-out target data may be used only for final scoring.

### P2 - prospective replication prediction

Use the discovery partition to predict whether a cross-layer relationship, module correspondence, or integration-readiness state will reproduce in an untouched holdout partition.

This asks whether the tool can predict **which apparent biological relationships will survive replication**, not merely describe the data on which they were discovered.

### P3 - selective prediction / refusal

The tool's refusal or integration-readiness state must itself be tested prospectively.

A useful auditor should not merely predict. It should identify situations in which prediction or shared interpretation is unreliable.

Therefore evaluate whether the frozen accept / caution / refuse states prospectively stratify:

- held-out prediction error;
- held-out predictive R2 or task-appropriate discrimination;
- calibration error;
- replication probability;
- robustness under technical or confounding attacks.

The tool should be compared with an always-predict baseline and with simpler uncertainty or quality-control baselines.

Coverage-risk or equivalent selective-prediction analysis should be used where appropriate. Acceptance thresholds may not be chosen after inspecting holdout performance.

## 5. Prospective-data hierarchy

Evidence strength is ordered as:

1. synthetic known-truth challenge;
2. internal strict held-out prediction with leakage-proof preprocessing;
3. untouched internal replication partition;
4. external independent cohort with the architecture and parameters frozen;
5. genuinely future / newly arriving data when feasible.

Internal cross-validation is useful engineering evidence but is not described as external prospective validation.

## 6. External validation is mandatory for tool promotion

A promoted biomedical tool must eventually be frozen and tested on data that were not used to choose its architecture, thresholds, feature definitions, or interpretation.

No TCGA-only result is sufficient for a strong general-purpose biomedical prediction claim.

If an external cohort requires a reduced common-feature representation, that mapping must be frozen from source compatibility and biological measurement constraints rather than chosen because it improves external performance.

## 7. Clinical outcomes remain a separate gate

Survival, treatment response, recurrence, toxicity, or other clinical endpoints may become predictive targets only under a separately frozen outcome protocol.

They must not be used now to choose the architecture of the cross-omic tool.

This prevents the tool from quietly becoming an outcome-optimized model before its basic cross-layer behavior is established.

## 8. Component-retention rule

For every candidate component, ask:

> Does removing this component worsen prospective prediction, calibration, selective prediction, replication forecasting, robustness, or scientifically useful traceability?

If no, the component may be removed even if mathematically interesting.

If yes, it may be retained even if the underlying mathematics is established rather than novel.

This rule applies to scalar summaries, modal quantities, conglomeration measures, autonomy statistics, null layers, technical tracks, and refusal logic.

## 9. Tool-level novelty rule

No component-level novelty claim is required for program success.

If novelty is eventually claimed, the preferred claim is at the level actually demonstrated by evidence, for example:

- a prospectively validated integrated prediction-and-refusal workflow;
- improved prediction of cross-layer replicability;
- improved selective prediction under confounding or technical failure;
- a useful combination of modal, scalar, and conglomeration evidence that generalizes better than appropriate baselines.

Novelty must never be inferred merely from using a new name for an existing statistic.

## 10. Novelty as a diagnostic lens

Novelty will still be checked continuously at the component level, but as a **diagnostic and lead-generation process rather than a development objective**.

For each mathematical object, estimator, decomposition, null, decision rule, and predictive layer, ask two separate questions:

1. **Prior-art / equivalence question:** is the component already known, mathematically equivalent to an established quantity, or functionally supplied by an existing method?
2. **Difference / lead question:** if a real difference remains, does it reveal a limitation of the established method, a limitation of the candidate, a new falsification test, a useful scientific interpretation, or a prospectively testable predictive advantage?

Possible outcomes include:

- **REDUNDANT:** established method supplies the same information adequately; simplify or reuse the established method;
- **COMPLEMENTARY:** the component is not novel by itself but contributes useful information when combined with other evidence;
- **LIMITATION_FOUND:** comparison exposes a failure mode that should become a guardrail or refusal condition;
- **LEAD_FOUND:** a nontrivial difference suggests a new prospectively testable capability;
- **NOVEL_CANDIDATE:** a potentially new object or behavior appears, but receives no promotion until its utility and prior art are independently established.

This novelty scan must not alter already frozen test thresholds or rescue failed prospective results.

A novelty lead is therefore treated as a **new question to test**, not as evidence that the tool is valuable.

## 11. F4 meaning after this amendment

F4 remains GO / NARROW / STOP, but it is an **engineering investment decision**, not a declaration of methodological novelty.

- **GO**: the architecture is worth taking into prospectively frozen predictive testing.
- **NARROW**: retain only components justified for predictive testing.
- **STOP**: do not invest further in the standalone architecture.

A GO at F4 does not validate the tool. Tool promotion requires the predictive and external-validation sequence above.

## 12. Stage C1 relationship

Stage C1 v2 remains sealed and unchanged.

C1 may serve as the first prospectively frozen biological architecture case study because its rules were fixed before beta-value biological results were inspected.

Separate prediction/holdout protocols must be frozen before any data used for those predictive targets are examined. They may reuse eligible samples and fixed biological definitions but may not retroactively alter C1's preregistered inferential tests.

## 13. Success criterion

Program success is a reproducible tool that prospectively helps researchers predict, decide, or refuse more reliably than appropriate alternatives.

Finding a new mathematical object is optional.

Prospectively useful prediction is not.
