from activity import Activity
import pytest
from elements import AccelBrake, CajonTime, Location, TrainId
from local_timetable import LocalTimetable
from timing_point import TimingPoint
from train_category import DwellTimes, PowerType, SpeedClass, TrainType


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
    tt_str = """
EASTON    00:01
FOUROKS.3 00:15
ASTON     00/30
    """.strip()

    timing_points = [TimingPoint.from_str(line) for line in tt_str.splitlines()]
    initial, timing_points = timing_points[0], timing_points[1:]

    return dict(
        train_id=TrainId(id="2A01", uid="ZBB159"),
        depart_time=initial.depart,
        train_type=dmu_train_type,
        description="""Entry with 3-car DMU type""",
        delay_min=3,
        entry_point=initial.location,
        timing_points=timing_points,
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
            TimingPoint.from_str("FOUROKS.3 00:35"),
            TimingPoint.from_str("ASTON     00/45"),
        ],
    )
    xt.assert_equivalent(expected, tt.xml())


def test_train_terminating_in_sim(xml_test_tools, dmu_train_type):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_2A03.xml")

    train_id = TrainId(id="2A03", uid="ZBD037")
    next_activity = Activity.next(TrainId(id="2A04", uid="ZDC316"))

    tt = LocalTimetable(
        train_id=train_id,
        train_type=dmu_train_type,
        depart_time=CajonTime.from_str("00:20"),
        entry_point=Location("EASTON"),
        description="Entry with 3-car DMU type",
        timing_points=[TimingPoint.from_str("FOUROKS.3 00:35 N:2A04/ZDC316")],
    )

    xt.assert_equivalent(expected, tt.xml())
