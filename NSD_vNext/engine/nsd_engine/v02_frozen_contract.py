"""NSD v0.2 frozen scientific identity validator.

Mechanical-only guard for the prospectively frozen v0.2 packet.  This module
does not evaluate scientific outcomes or assign scientific verdicts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class FrozenContractError(RuntimeError):
    """Raised when a frozen scientific identity is missing or mismatched."""


def _repo_root() -> Path:
    # .../NSD_vNext/engine/nsd_engine/v02_frozen_contract.py -> repository root
    return Path(__file__).resolve().parents[3]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha_bytes(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def git_blob_sha(path: Path) -> str:
    return git_blob_sha_bytes(path.read_bytes())


def _iter_bound_files(value: Any):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("blob"), str):
            yield value["path"], value["blob"]
        for child in value.values():
            yield from _iter_bound_files(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_bound_files(child)


def _derive_parent_seed(index: int) -> int:
    if not 0 <= index < 16:
        raise ValueError("replicate index out of frozen range")
    base = f"NSD-NB1-v0.2-B01|replicate|{index}"
    retry = 0
    while True:
        text = base if retry == 0 else f"{base}|retry|{retry}"
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(digest[:8], "big", signed=False) % ((1 << 63) - 1)
        if seed != 0:
            return seed
        retry += 1


def validate_frozen_science(repo_root: Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else _repo_root()
    freeze_path = root / "NSD_vNext/control/V0_2_FINAL_SCIENTIFIC_FREEZE_v0.1.json"
    if not freeze_path.exists():
        raise FrozenContractError("final scientific freeze record is missing")
    freeze = _load_json(freeze_path)

    if freeze.get("status") != "SCIENTIFIC_PACKET_FROZEN_IMPLEMENTATION_NOT_YET_AUTHORIZED":
        raise FrozenContractError("unexpected scientific-freeze status")
    if freeze.get("execution_authorized") is not False:
        raise FrozenContractError("scientific freeze must not itself authorize execution")
    if freeze.get("scientific_outcomes_opened") is not False:
        raise FrozenContractError("scientific outcomes must remain unopened at this stage")

    checked: list[str] = []
    for rel, expected in _iter_bound_files(freeze):
        path = root / rel
        if not path.exists():
            raise FrozenContractError(f"missing frozen artifact: {rel}")
        observed = git_blob_sha(path)
        if observed != expected:
            raise FrozenContractError(
                f"FROZEN_CONTRACT_VIOLATION: {rel} blob {observed} != {expected}"
            )
        checked.append(rel)

    seeds_path = root / "NSD_vNext/control/NB1_PACKET_SEEDS_v0.2.json"
    seeds = _load_json(seeds_path)
    if seeds.get("rng") != "PCG64DXSM" or seeds.get("replicate_count") != 16:
        raise FrozenContractError("N-B1 RNG identity mismatch")
    observed_seeds = [int(x) for x in seeds.get("seeds", [])]
    expected_seeds = [_derive_parent_seed(i) for i in range(16)]
    if observed_seeds != expected_seeds:
        raise FrozenContractError("N-B1 final seeds do not match frozen derivation rule")
    if len(set(observed_seeds)) != len(observed_seeds) or any(x == 0 for x in observed_seeds):
        raise FrozenContractError("N-B1 final seed uniqueness/nonzero contract failed")

    f = _load_json(root / "NSD_vNext/control/NB1_PACKET_FUNCTION_TRUTHS_v0.1.json")
    l = _load_json(root / "NSD_vNext/control/NB1_PACKET_LIMIT_TRUTHS_v0.1.json")
    n1_ids = {x["id"] for x in f["truths"]} | {x["id"] for x in l["truths"]}
    n23 = _load_json(root / "NSD_vNext/control/NB23_EXHAUSTIVE_SUITE_CANDIDATE_v0.1.json")
    n23_ids = set(n23["members"])
    if n1_ids & n23_ids:
        raise FrozenContractError("cross-lane case identity overlap")
    if n23.get("primary_recoverability") != "DETERMINISTIC_NOISELESS_SAMPLED_OBSERVATION":
        raise FrozenContractError("N-B2/N-B3 primary recoverability identity mismatch")
    if n23.get("stochastic_extension") != "NOT_AUTHORIZED_WITHOUT_SEPARATE_PACKET_APQ":
        raise FrozenContractError("unexpected N-B2/N-B3 stochastic extension state")

    return {
        "status": "PASS",
        "design_baseline_id": freeze["design_baseline_id"],
        "checked_bound_artifacts": len(set(checked)),
        "nb1_case_count": len(n1_ids),
        "nb1_seed_count": len(observed_seeds),
        "nb23_case_count": len(n23_ids),
        "cross_lane_case_overlap": False,
        "scientific_outcomes_opened": False,
        "execution_authorized": False,
    }
