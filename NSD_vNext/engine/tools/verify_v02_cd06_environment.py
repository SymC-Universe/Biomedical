import json, platform
from pathlib import Path
import numpy, scipy, pytest

ROOT=Path(__file__).resolve().parents[3]
CFG=json.loads((ROOT/"NSD_vNext/engine/v02_environment_candidate.json").read_text())

def verify():
    actual={"python":platform.python_version(),"numpy":numpy.__version__,"scipy":scipy.__version__,"pytest":pytest.__version__}
    for key in ("numpy","scipy","pytest"):
        if actual[key] != CFG[key]:
            raise RuntimeError(key+" mismatch")
    if not actual["python"].startswith("3.11."):
        raise RuntimeError("python mismatch")
    return {"status":"PASS","actual":actual,"scientific_adjudication":"NOT_PERFORMED_BY_GITHUB"}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
