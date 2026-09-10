from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from src.integrity import verify_manifest

ok, problems = verify_manifest(root, root / "FREEZE_MANIFEST.sha256")
if not ok:
    print("FREEZE MANIFEST VERIFICATION FAILED")
    for p in problems: print(p)
    raise SystemExit(2)
print("FREEZE MANIFEST VERIFIED")
