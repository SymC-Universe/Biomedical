# NSD Structural Engine Contract Scaffold

Status: PRE-ALGORITHM IMPLEMENTATION SCAFFOLD + KNOWN-TRUTH FIXTURES
Date: 14 September 2026

This directory begins the executable NSD vNext Structural Engine without prematurely implementing a clinical estimator.

The executable layer is deliberately limited to **contracts, safeguards, analytically defined known-truth fixtures, and admission interfaces**:
- provenance is mandatory;
- subject/session identity is explicit;
- duplicate hierarchy keys are auditable;
- ambiguous metadata joins are exposed rather than assigned by first match;
- subject leakage across train/test splits is mechanically rejectable;
- spectral peaks remain descriptive until a dynamical model licenses more;
- modal estimators must return named/versioned mode batches with explicit source-method lineage;
- scalar admission requires identifiable mode status plus explicit qualification evidence;
- missing natural-frequency mapping, unlicensed damping mapping, unresolved broadening, excessive uncertainty, or out-of-domain status produce refusal rather than a substitute scalar;
- mode-specific scalar lineage is mandatory;
- whole-brain/global chi is rejected by contract;
- refusals are first-class outputs;
- zero-peak states are valid;
- candidate mode identifiers must be unique;
- configuration hashes and JSON serialization are deterministic;
- exact underdamped second-order oscillator fixtures lock natural frequency, damped frequency, resonance frequency, decay rate, and pole conventions.

Current files:
- `pyproject.toml` — minimal package/test configuration;
- `nsd_engine/schema.py` — result, provenance, mode, scalar, and refusal contracts;
- `nsd_engine/provenance.py` — hierarchy, join-cardinality, and split-leakage safeguards;
- `nsd_engine/serialization.py` — deterministic JSON serialization;
- `nsd_engine/known_truth.py` — exact underdamped oscillator impulse/transfer fixtures;
- `nsd_engine/modal.py` — implementation-neutral modal-estimator interface;
- `nsd_engine/admission.py` — scalar-proposal admission/refusal firewall;
- `nsd_engine/__init__.py` — public contract API;
- `tests/test_contracts.py` — scalar/refusal/result safeguards;
- `tests/test_provenance.py` — hierarchy/join/split safeguards;
- `tests/test_serialization.py` — deterministic serialization safeguard;
- `tests/test_known_truth.py` — oscillator convention/regression safeguards;
- `tests/test_modal_interface.py` — modal lineage/interface safeguards;
- `tests/test_admission.py` — scalar-admission/refusal safeguards.

Current CI verification: **32 tests passed** on GitHub Actions (`pytest -q`, Python 3.11).

## Important scientific boundary

There is intentionally no clinical classifier, disorder threshold, fitted damping estimator, fitted chi estimator, DMD implementation, SpecParam implementation, or normative model in this scaffold yet.

The known-truth oscillator module is **not a claim that resting scalp EEG is a damped harmonic oscillator**. It is an exact mathematical fixture used to test whether future estimators recover truth or confuse distinct frequency/damping quantities.

The modal and admission interfaces similarly do not claim that a mode exists in any clinical signal. They make future estimators expose their identity, diagnostics, qualification status, and reasons for refusal.

Those scientific modules enter only after their qualification plan is linked to:
- `../docs/ESTIMATOR_LICENSING_MATRIX_v0.1.md`
- `../docs/KNOWN_TRUTH_ADVERSARIAL_TEST_MATRIX_v0.1.md`
- `../docs/STRUCTURAL_ENGINE_SPEC_v0.1.md`
- `../docs/ENGINE_IMPLEMENTATION_PLAN_v0.1.md`
- `../docs/DHO_CONVENTION_NOTE_v0.1.md`

The scaffold makes it harder for later code to silently convert a descriptive feature into a dynamical claim, a repeated session into an independent subject, or a spectral peak center into an undamped natural frequency.