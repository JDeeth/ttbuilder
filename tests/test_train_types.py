import pytest

from cajontime import CajonTime
from train_types import AccelBrake, DwellTimes, PowerType, SpeedClass, TrainType

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


def test_dwell_time_can_populate_from_int():
    dt = DwellTimes(terminate_forward=150)
    assert dt.terminate_forward == CajonTime.from_hms(minutes=2, seconds=30)


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


dmu_traintype = """
<TrainCategory ID="23F09234">
    <Description>3-car DMU</Description>
    <AccelBrakeIndex>3</AccelBrakeIndex>
    <IsFreight>0</IsFreight>
    <CanUseGoodsLines>0</CanUseGoodsLines>
    <MaxSpeed>70</MaxSpeed>
    <TrainLength>60</TrainLength>
    <SpeedClass>16</SpeedClass>
    <PowerToWeightCategory>0</PowerToWeightCategory>
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
    <Electrification>D</Electrification>
</TrainCategory>
"""


def test_train_types_get_unique_default_ids():
    tt1 = TrainType()
    tt2 = TrainType()
    assert tt1.id != tt2.id


# @pytest.mark.xfail
def test_make_dmu_train_type(xml_test_tools):
    xt = xml_test_tools
    dmu_dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)
    dmu = TrainType(
        id="23F09234",
        description="3-car DMU",
        length=60,
        accel=AccelBrake.HIGH,
        max_speed=70,
        speed_classes=SpeedClass.DMU,
        dwell_times=dmu_dwell_times,
        power_type=PowerType.DIESEL,
    )
    expected = xt.fromstr(dmu_traintype)
    assert xt.agnostic_diff(expected, dmu.xml()) == []
