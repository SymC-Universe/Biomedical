# NSD v0.2 Implementation-Gap Audit v0.1

**Status:** PREFREEZE / OUTCOME-BLIND / NO EXECUTION AUTHORITY

The existing v0.1 conveyor cannot mechanically consume the current fresh v0.2 draft without prospective implementation work. No v0.1 scientific result payload was inspected.

## N-B1

Current conveyor support is limited to CONTINUOUS_C, D_NOT_C_POS/NEG, S_NOT_D_POS/NEG, COLORED_MEMORY, and GENUINE_TWO_MODE.

The fresh v0.2 draft also requires CONTINUOUS_C_REFERENCE_GAIN_CONTROL, PIECEWISE_C_REORGANIZATION, AR1_NONOSCILLATORY, and REFERENCE_MIXTURE_TWO_MODE. These are not implemented in the v0.1 conveyor. Observation/reference cases also need explicit transform handling rather than silent reuse of a single-series route.

## N-B2/N-B3

The v0.1 code expects time_samples while the draft uses base_time_samples.

The v0.1 code expects B keys first_velocity, second_velocity, both_velocity; the draft uses first_biased, second_biased, balanced.

The v0.1 code expects C keys first_position, second_position, both_positions, full_state; the draft uses first_mixed, second_mixed, differential, full_state.

The draft requires continuous peak refinement; v0.1 reports only a base-grid peak.

The draft includes phase_offset_seconds; v0.1 switching starts at phase zero.

The draft declares fresh sampling projections and observation-conditioned recoverability; v0.1 records exact deterministic responses and does not implement that sampled recoverability layer or a noise/RNG contract.

The v0.2 plan separates autonomous, B-driven, and C-observed targets. A future implementation may record them together mechanically only if labels remain distinct and no scientific equivalence is inferred.

## Required before execution

After architecture APQ and exact packet-level APQ/freeze, prospective v0.2 implementation must bind a fresh code/dependency manifest and tests proving that every frozen key is consumed, observation transforms are explicit, physical-metric similarity is correct, peak refinement and switching phase are honored, sampled recovery cannot access latent exact descriptors, GitHub performs no scientific verdict/ranking, and checkpoint resume refuses identity mismatch.

**Disposition:** IMPLEMENTATION_NOT_READY_FOR_V0_2. This is expected prefreeze implementation debt, not a scientific failure.
