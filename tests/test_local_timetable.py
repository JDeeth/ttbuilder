import pytest
from elements import AccelBrake, CajonTime, Location
from local_timetable import LocalTimetable, TimingPoint
from train_category import DwellTimes, PowerType, SpeedClass, TrainType


basic_tt_xml = """\
<Timetable>
    <ID>2A01</ID>
    <UID>ZBB159</UID>
    <AccelBrakeIndex>3</AccelBrakeIndex>
    <AsRequiredPercent>50</AsRequiredPercent>
    <Delay>3</Delay>
    <DepartTime>60</DepartTime>
    <Description>Entry with 3-car DMU type</Description>
    <SeedingGap>15</SeedingGap>
    <EntryPoint>EASTON</EntryPoint>
    <MaxSpeed>70</MaxSpeed>
    <SpeedClass>16</SpeedClass>
    <TrainLength>60</TrainLength>
    <Electrification>D</Electrification>
    <StartTraction>D</StartTraction>
    <Category>23F09234</Category>
    <RedSignalMoveOff>10</RedSignalMoveOff>
    <StationForward>45</StationForward>
    <StationReverse>180</StationReverse>
    <TerminateForward>60</TerminateForward>
    <TerminateReverse>240</TerminateReverse>
    <Join>300</Join>
    <Divide>120</Divide>
    <CrewChange>300</CrewChange>
    <Trips>
    <Trip>
        <Location>FOUROKS</Location>
        <DepPassTime>900</DepPassTime>
        <Platform>3</Platform>
    </Trip>
    <Trip>
        <Location>ASTON</Location>
        <DepPassTime>1800</DepPassTime>
        <IsPassTime>-1</IsPassTime>
    </Trip>
    </Trips>
</Timetable>
"""


def test_stopping_timing_point(xml_test_tools):
    xt = xml_test_tools

    tp = TimingPoint(
        location=Location("FOUROKS"),
        depart=CajonTime.from_str("00:15"),
        platform="3",
    )

    expected_str = """
    <Trip>
        <Location>FOUROKS</Location>
        <DepPassTime>900</DepPassTime>
        <Platform>3</Platform>
    </Trip>
    """
    expected = xt.fromstr(expected_str)

    assert xt.agnostic_diff(expected, tp.xml()) == []


def test_passing_timing_point(xml_test_tools):
    xt = xml_test_tools

    tp = TimingPoint(
        location=Location("ASTON"),
        depart=CajonTime.from_str("00:30"),
        passing=True,
    )

    expected_str = """
    <Trip>
        <Location>ASTON</Location>
        <DepPassTime>1800</DepPassTime>
        <IsPassTime>-1</IsPassTime>
    </Trip>
    """
    expected = xt.fromstr(expected_str)

    assert xt.agnostic_diff(expected, tp.xml()) == []


def test_local_tt(xml_test_tools):
    xt = xml_test_tools

    dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)

    train_type = TrainType(
        id="23F09234",
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        speed_classes=SpeedClass.DMU,
        length_m=60,
        power_type=PowerType.DIESEL,
        dwell_times=dwell_times,
    )

    tt = LocalTimetable(
        id="2A01",
        uid="ZBB159",
        depart_time=CajonTime.from_str("00:01"),
        train_type=train_type,
        description="""Entry with 3-car DMU type""",
        delay_min=3,
        entry_point=Location("EASTON"),
        timing_points=[
            TimingPoint(
                location=Location("FOUROKS"),
                depart=CajonTime.from_str("00:15"),
                platform="3",
            ),
            TimingPoint(
                location=Location("ASTON"),
                depart=CajonTime.from_str("00:30"),
                passing=True,
            ),
        ],
    )

    expected = xt.fromstr(basic_tt_xml)
    assert xt.agnostic_diff(expected, tt.xml()) == []
