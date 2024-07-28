import pytest
from lxml import etree
import zipfile

from wtt import Wtt, SimSigSim
from helper import Version
from cajontime import CajonTime


@pytest.fixture
def aston_none():
    return Wtt(
        sim=SimSigSim("aston", Version(5, 15)),
        name="Empty timetable",
        start_time=CajonTime.from_str("00:00"),
        end_time=CajonTime.from_str("27:00"),
    )


def test_make_header(xml_test_tools, aston_none):
    sample = etree.parse(
        "tests/sample/aston_none_TimetableHeader.xml",
        parser=etree.XMLParser(remove_blank_text=True),
    )

    header = aston_none.header()
    assert xml_test_tools.agnostic_diff(sample, header) == []

    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str


def test_make_savedtimetable_xml(xml_test_tools, aston_none):
    sample = etree.parse(
        "tests/sample/aston_none_SavedTimetable.xml",
        parser=etree.XMLParser(remove_blank_text=True),
    )

    saved_timetable = aston_none.saved_timetable()
    assert xml_test_tools.agnostic_diff(sample, saved_timetable) == []


def test_header_description_escaped(xml_test_tools):
    description = """\
<>"'&£ 
(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    wtt = Wtt(
        sim=SimSigSim("aston", Version(5, 15)), name="asdf", description=description
    )

    header = wtt.header()
    xml_description = header.find("./Description").text
    assert (
        xml_description
        == """&lt;&gt;&quot;&apos;&amp;&#x00A3;&#x00A0;\n(less than, greater than, double quote, single quote, ampersand, GBP, nbsp)"""
    )


def test_wtt_compilation(tmp_path, aston_none, xml_test_tools):
    filename = f"{tmp_path}.wtt"
    aston_none.compile_wtt(filename)
    assert zipfile.is_zipfile(filename)
    with zipfile.ZipFile(filename) as wtt:
        assert sorted(wtt.namelist()) == ["SavedTimetable.xml", "TimetableHeader.xml"]

        def parse(file):
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.XML(file.read(), parser=parser)

        with wtt.open("TimetableHeader.xml") as header:
            expected = aston_none.header()
            result = parse(header)
            assert xml_test_tools.agnostic_diff(expected, result) == []
        with wtt.open("SavedTimetable.xml") as timetable:
            expected = aston_none.saved_timetable()
            result = parse(timetable)
            assert xml_test_tools.agnostic_diff(expected, result) == []
