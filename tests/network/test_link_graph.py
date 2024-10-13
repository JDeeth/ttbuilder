import pytest
from contextlib import nullcontext as does_not_raise

from network.link_graph import LinkGraph, NoPath, LocationNotFound
from conftest import xfail


@pytest.fixture
def aston():
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


def test_mandatory_points_parsed(aston):
    assert aston.mandatory_points() == set(
        "ALRWAS LCHTTVJ LCHTTVH LCHC BLKST FOUROKS".split()
    )


@pytest.mark.parametrize(
    "dep,dest,path,expectation",
    [
        ("LCHTTVH", "SUTCO", "LCHTTVH LCHC BLKST FOUROKS SUTCO", does_not_raise()),
        ("LCHTTVH", "WYGN", "LCHTTVH LCHC BLKST FOUROKS WYGN", does_not_raise()),
        ("SUTCO", "ASTON", "SUTCO ASTON", does_not_raise()),
        ("ELCHTTVL", "WICHNRJ", "ELCHTTVL LCHTTVJ ALRWAS WICHNRJ", does_not_raise()),
        ("WYGN", "WYGN", "WYGN", does_not_raise()),
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
def test_find_minimal_path(aston, dep, dest, path, expectation):
    with expectation:
        assert aston.min_path(dep, dest) == path.split()
