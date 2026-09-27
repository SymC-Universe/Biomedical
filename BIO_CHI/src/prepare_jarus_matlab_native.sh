#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/BIO_CHI/artifacts/generated/jarus_matlab_native"
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

printf '%s  %s\n' \
  "b42924cf0b30b8dcb15dac1022f93dd57a535501bd0dcdfa96ed516cb7e25c6c" "$BASE/reduced.m" \
  "2acbc191ff2f48bb6f4382a7156b3bf3eaf58122fa06d06c76e3b7a39d51e951" "$BASE/run_simulate_reduced.m" \
  "4660bd10fbfeddee2cb2061e79c10b922b3a6c87ae736ee7ef51dfc6a3d5ec8a" "$BASE/simulate_reduced.m" \
  | sha256sum -c -

cat > "$OUT/source_identity.json" <<EOF
{
  "schema_version": "0.1",
  "audit_type": "pinned_published_source_preparation",
  "published_source_modified": false,
  "chi_bio_constructed": false,
  "doi_asset": "$URL",
  "archive_sha256": "$EXPECTED",
  "runtime_freeze": {
    "engine": "MATLAB",
    "release": "R2023b",
    "selection_basis": "publication-era native runtime; frozen before execution outcome"
  }
}
EOF

echo "BIO_CHI_JARUS_MATLAB_SOURCE_PREP_PASS"
