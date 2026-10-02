from tools.verify_v02_cd06_environment import verify

def test_cd06_environment_contract():
    out=verify()
    assert out["status"]=="PASS"
