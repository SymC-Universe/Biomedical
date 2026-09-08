from pathlib import Path
import subprocess,sys,time
R=Path(__file__).resolve().parent; O=R/'results'/'phase0_structure'; O.mkdir(parents=True,exist_ok=True); L=O/'RUN_LOG.txt'
def log(s): print(s,flush=True); open(L,'a',encoding='utf-8').write(s+'\n')
def cmd(a): return subprocess.run(a,cwd=R).returncode
if __name__=='__main__':
 L.write_text(''); log('NSD Phase 0 structure-recovery local runner v0.1'); log('Scientific contract: structure first; no EEG labels; no clinical tuning.'); log('[A] Running engineering/unit tests before synthetic execution...')
 rc=cmd([sys.executable,'-m','pytest','-q'])
 if rc: log('TEST GATE FAILED. Synthetic execution not authorized.'); raise SystemExit(rc)
 log('    tests PASS'); log('[B] Writing code/config SHA-256 manifest...'); rc=cmd([sys.executable,'scripts/make_manifest.py'])
 if rc: log('MANIFEST FAILURE. Execution stopped.'); raise SystemExit(rc)
 for a in range(1,4):
  log(f'WORKER ATTEMPT {a}/3'); rc=cmd([sys.executable,'run_phase0_structure.py'])
  if rc==0: log('RUN COMPLETE. Review summary.json and trial_results.csv before changing any configuration.'); raise SystemExit(0)
  log(f'Worker exited with code {rc}. Mechanical retry in 5 seconds; science unchanged.'); time.sleep(5)
 log('RUN DID NOT COMPLETE. Preserve results/phase0_structure and send RUN_LOG.txt.'); raise SystemExit(1)
