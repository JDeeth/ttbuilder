import pytest

from ttbuilder.common.ttime import TTime


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
def test_time_from_hms(args, seconds):
    assert TTime.from_hms(*args).seconds == seconds


@pytest.mark.parametrize(
    "time_str",
    "00:00 00/00 01:00 01:01 01/01 27:00 01:00H 12:05H 12/05H 27:00 27/00".split(),
)
def test_time_to_timetable_str(time_str, ttime_parser):
    assert str(ttime_parser.parse(time_str)) == time_str


def test_float_seconds_are_converted_to_int():
    time = TTime(seconds=3750.0)
    assert str(time) == "01:02H"


def test_time_to_half_minutes():
    assert f"{TTime.from_hms(minutes=5):MH}" == "5"
    assert f"{TTime.from_hms(minutes=5, seconds=15):MH}" == "5"
    assert f"{TTime.from_hms(minutes=5, seconds=30):MH}" == "5H"
    assert f"{TTime.from_hms(minutes=5, seconds=45):MH}" == "5H"


def test_time_truthy():
    assert TTime(seconds=1)
    assert not TTime(seconds=0)


def test_equivalent_from_different_construction_methods():
    a = TTime.from_hms(minutes=2, seconds=30)
    b = TTime(seconds=150)
    assert a == b
