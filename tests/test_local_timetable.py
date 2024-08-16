import pytest
from elements import AccelBrake, CajonTime, Location
from local_timetable import Activity, LocalTimetable, TimingPoint
from train_category import DwellTimes, PowerType, SpeedClass, TrainType


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
        id="2A01",
        uid="ZBB159",
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
                depart=CajonTime.from_str("00:30"),
                passing=True,
            ),
        ],
    )


def test_out_and_back_tt(xml_test_tools, args_2a01):
    xt = xml_test_tools

    tt = LocalTimetable(**args_2a01)

    expected = xt.fromfile("tests/sample/aston_2A01.xml")
    assert xt.agnostic_diff(expected, tt.xml()) == []


def test_starting_power_inferred_if_unambiguous():
    tt = LocalTimetable(
        id="0A00",
        uid="AAA000",
        train_type=TrainType(power_type=PowerType.TRAMWAY),
    )
    assert tt.initial_power == PowerType.TRAMWAY


def test_starting_power_assumed_if_ambiguous():
    tt = LocalTimetable(
        id="0A00",
        uid="AAA000",
        train_type=TrainType(power_type=PowerType.TRAMWAY | PowerType.DIESEL),
    )
    assert tt.initial_power == PowerType.DIESEL


def test_train_starting_in_sim(xml_test_tools, dmu_train_type):
    xt = xml_test_tools

    tt = LocalTimetable(
        id="2A04",
        uid="ZDC316",
        train_type=dmu_train_type,
        timing_points=[
            TimingPoint(
                location=Location("FOUROKS"),
                depart=CajonTime.from_str("00:35"),
                platform="3",
            ),
            TimingPoint(
                location=Location("ASTON"),
                passing=True,
            ),
        ],
    )
    expected = xt.fromfile("tests/sample/aston_2A04.xml")
    assert xt.agnostic_diff(expected, tt.xml()) == []


def test_train_terminating_in_sim(xml_test_tools, dmu_train_type):
    xt = xml_test_tools

    tt = LocalTimetable(
        id="2A03",
        uid="ZBD037",
        train_type=dmu_train_type,
        depart_time=CajonTime.from_str("00:20"),
        entry_point=Location("EASTON"),
        description="Entry with 3-car DMU type",
        timing_points=[
            TimingPoint(
                location=Location("FOUROKS"),
                depart=CajonTime.from_str("00:35"),
                platform="3",
                activities=[Activity(next_uid="ZDC316")],
            )
        ],
    )

    expected = xt.fromfile("tests/sample/aston_2A03.xml")
    assert xt.agnostic_diff(expected, tt.xml()) == []
