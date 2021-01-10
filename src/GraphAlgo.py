from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import *

from queue import PriorityQueue
import math
import json


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: GraphInterface = None):
        self.graph = g
        if g is None:
            self.graph = DiGraph()
    
    def get_graph(self):
        return self.graph

    def load_from_json(self, file_name: str):
        try:
            self.graph = DiGraph()
            with open(file_name, 'r') as f:
                g = json.load(f)
            for n in g["Nodes"]:
                self.graph.add_node(n["id"], n["pos"])
            for e in g["Edges"]:
                self.graph.add_edge(e["src"], e["dest"], e["w"])
        except:
            return False
        return True

    def save_to_json(self, file_name: str):
        try:
            Nodes = []
            Edges = []
            for n in self.graph.get_all_v():
                node = json.dumps({"id": n.id, "pos": n.pos})
                Nodes.append(node)
                out = self.graph.all_out_edges_of_node(n.id)
                for e in out.keys():
                    edge = json.dumps({"src": n.id, "dest": e, "w": out[e]})
                    Edges.append(edge)
            with open(file_name, 'w') as f:
                json.dump({"Nodes": Nodes, "Edges": Edges}, f)
        except:
            return False
        return True

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
        path.insert(0, id2)
        node_id = parents.get(id2)
        path.insert(0, node_id)
        while parents.get(node_id) is not None:
            node_id = parents.get(node_id)
            path.insert(0, node_id)
        return dist[id2], path

    def dijkstra(self, src: int):
        parents = {}
        dist = {}
        visited = {}
        #queue is a priorityQueue that get a tuple
        #the tuple looks like (distance from src, id of node)
        queue = PriorityQueue()
        for n_id in self.graph.get_all_v().keys():
            dist[n_id] = math.inf
            parents[n_id] = None
            visited[n_id] = False
        dist[src] = 0
        queue.put((dist[src], src))
        while queue.qsize() != 0:
            v = queue.get()
            v_id = v[1]
            v_dist = v[0]
            neighbors = self.graph.all_out_edges_of_node(v_id)
            for u_id in neighbors.keys():
                if not visited[u_id]:
                    if dist[u_id] > v_dist + neighbors[u_id]:
                        dist[u_id] = v_dist + neighbors[u_id]
                        parents[u_id] = v_id
                        queue.put((dist[u_id], u_id))
            visited[v_id] = True
        return dist, parents
