from __future__ import annotations
from pathlib import Path
import hashlib

EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".git"}
EXCLUDED_FILES = {"FREEZE_MANIFEST.sha256", "CANDIDATE_MANIFEST.sha256"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def iter_frozen_files(root: Path):
    root = Path(root)
    for p in sorted(root.rglob("*")):
        if not p.is_file(): continue
        rel = p.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in rel.parts): continue
        if rel.parts and rel.parts[0] == "results": continue
        if p.name in EXCLUDED_FILES: continue
        yield p


def build_manifest_text(root: Path) -> str:
    root = Path(root)
    lines = [f"{sha256_file(p)}  {p.relative_to(root).as_posix()}" for p in iter_frozen_files(root)]
    return "\n".join(lines) + "\n"


def parse_manifest(path: Path) -> dict[str, str]:
    out = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        if not raw.strip(): continue
        digest, rel = raw.split("  ", 1)
        out[rel] = digest
    return out


def verify_manifest(root: Path, manifest_path: Path) -> tuple[bool, list[str]]:
    root = Path(root); manifest_path = Path(manifest_path)
    if not manifest_path.exists(): return False, ["FREEZE_MANIFEST_MISSING"]
    expected = parse_manifest(manifest_path)
    current = {p.relative_to(root).as_posix():sha256_file(p) for p in iter_frozen_files(root)}
    problems = []
    for rel, digest in sorted(expected.items()):
        if rel not in current: problems.append(f"MISSING:{rel}")
        elif current[rel] != digest: problems.append(f"HASH_MISMATCH:{rel}")
    for rel in sorted(set(current) - set(expected)): problems.append(f"UNFROZEN_FILE:{rel}")
    return not problems, problems
