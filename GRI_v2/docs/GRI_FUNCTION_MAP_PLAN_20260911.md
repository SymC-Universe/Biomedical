# GRI Function Map plan

**Date:** 2026-09-11  
**Mode:** P0-D DISCOVERY / MECHANISM MAPPING  
**Protocol:** v0.7.1 + v0.7.1A  
**Confirmatory status:** NONE

## Purpose

Map the supported interior of the current GRI architecture with the same seriousness used to map failure boundaries. This work is descriptive/discovery-oriented and may use already-viewed data. It cannot confirm itself.

## Existing function evidence to organize

1. **RNA architecture after fixed-n calibration**
   - n=30, 100 deterministic draws/cancer.
   - cohort-size bias strongly reduced after calibration.
   - rank topology largely preserved.

2. **Composition-projected RNA architecture**
   - broad topology persists after purity/leukocyte projection.
   - immune/inflammatory programs show greater context sensitivity.

3. **RPPA cross-layer support**
   - aligned RNA/RPPA coupling is positive across evaluated cancers.
   - this provides orthogonal cross-modal context but does not prove causality.

4. **Methylation within-layer organization**
   - C1 H1 supports nonrandom methylation spectral organization relative to its construction-aware null in the internal TCGA lineage.

5. **Methylation-RNA global geometry**
   - C1 H2 supports patient-geometry alignment internally.
   - principal-angle structure indicates strongest alignment in leading modes.

6. **Patient-specific Hallmark coupling**
   - C1 H3a supports patient-specific same-Hallmark coupling internally.
   - H3b semantic-label specificity is weaker and support-sensitive and must not be folded into the general function claim.

7. **Internal held-out prediction**
   - discovery-trained methylation representation contains held-out information about RNA Hallmark states beyond purity/leukocyte covariates in the evaluated internal TCGA partitions.
   - this is internal, not external, generalization.

## Function Map axes

The first systematic map should represent, where data support it:

- cancer type;
- modality pair;
- raw versus context-projected state;
- publication-faithful versus technical-mask track;
- scalar spectral organization;
- modal concentration / effective-rank structure;
- leading principal-angle alignment;
- global CKA with null-floor/headroom context;
- patient-specific Hallmark coupling;
- semantic-label specificity as a separate, non-promoted layer;
- prediction risk and internal confidence coordinate;
- sample support / missingness burden;
- platform/source context;
- refusal/not-evaluable states.

## Questions to answer in P0-D

1. What regions of the current multidimensional GRI state space are actually occupied by the evaluated cancers?
2. Which combinations of scalar, modal, conglomerate, and cross-component states recur?
3. Can different internal modal organizations yield similar global patient geometry?
4. Which function patterns persist after purity/leukocyte projection?
5. Which architectures are robust to technical masking?
6. How much of global CKA is carried by leading modes versus distributed modes?
7. Where does patient-specific coupling remain informative even when label-specific semantic promotion is weak?
8. Which observed states show compensation or redistribution across layers rather than simple loss of structure?
9. Which function regions correspond to lower versus higher internal prediction risk, without treating that retrospective map as new prospective evidence?
10. Which areas are not identifiable with the current data and should be marked `NOT_KNOWN_HERE`?

## Required outputs

A mature Function Map dataset should include one row per defined state/cancer/track/analysis unit with fields for:

- `function_map_id`
- `analysis_unit`
- `cancer_type`
- `track`
- `context_state`
- `sample_support`
- `scalar_state`
- `modal_state`
- `conglomerate_state`
- `cross_component_state`
- `uncertainty`
- `missingness_state`
- `technical_state`
- `prediction_context`
- `epistemic_status`
- `coverage_role = NOMINAL_FUNCTION | PERTURBED_FUNCTION | NOT_AVAILABLE`
- `support_state = WORKS_HERE | NOT_KNOWN_HERE`
- `provenance`

## Guardrails

- Do not rename empirical architecture as biological chi.
- Do not convert cross-sectional differences into temporal trajectories.
- Do not infer causality from cross-layer alignment.
- Do not use function-map coherence as confirmation of the same map.
- Preserve cancers/conditions that do not fit visually clean clusters.
- Report occupancy, not only mathematically possible regions.
- Preserve multiple internal organizations when they yield similar system-level outputs.
- Keep H3b/semantic specificity separate from global/patient-specific function evidence.

## Interaction with the post-C1 sensitivity

The frozen sensitivity v2.2 is P0-Q and should not be altered by this Function Map work. Its results may later narrow which current coordinates are stable enough to retain in the Function Map. No result-dependent threshold is frozen here.

## Exit condition

P0-D Function Map v0.1 is complete when the existing supported interior has been assembled into a reproducible machine-readable landscape with explicit uncertainty, provenance, and `WORKS_HERE` / `NOT_KNOWN_HERE` states, without changing any confirmatory claim.