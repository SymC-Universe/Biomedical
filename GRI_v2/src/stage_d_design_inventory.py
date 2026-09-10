"""Offline metadata reconciliation. Preserves rows; assigns no scientific eligibility."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path


def run(source, output):
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    manifest = source / 'SAMPLE_MANIFEST_RAW.csv'
    with manifest.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError('Empty manifest')
    counts = collections.Counter(r['geo_accession'] for r in rows)
    fields = ['source_row', 'stage_id', 'series_accession', 'geo_accession',
              'accession_listing_count', 'platform', 'title', 'channel_1_source',
              'channel_2_source', 'processing', 'design_status']
    with (output / 'SOURCE_ROW_INDEX.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for i, r in enumerate(rows, 1):
            w.writerow(dict(zip(fields, [i, r['stage_id'], r['series_accession'],
                r['geo_accession'], counts[r['geo_accession']], r.get('Sample_platform_id',''),
                r.get('Sample_title',''),r.get('Sample_source_name_ch1',''),
                r.get('Sample_source_name_ch2',''),r.get('Sample_data_processing',''),
                'UNRESOLVED_NOT_ANALYSIS_ELIGIBILITY'])))
    stages = {}
    for stage in sorted({r['stage_id'] for r in rows}):
        rs = [r for r in rows if r['stage_id'] == stage]
        stages[stage] = {'source_rows': len(rs),
            'distinct_gsm_accessions': len({r['geo_accession'] for r in rs}),
            'rows_with_second_channel': sum(bool(r.get('Sample_source_name_ch2')) for r in rs),
            'platform_listing_counts': dict(collections.Counter(r.get('Sample_platform_id','') for r in rs)),
            'independent_biological_n': None}
    report = {'status': 'PASS_ROW_PRESERVATION_DESIGN_UNRESOLVED', 'source_rows': len(rows),
        'output_rows': len(rows), 'source_rows_removed': 0, 'stages': stages,
        'biological_matrix_access': False, 'scientific_eligibility_assigned': False,
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(source.iterdir()) if p.is_file()},
        'index_sha256': hashlib.sha256((output/'SOURCE_ROW_INDEX.csv').read_bytes()).hexdigest()}
    (output/'DESIGN_INVENTORY.json').write_text(json.dumps(report, indent=2)+'\n')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True); parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.out), indent=2))
