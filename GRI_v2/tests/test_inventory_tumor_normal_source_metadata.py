import json, tempfile
from pathlib import Path
import subprocess, sys

SCRIPT = str(Path(__file__).resolve().parents[1] / "src" / "inventory_tumor_normal_source_metadata.py")


def test_metadata_only_inventory():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        rna = td / "rna.tsv"
        meth = td / "meth.tsv"
        ann = td / "ann.tsv"
        out = td / "out.json"
        rna.write_text('gene\t"TCGA-AA-0001-01A"\t"TCGA-AA-0002-11A"\nG1\tSECRET_TUMOR\tSECRET_NORMAL\n')
        meth.write_text('probe\t"TCGA-AA-0001-01A"\t"TCGA-AA-0002-11A"\nP1\t999\t888\n')
        ann.write_text("aliquot_barcode\tcancer type\tDo_not_use\nTCGA-AA-0001-01A\tTEST\tFalse\nTCGA-AA-0002-11A\tTEST\tFalse\n")
        subprocess.run([
            sys.executable, SCRIPT,
            "--rna", str(rna),
            "--methylation", str(meth),
            "--annotation", str(ann),
            "--out", str(out),
        ], check=True)
        data = json.loads(out.read_text())
        assert data["molecular_values_read"] is False
        assert data["outcome_sealed"] is True
        assert data["rna_header_tcga_samples"] == 2
        assert data["methylation_header_tcga_samples"] == 2
        assert data["cancers"][0]["rna_tumor_01_n"] == 1
        assert data["cancers"][0]["rna_normal_11_n"] == 1
        assert data["cancers"][0]["rna_meth_tumor_overlap_n"] == 1
        assert data["cancers"][0]["rna_meth_normal_overlap_n"] == 1
        assert "SECRET_TUMOR" not in out.read_text()
        assert "SECRET_NORMAL" not in out.read_text()


if __name__ == "__main__":
    test_metadata_only_inventory()
    print("metadata-only firewall test PASS")
