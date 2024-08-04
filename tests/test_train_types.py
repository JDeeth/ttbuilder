from cajontime import CajonTime
import pytest

from train_types import DwellTimes

empty_dt = """
<DwellTimes>
    <RedSignalMoveOff>0</RedSignalMoveOff>
    <StationForward>0</StationForward>
    <StationReverse>0</StationReverse>
    <TerminateForward>0</TerminateForward>
    <TerminateReverse>0</TerminateReverse>
    <Join>0</Join>
    <Divide>0</Divide>
    <CrewChange>0</CrewChange>
</DwellTimes>
"""

populated_dt = """
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


def test_default_dwell_times(xml_test_tools):
    xt = xml_test_tools
    dt = DwellTimes()
    expected = xt.fromstr(empty_dt)
    assert xt.agnostic_diff(expected, dt.xml()) == []


def test_populated_dwell_times(xml_test_tools):
    xt = xml_test_tools
    dt = DwellTimes(
        red_signal_move_off=CajonTime.from_str("0:00:10"),
        station_forward=CajonTime.from_hms(seconds=45),
        station_reverse=CajonTime.from_hms(minutes=3),
        terminate_forward=CajonTime.from_hms(seconds=60),
        terminate_reverse=CajonTime(240),
    )
    dt.join = CajonTime.from_hms(minutes=5)
    dt.divide = CajonTime(120)
    dt.crew_change = CajonTime.from_str("0:05")
    expected = xt.fromstr(populated_dt)
    assert xt.agnostic_diff(expected, dt.xml()) == []
