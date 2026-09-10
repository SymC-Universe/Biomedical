from __future__ import annotations

ALLOWED_SELECTOR_KEYS = frozenset({"fits", "decomps", "candidate_orders", "rules"})
FORBIDDEN_SCIENTIFIC_KEYS = frozenset({
    "truth", "true_vals", "true_shapes", "chi", "diagnosis", "phenotype",
    "treatment", "treatment_response", "outcome", "label", "labels", "gri_outcome",
    "historical_desired_ordering"
})


def validate_selector_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise TypeError("selector payload must be a dict")
    keys = set(payload)
    forbidden = {k for k in keys if k.lower() in FORBIDDEN_SCIENTIFIC_KEYS}
    if forbidden:
        raise ValueError(f"forbidden selector inputs: {sorted(forbidden)}")
    unknown = keys - ALLOWED_SELECTOR_KEYS
    missing = ALLOWED_SELECTOR_KEYS - keys
    if unknown:
        raise ValueError(f"unexpected selector inputs: {sorted(unknown)}")
    if missing:
        raise ValueError(f"missing selector inputs: {sorted(missing)}")
    return payload


def selector_payload(*, fits, decomps, candidate_orders, rules, **extra) -> dict:
    payload = {"fits":fits,"decomps":decomps,"candidate_orders":candidate_orders,"rules":rules,**extra}
    return validate_selector_payload(payload)
