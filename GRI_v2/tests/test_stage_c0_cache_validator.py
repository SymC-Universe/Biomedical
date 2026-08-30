from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from src import validate_stage_c0_cache as v


def test_missing_cache_is_rejected(tmp_path):
    missing = tmp_path / "hallmark_profile_cache.npz"
    try:
        v.validate_cache(missing)
    except FileNotFoundError as exc:
        assert "does not exist" in str(exc)
    else:
        raise AssertionError("missing cache must fail before source acquisition")


def test_wrong_cache_hash_is_rejected(tmp_path):
    wrong = tmp_path / "hallmark_profile_cache.npz"
    wrong.write_bytes(b"not-the-frozen-stage-a-cache")
    try:
        v.validate_cache(wrong)
    except ValueError as exc:
        assert "not the frozen completed Stage A" in str(exc)
    else:
        raise AssertionError("wrong cache hash must fail before source acquisition")
