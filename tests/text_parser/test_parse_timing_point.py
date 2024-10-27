import pytest
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.ttime import TTime


@pytest.mark.parametrize(
    "expected,text",
    [
        (
            TimingPoint("FOUROKS", "12:05"),
            "FOUROKS 12:05",
        ),
        (
            TimingPoint("FOUROKS", "12:05:30"),
            "FOUROKS 12:05H",
        ),
        (
            TimingPoint("FOUROKS", "12/05"),
            "FOUROKS 12/05",
        ),
        (
            TimingPoint(Location("FOUROKS", platform="3"), "12:05"),
            "FOUROKS.3 12:05",
        ),
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
        (
            TimingPoint("FOUROKS", "12:05"),
            "FOUROKS 12:05 <0> [0] (0)",
        ),
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
        # (
        #     TimingPoint("FOUROKS", "12:05", activities=[Activity.next("9Z99")]),
        #     "FOUROKS 12:05 N:9Z99",
        # ),
        # (
        #     TimingPoint(
        #         "FOUROKS",
        #         "12:05",
        #         activities=[
        #             Activity.detach_engine_front("0A01"),
        #             Activity.join("0A01"),
        #         ],
        #     ),
        #     "FOUROKS 12:05 DEF:0A01 J:0A01",
        # ),
    ],
)
def test_parse_timing_point_from_text(expected, text, ttime_parser):
    assert expected == ttime_parser.parse(text)
