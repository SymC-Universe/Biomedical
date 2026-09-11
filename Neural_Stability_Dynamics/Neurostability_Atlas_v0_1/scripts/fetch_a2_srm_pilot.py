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
DIAGNOSTIC = ROOT / "results" / "a2_srm" / "transport_failure.json"


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


def _run_capture(args, cwd=None):
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def _write_diagnostic(payload: dict) -> None:
    DIAGNOSTIC.parent.mkdir(parents=True, exist_ok=True)
    DIAGNOSTIC.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        shutil.rmtree(checkout, ignore_errors=True)
    checkout.parent.mkdir(parents=True, exist_ok=True)

    _run(["git", "clone", "--no-checkout", url, str(checkout)])
    _run(["git", "checkout", "--detach", expected], cwd=checkout)
    observed = _run(["git", "rev-parse", "HEAD"], cwd=checkout, capture=True).stdout.strip()
    if observed != expected:
        raise RuntimeError(f"checkout drift: expected {expected}, observed {observed}")

    _run(["git", "config", "user.name", "NSD Atlas CI"], cwd=checkout)
    _run(["git", "config", "user.email", "nsd-atlas-ci@invalid.local"], cwd=checkout)
    _run(["git", "annex", "init", "NSD-Atlas-A2-ephemeral"], cwd=checkout)
    annex_info = _run(["git", "annex", "info", "--json"], cwd=checkout, capture=True).stdout
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
        "annex_info_json_lines_sha256": hashlib.sha256(annex_info.encode("utf-8")).hexdigest(),
        "available_git_remotes": available_remotes,
        "annex_remote_preferred": PUBLIC_REMOTE,
        "ephemeral_git_identity": {
            "name": "NSD Atlas CI",
            "email": "nsd-atlas-ci@invalid.local"
        }
    }


