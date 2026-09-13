from __future__ import annotations

from src.probe_chi_bio_dorothea_export import (
    COMMIT,
    EXPECTED_BYTES,
    EXPECTED_GIT_BLOB_SHA1,
    REQUIRED_COLUMNS,
    SOURCE_PATH,
)


def test_dorothea_probe_is_pinned_to_architecture_frozen_human_blob() -> None:
    assert COMMIT == "1461fb75e23e110c2281860526d4333920925282"
    assert SOURCE_PATH == "data/dorothea_hs.rda"
    assert EXPECTED_GIT_BLOB_SHA1 == "75c9c0b6f9e9cfc6c34f86e2e0bf0b055ce1d9d9"
    assert EXPECTED_BYTES == 894_668


def test_dorothea_probe_requires_signed_regulon_schema_only() -> None:
    assert REQUIRED_COLUMNS == ("tf", "confidence", "target", "mor")
