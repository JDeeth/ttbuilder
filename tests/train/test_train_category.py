import pytest

from ttbuilder.train.accel_brake import AccelBrake
from ttbuilder.train.dwell_times import DwellTimes
from ttbuilder.train.power_type import PowerType
from ttbuilder.train.speed_class import SpeedClass
from ttbuilder.train.train_category import TrainCategory


@pytest.fixture(name="dmu_traintype")
def fixture_dmu_traintype():
    return """
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
    tt1 = TrainCategory()
    tt2 = TrainCategory()
    assert tt1.id != tt2.id


def test_make_dmu_train_type(xml_test_tools, dmu_traintype):
    xt = xml_test_tools
    expected = xt.fromstr(dmu_traintype)

    dmu_dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)
    dmu = TrainCategory(
        id="23F09234",
        description="3-car DMU",
        length_m=60,
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        speed_classes=SpeedClass.DMU,
        dwell_times=dmu_dwell_times,
        power_type=PowerType.DIESEL,
    )
    xt.assert_equivalent(expected, dmu.xml())


@pytest.fixture(name="no_power_traintype")
def fixture_no_power_traintype():
    return """
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


def test_no_power_train_type(xml_test_tools, no_power_traintype):
    xt = xml_test_tools
    expected = xt.fromstr(no_power_traintype)

    tt = TrainCategory(
        id="ED5BFABD",
        description="No power",
        max_speed_mph=90,
        length_m=20,
        power_type=PowerType.NONE,
    )

    print(f"{tt = }")

    xt.assert_equivalent(expected, tt.xml())


def test_train_type_description_punctuation():
    tt = TrainCategory(
        description="""Punctuation "a" 'b' & £5""",
    )
    assert (
        tt.xml().find("./Description").text
        == "Punctuation &quot;a&quot; &apos;b&apos; &amp; &#x00A3;5"
    )
