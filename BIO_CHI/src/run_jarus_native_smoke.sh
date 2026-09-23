#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/BIO_CHI/artifacts/generated/jarus_native_smoke"
SRC="$OUT/source"
mkdir -p "$SRC"

ZIP="$OUT/pone.0286416.s015.zip"
URL="https://doi.org/10.1371/journal.pone.0286416.s015"
EXPECTED="76c51b2b9c44e931f62d4956df2a0aee1b02a481472125d4ae8a0e268ad885f0"

curl -L --fail --retry 3 --retry-delay 2 "$URL" -o "$ZIP"
ACTUAL="$(sha256sum "$ZIP" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "archive SHA mismatch: $ACTUAL" >&2
  exit 2
fi

unzip -q "$ZIP" -d "$SRC"

BASE="$SRC/S1_Codes/MATLAB files/Reduced2023"
for f in reduced.m run_simulate_reduced.m simulate_reduced.m; do
  test -s "$BASE/$f"
done

printf '%s  %s\n' \
  "b42924cf0b30b8dcb15dac1022f93dd57a535501bd0dcdfa96ed516cb7e25c6c" "$BASE/reduced.m" \
  "2acbc191ff2f48bb6f4382a7156b3bf3eaf58122fa06d06c76e3b7a39d51e951" "$BASE/run_simulate_reduced.m" \
  "4660bd10fbfeddee2cb2061e79c10b922b3a6c87ae736ee7ef51dfc6a3d5ec8a" "$BASE/simulate_reduced.m" \
  | sha256sum -c -

cat > "$OUT/native_wrapper.m" <<'EOF'
set(0,'defaultfigurevisible','off');
base = getenv('JARUS_REDUCED_DIR');
outdir = getenv('JARUS_OUTDIR');
cd(base);
addpath(base);
diary(fullfile(outdir,'octave_stdout.txt'));
disp('BIO_CHI_JARUS_NATIVE_SMOKE_BEGIN');
run('run_simulate_reduced.m');
disp('BIO_CHI_JARUS_NATIVE_SMOKE_END');
whos;
save('-mat7-binary', fullfile(outdir,'native_workspace.mat'));
diary off;
EOF

export JARUS_REDUCED_DIR="$BASE"
export JARUS_OUTDIR="$OUT"
octave --no-gui --quiet "$OUT/native_wrapper.m"

python3 - <<'PY'
import hashlib, json, os, pathlib
root=pathlib.Path(os.environ["JARUS_OUTDIR"])
base=pathlib.Path(os.environ["JARUS_REDUCED_DIR"])
def h(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
stdout=(root/"octave_stdout.txt").read_text(errors="replace") if (root/"octave_stdout.txt").exists() else ""
result={
  "schema_version":"0.1",
  "audit_type":"native_source_smoke_only",
  "chi_bio_constructed":False,
  "scientific_endpoint_opened":False,
  "source":{
    "doi_asset":"https://doi.org/10.1371/journal.pone.0286416.s015",
    "archive_sha256":"76c51b2b9c44e931f62d4956df2a0aee1b02a481472125d4ae8a0e268ad885f0",
    "reduced_m_sha256":h(base/"reduced.m"),
    "run_simulate_reduced_m_sha256":h(base/"run_simulate_reduced.m"),
    "simulate_reduced_m_sha256":h(base/"simulate_reduced.m")
  },
  "native_smoke":{
    "begin_marker": "BIO_CHI_JARUS_NATIVE_SMOKE_BEGIN" in stdout,
    "end_marker": "BIO_CHI_JARUS_NATIVE_SMOKE_END" in stdout,
    "workspace_created": (root/"native_workspace.mat").exists(),
    "stdout_sha256": h(root/"octave_stdout.txt") if (root/"octave_stdout.txt").exists() else None,
    "workspace_sha256": h(root/"native_workspace.mat") if (root/"native_workspace.mat").exists() else None
  }
}
(root/"native_smoke_manifest.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
if not all(result["native_smoke"][k] for k in ("begin_marker","end_marker","workspace_created")):
    raise SystemExit("BIO_CHI_JARUS_NATIVE_SMOKE_FAIL")
print("BIO_CHI_JARUS_NATIVE_SMOKE_PASS")
PY
