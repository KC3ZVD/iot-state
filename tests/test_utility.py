from kc3zvd.iot_state import utility

def test_utility():
    assert utility.normalize('TesT sTRiNg') == 'test_string'
