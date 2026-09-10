import csv
from src.stage_d_design_inventory import run


def test_preserves_repeated_accessions_without_inventing_biological_n(tmp_path):
    source = tmp_path/'source'; source.mkdir()
    path = source/'SAMPLE_MANIFEST_RAW.csv'
    fields = ['stage_id','series_accession','geo_accession','Sample_source_name_ch2']
    with path.open('w', newline='') as f:
        w=csv.writer(f); w.writerow(fields)
        w.writerows([['D2','GSE1','GSM1','treated'],['D2','GSE2','GSM1','treated']])
    original=path.read_bytes()
    report=run(source,tmp_path/'out')
    assert path.read_bytes()==original
    assert report['source_rows']==report['output_rows']==2
    assert report['stages']['D2']['distinct_gsm_accessions']==1
    assert report['stages']['D2']['independent_biological_n'] is None
    with (tmp_path/'out'/'SOURCE_ROW_INDEX.csv').open() as f:
        indexed=list(csv.DictReader(f))
    assert [r['source_row'] for r in indexed]==['1','2']
    assert all(r['accession_listing_count']=='2' for r in indexed)
    assert all(r['channel_2_source']=='treated' for r in indexed)
