import unittest

from GraphAlgo import GraphAlgo
from DiGraph import *

class TestGraphAlgo(unittest.TestCase):

    def test_get_graph(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_edge(0, 2, 3.2)
        ga = GraphAlgo(g)
        g2 = ga.get_graph()
        self.assertEqual(g2.v_size(), 3, "node size is: " + str(g2.v_size()))
        self.assertEqual(g2.e_size(), 1, "edge size is: " + str(g2.e_size()))
        for node in g2.get_all_v().keys():
            nodes = g.get_all_v()
            self.assertIsNotNone(nodes[node])

    def test_load_and_save(self):
        a=1

    def test_shortest_path(self):
        g = DiGraph()
        for i in range(6):
            g.add_node(i)
        g.add_edge(0, 1, 2.5)
        g.add_edge(0, 3, 3.1)
        g.add_edge(1, 2, 1.2)
        g.add_edge(2, 3, 0.6)
        g.add_edge(3, 4, 2.3)
        g.add_edge(3, 5, 3.7)
        g.add_edge(4, 5, 1.7)
        ga = GraphAlgo(g)
        dist, path = ga.shortest_path(0,5)
        self.assertEqual(dist, 3.1 + 3.7, "dist is: " + str(dist))
        self.assertEqual(len(path), 3, "length of path is:" + str(len(path)))
        self.assertEqual(path[0], 0, "node id of first node in path=" + str(path[0]))
        self.assertEqual(path[1], 3, "node id of second node in path=" + str(path[1]))
        self.assertEqual(path[2], 5, "node id of third node in path=" + str(path[2]))

    def test_connected_component(self):
        a =1

    def test_connected_components(self):
        a=1

    def test_plot_graph(self):
        a=1

if __name__ == '__main__':
    unittest.main()