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
        ga = GraphAlgo(self.graph_factory(1))
        self.assertTrue(ga.save_to_json("../data/graph.json"))
        ga2 = GraphAlgo()
        self.assertTrue(ga2.load_from_json("../data/graph.json"))
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A0")
        ga.save_to_json("../data/A0_test")
        ga2.load_from_json("../data/A0_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A1")
        ga.save_to_json("../data/A1_test")
        ga2.load_from_json("../data/A1_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A2")
        ga.save_to_json("../data/A2_test")
        ga2.load_from_json("../data/A2_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A3")
        ga.save_to_json("../data/A3_test")
        ga2.load_from_json("../data/A3_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A4")
        ga.save_to_json("../data/A4_test")
        ga2.load_from_json("../data/A4_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/A5")
        ga.save_to_json("../data/A5_test")
        ga2.load_from_json("../data/A5_test")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")
        ga.load_from_json("../data/T0.json")
        ga.save_to_json("../data/T0_test.json")
        ga2.load_from_json("../data/T0_test.json")
        self.assertEqual(ga.get_graph(), ga2.get_graph(), "")


    def test_shortest_path(self):
        #graph 1
        ga = GraphAlgo(self.graph_factory(1))
        dist, path = ga.shortest_path(0, 5)
        self.assertEqual(dist, 3.1 + 3.7, "dist is: " + str(dist))
        self.assertEqual(len(path), 3, "length of path is:" + str(len(path)))
        self.assertEqual(path[0], 0, "node id of first node in path=" + str(path[0]))
        self.assertEqual(path[1], 3, "node id of second node in path=" + str(path[1]))
        self.assertEqual(path[2], 5, "node id of third node in path=" + str(path[2]))
        #graph 2
        ga = GraphAlgo(self.graph_factory(2))
        dist, path = ga.shortest_path(4, 6)
        self.assertTrue(dist-8.12554 < 0.0000001, "dist=" + str(dist))
        self.assertEqual(len(path), 4, "size of path=" + str(len(path)))
        self.assertEqual(path[0], 4, "node id of the first node in path=" + str(path[0]))
        self.assertEqual(path[1], 3, "node id of the first node in path=" + str(path[1]))
        self.assertEqual(path[2], 5, "node id of the first node in path=" + str(path[2]))
        self.assertEqual(path[3], 6, "node id of the first node in path=" + str(path[3]))



    def test_connected_component(self):
        #graph 1
        ga = GraphAlgo(self.graph_factory(1))
        keys = ga.get_graph().get_all_v().keys()
        nodes = ga.get_graph().get_all_v().values()
        for key in keys:
            scc = ga.connected_component(key)
            self.assertEqual(len(scc), 1, "scc=" + str(len(scc)))
        #graph 2
        ga = GraphAlgo(self.graph_factory(2))
        keys = ga.get_graph().get_all_v().keys()
        scc1 = [0, 1, 2, 7]
        scc2 = [3, 5, 6]
        scc3 = [4]
        for key in keys:
            scc = ga.connected_component(key)
            if key in scc1:
                for node in scc:
                    self.assertTrue(node.node_id in scc1, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc2, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc3, "node id=" + str(node.node_id))
            elif key in scc2:
                for node in scc:
                    self.assertTrue(node.node_id in scc2, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc1, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc3, "node id=" + str(node.node_id))
            else:
                for node in scc:
                    self.assertTrue(node.node_id in scc3, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc1, "node id=" + str(node.node_id))
                    self.assertTrue(node.node_id not in scc2, "node id=" + str(node.node_id))

    def test_connected_components(self):
        #graph 1
        ga = GraphAlgo(self.graph_factory(1))
        components = ga.connected_components()
        self.assertEqual(len(components), len(ga.get_graph().get_all_v()), "size should be equal")
        for component in components:
            self.assertEqual(len(component), 1, "component size=" + str(len(component)))
        #graph 2
        ga = GraphAlgo(self.graph_factory(2))
        keys = ga.get_graph().get_all_v().keys()
        scc1 = [0, 1, 2, 7]
        scc2 = [3, 5, 6]
        scc3 = [4]
        components = ga.connected_components()
        self.assertEqual(len(components), 3, "number of components in the graph=" + str(len(components)))
        self.assertEqual(len(components[0])+len(components[1])+len(components[2]),
                         len(ga.get_graph().get_all_v().values()))

    def test_plot_graph(self):
        ga = GraphAlgo(self.graph_factory(1))
        ga.plot_graph()
        ga = GraphAlgo(self.graph_factory(2))
        ga.plot_graph()

    def graph_factory(self, number: int):
        g = DiGraph()
        if number == 1:
            for i in range(6):
                g.add_node(i)
            g.add_edge(0, 1, 2.5)
            g.add_edge(0, 3, 3.1)
            g.add_edge(1, 2, 1.2)
            g.add_edge(2, 3, 0.6)
            g.add_edge(3, 4, 2.3)
            g.add_edge(3, 5, 3.7)
            g.add_edge(4, 5, 1.7)
        elif number == 2:
            for i in range(8):
                g.add_node(i)
            g.add_edge(0, 1, 4.65)
            g.add_edge(1, 2, 7.235)
            g.add_edge(2, 0, 0.8645)
            g.add_edge(2, 7, 12.7524)
            g.add_edge(3, 5, 2.134)
            g.add_edge(3, 6, 5.1236)
            g.add_edge(4, 1, 6.823645)
            g.add_edge(4, 3, 3.713)
            g.add_edge(5, 6, 2.27854)
            g.add_edge(6, 3, 5.42)
            g.add_edge(7, 1, 16.3245)
        return g


if __name__ == '__main__':
    unittest.main()
