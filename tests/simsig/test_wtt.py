import zipfile
from lxml import etree
import pytest

from ttbuilder.common.activity import Activity
from ttbuilder.common.location import Location
from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common.train_id import TrainId
from ttbuilder.common.ttime import TTime
from ttbuilder.simsig.local_timetable import LocalTimetable
from ttbuilder.simsig.version import Version
from ttbuilder.simsig.wtt import Sim, Wtt
from ttbuilder.train.accel_brake import AccelBrake
from ttbuilder.train.dwell_times import DwellTimes
from ttbuilder.train.power_type import PowerType
from ttbuilder.train.speed_class import SpeedClass
from ttbuilder.train.train_category import TrainCategory


@pytest.fixture(name="aston_none")
def fixture_aston_none():
    return Wtt(
        sim=Sim("aston", Version(5, 23, 4)),
        name="empty",
        start_time=TTime.from_hms(0, 0),
        end_time=TTime.from_hms(27, 0),
    )


def test_make_xml_header(xt, aston_none):
    expected = xt.fromfile("tests/sample/aston_empty_TimetableHeader.xml")

    header = aston_none.xml_header()

    xt.assert_equivalent(expected, header)


def test_xml_header_empty_description_is_empty_element_not_empty_tag(aston_none):
    # empty element: <asdf></asdf>
    # empty tag: <asdf />
    header = aston_none.xml_header()
    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str


def test_make_savedtimetable_xml(xt, aston_none):
    expected = xt.fromfile("tests/sample/aston_empty_SavedTimetable.xml")

    saved_timetable = aston_none.xml()
    xt.assert_equivalent(expected, saved_timetable)


def test_header_description_escaped():
    description = """\
<>"'&£ 
(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    wtt = Wtt(sim=Sim("aston", Version(5, 15)), name="asdf", description=description)

    header = wtt.xml_header()
    xml_description = header.find("./Description").text
    assert (
        xml_description
        == """&lt;&gt;&quot;&apos;&amp;&#x00A3;&#x00A0;\n(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    )


def test_wtt_compilation(tmp_path, aston_none, xt):
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


def test_basic_wtt(xt):
    expected = xt.fromfile("tests/sample/basic_SavedTimetable.xml")

    dmu = TrainCategory(
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
                location=Location(tiploc="FOUROKS", platform="3"),
                depart=TTime.stopping(0, 35),
            ),
            TimingPoint(
                location=Location(tiploc="ASTON"),
                depart=TTime.passing(0, 45),
            ),
        ],
    )
    tt_2a03 = LocalTimetable(
        train_id=TrainId("2A03", "ZBD037"),
        train_type=dmu,
        entry_point=Location(tiploc="EASTON"),
        depart_time=TTime.from_hms(0, 20),
        timing_points=[
            TimingPoint(
                location=Location(tiploc="FOUROKS", platform="3"),
                depart=TTime.stopping(0, 35),
                activities=[Activity.next(tt_2a04.train_id)],
            )
        ],
    )
    tt_2a01 = LocalTimetable(
        train_id=TrainId("2A01", "ZBB159"),
        train_type=dmu,
        description="Entry with 3-car DMU type",
        entry_point=Location(tiploc="EASTON"),
        depart_time=TTime.from_hms(0, 1),
        timing_points=[
            TimingPoint(
                location=Location(tiploc="FOUROKS", platform="3"),
                depart=TTime.stopping(0, 15),
            ),
            TimingPoint(
                location=Location(tiploc="ASTON"),
                depart=TTime.passing(0, 30),
            ),
        ],
    )

    tt = Wtt(
        sim=Sim("aston", Version(5, 23, 4)),
        name="basic_tt",
        description="",
        train_types=[dmu],
        workings=[tt_2a01, tt_2a03, tt_2a04],
    )

    xt.assert_equivalent(expected, tt.xml())
