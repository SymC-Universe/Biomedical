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
PUBLIC_REMOTE = "s3-PUBLIC"


def _hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _url_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read().decode("utf-8").strip()


def _run(args, cwd=None, capture=False):
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )


def _verify_git_tag(cfg: dict) -> None:
    repo = cfg["source_snapshot"]["GitHub_mirror"]
    tag = cfg["source_snapshot"]["Git_tag"]
    expected = cfg["source_snapshot"]["Git_commit"]
    url = f"https://github.com/{repo}.git"
    proc = _run(
        ["git", "ls-remote", "--tags", url, f"refs/tags/{tag}"],
        capture=True,
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


def _prepare_annex_checkout(cfg: dict, checkout: Path) -> dict:
    if shutil.which("git-annex") is None:
        raise RuntimeError("git-annex is required for OpenNeuro annex content retrieval")
    repo = cfg["source_snapshot"]["GitHub_mirror"]
    tag = cfg["source_snapshot"]["Git_tag"]
    expected = cfg["source_snapshot"]["Git_commit"]
    url = f"https://github.com/{repo}.git"

    if checkout.exists():
        shutil.rmtree(checkout)
    checkout.parent.mkdir(parents=True, exist_ok=True)

    # Clone Git metadata only. Annexed EEG content remains absent until the
    # explicit pilot-only `git annex get` calls below.
    _run(["git", "clone", "--no-checkout", url, str(checkout)])
    _run(["git", "checkout", "--detach", expected], cwd=checkout)
    observed = _run(["git", "rev-parse", "HEAD"], cwd=checkout, capture=True).stdout.strip()
    if observed != expected:
        raise RuntimeError(f"checkout drift: expected {expected}, observed {observed}")

    # git-annex records local repository state on its own local metadata branch.
    # Hosted CI clones have no author identity by default, so give this
    # disposable checkout an explicitly non-personal local identity. This does
    # not alter the source repository or Biomedical repository history.
    _run(["git", "config", "user.name", "NSD Atlas CI"], cwd=checkout)
    _run(["git", "config", "user.email", "nsd-atlas-ci@invalid.local"], cwd=checkout)

    # Ensure annex metadata/special remotes are initialized from the cloned
    # repository. No annex content is fetched by init. OpenNeuro's public
    # special remote auto-enables in this snapshot as `s3-PUBLIC`.
    _run(["git", "annex", "init", "NSD-Atlas-A2-ephemeral"], cwd=checkout)
    remotes = _run(["git", "annex", "info", "--json"], cwd=checkout, capture=True).stdout
    available_remotes = _run(["git", "remote"], cwd=checkout, capture=True).stdout.split()
    if PUBLIC_REMOTE not in available_remotes:
        raise RuntimeError(
            f"expected auto-enabled OpenNeuro annex remote {PUBLIC_REMOTE!r} not available; "
            f"observed remotes {available_remotes}"
        )
    return {
        "repository": repo,
        "tag": tag,
        "commit": observed,
        "git_annex_version": _run(["git", "annex", "version"], cwd=checkout, capture=True).stdout.splitlines()[0].strip(),
        "annex_info_json_lines_sha256": hashlib.sha256(remotes.encode("utf-8")).hexdigest(),
        "annex_remote_used": PUBLIC_REMOTE,
        "ephemeral_git_identity": {
            "name": "NSD Atlas CI",
            "email": "nsd-atlas-ci@invalid.local"
        }
    }


def _copy_regular_snapshot_file(checkout: Path, rel: str, out: Path) -> dict:
    src = checkout / rel
    if not src.exists():
        raise RuntimeError(f"missing source sidecar at frozen checkout: {rel}")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)
    return {
        "path": rel,
        "bytes": out.stat().st_size,
        "sha256": _hash(out, "sha256"),
        "source": "frozen Git checkout",
    }


