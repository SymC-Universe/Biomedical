# Known-Bad Qualification Map

Status: **P0 engineering qualification only**. This document does not qualify a P1 scientific claim.

General Protocol v0.7.1 requires consequential checks to be demonstrated failing on known-bad inputs and to exercise the production code they protect. The current P0 production interface is `src.engine_interface.evaluate_all_layers`.

| Production behavior | Known-bad input | Required result | Test |
|---|---|---|---|
| Scientific-input firewall | diagnosis / phenotype / treatment / outcome / truth / chi / labels | `ValueError` | `test_production_input_contract_fails_on_known_bad_scientific_input` |
| Unknown-side-channel firewall | unexpected payload key | `ValueError` | `test_unknown_payload_key_fails_closed_at_production_interface` |
| Scalar stationarity gate | coherent global pole rescaling across halves | scalar refusal | `test_known_bad_scalar_nonstationarity_fails_through_production_interface` |
| Modal carrier gate | observation-space carrier rotation | modal refusal | `test_known_bad_carrier_rotation_fails_modal_gate_through_production_interface` |
| System organization gate | relative spectral reorganization | system refusal | `test_known_bad_structural_reorganization_fails_system_gate_through_production_interface` |
| Order-identifiability gate | no qualifying singular-value gap | all layers refuse | `test_known_bad_no_order_is_refused_by_all_layers_through_production_interface` |
| Candidate-grid edge gate | selected order equals maximum candidate order | all layers refuse | `test_known_bad_edge_order_is_refused_by_all_layers_through_production_interface` |
| Stability gate | selected fit contains nonnegative-real-part pole | all layers refuse | `test_known_bad_unstable_pole_is_refused_by_all_layers_through_production_interface` |
| Oscillatory-structure gate | selected fit contains no positive complex mode | all layers refuse | `test_known_bad_no_complex_structure_is_refused_by_all_layers_through_production_interface` |
| Byte-integrity gate | mutate a frozen file after manifest creation | manifest failure | `test_manifest_verifier_detects_known_bad_mutation` |
| Freeze-completeness gate | add unmanifested file | manifest failure | `test_manifest_verifier_detects_unfrozen_added_file` |
| Semantic-summary gate | alter a reported primary summary rate | semantic failure | `test_semantic_validator_fails_on_known_bad_summary_mutation` |
| Confirmatory-execution gate | omit P1 readiness record | nonzero exit before scientific generation | `test_confirmatory_runner_is_fail_closed_before_p1_ready_record` |

This table qualifies only implemented engineering and method-scope guards. It does not establish that current thresholds are biologically meaningful, that SSI-COV is adequate for EEG, or that the NSD System Model is empirically validated.
