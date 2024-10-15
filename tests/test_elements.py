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
        # HH:MM[:SS] times
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
    assert time.passing is False
    assert time.seconds == seconds


@pytest.mark.parametrize(
    "time_str",
    "00:00 00/00 01:00 01:01 01/01 27:00 01:00H 12:05H 12/05H 27:00 27/00".split(),
)
def test_cajontime_to_timetable_str(time_str):
    assert str(CajonTime.from_str(time_str)) == time_str


def test_float_seconds_are_converted_to_int():
    time = CajonTime(seconds=3750.0, passing=True)
    assert str(time) == "01/02H"


def test_cajontime_to_half_minutes():
    assert f"{CajonTime.from_hms(minutes=5):MH}" == "5"
    assert f"{CajonTime.from_hms(minutes=5, seconds=15):MH}" == "5"
    assert f"{CajonTime.from_hms(minutes=5, seconds=30):MH}" == "5H"
    assert f"{CajonTime.from_hms(minutes=5, seconds=45):MH}" == "5H"


def test_cajontime_passing_from_str():
    time = CajonTime.from_str("01/05H")
    assert time.passing is True
    assert time.seconds == 3600 + 5 * 60 + 30


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
    expected = xt.fromstr(expected_xml)

    train = TrainId(**params)

    xt.assert_equivalent(expected, train.activity_xml())
