import pytest

from ttbuilder.common.ttime import TTime


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
def test_time_from_str(text, expected, ttime_parser):
    assert expected == ttime_parser.parse(text)
