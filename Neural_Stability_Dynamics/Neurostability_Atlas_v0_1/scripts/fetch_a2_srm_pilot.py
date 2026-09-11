from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "registries" / "A2_SRM_CSD_SVD_PILOT_FREEZE.json"
ANNEX_RE = re.compile(r"MD5E-s(?P<size>\d+)--(?P<md5>[0-9a-fA-F]{32})\.set$")


def _hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _url_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read().decode("utf-8").strip()


def _download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".part")
    if tmp.exists():
        tmp.unlink()
    with urllib.request.urlopen(url, timeout=300) as response, tmp.open("wb") as f:
        shutil.copyfileobj(response, f, length=1024 * 1024)
    tmp.replace(out)


def _verify_git_tag(cfg: dict) -> None:
    repo = cfg["source_snapshot"]["GitHub_mirror"]
    tag = cfg["source_snapshot"]["Git_tag"]
    expected = cfg["source_snapshot"]["Git_commit"]
    url = f"https://github.com/{repo}.git"
    proc = subprocess.run(
        ["git", "ls-remote", "--tags", url, f"refs/tags/{tag}"],
        check=True,
        capture_output=True,
        text=True,
    )
    observed = proc.stdout.strip().split()[0]
    if observed != expected:
        raise RuntimeError(f"OpenNeuro mirror tag drift: expected {expected}, observed {observed}")


def _paths(cfg: dict, subject: str, session: str) -> tuple[str, str, str]:
    layer = cfg["input_layer"]
    repl = {"subject": subject, "session": session}
    return (
        f"{layer['root']}/{layer['file_pattern'].format(**repl)}",
        f"{layer['root']}/{layer['channel_sidecar_pattern'].format(**repl)}",
        f"{layer['root']}/{layer['eeg_sidecar_pattern'].format(**repl)}",
    )


def fetch(output_root: Path) -> dict:
    cfg = json.loads(FREEZE.read_text(encoding="utf-8"))
    if cfg["status"] != "FROZEN_BEFORE_EEG_VALUE_INSPECTION":
        raise RuntimeError("SRM pilot freeze is not valid")
    _verify_git_tag(cfg)

    repo = cfg["source_snapshot"]["GitHub_mirror"]
    tag = cfg["source_snapshot"]["Git_tag"]
    s3_http = "https://s3.amazonaws.com/openneuro.org/ds003775"
    raw_git = f"https://raw.githubusercontent.com/{repo}/{tag}"

    records = []
    for subject in cfg["pilot_subjects"]:
        for session in cfg["sessions"]:
            set_rel, channels_rel, eeg_json_rel = _paths(cfg, subject, session)

            annex_target = _url_text(f"{raw_git}/{set_rel}")
            match = ANNEX_RE.search(annex_target)
            if not match:
                raise RuntimeError(f"could not parse MD5E annex identity for {set_rel}: {annex_target}")
            expected_size = int(match.group("size"))
            expected_md5 = match.group("md5").lower()

            set_out = output_root / set_rel
            _download(f"{s3_http}/{set_rel}", set_out)
            actual_size = set_out.stat().st_size
            actual_md5 = _hash(set_out, "md5")
            actual_sha256 = _hash(set_out, "sha256")
            if actual_size != expected_size or actual_md5 != expected_md5:
                raise RuntimeError(
                    f"annex verification failed for {set_rel}: "
                    f"expected size/md5 {expected_size}/{expected_md5}, "
                    f"observed {actual_size}/{actual_md5}"
                )

            sidecars = []
            for rel in (channels_rel, eeg_json_rel):
                out = output_root / rel
                _download(f"{raw_git}/{rel}", out)
                sidecars.append({
                    "path": rel,
                    "bytes": out.stat().st_size,
                    "sha256": _hash(out, "sha256"),
                    "source": f"Git tag {tag}",
                })

            records.append({
                "subject": subject,
                "session": session,
                "set_path": set_rel,
                "annex_target": annex_target,
                "annex_backend": "MD5E",
                "expected_bytes": expected_size,
                "expected_md5": expected_md5,
                "actual_bytes": actual_size,
                "actual_md5": actual_md5,
                "actual_sha256": actual_sha256,
                "verified": True,
                "sidecars": sidecars,
            })

    return {
        "schema": "neurostability-atlas-a2-srm-input-manifest-v0.1",
        "status": "ALL_FROZEN_INPUTS_RETRIEVED_AND_BYTE_VERIFIED",
        "source_snapshot": cfg["source_snapshot"],
        "pilot_subjects": cfg["pilot_subjects"],
        "sessions": cfg["sessions"],
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="input/srm_a2")
    parser.add_argument("--manifest", default="results/a2_srm/input_manifest.json")
    args = parser.parse_args()
    out_root = ROOT / args.output_root
    manifest_path = ROOT / args.manifest
    manifest = fetch(out_root)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest_path)
    print(f"verified sessions: {len(manifest['records'])}")
    print("A2 SRM INPUT FETCH PASS")


if __name__ == "__main__":
    main()