def _annex_get(checkout: Path, rel: str, expected_size: int, expected_md5: str, events: list[dict]) -> str:
    preferred_cmd = ["git", "annex", "get", "--from", PUBLIC_REMOTE, "--", rel]
    preferred = _run_capture(preferred_cmd, cwd=checkout)
    if preferred.returncode == 0:
        events.append({
            "path": rel,
            "preferred_remote_returncode": 0,
            "retrieval_route": f"explicit:{PUBLIC_REMOTE}",
        })
        return f"explicit:{PUBLIC_REMOTE}"

    whereis = _run_capture(["git", "annex", "whereis", "--json", "--", rel], cwd=checkout)
    remote_info = _run_capture(["git", "remote", "-v"], cwd=checkout)
    diagnostic = {
        "schema": "neurostability-atlas-a2-srm-transport-diagnostic-v0.1",
        "status": "PREFERRED_ANNEX_REMOTE_FAILED_ATTEMPTING_KEY_VERIFIED_AUTOMATIC_FALLBACK",
        "frozen_path": rel,
        "expected_source_annex_identity": {
            "backend": "MD5E",
            "bytes": expected_size,
            "md5": expected_md5,
        },
        "preferred_command": preferred_cmd,
        "preferred_returncode": preferred.returncode,
        "preferred_stdout": preferred.stdout[-12000:],
        "preferred_stderr": preferred.stderr[-12000:],
        "whereis_returncode": whereis.returncode,
        "whereis_stdout": whereis.stdout[-20000:],
        "whereis_stderr": whereis.stderr[-12000:],
        "git_remote_v": remote_info.stdout[-12000:],
        "fallback_policy": "allow git-annex to choose another advertised source for this exact frozen path; accept content only after frozen MD5E size+MD5 verification and additional Atlas SHA-256",
        "reservoir_access": false,
    }
    _write_diagnostic(diagnostic)

    fallback_cmd = ["git", "annex", "get", "--", rel]
    fallback = _run_capture(fallback_cmd, cwd=checkout)
    diagnostic["fallback_command"] = fallback_cmd
    diagnostic["fallback_returncode"] = fallback.returncode
    diagnostic["fallback_stdout"] = fallback.stdout[-12000:]
    diagnostic["fallback_stderr"] = fallback.stderr[-12000:]
    if fallback.returncode != 0:
        diagnostic["status"] = "ANNEX_RETRIEVAL_FAILED_BEFORE_EEG_RECONSTRUCTION"
        _write_diagnostic(diagnostic)
        raise RuntimeError(
            f"annex retrieval failed for frozen pilot path {rel}; "
            f"preferred rc={preferred.returncode}, fallback rc={fallback.returncode}; "
            f"see {DIAGNOSTIC.relative_to(ROOT)}"
        )

    diagnostic["status"] = "PREFERRED_REMOTE_FAILED_AUTOMATIC_FALLBACK_RETRIEVED_PENDING_BYTE_VERIFICATION"
    _write_diagnostic(diagnostic)
    events.append({
        "path": rel,
        "preferred_remote_returncode": preferred.returncode,
        "retrieval_route": "git-annex:auto-fallback",
        "preferred_stderr_tail": preferred.stderr[-2000:],
    })
    return "git-annex:auto-fallback"


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
    transport_events = []
    requested_annex_paths = []
    for subject in cfg["pilot_subjects"]:
        for session in cfg["sessions"]:
            set_rel, channels_rel, eeg_json_rel = _paths(cfg, subject, session)
            annex_target = _url_text(f"{raw_git}/{set_rel}")
            match = ANNEX_RE.search(annex_target)
            if not match:
                raise RuntimeError(f"could not parse MD5E annex identity for {set_rel}: {annex_target}")
            expected_size = int(match.group("size"))
            expected_md5 = match.group("md5").lower()

            requested_annex_paths.append(set_rel)
            retrieval_route = _annex_get(
                checkout, set_rel, expected_size, expected_md5, transport_events
            )
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
                _write_diagnostic({
                    "schema": "neurostability-atlas-a2-srm-transport-diagnostic-v0.1",
                    "status": "SOURCE_ANNEX_IDENTITY_MISMATCH_REFUSED",
                    "frozen_path": set_rel,
                    "retrieval_route": retrieval_route,
                    "expected_bytes": expected_size,
                    "observed_bytes": actual_size,
                    "expected_md5": expected_md5,
                    "observed_md5": actual_md5,
                    "observed_sha256": actual_sha256,
                    "reservoir_access": false,
                })
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
                "retrieval_route": retrieval_route,
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

    # The source checkout is ephemeral and is never uploaded. git-annex stores
    # content in read-only object directories, so cleanup is best-effort only
    # after every frozen object has already passed source size+MD5 verification
    # and been copied to the isolated pilot input tree.
    cleanup_warning = None
    try:
        shutil.rmtree(checkout)
    except Exception as exc:
        cleanup_warning = f"{type(exc).__name__}: {exc}"
        shutil.rmtree(checkout, ignore_errors=True)

    if DIAGNOSTIC.exists():
        diagnostic_sha256 = _hash(DIAGNOSTIC, "sha256")
    else:
        diagnostic_sha256 = None

    return {
        "schema": "neurostability-atlas-a2-srm-input-manifest-v0.1",
        "status": "ALL_FROZEN_INPUTS_RETRIEVED_AND_BYTE_VERIFIED",
        "source_snapshot": cfg["source_snapshot"],
        "annex_checkout": checkout_meta,
        "pilot_subjects": cfg["pilot_subjects"],
        "sessions": cfg["sessions"],
        "requested_annex_path_count": len(requested_annex_paths),
        "reservoir_annex_paths_requested": 0,
        "transport_events": transport_events,
        "transport_diagnostic_sha256_if_present": diagnostic_sha256,
        "ephemeral_checkout_cleanup_warning": cleanup_warning,
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
    if manifest["ephemeral_checkout_cleanup_warning"]:
        print(f"non-blocking cleanup warning: {manifest['ephemeral_checkout_cleanup_warning']}")
    print("A2 SRM INPUT FETCH PASS")


if __name__ == "__main__":
    main()
