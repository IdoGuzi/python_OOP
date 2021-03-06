from GraphInterface import GraphInterface


class GeoLocation(object):
    def __init__(self, pos=None):
        self.pos = pos
        if pos is not None:
            self.x = pos[0]
            self.y = pos[1]
            self.z = pos[2]
        else:
            self.x = 0
            self.y = 0
            self.z = 0

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) is not type(self):
            return False
        if other.x != self.x:
            return False
        if other.y != self.y:
            return False
        if other.z != self.z:
            return False
        return True

    def __repr__(self):
        return "("+str(self.x) + ", "+str(self.y) + ", "+str(self.z)+")"

    def to_string(self):
        return str(self.x) + ","+str(self.y) + ","+str(self.z)

class NodeData(object):
    def __init__(self, node_id: int, pos=None, weight=1, tag=0, info=""):
        self.node_id = node_id
        self.pos = GeoLocation(pos)
        self.weight = weight
        self.tag = tag
        self.info = info

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) is not type(self):
            return False
        if other.node_id != self.node_id:
            return False
        if other.pos != self.pos:
            return False
        return True

    def __repr__(self):
        return "node id: " + str(self.node_id) + ", pos: " + str(self.pos)


class DiGraph(GraphInterface):

    def __init__(self):
        self.v = dict()
        self._nodeSize = 0
        self._edgeSize = 0
        self._mc = 0
        self.nei_nodes_in = dict()
        self.nei_nodes_out = dict()

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) is not type(self):
            return False
        if len(other.get_all_v()) != len(self.get_all_v()):
            return False
        nodes = other.get_all_v()
        for node in self.v.values():
            if nodes[node.node_id] != node:
                return False
            out_edges_other = other.all_out_edges_of_node(node.node_id)
            out_edges_self = self.all_out_edges_of_node(node.node_id)
            if len(out_edges_other) != len(out_edges_self):
                return False
            for dest in out_edges_self.keys():
                if out_edges_other[dest] is None:
                    return False
                if out_edges_other[dest] != out_edges_self[dest]:
                    return False
            in_edges_other = other.all_in_edges_of_node(node.node_id)
            in_edges_self = self.all_in_edges_of_node(node.node_id)
            if len(in_edges_other) != len(in_edges_self):
                return False
            for src in in_edges_self.keys():
                if in_edges_other[src] is None:
                    return False
                if in_edges_other[src] != in_edges_self[src]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        nodes = "nodes: " + str(self.v) + '\n'
        edges = "edges: " + str(self.nei_nodes_out) + '\n'
        return nodes + edges

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        if self._nodeSize >= 0:
            return self._nodeSize
        raise ValueError

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        if self._edgeSize >= 0:
            return self._edgeSize
        raise ValueError

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        if self._mc >= 0:
            return self._mc
        raise ValueError

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        return self.v

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        if node_id in self.v:
            return False
        self.v[node_id] = NodeData(node_id, pos)
        self.nei_nodes_out[node_id] = {}
        self.nei_nodes_in[node_id] = {}
        self._mc += 1
        self._nodeSize += 1
        return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 not in self.v or id2 not in self.v:
            return False
        if id2 in self.nei_nodes_out[id1]:
            return False

        self.nei_nodes_out[id1][id2] = weight
        self.nei_nodes_in[id2][id1] = weight

        self._mc += 1
        self._edgeSize += 1
        return True

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        if id1 not in self.nei_nodes_in:
            raise ValueError("id not exist")
        return self.nei_nodes_in.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if id1 not in self.nei_nodes_out:
            raise ValueError("id not exist")
        return self.nei_nodes_out.get(id1)

    def remove_node(self, node_id: int) -> bool:
        """
         Removes a node from the graph.
         @param node_id: The node ID
         @return: True if the node was removed successfully, False o.w.

         Note: if the node id does not exists the function will do nothing
         """
        if node_id not in self.v:
            return False
        in_edges = self.all_in_edges_of_node(node_id)
        for key in in_edges.keys():
            del self.nei_nodes_out[key][node_id]
        out_edges = self.all_out_edges_of_node(node_id)
        for key in out_edges.keys():
            del self.nei_nodes_in[key][node_id]

        del self.nei_nodes_out[node_id]
        del self.nei_nodes_in[node_id]
        del self.v[node_id]

        self._mc += 1
        self._nodeSize -= 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 not in self.v or node_id2 not in self.v:
            return False
        if node_id2 not in self.nei_nodes_out[node_id1]:
            return False

        del self.nei_nodes_out[node_id1][node_id2]
        del self.nei_nodes_in[node_id2][node_id1]

        self._mc += 1
        self._edgeSize -= 1
        return True

