import pytest
from elements import AccelBrake, CajonTime, TrainId, Version


def test_cajontime_from_hms():
    assert CajonTime.from_hms(0, 0, 3).seconds == 3
    assert CajonTime.from_hms(0, 2, 3).seconds == 123
    assert CajonTime.from_hms(1, 2, 3).seconds == 3723
    assert CajonTime.from_hms(0, 2).seconds == 120
    assert CajonTime.from_hms(27).seconds == 97200


def test_cajontime_from_str():
    time = CajonTime.from_str("27:00")
    assert time.seconds == 97200


def test_cajontime_truthy():
    assert CajonTime(seconds=1)
    assert not CajonTime(seconds=0)


def test_version_major_only():
    v = Version(3)
    assert v.text == "3"


def test_version_major_minor():
    v = Version(5, 15)
    assert v.text == "5.15"


def test_version_full():
    v = Version(1, 34, 2)
    assert v.text == "1.34.2"


@pytest.mark.parametrize(
    "ab,value",
    [
        (AccelBrake.VERY_LOW, 0),
        (AccelBrake.LOW, 1),
        (AccelBrake.MEDIUM, 2),
        (AccelBrake.HIGH, 3),
        (AccelBrake.VERY_HIGH, 4),
    ],
)
def test_accel_brake(ab, value):
    assert ab.value == value


@pytest.mark.parametrize(
    "params,expected_xml",
    [
        ({"id": "1A01"}, "<AssociatedTrain>1A01</AssociatedTrain>"),
        ({"id": "2A04", "uid": "ZDC316"}, "<AssociatedUID>ZDC316</AssociatedUID>"),
    ],
)
def test_train_id(xml_test_tools, params, expected_xml):
    xt = xml_test_tools
    train = TrainId(**params)
    expected = xt.fromstr(expected_xml)
    assert xt.agnostic_diff(expected, train.activity_xml()) == []
