import pytest

from ttbuilder.common.ttime import Allowance, TMin, TTime


@pytest.mark.parametrize(
    "text,expected",
    [
        ("01:00", TTime.from_hms(hours=1, minutes=0, seconds=0, passing=False)),
        ("01/00", TTime.from_hms(hours=1, minutes=0, seconds=0, passing=True)),
        ("01:01", TTime.from_hms(hours=1, minutes=1, seconds=0, passing=False)),
        ("27:00", TTime.from_hms(hours=27, minutes=0, seconds=0, passing=False)),
        ("01:00H", TTime.from_hms(hours=1, minutes=0, seconds=30, passing=False)),
        ("29/59H", TTime.from_hms(hours=29, minutes=59, seconds=30, passing=True)),
    ],
)
def test_time_from_str(text, expected, ttparser):
    assert expected == ttparser.parse_ttime(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("0", TMin(0)),
        ("0h", TMin(0, True)),
        ("4", TMin(4, False)),
        ("59½", TMin(59, True)),
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
