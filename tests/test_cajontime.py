from cajontime import CajonTime


def test_from_hms():
    assert CajonTime.from_hms(0, 0, 3).value == 3
    assert CajonTime.from_hms(0, 2, 3).value == 123
    assert CajonTime.from_hms(1, 2, 3).value == 3723
    assert CajonTime.from_hms(0, 2).value == 120
    assert CajonTime.from_hms(27).value == 97200


def test_from_str():
    time = CajonTime.from_str("27:00")
    assert time.value == 97200
