from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[1]; O=R/'results'/'phase0d_v01'; O.mkdir(parents=True,exist_ok=True)
inc=[]
for rr in ['src','configs','tests','scripts']:
    for p in sorted((R/rr).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts: inc.append(p)
for n in ['README_FIRST.md','PREREGISTRATION.md','SCIENTIFIC_CONTRACT.md','RATIONALE_THREE_LAYER.md','PRE_RUN_FREEZE.json','CALIBRATION_AUDIT.md','run_phase0d.py','local_runner.py','.gitignore']:
    p=R/n
    if p.exists(): inc.append(p)
lines=[f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(R).as_posix()}" for p in sorted(set(inc))]
(O/'CODE_MANIFEST.sha256').write_bytes(('\n'.join(lines)+'\n').encode('utf-8'))
print(f'WROTE {len(lines)} manifest entries')
