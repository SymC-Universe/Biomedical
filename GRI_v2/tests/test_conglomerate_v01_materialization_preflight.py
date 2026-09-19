import tempfile
from pathlib import Path
import json

from src.preflight_conglomerate_v01_materialization import EXPECTED

def test_expected_small_source_hashes_are_frozen():
    assert EXPECTED["aneuploidy_loh"] == "4e115fd7408a06b002f34678fa46df0b05aa20ac71db57acf535238f37aa64c8"
    assert EXPECTED["cnv_burden"] == "4b63eefb164866a3c49c50c04ee423d3ad1c25540f7cf39e08d997b454a189d0"
    assert EXPECTED["rppa_final"] == "06246573836865589134bd9424189f81b0d9fb436fcbf5e72024225442c400de"
