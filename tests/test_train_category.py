import pytest

from elements import AccelBrake, CajonTime
from train_category import (
    DwellTimes,
    PowerType,
    SpeedClass,
    TrainType,
    Weight,
)


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
    expected = xt.fromstr("<DwellTimes/>")
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


@pytest.mark.parametrize(
    "pt,string",
    [
        (PowerType.AC_OVERHEAD, "O"),
        (PowerType.DC_3RAIL, "3"),
        (PowerType.DC_4RAIL, "4"),
        (PowerType.DIESEL, "D"),
        (PowerType.DC_OVERHEAD, "V"),
        (PowerType.TRAMWAY, "T"),
        (PowerType.SIM_1, "X1"),
        (PowerType.SIM_2, "X2"),
        (PowerType.SIM_3, "X3"),
        (PowerType.SIM_4, "X4"),
        (PowerType.DC_3RAIL | PowerType.AC_OVERHEAD | PowerType.DC_OVERHEAD, "O3V"),
    ],
)
def test_power_type_string(pt, string):
    assert pt.str() == string


@pytest.mark.parametrize(
    "sc,value",
    [
        (SpeedClass.EPS_E, 1),
        (SpeedClass.EPS_D, 2),
        (SpeedClass.HST, 4),
        (SpeedClass.EMU, 8),
        (SpeedClass.DMU, 16),
        (SpeedClass.SPRINTER, 32),
        (SpeedClass.CS_67, 64),
        (SpeedClass.MGR, 128),
        (SpeedClass.TGV_373, 256),
        (SpeedClass.LOCO_H, 512),
        (SpeedClass.METRO, 1024),
        (SpeedClass.WES_442, 2048),
        (SpeedClass.TRIPCOCK, 4096),
        (SpeedClass.STEAM, 8192),
        (SpeedClass.SIM_1, 16777216),
        (SpeedClass.SIM_2, 33554432),
        (SpeedClass.SIM_3, 67108864),
        (SpeedClass.SIM_4, 134217728),
        (SpeedClass.TGV_373 | SpeedClass.EMU | SpeedClass.HST, 4 + 8 + 256),
    ],
)
def test_speedclass(sc, value):
    assert sc.value == value


@pytest.mark.parametrize(
    "weight,value",
    [
        (Weight.LIGHT, 1),
        (Weight.NORMAL, 0),
        (Weight.HEAVY, 2),
    ],
)
def test_weight(weight, value):
    assert weight.value == value


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


def test_make_dmu_train_type(xml_test_tools):
    xt = xml_test_tools
    dmu_dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)
    dmu = TrainType(
        id="23F09234",
        description="3-car DMU",
        length_m=60,
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        speed_classes=SpeedClass.DMU,
        dwell_times=dmu_dwell_times,
        power_type=PowerType.DIESEL,
    )
    expected = xt.fromstr(dmu_traintype)
    assert xt.agnostic_diff(expected, dmu.xml()) == []


no_power_traintype = """
<TrainCategory ID="ED5BFABD">
    <Description>No power</Description>
    <AccelBrakeIndex>2</AccelBrakeIndex>
    <IsFreight>0</IsFreight>
    <CanUseGoodsLines>0</CanUseGoodsLines>
    <MaxSpeed>90</MaxSpeed>
    <TrainLength>20</TrainLength>
    <SpeedClass>0</SpeedClass>
    <PowerToWeightCategory>0</PowerToWeightCategory>
    <DwellTimes/>
</TrainCategory>
"""


def test_no_power_train_type(xml_test_tools):
    xt = xml_test_tools
    tt = TrainType(
        id="ED5BFABD",
        description="No power",
        max_speed_mph=90,
        length_m=20,
        power_type=PowerType.NONE,
    )
    expected = xt.fromstr(no_power_traintype)
    assert xt.agnostic_diff(expected, tt.xml()) == []


def test_train_type_description_punctuation(xml_test_tools):
    tt = TrainType(
        description="""Punctuation "a" 'b' & £5""",
    )
    assert (
        tt.xml().find("./Description").text
        == "Punctuation &quot;a&quot; &apos;b&apos; &amp; &#x00A3;5"
    )
