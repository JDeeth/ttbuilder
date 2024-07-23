import pytest
from xmldiff import main as xd
from lxml import etree

from wtt import Wtt, SimSigSim
from version import Version
from cajontime import CajonTime


def test_make_header():
    sample = etree.parse("tests/sample/aston_none_TimetableHeader.xml")
    sim = SimSigSim("aston", Version(5, 15))
    wtt = Wtt(
        sim=sim,
        start_time=CajonTime.from_str("00:00"),
        end_time=CajonTime.from_str("27:00"),
    )
    header = wtt.header("None.WTT")
    header_str = etree.tostring(header, pretty_print=True).decode()
    assert "<Description></Description>" in header_str
    parsed_header = etree.fromstring(header_str)
    assert xd.diff_trees(sample, parsed_header) == []
