"""Deterministic JSON serialization helpers for NSD contract objects."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from typing import Any


def _normalize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_normalize(item) for item in value]
    return value


def to_canonical_json(value: Any) -> str:
    """Serialize supported NSD contract objects to deterministic JSON."""
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
