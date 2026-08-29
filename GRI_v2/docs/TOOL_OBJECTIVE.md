# Cancer Stability Atlas - Tool Objective

## Primary objective

Build a predictive cancer-stability instrument whose variables and model structure are selected by what the data support, not by fidelity to the historical GRI manuscript.

The historical manuscript remains part of the provenance record. Its observations may motivate candidate measurements, and its failures may motivate safeguards, but the new tool is free to diverge completely from the old formulation.

## What the tool should eventually do

A successful tool should predict or stratify a prospectively defined biological behavior on held-out data. Candidate targets may include perturbational response, state transition, recovery behavior, drug response, progression, or another independently measured outcome. The target must be fixed before model evaluation for the relevant validation phase.

The tool should also provide interpretable state coordinates so that predictive performance is not obtained only from an opaque aggregate score.

## Methodological inheritance from Chemistry and Stability Arc

The inherited methodology is procedural, not evidential:

- separate the balancing coordinate from the rest of the landscape;
- keep physically or biologically distinct measurements distinct;
- define estimator provenance and uncertainty;
- prevent calibration data from serving as independent validation;
- compare against construction-aware nulls and established baselines;
- locate empirical organization/turnover/transition structure rather than forcing an optimum at chi = 1;
- require genuine dynamic evidence before making dynamical claims;
- preserve failed hypotheses rather than retuning them into successes.

## Historical GRI status

`CV/2` is a historical comparator. It is not chi and is not a required feature of the final model.

The old substrate-capture, bandwidth, executor, critical-boundary, and therapeutic interpretations are not active assumptions. Any related concept must be re-earned using independently defined measurements and prospective tests.

## Development ladder

### A. Static map

Measure independent static coordinates from PanCanAtlas and matched data: variability, lineage/context, and network organization. Do not collapse them into a master score.

### B. Multiomic substrate/context map

Add independently measured methylation, chromatin, protein, purity/composition, and other appropriate layers. Evaluate which coordinates are redundant and which contribute unique structure.

### C. Dynamic benchmark

Use genuine ordered perturbation or time-course data. Implement established comparators such as Dynamic Network Biomarkers and ordinary predictive/network baselines.

### D. Candidate dynamical balance coordinate

Only if the data provide defensible, same-coordinate Gamma and Omega measurements or calibrated estimators, evaluate `chi = Gamma/(2 Omega)`. Chi is tested as one coordinate among others, not assumed to be the organizing answer.

### E. Predictive model selection

Freeze candidate models and compare them using held-out prediction, calibration, robustness, ablation, and baseline superiority. Complexity must earn itself.

### F. External validation

Freeze the selected tool and test it on data not used for architecture discovery or calibration. Failure remains a valid scientific outcome.

### G. Manuscript

Only after the evidence ladder closes do we write the replacement paper around what survived. The manuscript describes the tool; the manuscript does not determine the tool.

## Success and failure

Success is not recovery of the old GRI narrative. Success is a reproducible model that predicts an independently defined biological outcome better than appropriate baselines and whose claimed coordinates have valid measurement meaning.

If no stability-specific coordinate improves prediction beyond conventional methods, the correct conclusion is that the proposed stability framework did not add measurable predictive value in the tested setting.
