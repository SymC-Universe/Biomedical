from src.freeze_external_geo_miniml_sources import geo_bucket, miniml_url


def test_geo_bucket():
    assert geo_bucket("GSE59000") == "GSE59nnn"
    assert geo_bucket("GSE65186") == "GSE65nnn"
    assert geo_bucket("GSE262522") == "GSE262nnn"
    assert geo_bucket("GSE237995") == "GSE237nnn"


def test_miniml_url_is_accession_specific():
    assert miniml_url("GSE59000").endswith(
        "/GSE59nnn/GSE59000/miniml/GSE59000_family.xml.tgz"
    )
