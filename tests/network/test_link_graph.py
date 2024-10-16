from contextlib import nullcontext as does_not_raise
import pytest

from network.link_graph import LinkGraph, NoPath, LocationNotFound

from tests.conftest import xfail


@pytest.fixture(name="aston")
def fixture_aston():
    routes = [
        # Wichnor Jn > Aston
        "EWICHNRJ ALRWAS LCHTTVJ LCHTTVH LCHC SHNS BLKST BTLRSLA FOUROKS SUTCO WYGN CHSRD ERDNGTN GRAVLYH ASTON",
        # Aston > Wichnor Jn
        "EASTON GRAVLYH ERDNGTN CHSRD WYGN SUTCO FOUROKS BTLRSLA BLKST SHNS LCHC LCHTTVH LCHTTVJ ALRWAS WICHNRJ",
        # Lichfield Low Level, with junction on the branch
        "ELCHTTVL LCHTTVJ ALRWAS LCHTTVJ LCHTTVL",
        # Anglesea Sidings
        "EANGLSDG LCHC ANGLSDG",
        # Lichfield City sidings
        "LCHC LCHCAS LCHC LCHCCS LCHC",
        # disjoint point for testing
        "DISJOINT",
    ]
    routes = [r.split() for r in routes]
    # entry and off-sim departure points do not need to be marked mandatory
    mandatory_points = "ALRWAS LCHTTVJ LCHTTVH LCHC BLKST FOUROKS".split()

    #  o WICHNRJ
    #  o ALRWAS
    # /|
    # o| LCHTTVJ
    # o| LCHTTVL
    #  o LCHTTVH

    # Set up Lichfield TV Jn as a point on the branching line, not the line itself,
    # and marked as mandatory. This makes it mandatory for trains to/from the branch
    # but not for the main line. But it means it cannot be used as a timing point
    # on the main line.

    return LinkGraph(routes, mandatory_points)


@pytest.mark.parametrize(
    "dep,dest,path,expectation",
    [
        ("LCHTTVH", "SUTCO", "LCHC BLKST FOUROKS", does_not_raise()),
        ("LCHTTVH", "WYGN", "LCHC BLKST FOUROKS", does_not_raise()),
        ("SUTCO", "ASTON", "", does_not_raise()),
        ("ELCHTTVL", "WICHNRJ", "LCHTTVJ ALRWAS", does_not_raise()),
        ("WYGN", "WYGN", "", does_not_raise()),
        ("WYGN", "ATLANTIS", "", pytest.raises(LocationNotFound)),
        ("WYGN", "DISJOINT", "", pytest.raises(NoPath)),
        xfail(
            "ELCHTTVL",
            "ASTON",
            "",
            pytest.raises(NoPath),
            reason="paths are not checked for impossible reversals",
        ),
    ],
)
def test_find_min_via_points(aston, dep, dest, path, expectation):
    with expectation:
        assert aston.min_via_points(dep, dest) == path.split()


TRAIN_1M49 = """
TRENTJ      23/55H
SHEETSJ     23/56
SPDN        00/01
DRBY.6      00:13  [4] <4> Runround
DRBY.6      00:40
STSNJN      00/47H [0H]
NSJDRBY     00/48H
BURTNOT     00/53
WICHNRJ     00/58H
LCHTTVJ     01/06H
LCHTTVL     01/09  FL
ARMITAG     01/14H
COLWICH     01/19H
MILFDY      01/21H SL
STAFFRD.5   01/25
NTNB        01/29H
MADELEY     01/37H
CREWBHJ     01/46  [3]
""".strip()


def test_extract_sim_timing_points(aston):
    expected = """
WICHNRJ    00/58H
ALRWAS     01/02H
LCHTTVJ    01/06H
LCHTTVL    01/09
""".strip()
    # 01/02H is a simple average of the times before and after

    aston_path = aston.extract(TRAIN_1M49)

    assert expected == aston_path
