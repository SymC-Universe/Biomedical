#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/BIO_CHI/artifacts/generated/jarus_matlab_compat"
NATIVE_OUT="$ROOT/BIO_CHI/artifacts/generated/jarus_matlab_native"
mkdir -p "$OUT"

# Reuse the pinned-source preparation contract. It verifies the immutable DOI
# archive and all three Reduced2023 MATLAB member hashes before extraction.
bash "$ROOT/BIO_CHI/src/prepare_jarus_matlab_native.sh"

ORIG="$NATIVE_OUT/source/S1_Codes/MATLAB files/Reduced2023"
PATCHED="$OUT/source/S1_Codes/MATLAB files/Reduced2023"
rm -rf "$OUT/source"
mkdir -p "$(dirname "$PATCHED")"
cp -a "$ORIG" "$PATCHED"

python3 - "$ORIG/simulate_reduced.m" "$PATCHED/simulate_reduced.m" "$OUT/compatibility_patch.json" <<'PY'
from __future__ import annotations
import hashlib, json, pathlib, sys
from datetime import datetime, timezone

orig = pathlib.Path(sys.argv[1])
patched = pathlib.Path(sys.argv[2])
manifest = pathlib.Path(sys.argv[3])

expected_orig_sha = "4660bd10fbfeddee2cb2061e79c10b922b3a6c87ae736ee7ef51dfc6a3d5ec8a"
def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

if sha(orig) != expected_orig_sha:
    raise SystemExit("BIO_CHI_JARUS_COMPAT_ORIGINAL_HASH_MISMATCH")
if sha(patched) != expected_orig_sha:
    raise SystemExit("BIO_CHI_JARUS_COMPAT_COPY_HASH_MISMATCH")

before = "    [t, y] = ode23s(@(t, y) reduced(t, y, tnf), [tspan_begin, tspan_end], species(end, :), tnf);"
after = "    [t, y] = ode23s(@(t, y) reduced(t, y, tnf), [tspan_begin, tspan_end], species(end, :), []);"
text = patched.read_text(encoding="utf-8")
count = text.count(before)
if count != 1:
    raise SystemExit(f"BIO_CHI_JARUS_COMPAT_PATCH_TARGET_COUNT_{count}")
text2 = text.replace(before, after, 1)
patched.write_text(text2, encoding="utf-8")

record = {
    "schema_version": "0.1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "audit_type": "mechanical_matlab_solver_call_compatibility_repair",
    "source_failure_run": 35831641361,
    "source_failure_status": "NATIVE_RUNTIME_FAILURE",
    "scientific_endpoint_opened": False,
    "chi_bio_constructed": False,
    "published_source_preserved": True,
    "execution_copy_modified": True,
    "repair_count": 1,
    "original_simulate_reduced_sha256": expected_orig_sha,
    "patched_simulate_reduced_sha256": sha(patched),
    "exact_replacement": {"before": before.strip(), "after": after.strip()},
    "mechanical_justification": (
        "The anonymous ODE function already captures tnf lexically as reduced(t,y,tnf). "
        "In MATLAB ode23s the fourth positional argument is the ODE options structure. "
        "The published numeric tnf value in that slot causes odeget to fail before integration. "
        "Replacing only that invalid options value with [] leaves the RHS, TNF input, parameters, "
        "time span, initial condition, solver family, and every biological/model quantity unchanged."
    ),
    "forbidden_interpretation": "This repair is not an untouched-source reproduction and does not license chi_bio."
}
manifest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))
PY

echo "BIO_CHI_JARUS_MATLAB_COMPAT_PREP_PASS"
