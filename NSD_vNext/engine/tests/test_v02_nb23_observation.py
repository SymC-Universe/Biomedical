import numpy as np
from nsd_engine.v02_nb23_observation import recovery_classes,schedule

def test_observation_classes_use_only_arrays():
    obs={"a":np.arange(4.0),"b":np.arange(4.0),"c":np.arange(4.0)+1}
    out=recovery_classes(["a","b","c"],obs)
    assert out["compatible_classes"][0]==["a","b"]
    assert out["hidden_descriptor_accessed"] is False

def test_frozen_96hz_schedule_count():
    assert schedule(96.0).size==3073
