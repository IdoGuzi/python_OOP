import GraphAlgoInterface
import GraphInterface

from queue import PriorityQueue
import math
import matplotlib


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: GraphInterface):
        self.graph = g
    
    def get_graph(self):
        return self.graph

    def connected_component(self, id1: int):
        if self.graph is None or self.graph.get_all_v()[id1] is None:
            return []
        component = []
        dist, parents = self.dijkstra(id1)
        nodes = self.graph.get_all_v()
        for node_id in dist.keys():
            if dist[node_id] is not math.inf:
                component.append(nodes[node_id])
        return component

    def connected_components(self):
        seen = {}
        components = []
        for n in self.graph.get_all_v().keys():
            seen[n] = False
        for n in self.graph.get_all_v().keys():
            if seen[n]:
                continue
            component = self.connected_component(n)
            for v in component:
                seen[v.id] = True
            components.append(component)
        return components

    def shortest_path(self, id1: int, id2: int):
        dist, parents = self.dijkstra(id1)
        path = list()
        path.append(id2)
        node = parents.get(id2)
        path.append(node.id)
        while parents.get(node.id) is not None:
            node = parents.get(node.id)
            path.append(node.id)
        return dist[id2], path

    def dijkstra(self, src: int):
        parents = {}
        dist = {}
        visited = {}
        queue = PriorityQueue()
        for n in self.graph.get_all_v:
            dist[n.id] = math.inf
            parents[n.id] = None
            visited[n.id] = False
        dist[src] = 0
        queue.put((dist[src], src))
        while queue.qsize() != 0:
            v = queue.get()
            for u in self.graph.all_out_edges_of_node(v.id):
                if not visited[u[0]]:
                    if dist[u[0]] < dist[v.id] + u[1]:
                        dist[u[0]] = dist[v.id] + u[1]
                        queue.put((dist[u[0]], u[0]))
            visited[v.id] = True
        return dist, parents
