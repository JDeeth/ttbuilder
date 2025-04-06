import pytest

from ttbuilder.common.location import Location
from ttbuilder.common.train_id import TrainId
from ttbuilder.common.ttime import TTime
from ttbuilder.simsig.local_timetable import LocalTimetable
from ttbuilder.train.accel_brake import AccelBrake
from ttbuilder.train.dwell_times import DwellTimes
from ttbuilder.train.power_type import PowerType
from ttbuilder.train.speed_class import SpeedClass
from ttbuilder.train.train_category import TrainCategory


@pytest.fixture(name="dmu_train_type")
def fixture_dmu_train_type():
    dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)

    return TrainCategory(
        id="23F09234",
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        speed_classes=SpeedClass.DMU,
        length_m=60,
        power_type=PowerType.DIESEL,
        dwell_times=dwell_times,
    )


@pytest.fixture(name="args_2a01")
def fixture_args_2a01(dmu_train_type, ttparser):
    tt_str = """
EASTON    00:01
FOUROKS.3 00:15
ASTON     00/30
    """.strip()

    timing_points = [ttparser.parse_timing_point(line) for line in tt_str.splitlines()]
    initial, timing_points = timing_points[0], timing_points[1:]

    return {
        "train_id": TrainId(id="2A01", uid="ZBB159"),
        "depart_time": initial.depart,
        "train_type": dmu_train_type,
        "description": """Entry with 3-car DMU type""",
        "delay_min": 3,
        "entry_point": initial.location,
        "timing_points": timing_points,
    }


def test_out_and_back_tt(xt, args_2a01):
    expected = xt.fromfile("tests/sample/aston_2A01.xml")

    tt = LocalTimetable(**args_2a01)

    xt.assert_equivalent(expected, tt.xml())


def test_starting_power_inferred_if_unambiguous():
    tt = LocalTimetable(
        train_id=TrainId(id="0A00", uid="AAA000"),
        train_type=TrainCategory(power_type=PowerType.TRAMWAY),
    )
    assert tt.initial_power == PowerType.TRAMWAY


def test_starting_power_assumed_if_ambiguous():
    tt = LocalTimetable(
        train_id=TrainId(id="0A00", uid="AAA000"),
        train_type=TrainCategory(power_type=PowerType.TRAMWAY | PowerType.DIESEL),
    )
    assert tt.initial_power == PowerType.DIESEL


def test_train_starting_in_sim(xt, dmu_train_type, ttparser):
    expected = xt.fromfile("tests/sample/aston_2A04.xml")

    tt = LocalTimetable(
        train_id=TrainId(id="2A04", uid="ZDC316"),
        train_type=dmu_train_type,
        timing_points=[
            ttparser.parse_timing_point("FOUROKS.3 00:35"),
            ttparser.parse_timing_point("ASTON     00/45"),
        ],
    )
    xt.assert_equivalent(expected, tt.xml())


def test_train_terminating_in_sim(xt, dmu_train_type, ttparser):
    expected = xt.fromfile("tests/sample/aston_2A03.xml")

    train_id = TrainId(id="2A03", uid="ZBD037")

    tt = LocalTimetable(
        train_id=train_id,
        train_type=dmu_train_type,
        depart_time=TTime.from_hms(0, 20),
        entry_point=Location("EASTON"),
        description="Entry with 3-car DMU type",
        timing_points=[ttparser.parse_timing_point("FOUROKS.3 00:35 N:2A04/ZDC316")],
    )

    xt.assert_equivalent(expected, tt.xml())


