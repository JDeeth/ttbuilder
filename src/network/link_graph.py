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
