import pytest
from elements import AccelBrake, CajonTime, TrainId, Version


@pytest.mark.parametrize(
    "args,seconds",
    [
        ((0, 0, 3), 3),
        ((0, 2, 3), 123),
        ((1, 2, 3), 3723),
        ((0, 2), 120),
        ((27,), 97200),
    ],
)
def test_cajontime_from_hms(args, seconds):
    assert CajonTime.from_hms(*args).seconds == seconds


@pytest.mark.parametrize(
    "text,seconds",
    [
        ("01:00", 3600),
        ("01:01", 3600 + 60),
        ("01:01:01", 3600 + 60 + 1),
        ("27:00", 27 * 3600),
        ("01:00H", 3600 + 30),
        ("12:05H", 12 * 3600 + 5 * 60 + 30),
    ],
)
def test_cajontime_from_str(text, seconds):
    time = CajonTime.from_str(text)
    assert time.seconds == seconds


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
