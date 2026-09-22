from __future__ import annotations

import json
from pathlib import Path

from src.stream_verify_conglomerate_rs_sources import (
    _parse_content_range,
    _source_specs,
)


def test_parse_content_range_accepts_standard_and_observed_forms():
    assert _parse_content_range("bytes 0-9/100") == (0, 9, 100)
    assert _parse_content_range("0-9/100") == (0, 9, 100)
    assert _parse_content_range(None) is None
    assert _parse_content_range("nonsense") is None


def test_source_specs_bind_existing_frozen_identities():
    specs = _source_specs()
    by_block = {x["block_id"]: x for x in specs}
    assert set(by_block) == {"R", "S"}

    assert by_block["R"]["expected_size_bytes"] == 1882540959
    assert by_block["R"]["expected_sha256"] == (
        "674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658"
    )

    assert by_block["S"]["expected_size_bytes"] == 5022150019
    assert by_block["S"]["expected_sha256"] == (
        "5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77"
    )
