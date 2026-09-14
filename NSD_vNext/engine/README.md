# NSD Structural Engine Contract Scaffold

Status: PRE-ALGORITHM IMPLEMENTATION SCAFFOLD
Date: 14 September 2026

This directory begins the executable NSD vNext Structural Engine without prematurely implementing a scientific estimator.

The first executable layer is deliberately limited to **contracts and safeguards**:
- provenance is mandatory;
- subject/session identity is explicit;
- duplicate hierarchy keys are auditable;
- ambiguous metadata joins are exposed rather than assigned by first match;
- subject leakage across train/test splits is mechanically rejectable;
- spectral peaks remain descriptive until a dynamical model licenses more;
- mode-specific scalar lineage is mandatory;
- whole-brain/global chi is rejected by contract;
- refusals are first-class outputs;
- zero-peak states are valid;
- candidate mode identifiers must be unique;
- configuration hashes and JSON serialization are deterministic.

Current files:
- `pyproject.toml` — minimal package/test configuration;
- `nsd_engine/schema.py` — result, provenance, mode, scalar, and refusal contracts;
- `nsd_engine/provenance.py` — hierarchy, join-cardinality, and split-leakage safeguards;
- `nsd_engine/serialization.py` — deterministic JSON serialization;
- `nsd_engine/__init__.py` — public contract API;
- `tests/test_contracts.py` — scalar/refusal/result safeguards;
- `tests/test_provenance.py` — hierarchy/join/split safeguards;
- `tests/test_serialization.py` — deterministic serialization safeguard.

Current local verification after provenance expansion: **15 tests passed**.

## Important boundary

There is intentionally no clinical classifier, disorder threshold, damping estimator, chi estimator, DMD implementation, SpecParam implementation, or normative model in this scaffold.

Those scientific modules enter only after their qualification plan is linked to:
- `../docs/ESTIMATOR_LICENSING_MATRIX_v0.1.md`
- `../docs/KNOWN_TRUTH_ADVERSARIAL_TEST_MATRIX_v0.1.md`
- `../docs/STRUCTURAL_ENGINE_SPEC_v0.1.md`
- `../docs/ENGINE_IMPLEMENTATION_PLAN_v0.1.md`

The scaffold makes it harder for later code to silently convert a descriptive feature into a dynamical claim or a repeated session into an independent subject.