import pytest

from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.ttime import Allowance, TMin, TTime


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
    tp = TimingPoint(
        location=Location("FOUROKS", platform="3"),
        depart=TTime.from_hms(0, 15),
    )
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
        location=Location("LCHC", platform="2"),
        depart=TTime.from_hms(
            0,
            35,
            passing=True,
            allowances=[
                Allowance.engineering(TMin(1)),
                Allowance.pathing(TMin(2, True)),
            ],
        ),
    )

    print()
    eng = tp.depart.allowances[0].time
    print(f"{eng=} {eng.thirty_sec=}")
    print(xt.pretty(tp.xml()))

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
        depart=TTime.from_hms(0, 40),
        request_stop_percent=25,
    )

    xt.assert_equivalent(expected, tp.xml())


@pytest.mark.parametrize(
    "pt,expected",
    [
        (
            TimingPoint("FOUROKS", TTime.from_hms(12, 5)),
            "FOUROKS 12:05",
        ),
        (
            TimingPoint(Location("FOUROKS", platform="3"), TTime.from_hms(12, 5)),
            "FOUROKS.3 12:05",
        ),
        (
            TimingPoint(Location("FOUROKS", platform="3"), TTime.from_hms(12, 5, 30)),
            "FOUROKS.3 12:05H",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.from_hms(
                    hours=25,
                    minutes=5,
                    allowances=[
                        Allowance.engineering(TMin(2, True)),
                    ],
                ),
            ),
            "FOUROKS 25:05 [2H]",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.from_hms(
                    hours=25,
                    minutes=5,
                    allowances=[
                        Allowance.pathing(TMin(4, True)),
                    ],
                ),
            ),
            "FOUROKS 25:05 (4H)",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.from_hms(
                    hours=25,
                    minutes=5,
                    allowances=[
                        Allowance.performance(TMin(2, False)),
                    ],
                ),
            ),
            "FOUROKS 25:05 <2>",
        ),
        (
            TimingPoint(
                "FOUROKS", TTime.from_hms(12, 5), activities=[Activity.next("2Z99")]
            ),
            "FOUROKS 12:05 N:2Z99",
        ),
        (
            TimingPoint(
                location="FOUROKS",
                depart=TTime.from_hms(
                    hours=25,
                    minutes=5,
                    allowances=[
                        Allowance.engineering(TMin(2, True)),
                        Allowance.pathing(TMin(4, True)),
                        Allowance.performance(TMin(2, False)),
                    ],
                ),
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