ANGLESEA_OUT_AND_BACK = """\
<Timetable>
    <ID>2S01</ID>
    <AccelBrakeIndex>2</AccelBrakeIndex>
    <AsRequiredPercent>50</AsRequiredPercent>
    <Description>Anglesea Sidings &gt; Lichfield City &gt; Anglesea Sidings</Description>
    <SeedingGap>15</SeedingGap>
    <EntryPoint>EANGLSDG</EntryPoint>
    <MaxSpeed>90</MaxSpeed>
    <TrainLength>20</TrainLength>
    <Electrification>D</Electrification>
    <StartTraction>D</StartTraction>
    <Trips>
        <Trip>
            <Location>LCHC</Location>
            <Platform>2</Platform>
            <DownDirection>-1</DownDirection>
            <PrevPathEndDown>-1</PrevPathEndDown>
            <NextPathStartDown>-1</NextPathStartDown>
        </Trip>
        <Trip>
            <Location>LCHCAS</Location>
            <PrevPathEndDown>-1</PrevPathEndDown>
        </Trip>
        <Trip>
            <Location>LCHC</Location>
            <DownDirection>-1</DownDirection>
            <NextPathStartDown>-1</NextPathStartDown>
        </Trip>
        <Trip>
            <Location>LCHCCS</Location>
            <PrevPathEndDown>-1</PrevPathEndDown>
        </Trip>
        <Trip>
            <Location>LCHC</Location>
            <Platform>2</Platform>
        </Trip>
        <Trip>
            <Location>ANGLSDG</Location>
        </Trip>
    </Trips>
</Timetable>
""".strip()


def test_basic_from_xml(xt):
    xml_root = xt.fromstr(ANGLESEA_OUT_AND_BACK)

    lt = LocalTimetable.from_xml(xml_root)
    assert lt.train_id.id == "2S01"
    assert lt.description == "Anglesea Sidings > Lichfield City > Anglesea Sidings"
    assert lt.entry_point == Location("EANGLSDG")
    assert [
        pt.location.tiploc for pt in lt.timing_points
    ] == "LCHC LCHCAS LCHC LCHCCS LCHC ANGLSDG".split()


ASTON_1M45_HEADER = """
<Timetable>
    <ID>1M45</ID>
    <UID>ZCB858</UID>
    <AccelBrakeIndex>2</AccelBrakeIndex>
    <AsRequiredPercent>50</AsRequiredPercent>
    <DepartTime>3510</DepartTime>
    <Description>$template</Description>
    <SeedingGap>15</SeedingGap>
    <EntryPoint>EWICHNRJ</EntryPoint>
    <EntryDecision>decision</EntryDecision>
    <EntryChoice>choice</EntryChoice>
    <MaxSpeed>90</MaxSpeed>
    <Started>-1</Started>
    <TrainLength>220</TrainLength>
    <Electrification>D</Electrification>
    <OriginName>Peterborough</OriginName>
    <DestinationName>Carlisle</DestinationName>
    <OriginTime>81000</OriginTime>
    <DestinationTime>108000</DestinationTime>
    <OperatorCode>operator</OperatorCode>
    <Notes>These are some notes</Notes>
    <StartTraction>D</StartTraction>
    <Category>8933A9B3</Category>
    <RedSignalMoveOff>5</RedSignalMoveOff>
    <StationForward>60</StationForward>
    <StationReverse>60</StationReverse>
    <TerminateForward>60</TerminateForward>
    <TerminateReverse>60</TerminateReverse>
    <Join>300</Join>
    <Divide>120</Divide>
    <CrewChange>180</CrewChange>
    <Trips />
</Timetable>
"""


def test_header_from_xml(xt):
    xml_root = xt.fromstr(ASTON_1M45_HEADER)
    lt = LocalTimetable.from_xml(xml_root)

    assert lt.depart_time == TTime(3510)
    # not implemented:
    # decision
    # choice
    # assert lt.initial_power == PowerType.DIESEL
    # assert lt.as_required_pc == 50
    # assert lt.delay_min ==
    # assert lt.seeding_gap_m == 15
    # operator code

    assert lt.origin == "Peterborough"
    assert lt.destination == "Carlisle"
    assert lt.origin_dep == TTime(81000)
    assert lt.destination_arr == TTime(108000)
    assert lt.notes == "These are some notes"
