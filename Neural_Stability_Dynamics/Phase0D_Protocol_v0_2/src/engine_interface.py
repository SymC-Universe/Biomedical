from __future__ import annotations

from .contracts import selector_payload
from .selector import evaluate_scalar_layer, evaluate_modal_layer, evaluate_system_layer


def evaluate_all_layers(*, fits, decomps, candidate_orders, rules, **extra):
    """Production selector interface. Extra scientific/clinical inputs are rejected."""
    payload = selector_payload(fits=fits,decomps=decomps,candidate_orders=candidate_orders,rules=rules,**extra)
    return {"scalar":evaluate_scalar_layer(**payload),"modal":evaluate_modal_layer(**payload),"system":evaluate_system_layer(**payload)}
