from activity import Activity, ActivityType
from elements import CajonTime, Location, TrainId
from local_timetable import TimingPoint
import pytest


@pytest.mark.parametrize(
    "expected,text",
    [
        (TimingPoint("FOUROKS", "12:05"), "FOUROKS 12:05"),
        (TimingPoint("FOUROKS", "12:05:30"), "FOUROKS 12:05H"),
        (TimingPoint("FOUROKS", "12/05"), "FOUROKS 12/05"),
        (TimingPoint("FOUROKS", "12:05", platform="3"), "FOUROKS.3 12:05"),
    ],
)
def test_timing_point_from_text(xml_test_tools, expected, text):
    xt = xml_test_tools

    result = TimingPoint.from_str(text)

    xt.assert_equivalent(expected.xml(), result.xml())


@pytest.mark.parametrize(
    "pt,expected",
    [
        (TimingPoint("FOUROKS", "12:05"), "FOUROKS 12:05"),
        (TimingPoint("FOUROKS", "12:05", platform=3), "FOUROKS.3 12:05"),
        (TimingPoint("FOUROKS", "12:05H", platform=3), "FOUROKS.3 12:05H"),
        (
            TimingPoint("FOUROKS", "25:05", engineering_allowance=CajonTime(150)),
            "FOUROKS 25:05 [2H]",
        ),
        (
            TimingPoint("FOUROKS", "25:05", pathing_allowance=CajonTime(270)),
            "FOUROKS 25:05 (4H)",
        ),
        (
            TimingPoint("FOUROKS", "25:05", performance_allowance=CajonTime(120)),
            "FOUROKS 25:05 <2>",
        ),
        (
            TimingPoint("FOUROKS", "12:05", activities=[Activity.next("2Z99")]),
            "FOUROKS 12:05 N:2Z99",
        ),
        (
            TimingPoint(
                location="FOUROKS",
                depart=CajonTime.from_hms(25, 5),
                engineering_allowance=CajonTime(150),
                pathing_allowance=CajonTime(270),
                performance_allowance=CajonTime(120),
                activities=[Activity.next("2Z99")],
            ),
            "FOUROKS 25:05 [2H] (4H) <2> N:2Z99",
        ),
    ],
)
def test_timing_point_to_str(pt, expected):
    # ignoring whitespace
    assert str(pt).split() == expected.split()
