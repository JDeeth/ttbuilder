import pytest

from ttbuilder.common.activity import Activity
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.ttime import TTime


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
    tp = TimingPoint(location="FOUROKS", depart=TTime.from_hms(0, 15), platform="3")
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
    tp = TimingPoint(location="ASTON", depart=TTime.from_hms(0, 30, passing=True))

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
        depart=TTime.from_hms(0, 35, passing=True),
        platform="2",
        engineering_allowance=TTime.from_hms(minutes=1),
        pathing_allowance=TTime.from_hms(minutes=2, seconds=30),
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
        depart=TTime.from_str("00:40"),
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
        (
            TimingPoint("FOUROKS", "12:05", engineering_allowance=TTime(90)),
            "FOUROKS 12:05 [1H]",
        ),
        (
            TimingPoint("FOUROKS", "12:05", pathing_allowance=TTime(30)),
            "FOUROKS 12:05 (0H)",
        ),
        (
            TimingPoint("FOUROKS", "12:05", performance_allowance=TTime(120)),
            "FOUROKS 12:05 <2>",
        ),
        (TimingPoint("FOUROKS", "12:05"), "FOUROKS 12:05 <0> [0] (0)"),
        (
            TimingPoint(
                "FOUROKS",
                "12:05",
                pathing_allowance=TTime(30),
                engineering_allowance=TTime(90),
            ),
            "FOUROKS 12:05 [1H] (0H)",
        ),
        (
            TimingPoint(
                "FOUROKS",
                "12:05",
                pathing_allowance=TTime(30),
                engineering_allowance=TTime(90),
            ),
            "FOUROKS 12:05 (0H) [1H]",
        ),
        (
            TimingPoint("FOUROKS", "12:05", activities=[Activity.next("9Z99")]),
            "FOUROKS 12:05 N:9Z99",
        ),
        (
            TimingPoint(
                "FOUROKS",
                "12:05",
                activities=[
                    Activity.detach_engine_front("0A01"),
                    Activity.join("0A01"),
                ],
            ),
            "FOUROKS 12:05 DEF:0A01 J:0A01",
        ),
    ],
)
def test_timing_point_from_text(expected, text):
    assert expected == TimingPoint.from_str(text)


@pytest.mark.parametrize(
    "pt,expected",
    [
        (TimingPoint("FOUROKS", "12:05"), "FOUROKS 12:05"),
        (TimingPoint("FOUROKS", "12:05", platform=3), "FOUROKS.3 12:05"),
        (TimingPoint("FOUROKS", "12:05H", platform=3), "FOUROKS.3 12:05H"),
        (
            TimingPoint("FOUROKS", "25:05", engineering_allowance=TTime(150)),
            "FOUROKS 25:05 [2H]",
        ),
        (
            TimingPoint("FOUROKS", "25:05", pathing_allowance=TTime(270)),
            "FOUROKS 25:05 (4H)",
        ),
        (
            TimingPoint("FOUROKS", "25:05", performance_allowance=TTime(120)),
            "FOUROKS 25:05 <2>",
        ),
        (
            TimingPoint("FOUROKS", "12:05", activities=[Activity.next("2Z99")]),
            "FOUROKS 12:05 N:2Z99",
        ),
        (
            TimingPoint(
                location="FOUROKS",
                depart=TTime.from_hms(25, 5),
                engineering_allowance=TTime(150),
                pathing_allowance=TTime(270),
                performance_allowance=TTime(120),
                activities=[Activity.next("2Z99")],
            ),
            "FOUROKS 25:05 [2H] (4H) <2> N:2Z99",
        ),
    ],
)
def test_timing_point_to_str(pt, expected):
    # ignoring whitespace
    assert str(pt).split() == expected.split()


LCHC_TIMING_POINT = """\
<Trip>
    <Location>LCHC</Location>
    <Platform>2</Platform>
    <DownDirection>-1</DownDirection>
    <PrevPathEndDown>-1</PrevPathEndDown>
    <NextPathStartDown>-1</NextPathStartDown>
</Trip>
""".strip()


def test_from_xml(xml_test_tools):
    xt = xml_test_tools
    xml_root = xt.fromstr(LCHC_TIMING_POINT)

    tp = TimingPoint.from_xml(xml_root)
    assert tp.location.tiploc == "LCHC"
