from cajontime import CajonTime


def test_from_hms():
    assert CajonTime.from_hms(0, 0, 3).seconds == 3
    assert CajonTime.from_hms(0, 2, 3).seconds == 123
    assert CajonTime.from_hms(1, 2, 3).seconds == 3723
    assert CajonTime.from_hms(0, 2).seconds == 120
    assert CajonTime.from_hms(27).seconds == 97200


def test_from_str():
    time = CajonTime.from_str("27:00")
    assert time.seconds == 97200
