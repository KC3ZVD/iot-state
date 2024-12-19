import kc3zvd.iot_state.utility as utility

def test_utility():
    assert utility.normalize('TesT sTRiNg') == 'test_string'
