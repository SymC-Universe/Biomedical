from pathlib import Path
import hashlib
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from src import validate_stage_c0_cache as v

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "RUN_STAGE_C0_METHYLATION_WINDOWS.bat"


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


def test_validator_accepts_parentheses_in_cache_path_when_hash_matches(tmp_path, monkeypatch):
    cache = tmp_path / "hallmark_profile_cache(1).npz"
    payload = b"synthetic-cache-for-path-regression"
    cache.write_bytes(payload)
    expected = hashlib.sha256(payload).hexdigest()
    monkeypatch.setattr(v, "EXPECTED_CACHE_SHA256", expected)
    assert v.validate_cache(cache) == expected


def test_windows_launcher_never_expands_cache_inside_parenthesized_command_block():
    launcher = LAUNCHER.read_text(encoding="utf-8")
    cache_lines = [line for line in launcher.splitlines() if "%CACHE%" in line]
    assert cache_lines
    for line in cache_lines:
        assert "(" not in line and ")" not in line, (
            "Windows cmd may misparse selected filenames containing parentheses when %CACHE% "
            f"is expanded on a parenthesized command line: {line!r}"
        )
    assert 'if not exist "%CACHE%" (' not in launcher
