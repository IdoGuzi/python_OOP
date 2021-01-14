from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import *

from queue import PriorityQueue
import math
import json
import random
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: GraphInterface = None):
        self.graph = g
        if g is None:
            self.graph = DiGraph()
    
    def get_graph(self) -> GraphInterface:
        """
        @return: the graph this object holds.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        loads a graph from a file in json format.
        @param file_name: name of the file (relative and absolute path).
        @return: true for success, false for failure and keeps the old graph.
        """
        try:
            old = self.graph
            self.graph = DiGraph()
            with open(file_name, 'r') as f:
                g = json.load(f)
            for n in g["Nodes"]:
                if n.get("pos") is not None:
                    string = n["pos"]
                    string_list = string.split(',')
                    self.graph.add_node(n["id"], (float(string_list[0]), float(string_list[1]), float(string_list[2])))
                else:
                    self.graph.add_node(n["id"])
            for e in g["Edges"]:
                self.graph.add_edge(e["src"], e["dest"], e["w"])
        except Exception as e:
            print(e)
            self.graph = old
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        save the graph in this object to a file in json format.
        @param file_name: the name of the file.
        @return: true for success, false for failure
        """
        try:
            json_graph = dict()
            Nodes = []
            Edges = []
            for n in self.graph.get_all_v().values():
                node = {"id": n.node_id, "pos": n.pos.to_string()}
                Nodes.append(node)
                out = self.graph.all_out_edges_of_node(n.node_id)
                for e in out.keys():
                    edge = {"src": n.node_id, "dest": e, "w": out[e]}
                    Edges.append(edge)
            json_graph["Nodes"] = Nodes
            json_graph["Edges"] = Edges
            with open(file_name, 'w+') as file:
                json.dump(json_graph, file, indent=4)
        except Exception as e:
            print(e)
            return False
        return True

    def connected_component(self, id1: int) -> list:
        """
        finds the Strongly Connected Component of the node id1 in the graph.
        @param id1: id of the node to find his SCC
        @return: list of the node in the SCC, empty list if graph is None or id1 is not in the graph.
        """
        if self.graph is None or self.graph.get_all_v()[id1] is None:
            return []
        connected_component = []
        strongly_connected_componect = []
        dist, parents = self.dijkstra(id1)
        nodes = self.graph.get_all_v()
        for node_id in dist.keys():
            if dist[node_id] is not math.inf:
                connected_component.append(nodes[node_id])
        g = self.get_graph()
        self.graph = self.get_graph_transpose()
        dist, parents = self.dijkstra(id1)
        for node in connected_component:
            if dist[node.node_id] is not math.inf :
                strongly_connected_componect.append(node)
        self.graph = g
        return strongly_connected_componect

    def connected_components(self) -> List[list]:
        """
        finds all the Strongly Connected Component in the graph.
        @return: list of all the SCC, empty list if graph is None.
        """
        seen = {}
        components = []
        for n in self.graph.get_all_v().keys():
            seen[n] = False
        for n in self.graph.get_all_v().keys():
            if seen[n]:
                continue
            component = self.connected_component(n)
            for v in component:
                seen[v.node_id] = True
            components.append(component)
        return components

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        find the shortest path between 2 nodes in the graph.
        @param id1: id of the src node.
        @param id2: id of the dst node.
        @return: distance of the path, list of the node ids in the path,
        if path not exist distance is infinity and the list will be empty.
        """
        dist, parents = self.dijkstra(id1)
        path = list()
        path.insert(0, id2)
        node_id = parents.get(id2)
        path.insert(0, node_id)
        while parents.get(node_id) is not None:
            node_id = parents.get(node_id)
            path.insert(0, node_id)
        return dist[id2], path

    def plot_graph(self) -> None:
        """
        drawing the graph with matplotlib.
        """
        plt.figure()
        plt.title("Graph")
        plt.xlabel("x")
        plt.ylabel("y")
        max_x = len(self.get_graph().get_all_v())*2
        min_x = 0
        max_y = len(self.get_graph().get_all_v())*2
        min_y = 0
        on_x = dict()
        on_y = dict()
        for node in self.get_graph().get_all_v().values():
            if node.pos.x == 0 and node.pos.y == 0:
                x = random.uniform(min_x, max_x)
                y = random.uniform(min_y, max_y)
                while on_x.get(x) is not None:
                    x = random.uniform(min_x, max_x)
                node.pos.x = x
                on_x[x] = node.node_id
                while on_y.get(y) is not None:
                    y = random.uniform(min_y, max_y)
                node.pos.y = y
                on_y[y] = node.node_id
            if node.pos.x > max_x:
                max_x = node.pos.x + 1
            if node.pos.x < min_x:
                min_x = node.pos.x - 1
            if node.pos.y > max_y:
                max_y = node.pos.y + 1
            if node.pos.y < min_y:
                min_y = node.pos.y - 1
        plt.axis([min_x, max_x, min_y, max_y])
        nodes = self.graph.get_all_v()
        for node in nodes.values():
            plt.plot(node.pos.x, node.pos.y, 'ro')
            plt.text(node.pos.x, node.pos.y, str(node.node_id))
            edges = self.graph.all_out_edges_of_node(node.node_id)
            for dest in edges.keys():
                dest_node = nodes[dest]
                dx = dest_node.pos.x-node.pos.x
                dy = dest_node.pos.y-node.pos.y
                plt.arrow(node.pos.x, node.pos.y, dx, dy, length_includes_head=True, head_width=0.15, width=0.001)
                plt.text(node.pos.x+dx/3,node.pos.y+dy/3, "s="+str(node.node_id)+", d="+str(dest)+", w="+str(edges[dest]), fontsize=8)
        plt.show()
        return None

    def dijkstra(self, src: int):
        """
        perform dijksta algorithm on the graph from node src.
        @param src: id of the node.
        @return: dictionary of node id such that the value is the node id who found the key.
        """
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

    def get_graph_transpose(self):
        """
        taking the graph in this object and create the graph^T (transpose).
        @return: the transpose graph.
        """
        g = DiGraph()
        nodes = self.graph.get_all_v()
        for key in nodes.keys():
            g.add_node(key)
        for key in nodes.keys():
            out_edges = self.graph.all_out_edges_of_node(key)
            for dest in out_edges.keys():
                g.add_edge(dest, key, out_edges[dest])
        return g
