from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT.parent / ".github" / "workflows" / "gri-v2-stage-c1a-annotation-source.yml"
EXPORTER = ROOT / "src" / "export_stage_c1a_annotation.R"


def test_c1a_source_gate_does_not_resolve_minfi_circular_dependency():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    exporter = EXPORTER.read_text(encoding="utf-8")
    assert "bioc::minfi" not in workflow
    assert 'install.packages(ann_tar' not in exporter
    assert "library(pkg" not in exporter


def test_c1a_export_reads_frozen_tarball_dataframes_directly():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    exporter = EXPORTER.read_text(encoding="utf-8")
    assert 'BiocManager::install("S4Vectors"' in workflow
    assert "untar(ann_tar" in exporter
    assert "library(S4Vectors)" in exporter
    assert "Other|Locations|SNPs" in exporter
    assert "direct_frozen_tarball_dataframes_no_package_install" in exporter
