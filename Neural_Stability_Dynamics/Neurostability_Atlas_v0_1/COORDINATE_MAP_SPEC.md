# Neurostability Atlas v0.1 Coordinate Map Specification

Status: **P0 ATLAS SCHEMA CANDIDATE. VALUES NOT YET POPULATED.**
System Model: NSD v1.0
Protocol: General v0.7.1 FINAL + v0.7.1A

## 1. Coordinate-map principle

The Atlas maps supported coordinates and supported absences. It does not force every source into a complete coordinate vector.

Each Atlas entry is therefore a sparse, provenance-bearing object with:

- source/context identity;
- native model identity;
- coordinate values where supported;
- derivation eligibility/status for each requested coordinate;
- uncertainty/identifiability;
- Function/Limit research role;
- pathway-specific independence;
- scope and missingness.

## 2. Coordinate family A: native scalar / spectral

Preferred native coordinates, where the source/model provides them:

- `pole_real_per_s` — real part of continuous-time pole/eigenvalue;
- `pole_imag_rad_per_s` — imaginary part;
- `frequency_hz` — explicit or exact algebraic conversion from angular frequency;
- `decay_rate_per_s` — stable decay magnitude when sign convention is explicit;
- `decay_time_s` — exact reciprocal of a nonzero supported decay rate, with derivation recorded;
- `stability_class` — stable / unstable / neutral / unresolved under the source/model convention;
- `oscillation_class` — oscillatory / non-oscillatory / unresolved;
- `mode_count_or_observable_order` — only with the method/source definition attached.

Coordinate names do not erase source conventions. Original symbols and equations are retained in provenance.

## 3. Coordinate family B: model-conditional second-order / chi

These are **not default Atlas coordinates**.

Required provenance before a chi value is admitted:

1. explicit second-order factorization/model lineage;
2. native damping parameter or a mathematically equivalent quantity;
3. native frequency parameter with its exact meaning specified;
4. derivation from native quantities to the Atlas chi convention;
5. dimensional check;
6. uncertainty or uncertainty-withheld status;
7. no circular use of the target chi to choose the factorization.

Fields:

- `second_order_factorization_status`;
- `damping_parameter_native`;
- `frequency_parameter_native`;
- `chi_value`;
- `chi_status`;
- `chi_derivation`;
- `chi_uncertainty`.

A generic pole pair alone is insufficient unless the second-order interpretation is independently licensed.

## 4. Coordinate family C: modal / carrier

Where mode shapes, spatial patterns or equivalent observable carriers are available:

- `carrier_representation_type`;
- `carrier_vector_or_reference`;
- `carrier_normalization`;
- `carrier_channel_basis`;
- `individual_identity_status`;
- `subspace_dimension`;
- `subspace_basis_or_reference`;
- `channel_participation_vector`;
- `anatomical_or_sensor_context` as metadata, not mechanism by default.

Comparative coordinates may include, when two explicitly paired conditions/records are being compared:

- `MAC` or source-native carrier similarity;
- `subspace_similarity` / principal-angle summary;
- `participation_distance`;
- assignment margin/ambiguity.

Individual-mode and subspace coordinates remain separate.

## 5. Coordinate family D: conglomerate / system organization

Potential coordinates:

- `observable_order` / `observable_rank` with estimator definition;
- `positive_complex_mode_count` where meaningful;
- `whole_observable_subspace_dimension`;
- `channel_participation_distribution`;
- `cluster_count`;
- `cluster_signature`;
- `relational_spectral_geometry` or a provenance-bearing representation thereof;
- `shared_mode_count`;
- `added_mode_count`;
- `lost_mode_count`;
- `reorganized_mode_or_subspace_status`;
- `order_transition_status`.

No whole-system chi is inferred from these objects.

## 6. Coordinate family E: identifiability / crowding

Potential coordinates/descriptors:

- source-native modal separation measure;
- `crowding_ratio_delta_omega_over_sum_decay` when its terms are supported;
- individual-mode assignment ambiguity;
- cluster/subspace identifiability;
- rank/order ambiguity;
- observable-strength/weak-mode descriptor where available;
- conditioning metric where available.

Any cutoff separating `individual` from `subspace-only` remains method/version specific until qualified. The Atlas records continuous descriptors whenever possible.

## 7. Coordinate family F: model adequacy

Atlas-compatible adequacy descriptors include, with exact method definitions:

- residual/innovation temporal-structure statistic;
- covariance reconstruction error;
- out-of-sample prediction/reconstruction error;
- fitted spectral radius or stability/admissibility descriptor;
- order sensitivity;
- window sensitivity;
- goodness-of-fit/consistency measure native to the source;
- model exception/refusal status.

