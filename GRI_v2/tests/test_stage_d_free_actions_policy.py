from pathlib import Path
import re


ALLOWED_STANDARD_PUBLIC_RUNNERS = {
    "ubuntu-latest",
    "ubuntu-24.04",
    "ubuntu-22.04",
    "ubuntu-slim",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_all_workflows_use_standard_public_linux_runners_only():
    workflows = sorted((_repo_root() / ".github" / "workflows").glob("*.y*ml"))
    assert workflows, "No GitHub Actions workflows found"
    seen = []
    for path in workflows:
        text = path.read_text(encoding="utf-8")
        assert "self-hosted" not in text, f"self-hosted runner forbidden: {path.name}"
        for match in re.finditer(r"^\s*runs-on:\s*([^#\n]+)", text, flags=re.MULTILINE):
            value = match.group(1).strip().strip("'\"")
            seen.append((path.name, value))
            assert value in ALLOWED_STANDARD_PUBLIC_RUNNERS, (
                f"Non-free/nonstandard runner label in {path.name}: {value!r}"
            )
    assert seen, "No runs-on declarations found"


def test_stage_d_preflight_artifact_is_compact_short_retention():
    path = _repo_root() / ".github" / "workflows" / "gri-stage-d-preflight.yml"
    text = path.read_text(encoding="utf-8")
    assert "retention-days: 1" in text
    assert "if: success()" in text
    assert "ubuntu-latest" in text
    assert "runner.temp" not in text
    assert "family.soft" not in text
