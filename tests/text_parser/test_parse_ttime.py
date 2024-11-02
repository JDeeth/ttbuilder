import pytest

from ttbuilder.common.ttime import Allowance, TTime


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "01:00",
            TTime.from_hms(
                hours=1, minutes=0, seconds=0, stop_mode=TTime.StopMode.STOPPING
            ),
        ),
        (
            "01/00",
            TTime.from_hms(
                hours=1, minutes=0, seconds=0, stop_mode=TTime.StopMode.PASSING
            ),
        ),
        (
            "01:01",
            TTime.from_hms(
                hours=1, minutes=1, seconds=0, stop_mode=TTime.StopMode.STOPPING
            ),
        ),
        (
            "27:00",
            TTime.from_hms(
                hours=27, minutes=0, seconds=0, stop_mode=TTime.StopMode.STOPPING
            ),
        ),
        (
            "01:00H",
            TTime.from_hms(
                hours=1, minutes=0, seconds=30, stop_mode=TTime.StopMode.STOPPING
            ),
        ),
        (
            "29/59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.PASSING
            ),
        ),
        (
            "29w59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.DWELL_TIME
            ),
        ),
        (
            "29*59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.IF_REQUIRED
            ),
        ),
        (
            "29r59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.REQUEST_STOP
            ),
        ),
        (
            "29d59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.SET_DOWN
            ),
        ),
        (
            "29t59H",
            TTime.from_hms(
                hours=29, minutes=59, seconds=30, stop_mode=TTime.StopMode.THROUGH_LINE
            ),
        ),
    ],
)
def test_time_from_str(text, expected, ttparser):
    assert expected == ttparser.parse_ttime(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("0", TTime(0)),
        ("0h", TTime(30)),
        ("4", TTime(240)),
        ("59½", TTime.from_hms(minutes=59, seconds=30)),
    ],
)
def test_tmin_from_str(text, expected, ttparser):
    assert expected == ttparser.parse_tmin(text)


@pytest.mark.parametrize(
    "text,eng,path,perf",
    [
        ("[0]", "0", None, None),
        ("[1]", "1", None, None),
        ("(2½)", None, "2h", None),
        ("<3½>", None, None, "3h"),
        ("[4] <3½>", "4", None, "3h"),
    ],
)
def test_allowance(text, eng, path, perf, ttparser):
    p = ttparser
    expected = []
    for time, atype in (
        (eng, Allowance.Type.ENGINEERING),
        (path, Allowance.Type.PATHING),
        (perf, Allowance.Type.PERFORMANCE),
    ):
        if time is None:
            continue
        expected.append(Allowance(p.parse_tmin(time), atype))
    assert expected == ttparser.parse_allowances(text)
