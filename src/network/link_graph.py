from dataclasses import dataclass
from elements import CajonTime
from local_timetable import TimingPoint
import networkx as nx


class NoPath(Exception):
    pass


class LocationNotFound(Exception):
    pass


class LinkGraph:
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
        try:
            result = nx.shortest_path(self._route_graph, from_pt, to_pt)
            return result[1:-1]
        except nx.exception.NetworkXNoPath as error:
            raise NoPath(error)
        except nx.exception.NodeNotFound as error:
            raise LocationNotFound(error)

    def min_via_points(self, from_pt, to_pt):
        result = self.all_via_points(from_pt, to_pt)
        mandatory = lambda pt: self._route_graph.nodes[pt].get("mandatory")
        result = [pt for pt in result if mandatory(pt)]
        return result

    def has_tiploc(self, tiploc: str):
        return tiploc in self._route_graph.nodes

    def extract(self, path: str):
        points = [TimingPoint.from_str(line) for line in path.strip().splitlines()]
        result = []
        for a, b in zip(points, points[1:]):
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
                    depart = CajonTime(seconds=start + interval * i, passing=True)
                    result.append(TimingPoint(location=tiploc, depart=depart))
            if self.has_tiploc(b.location.tiploc):
                result.append(b)

        return "\n".join(str(pt) for pt in result)