def fetch(output_root: Path) -> dict:
    cfg = json.loads(FREEZE.read_text(encoding="utf-8"))
    if cfg["status"] != "FROZEN_BEFORE_EEG_VALUE_INSPECTION":
        raise RuntimeError("SRM pilot freeze is not valid")
    _verify_git_tag(cfg)

    repo = cfg["source_snapshot"]["GitHub_mirror"]
    tag = cfg["source_snapshot"]["Git_tag"]
    raw_git = f"https://raw.githubusercontent.com/{repo}/{tag}"
    checkout = output_root.parent / "srm_a2_source_checkout"
    checkout_meta = _prepare_annex_checkout(cfg, checkout)

    records = []
    requested_annex_paths = []
    for subject in cfg["pilot_subjects"]:
        for session in cfg["sessions"]:
            set_rel, channels_rel, eeg_json_rel = _paths(cfg, subject, session)

            # Read the annex symlink identity from the frozen Git tag before
            # asking git-annex for content.
            annex_target = _url_text(f"{raw_git}/{set_rel}")
            match = ANNEX_RE.search(annex_target)
            if not match:
                raise RuntimeError(f"could not parse MD5E annex identity for {set_rel}: {annex_target}")
            expected_size = int(match.group("size"))
            expected_md5 = match.group("md5").lower()

            requested_annex_paths.append(set_rel)
            _run(["git", "annex", "get", "--from", PUBLIC_REMOTE, "--", set_rel], cwd=checkout)
            src = checkout / set_rel
            if not src.exists():
                raise RuntimeError(f"git-annex did not materialize requested pilot file: {set_rel}")

            set_out = output_root / set_rel
            set_out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, set_out)
            actual_size = set_out.stat().st_size
            actual_md5 = _hash(set_out, "md5")
            actual_sha256 = _hash(set_out, "sha256")
            if actual_size != expected_size or actual_md5 != expected_md5:
                raise RuntimeError(
                    f"annex verification failed for {set_rel}: "
                    f"expected size/md5 {expected_size}/{expected_md5}, "
                    f"observed {actual_size}/{actual_md5}"
                )

            sidecars = [
                _copy_regular_snapshot_file(checkout, channels_rel, output_root / channels_rel),
                _copy_regular_snapshot_file(checkout, eeg_json_rel, output_root / eeg_json_rel),
            ]

            records.append({
                "subject": subject,
                "session": session,
                "set_path": set_rel,
                "annex_target": annex_target,
                "annex_backend": "MD5E",
                "annex_remote": PUBLIC_REMOTE,
                "expected_bytes": expected_size,
                "expected_md5": expected_md5,
                "actual_bytes": actual_size,
                "actual_md5": actual_md5,
                "actual_sha256": actual_sha256,
                "verified": True,
                "sidecars": sidecars,
            })

    allowed = {
        _paths(cfg, subject, session)[0]
        for subject in cfg["pilot_subjects"]
        for session in cfg["sessions"]
    }
    if set(requested_annex_paths) != allowed or len(requested_annex_paths) != len(allowed):
        raise RuntimeError("annex retrieval path set drifted from frozen 8-subject x 2-session pilot")

    # Remove the source checkout after copying the 16 verified pilot files so
    # workflow artifacts cannot accidentally include Git metadata or annex data.
    shutil.rmtree(checkout)

    return {
        "schema": "neurostability-atlas-a2-srm-input-manifest-v0.1",
        "status": "ALL_FROZEN_INPUTS_RETRIEVED_AND_BYTE_VERIFIED",
        "source_snapshot": cfg["source_snapshot"],
        "annex_checkout": checkout_meta,
        "pilot_subjects": cfg["pilot_subjects"],
        "sessions": cfg["sessions"],
        "requested_annex_path_count": len(requested_annex_paths),
        "reservoir_annex_paths_requested": 0,
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
    print(f"reservoir annex paths requested: {manifest['reservoir_annex_paths_requested']}")
    print("A2 SRM INPUT FETCH PASS")


if __name__ == "__main__":
    main()
