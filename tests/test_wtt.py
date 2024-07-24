import pytest
from xmldiff import main as xd
from lxml import etree

from wtt import Wtt, SimSigSim
from version import Version
from cajontime import CajonTime


def test_make_header(xml_helper):
    sample = etree.parse(
        "tests/sample/aston_none_TimetableHeader.xml",
        parser=etree.XMLParser(remove_blank_text=True),
    )

    wtt = Wtt(
        sim=SimSigSim("aston", Version(5, 15)),
        start_time=CajonTime.from_str("00:00"),
        end_time=CajonTime.from_str("27:00"),
    )
    header = wtt.header("None.WTT")

    print()
    print(etree.tostring(sample).decode())
    print(etree.tostring(header).decode())
    assert xml_helper.agnostic_diff(sample, header) == []

    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str
