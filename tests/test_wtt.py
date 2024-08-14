import pytest
from lxml import etree
import zipfile

from wtt import Wtt, SimSigSim
from elements import CajonTime, Version


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
    assert xt.agnostic_diff(expected, header) == []


def test_make_xml_header(xml_test_tools, aston_none):
    xt = xml_test_tools
    header = aston_none.xml_header()

    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str


def test_make_savedtimetable_xml(xml_test_tools, aston_none):
    xt = xml_test_tools
    expected = xt.fromfile("tests/sample/aston_empty_SavedTimetable.xml")

    saved_timetable = aston_none.xml()
    assert xt.agnostic_diff(expected, saved_timetable) == []


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
            assert xt.agnostic_diff(expected, result) == []
        with wtt.open("SavedTimetable.xml") as timetable:
            expected = aston_none.xml()
            result = xt.fromstr(timetable.read())
            assert xt.agnostic_diff(expected, result) == []
