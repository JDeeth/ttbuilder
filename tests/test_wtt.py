from activity import Activity, ActivityType
from local_timetable import LocalTimetable, TimingPoint
import pytest
from lxml import etree
import zipfile

from train_category import DwellTimes, SpeedClass, TrainType
from wtt import Wtt, SimSigSim
from elements import AccelBrake, CajonTime, Location, PowerType, TrainId, Version


@pytest.fixture
def aston_none():
    return Wtt(
        sim=SimSigSim("aston", Version(5, 23, 4)),
        name="empty",
        start_time=CajonTime.from_str("00:00"),
        end_time=CajonTime.from_str("27:00"),
    )


def test_make_xml_header(xml_test_tools, aston_none):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_empty_TimetableHeader.xml")

    header = aston_none.xml_header()

    xt.assert_equivalent(expected, header)


def test_make_xml_header(xml_test_tools, aston_none):
    xt = xml_test_tools
    header = aston_none.xml_header()

    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str


def test_make_savedtimetable_xml(xml_test_tools, aston_none):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_empty_SavedTimetable.xml")

    saved_timetable = aston_none.xml()
    xt.assert_equivalent(expected, saved_timetable)


def test_header_description_escaped():
    description = """\
<>"'&£ 
(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    wtt = Wtt(
        sim=SimSigSim("aston", Version(5, 15)), name="asdf", description=description
    )

    header = wtt.xml_header()
    xml_description = header.find("./Description").text
    assert (
        xml_description
        == """&lt;&gt;&quot;&apos;&amp;&#x00A3;&#x00A0;\n(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    )


def test_wtt_compilation(tmp_path, aston_none, xml_test_tools):
    xt = xml_test_tools

    filename = f"{tmp_path}.wtt"
    aston_none.compile_wtt(filename)
    assert zipfile.is_zipfile(filename)
    with zipfile.ZipFile(filename) as wtt:
        assert sorted(wtt.namelist()) == ["SavedTimetable.xml", "TimetableHeader.xml"]

        with wtt.open("TimetableHeader.xml") as header:
            expected = aston_none.xml_header()
            result = xt.fromstr(header.read())
            xt.assert_equivalent(expected, result)
        with wtt.open("SavedTimetable.xml") as timetable:
            expected = aston_none.xml()
            result = xt.fromstr(timetable.read())
            xt.assert_equivalent(expected, result)


def test_basic_wtt(xml_test_tools):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/basic_SavedTimetable.xml")

    dmu = TrainType(
        id="23F09234",
        description="3-car DMU",
        accel=AccelBrake.HIGH,
        max_speed_mph=70,
        length_m=60,
        speed_classes=SpeedClass.DMU,
        dwell_times=DwellTimes(10, 45, 180, 60, 240, 300, 120, 300),
        power_type=PowerType.DIESEL,
    )

    tt_2a04 = LocalTimetable(
        train_id=TrainId("2A04", "ZDC316"),
        train_type=dmu,
        timing_points=[
            TimingPoint(
                location=Location(tiploc="FOUROKS"),
                depart=CajonTime(2100),
                platform="3",
            ),
            TimingPoint(
                location=Location(tiploc="ASTON"), depart=CajonTime(2700, passing=True)
            ),
        ],
    )
    tt_2a03 = LocalTimetable(
        train_id=TrainId("2A03", "ZBD037"),
        train_type=dmu,
        entry_point=Location(tiploc="EASTON"),
        depart_time=CajonTime(1200),
        timing_points=[
            TimingPoint(
                location=Location(tiploc="FOUROKS"),
                depart=CajonTime(2100),
                platform=3,
                activities=[
                    Activity(
                        activity_type=ActivityType.NEXT,
                        associated_train_id=tt_2a04.train_id,
                    ),
                ],
            )
        ],
    )
    tt_2a01 = LocalTimetable(
        train_id=TrainId("2A01", "ZBB159"),
        train_type=dmu,
        description="Entry with 3-car DMU type",
        entry_point=Location(tiploc="EASTON"),
        depart_time=CajonTime(60),
        timing_points=[
            TimingPoint(
                location=Location(tiploc="FOUROKS"),
                depart=CajonTime(900),
                platform=3,
            ),
            TimingPoint(
                location=Location(tiploc="ASTON"),
                depart=CajonTime(1800, passing=True),
            ),
        ],
    )

    tt = Wtt(
        sim=SimSigSim("aston", Version(5, 23, 4)),
        name="basic_tt",
        description="",
        train_types=[dmu],
        workings=[tt_2a01, tt_2a03, tt_2a04],
    )

    xt.assert_equivalent(expected, tt.xml())
