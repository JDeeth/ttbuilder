"""For extracting TIPLOC and entrypoint names from an .SSG (SimSig saved game)"""

from ttbuilder.simsig.ssg import Ssg


def test_extract_locations_from_ssg():
    ssg = Ssg.from_file("tests/sample/cleaned.ssg")
    assert {"EALRWAS", "EBSBYJN", "ECREWBHF"}.issubset(ssg.entry_points)
    assert {"ALRWAS", "AMNGTNJ", "ARMITAG", "ATHRSTN"}.issubset(ssg.timing_points)