A source-native residual is not relabeled `innovation` unless the model actually defines it that way.

No cross-study numerical threshold is imposed during coordinate extraction.

## 8. Coordinate family G: uncertainty

Possible uncertainty objects:

- reported standard error;
- confidence/credible interval with level and construction;
- bootstrap distribution/reference;
- covariance matrix/reference;
- sampling-covariance estimator identity;
- model-order uncertainty;
- mode-assignment uncertainty;
- subspace uncertainty;
- repeated-realization variability;
- `UNCERTAINTY_NOT_REPORTED` / `UNCERTAINTY_NOT_RECONSTRUCTABLE`.

Uncertainty values are never detached from their estimator and confidence convention.

## 9. Context axes

Each coordinate record is contextualized by, where available:

- species/population;
- acquisition modality;
- recording state/task;
- perturbation/intervention;
- temporal window/epoch definition;
- sampling rate and duration;
- channel/sensor count and montage;
- preprocessing relevant to the coordinate;
- system/cohort inclusion rule;
- research role: `NOMINAL_FUNCTION`, `PERTURBED_FUNCTION`, `BOUNDARY_OR_TRANSITION`, `RARE_NATURAL_LIMIT`;
- base-rate/rarity context for rare natural cases.

These context fields are not automatically Engine selector inputs.

## 10. Coordinate eligibility

Every coordinate request returns an eligibility status even when it returns no number.

- `NATIVE_REPORTED`: numerical/object value is explicitly reported by the source;
- `NATIVE_RECONSTRUCTED_FROM_RAW_DATA`: independently recomputed using a frozen Atlas reconstruction method;
- `DERIVED_EXACT`: algebraic/unit conversion with no new model assumption;
- `DERIVED_MODEL_CONDITIONAL`: derivation requires a stated model assumption independently supported by the source;
- `WITHHELD_INSUFFICIENT_INFORMATION`;
- `WITHHELD_ASSUMPTION_NOT_LICENSED`;
- `NOT_APPLICABLE`;
- `UNRESOLVED`.

## 11. Evidence tier

Atlas evidence tier is separate from coordinate eligibility.

Initial tiers:

- `A_FULL_NUMERIC_PROVENANCE`: full source/raw data plus exact numerical location or reconstruction path;
- `B_FULL_METHOD_PARTIAL_NUMERIC`: full method provenance but incomplete numerical reconstruction;
- `C_ABSTRACT_OR_SNIPPET_ONLY`: insufficient for decisive coordinate population;
- `D_SOURCE_EXISTS_BLOCKED`: candidate retained but not populated;
- `E_REJECTED_FOR_ATLAS`: source fails predeclared intake/independence/provenance rules.

Only tier A should ordinarily supply decisive numerical Atlas coordinates. Tier B may supply method/context information or provisional non-decisive coordinates with explicit status.

## 12. Independence pathways

Each entry separately records:

- `data_independence`;
- `cohort_system_independence`;
- `outcome_label_independence`;
- `parameter_tuning_independence`;
- `method_estimator_independence`;
- `atlas_engine_independence`;
- `source_literature_independence`;
- `temporal_decisive_evidence_independence`.

A single `independent=true` field is prohibited.

## 13. Function / Limit occupancy

Atlas coordinate points may later be organized into:

- `WORKS_HERE` for the specific representation/claim supported in that source/context;
- `STOPS_WORKING_HERE` for a supported limit/failure/refusal of that specific representation;
- `NOT_KNOWN_HERE` where evidence cannot decide.

This classification describes evidence occupancy. It does not become an Engine threshold by lookup.

## 14. Source-selection firewall

Sources are selected by domain-native criteria such as:

- relevance to a predeclared coordinate family;
- adequate acquisition/method provenance;
- numerical extractability or open raw data;
- coverage-role need;
- independence pathway;
- reproducibility/accessibility.

Sources are **not** selected because their reported values lie near a desired SymC/chi boundary or because they support a preferred ordering.

Previously inspected sources can populate P0-D Atlas discovery but cannot independently confirm a rule chosen from them.

## 15. First coordinate-map deliverables

A0 deliverables:

1. `registries/COORDINATE_DEFINITIONS.json`;
2. `schemas/atlas_entry.schema.json`;
3. `registries/SOURCE_INTAKE_QUEUE.json`;
4. Atlas validator and regression tests;
5. source-search/extraction protocol;
6. first source candidate set spanning function and limit roles without outcome targeting.
