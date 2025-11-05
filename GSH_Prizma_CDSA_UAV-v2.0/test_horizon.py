from gsh_prizma.core.link_models import d_horizon_km

def test_horizon_sanity():
    assert abs(d_horizon_km(1,1) - 7.14) < 0.2
    assert abs(d_horizon_km(5,5) - 15.9) < 0.5
