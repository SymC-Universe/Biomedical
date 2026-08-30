from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "src" / "run_stage_c1a_windows.py"
WORKFLOW = ROOT.parent / ".github" / "workflows" / "gri-v2-stage-c1a-annotation-source.yml"


def test_windows_handoff_only_prompts_for_local_methylation_tsv():
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("pick(") == 2  # function definition plus exactly one call
    assert 'here / "stage_c1a_annotation_export.tsv.gz"' in text
    assert 'here / "stage_c1a_chen_crossreactive_probe_ids.txt"' in text
    assert 'here / "STAGE_C1A_ANNOTATION_SOURCE_SUMMARY.json"' in text
    assert "BUNDLED C1A FILE MISSING" in text


def test_source_artifact_manifest_is_extraction_root_relative():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "(cd stage_c1a_source_gate && sha256sum" in text
    manifest_block = text.split("(cd stage_c1a_source_gate && sha256sum", 1)[1].split(")", 1)[0]
    assert "stage_c1a_source_gate/" not in manifest_block
