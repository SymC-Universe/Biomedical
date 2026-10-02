from nsd_engine.v02_nb23_core import second_order_matrix

def test_nb23_frozen_core_shape():
    s={"omega1":1.0,"zeta1":0.2,"omega2":1.3,"zeta2":0.3,"k12":0.1,"k21":0.0,"c12":0.0,"c21":0.0}
    assert second_order_matrix(s).shape==(4,4)
