from activity import Activity
from elements import CajonTime
from local_timetable import TimingPoint
import pytest


def test_stopping_timing_point(xml_test_tools):
    xt = xml_test_tools

    expected_str = """
    <Trip>
        <Location>FOUROKS</Location>
        <DepPassTime>900</DepPassTime>
        <Platform>3</Platform>
    </Trip>
    """
    expected = xt.fromstr(expected_str)
    tp = TimingPoint(location="FOUROKS", depart="00:15", platform="3")
    xt.assert_equivalent(expected, tp.xml())


def test_passing_timing_point(xml_test_tools):
    xt = xml_test_tools

    expected_str = """
    <Trip>
        <Location>ASTON</Location>
        <DepPassTime>1800</DepPassTime>
        <IsPassTime>-1</IsPassTime>
    </Trip>
    """
    expected = xt.fromstr(expected_str)
    tp = TimingPoint(location="ASTON", depart="00/30")

    xt.assert_equivalent(expected, tp.xml())


def test_perf_path_times_in_timing_point(xml_test_tools):
    xt = xml_test_tools

    # Allowance times recorded in multiples of 30 seconds
    expected_str = """
        <Trip>
          <Location>LCHC</Location>
          <DepPassTime>2100</DepPassTime>
          <Platform>2</Platform>
          <EngAllowance>2</EngAllowance>
          <PathAllowance>5</PathAllowance>
          <IsPassTime>-1</IsPassTime>
        </Trip>
        """
    expected = xt.fromstr(expected_str)

    tp = TimingPoint(
        location="LCHC",
        depart="00/35",
        platform="2",
        engineering_allowance=CajonTime.from_hms(minutes=1),
        pathing_allowance=CajonTime.from_hms(minutes=2, seconds=30),
    )

    xt.assert_equivalent(expected, tp.xml())


def test_request_stop_percent(xml_test_tools):
    xt = xml_test_tools

    expected_str = """
        <Trip>
          <Location>BLKST</Location>
          <DepPassTime>2400</DepPassTime>
          <RequestPercent>25</RequestPercent>
        </Trip>
        """
    expected = xt.fromstr(expected_str)

    tp = TimingPoint(
        location="BLKST",
        depart=CajonTime.from_str("00:40"),
        request_stop_percent=25,
    )

    xt.assert_equivalent(expected, tp.xml())


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
