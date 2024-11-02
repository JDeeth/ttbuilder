import pytest

from ttbuilder.common import allowance, ttime


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "01:00",
            ttime.Stopping.from_hms(hours=1, minutes=0, seconds=0),
        ),
        (
            "01/00",
            ttime.Passing.from_hms(hours=1, minutes=0, seconds=0),
        ),
        (
            "01:01",
            ttime.Stopping.from_hms(hours=1, minutes=1, seconds=0),
        ),
        (
            "27:00",
            ttime.Stopping.from_hms(hours=27, minutes=0, seconds=0),
        ),
        (
            "01:00H",
            ttime.Stopping.from_hms(hours=1, minutes=0, seconds=30),
        ),
        (
            "29/59H",
            ttime.Passing.from_hms(hours=29, minutes=59, seconds=30),
        ),
        (
            "29w59H",
            ttime.DwellTime.from_hms(hours=29, minutes=59, seconds=30),
        ),
        (
            "29*59H",
            ttime.IfRequired.from_hms(hours=29, minutes=59, seconds=30),
        ),
        (
            "29r59H",
            ttime.RequestStop.from_hms(hours=29, minutes=59, seconds=30),
        ),
        (
            "29d59H",
            ttime.SetDown.from_hms(hours=29, minutes=59, seconds=30),
        ),
        (
            "29t59H",
            ttime.ThroughLine.from_hms(hours=29, minutes=59, seconds=30),
        ),
    ],
)
def test_time_from_str(text, expected, ttparser):
    assert expected == ttparser.parse_ttime(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("0", ttime.TTime(0)),
        ("0h", ttime.TTime(30)),
        ("4", ttime.TTime(240)),
        ("59½", ttime.TTime.from_hms(minutes=59, seconds=30)),
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
        (eng, allowance.Engineering),
        (path, allowance.Pathing),
        (perf, allowance.Performance),
    ):
        if time is None:
            continue
        expected.append(atype(p.parse_tmin(time)))
    assert expected == ttparser.parse_allowances(text)
