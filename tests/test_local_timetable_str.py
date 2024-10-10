from elements import CajonTime, Location
from local_timetable import TimingPoint
import pytest

FOUROKS = Location(tiploc="FOUROKS")


@pytest.mark.parametrize(
    "expected,text",
    [
        (
            TimingPoint(
                location=FOUROKS,
                depart=CajonTime.from_hms(12, 5),
            ),
            "FOUROKS\t12:05",
        ),
        (
            TimingPoint(
                location=FOUROKS,
                depart=CajonTime.from_hms(12, 5, 30),
            ),
            "FOUROKS\t12:05H",
        ),
        (
            TimingPoint(
                location=FOUROKS,
                depart=CajonTime.from_hms(12, 5),
                passing=True,
            ),
            "FOUROKS\t12/05",
        ),
        (
            TimingPoint(
                location=FOUROKS,
                depart=CajonTime.from_hms(12, 5),
                platform="3",
            ),
            "FOUROKS\tP3\t12:05",
        ),
    ],
)
def test_timing_point_from_text(xml_test_tools, expected, text):
    xt = xml_test_tools

    result = TimingPoint.from_str(text)

    xt.assert_equivalent(expected.xml(), result.xml())
