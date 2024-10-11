import networkx as nx
import pytest


@pytest.fixture
def aston():
    # this will mostly go to src eventually
    result = nx.MultiDiGraph()

    # Wichnor Jn to Aston route
    # Every possible timing point for a train travelling this entire route
    all_points = "EWICHNRJ ALRWAS LCHTTVJ LCHTTVH LCHC SHNS BLKST BTLRSLA FOUROKS SUTCO WYGN CHSRD ERDNGTN GRAVLYH ASTON".split()
    # Fewest possible timing points for a train travelling this route
    mandatory_points = "EWICHNRJ ALRWAS LCHTTVH LCHC BLKST FOUROKS ASTON".split()

    result.add_nodes_from(all_points, mandatory=False)
    result.add_nodes_from(mandatory_points, mandatory=True)
    assert result.nodes["LCHC"]["mandatory"] is True
    assert result.nodes["SUTCO"]["mandatory"] is False

    links = set()

    def add_links(stops):
        if len(stops) < 2:
            return
        for n0, n1 in zip(stops, stops[1:]):
            links.add((n0, n1))

    add_links(all_points)
    add_links(mandatory_points)

    result.add_edges_from(links)
    return result


def xfail(*args, reason=None):
    if reason:
        mark = pytest.mark.xfail(reason=reason)
    else:
        mark = pytest.mark.xfail
    return pytest.param(*args, marks=mark)


@pytest.mark.parametrize(
    "dep,dest,path",
    [
        ("LCHTTVH", "SUTCO", "LCHTTVH LCHC BLKST FOUROKS SUTCO"),
        xfail(
            "LCHTTVH",
            "WYGN",
            "LCHTTVH LCHC BLKST FOUROKS WYGN",
            reason="should skip optional points immediately before destination",
        ),
        xfail(
            "SUTCO",
            "ASTON",
            "SUTCO ASTON",
            reason="should skip optional points immediately after departure",
        ),
    ],
)
def test_find_best_path(aston, dep, dest, path):
    assert nx.shortest_path(aston, dep, dest) == path.split()
