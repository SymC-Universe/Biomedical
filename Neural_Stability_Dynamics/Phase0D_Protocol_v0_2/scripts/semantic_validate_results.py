from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from src.semantic_validation import compare_summary

results = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "results" / "phase0d_v02"
ok, problems = compare_summary(results)
if not ok:
    print("SEMANTIC VALIDATION FAILED")
    for p in problems: print(p)
    raise SystemExit(2)
print("SEMANTIC VALIDATION PASSED")
