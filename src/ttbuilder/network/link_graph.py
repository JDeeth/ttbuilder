import networkx as nx

from ttbuilder.common.timing_point import TimingPoint
from ttbuilder.common import ttime


class NoPath(Exception):
    # pylint: disable=missing-class-docstring
    pass


class LocationNotFound(Exception):
    # pylint: disable=missing-class-docstring
    pass


class LinkGraph:
    """Timing point network. Can represent a single SimSig sim or the wider network"""

    def __init__(self, routes: set[list[str]], mandatory_points: set[str]):
        self._route_graph = nx.MultiDiGraph()
        self._route_graph.add_nodes_from(
            (pt for rt in routes for pt in rt), mandatory=False
        )
        self._route_graph.add_nodes_from(mandatory_points, mandatory=True)
        self._route_graph.add_edges_from(
            (a, b) for rt in routes for a, b in zip(rt, rt[1:])
        )

    def all_via_points(self, from_pt, to_pt):
        """All points on shortest route by number of nodes omitting start and end. A-E = B,C,D"""
        try:
            result = nx.shortest_path(self._route_graph, from_pt, to_pt)
            return result[1:-1]
        except nx.exception.NetworkXNoPath as error:
            raise NoPath(error) from error
        except nx.exception.NodeNotFound as error:
            raise LocationNotFound(error) from error

    def min_via_points(self, from_pt, to_pt):
        """Mandatory points only on the shortest route by number of nodes"""
        result = self.all_via_points(from_pt, to_pt)

        def mandatory(pt):
            return self._route_graph.nodes[pt].get("mandatory")

        result = [pt for pt in result if mandatory(pt)]
        return result

    def has_tiploc(self, tiploc: str):
        """Tiploc is in graph"""
        return tiploc in self._route_graph.nodes

    def extract(self, timing_points: list[TimingPoint]):
        """Pulls section of longer timetable where it overlaps this"""
        result = []
        for a, b in zip(timing_points, timing_points[1:]):
            tiploc_a = a.location.tiploc
            if not result:
                # prepend E for entrypoint
                tiploc_a = f"E{tiploc_a}"
            if not self.has_tiploc(tiploc_a):
                continue
            if not result:
                result.append(a)
            try:
                missing_tiplocs = self.min_via_points(tiploc_a, b.location.tiploc)
            except LocationNotFound:
                break
            if missing_tiplocs:
                start = a.depart.seconds
                interval = (b.depart.seconds - a.depart.seconds) / (
                    len(missing_tiplocs) + 1
                )
                for i, tiploc in enumerate(missing_tiplocs, start=1):
                    depart = ttime.Passing.from_hms(seconds=start + interval * i)
                    result.append(TimingPoint(location=tiploc, depart=depart))
            if self.has_tiploc(b.location.tiploc):
                result.append(b)

        return "\n".join(str(pt) for pt in result)
