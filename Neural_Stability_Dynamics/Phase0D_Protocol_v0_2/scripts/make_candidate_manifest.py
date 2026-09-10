from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from src.integrity import build_manifest_text

out = root / "CANDIDATE_MANIFEST.sha256"
out.write_text(build_manifest_text(root), encoding="utf-8")
print(f"WROTE {out}")
print("P0 ONLY: this is not a freeze manifest and must not authorize P1 execution.")
