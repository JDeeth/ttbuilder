import pytest
from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.ttime import Allowance, TTime


@pytest.mark.parametrize(
    "expected,text",
    [
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
            ),
            "FOUROKS 12:05",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5, 30),
            ),
            "FOUROKS 12:05H",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.passing(12, 5),
            ),
            "FOUROKS 12/05",
        ),
        (
            TimingPoint(
                Location("FOUROKS", platform="3"),
                TTime.stopping(12, 5),
            ),
            "FOUROKS.3 12:05",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                allowances=[Allowance.engineering(TTime(90))],
            ),
            "FOUROKS 12:05 [1H]",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                allowances=[Allowance.pathing(TTime(30))],
            ),
            "FOUROKS 12:05 (0H)",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                allowances=[Allowance.performance(TTime(120))],
            ),
            "FOUROKS 12:05 <2>",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
            ),
            "FOUROKS 12:05 <0> [0] (0)",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                allowances=[
                    Allowance.engineering(TTime(90)),
                    Allowance.pathing(TTime(30)),
                ],
            ),
            "FOUROKS 12:05 [1H] (0H)",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                allowances=[
                    Allowance.pathing(TTime(30)),
                    Allowance.engineering(TTime(90)),
                ],
            ),
            "FOUROKS 12:05 (0H) [1H]",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                activities=[
                    Activity.next("9Z99"),
                ],
            ),
            "FOUROKS 12:05 N:9Z99",
        ),
        (
            TimingPoint(
                "FOUROKS",
                TTime.stopping(12, 5),
                activities=[
                    Activity.detach_engine_front("0A01"),
                    Activity.join("0A01"),
                ],
            ),
            "FOUROKS 12:05 DEF:0A01 J:0A01",
        ),
        (
            TimingPoint(
                "STSNJN",
                TTime.passing(0, 47, 30),
                allowances=[Allowance.engineering(TTime(30))],
            ),
            "STSNJN  00/47H [0H]",
        ),
    ],
)
def test_parse_timing_point_from_text(expected, text, ttparser):
    assert expected == ttparser.parse_timing_point(text)
