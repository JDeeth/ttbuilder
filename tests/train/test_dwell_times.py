import pytest

from ttbuilder.common.ttime import TTime
from ttbuilder.train.dwell_times import DwellTimes


@pytest.fixture(name="populated_dt")
def fixture_populated_dt():
    return """
<DwellTimes>
    <RedSignalMoveOff>10</RedSignalMoveOff>
    <StationForward>45</StationForward>
    <StationReverse>180</StationReverse>
    <TerminateForward>60</TerminateForward>
    <TerminateReverse>240</TerminateReverse>
    <Join>300</Join>
    <Divide>120</Divide>
    <CrewChange>300</CrewChange>
</DwellTimes>
"""


def test_default_dwell_times(xt):
    expected = xt.fromstr("<DwellTimes/>")

    dt = DwellTimes()

    xt.assert_equivalent(expected, dt.xml())


def test_dwell_time_can_populate_from_int():
    expected = TTime.from_hms(minutes=2, seconds=30)
    dt = DwellTimes(terminate_forward=150)
    assert dt.terminate_forward == expected


def test_populated_dwell_times(xt, populated_dt):
    expected = xt.fromstr(populated_dt)

    dt = DwellTimes(
        red_signal_move_off=TTime.from_hms(seconds=10),
        station_forward=TTime.from_hms(seconds=45),
        station_reverse=TTime.from_hms(minutes=3),
        terminate_forward=TTime.from_hms(seconds=60),
        terminate_reverse=TTime(240),
    )
    dt.join = TTime.from_hms(minutes=5)
    dt.divide = TTime(120)
    dt.crew_change = TTime.from_hms(0, 5)

    xt.assert_equivalent(expected, dt.xml())
