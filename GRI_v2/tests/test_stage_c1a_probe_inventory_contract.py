import hashlib
from pathlib import Path

from src.run_stage_c1a_probe_inventory import nonblank, split_tokens, stream_source_probe_ids


def test_semicolon_split_preserves_empty_tokens():
    assert split_tokens("GENE1;;GENE3") == ["GENE1", "", "GENE3"]
    assert split_tokens("") == [""]


def test_nonblank_common_snp_flag_logic():
    assert nonblank("rs123") is True
    assert nonblank("") is False
    assert nonblank("NA") is False
    assert nonblank(None) is False


def test_source_probe_stream_reads_first_field_and_hashes_entire_file(tmp_path: Path):
    p = tmp_path / "tiny.tsv"
    raw = b"probe\tS1\tS2\n\"cg0001\"\t0.11\t0.22\ncg0002\t0.33\t0.44\n"
    p.write_bytes(raw)
    ids, observed_sha, header_columns = stream_source_probe_ids(p)
    assert ids == ["cg0001", "cg0002"]
    assert observed_sha == hashlib.sha256(raw).hexdigest()
    assert header_columns == 3
