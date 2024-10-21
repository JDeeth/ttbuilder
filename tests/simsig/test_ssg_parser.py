"""For extracting TIPLOC and entrypoint names from an .SSG (SimSig saved game)"""

import pytest
from ttbuilder.simsig.ssg import Ssg


@pytest.fixture(name="aston_ssg")
def fixture_aston_ssg():
    return Ssg.from_file("tests/sample/aston_cleaned.ssg")


def test_extract_locations_from_ssg(aston_ssg):
    assert len(aston_ssg.entry_points) == 5
    assert {"EANGLSDG", "EASTON", "ELCHTTVL"}.issubset(aston_ssg.entry_points)
    assert len(aston_ssg.timing_points) == 26
    assert {"ALRWAS", "ANGLSDG", "ASTON", "BLKST"}.issubset(aston_ssg.timing_points)


def test_extract_trains_from_ssg(aston_ssg):
    timetables = aston_ssg.timetables
    assert len(timetables) == 6
    assert set(t.train_id.id for t in timetables) == set(
        "1A01 1A02 2A01 2A02 2L01 2S01".split()
    )
