from activity import ActivityType
import pytest
from elements import AccelBrake, CajonTime, Location, TrainId
from local_timetable import Activity, LocalTimetable, TimingPoint
from train_category import DwellTimes, PowerType, SpeedClass, TrainType


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
        location=Location("FOUROKS"),
        depart=CajonTime.from_str("00:15"),
        platform="3",
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

    tp = TimingPoint(
        location=Location("ASTON"),
        depart=CajonTime.from_str("00/30"),
    )

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
        location=Location("LCHC"),
        depart=CajonTime.from_str("00/35"),
        platform="2",
        engineering_allowance=CajonTime.from_hms(minutes=1),
        pathing_allowance=CajonTime.from_hms(minutes=2, seconds=30),
    )

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
        location=Location("BLKST"),
        depart=CajonTime.from_str("00:40"),
        request_stop_percent=25,
    )

    xt.assert_equivalent(expected, tp.xml())


@pytest.fixture
def dmu_train_type():
    dwell_times = DwellTimes(10, 45, 180, 60, 240, 300, 120, 300)

    return TrainType(
        id="23F09234",
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        speed_classes=SpeedClass.DMU,
        length_m=60,
        power_type=PowerType.DIESEL,
        dwell_times=dwell_times,
    )


@pytest.fixture
def args_2a01(dmu_train_type):
    return dict(
        train_id=TrainId(id="2A01", uid="ZBB159"),
        depart_time=CajonTime.from_str("00:01"),
        train_type=dmu_train_type,
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
                depart=CajonTime.from_str("00/30"),
            ),
        ],
    )


def test_out_and_back_tt(xml_test_tools, args_2a01):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_2A01.xml")

    tt = LocalTimetable(**args_2a01)

    xt.assert_equivalent(expected, tt.xml())


def test_starting_power_inferred_if_unambiguous():
    tt = LocalTimetable(
        train_id=TrainId(id="0A00", uid="AAA000"),
        train_type=TrainType(power_type=PowerType.TRAMWAY),
    )
    assert tt.initial_power == PowerType.TRAMWAY


def test_starting_power_assumed_if_ambiguous():
    tt = LocalTimetable(
        train_id=TrainId(id="0A00", uid="AAA000"),
        train_type=TrainType(power_type=PowerType.TRAMWAY | PowerType.DIESEL),
    )
    assert tt.initial_power == PowerType.DIESEL


def test_train_starting_in_sim(xml_test_tools, dmu_train_type):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_2A04.xml")

    tt = LocalTimetable(
        train_id=TrainId(id="2A04", uid="ZDC316"),
        train_type=dmu_train_type,
        timing_points=[
            TimingPoint(
                location=Location("FOUROKS"),
                depart=CajonTime.from_str("00:35"),
                platform="3",
            ),
            TimingPoint(
                location=Location("ASTON"),
                depart=CajonTime.from_str("00/45"),
            ),
        ],
    )
    xt.assert_equivalent(expected, tt.xml())


def test_train_terminating_in_sim(xml_test_tools, dmu_train_type):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_2A03.xml")

    train_id = TrainId(id="2A03", uid="ZBD037")
    next_id = TrainId(id="2A04", uid="ZDC316")
    next_activity = Activity(
        activity_type=ActivityType.NEXT, associated_train_id=next_id
    )

    tt = LocalTimetable(
        train_id=train_id,
        train_type=dmu_train_type,
        depart_time=CajonTime.from_str("00:20"),
        entry_point=Location("EASTON"),
        description="Entry with 3-car DMU type",
        timing_points=[
            TimingPoint(
                location=Location("FOUROKS"),
                depart=CajonTime.from_str("00:35"),
                platform="3",
                activities=[next_activity],
            )
        ],
    )

    xt.assert_equivalent(expected, tt.xml())
