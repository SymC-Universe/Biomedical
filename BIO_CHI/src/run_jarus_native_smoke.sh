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

export JARUS_REDUCED_DIR="$BASE"
export JARUS_OUTDIR="$OUT"

# Record the smallest source window needed to diagnose MATLAB/Octave runtime
# compatibility. Published source bytes remain untouched and hash-verified.
python3 - <<'PY'
import hashlib, json, os, pathlib, re
base=pathlib.Path(os.environ["JARUS_REDUCED_DIR"])
out=pathlib.Path(os.environ["JARUS_OUTDIR"])
p=base/"simulate_reduced.m"
lines=p.read_text(errors="replace").splitlines()
needle=[i for i,s in enumerate(lines, start=1) if "ode23s" in s]
windows=[]
for n in needle[:5]:
    lo=max(1,n-8); hi=min(len(lines),n+8)
    windows.append({
        "anchor_line":n,
        "start_line":lo,
        "end_line":hi,
        "lines":[{"line":i,"text":lines[i-1]} for i in range(lo,hi+1)]
    })
handles=[]
for i,s in enumerate(lines, start=1):
    if "@(" in s or re.search(r"\bfunction\b", s):
        if any(abs(i-n) <= 20 for n in needle):
            handles.append({"line":i,"text":s})
result={
  "schema_version":"0.1",
  "diagnostic_type":"published_source_runtime_compatibility",
  "published_source_modified":False,
  "scientific_parameters_modified":False,
  "chi_bio_constructed":False,
  "simulate_reduced_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
  "ode23s_call_windows":windows,
  "nearby_function_handles":handles[:20]
}
path=out/"octave_compat_diagnostic.json"
path.write_text(json.dumps(result,indent=2)+"\n")
print("BIO_CHI_JARUS_COMPAT_DIAGNOSTIC")
print(json.dumps(result,indent=2))
PY

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

set +e
octave --no-gui --quiet "$OUT/native_wrapper.m" 2>&1 | tee "$OUT/octave_console.txt"
OCTAVE_RC=${PIPESTATUS[0]}
set -e
export OCTAVE_RC

python3 - <<'PY'
import hashlib, json, os, pathlib
root=pathlib.Path(os.environ["JARUS_OUTDIR"])
base=pathlib.Path(os.environ["JARUS_REDUCED_DIR"])
rc=int(os.environ["OCTAVE_RC"])
def h(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(name):
    p=root/name
    return p.read_text(errors="replace") if p.exists() else ""
stdout=read("octave_stdout.txt")
console=read("octave_console.txt")
begin=("BIO_CHI_JARUS_NATIVE_SMOKE_BEGIN" in stdout) or ("BIO_CHI_JARUS_NATIVE_SMOKE_BEGIN" in console)
end=("BIO_CHI_JARUS_NATIVE_SMOKE_END" in stdout) or ("BIO_CHI_JARUS_NATIVE_SMOKE_END" in console)
workspace=(root/"native_workspace.mat").exists()
status="PASS" if rc == 0 and begin and end and workspace else "MECHANICAL_COMPATIBILITY_FAILURE"
result={
  "schema_version":"0.2",
  "audit_type":"native_source_smoke_only",
  "status":status,
  "chi_bio_constructed":False,
  "scientific_endpoint_opened":False,
  "published_source_modified":False,
  "source":{
    "doi_asset":"https://doi.org/10.1371/journal.pone.0286416.s015",
    "archive_sha256":"76c51b2b9c44e931f62d4956df2a0aee1b02a481472125d4ae8a0e268ad885f0",
    "reduced_m_sha256":h(base/"reduced.m"),
    "run_simulate_reduced_m_sha256":h(base/"run_simulate_reduced.m"),
    "simulate_reduced_m_sha256":h(base/"simulate_reduced.m")
  },
  "native_smoke":{
    "octave_return_code":rc,
    "begin_marker":begin,
    "end_marker":end,
    "workspace_created":workspace,
    "stdout_sha256":h(root/"octave_stdout.txt") if (root/"octave_stdout.txt").exists() else None,
    "console_sha256":h(root/"octave_console.txt") if (root/"octave_console.txt").exists() else None,
    "workspace_sha256":h(root/"native_workspace.mat") if workspace else None,
    "compatibility_diagnostic_sha256":h(root/"octave_compat_diagnostic.json")
  }
}
(root/"native_smoke_manifest.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
print("BIO_CHI_JARUS_NATIVE_SMOKE_" + status)
PY

if [[ "$OCTAVE_RC" -ne 0 ]]; then
  exit "$OCTAVE_RC"
fi

test -s "$OUT/native_workspace.mat"
grep -q 'BIO_CHI_JARUS_NATIVE_SMOKE_END' "$OUT/octave_console.txt" || grep -q 'BIO_CHI_JARUS_NATIVE_SMOKE_END' "$OUT/octave_stdout.txt"
echo "BIO_CHI_JARUS_NATIVE_SMOKE_PASS"
