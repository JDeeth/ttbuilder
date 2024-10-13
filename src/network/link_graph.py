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

    def mandatory_points(self):
        graph = self._route_graph
        return {pt for pt in graph.nodes if graph.nodes[pt].get("mandatory")}

    def full_path(self, from_pt, to_pt):
        try:
            return nx.shortest_path(self._route_graph, from_pt, to_pt)
        except nx.exception.NetworkXNoPath as error:
            raise NoPath(error)
        except nx.exception.NodeNotFound as error:
            raise LocationNotFound(error)

    def min_path(self, from_pt, to_pt):
        result = self.full_path(from_pt, to_pt)
        result = [
            pt
            for i, pt in enumerate(result)
            if i == 0 or i == len(result) - 1 or pt in self.mandatory_points()
        ]
        return result
