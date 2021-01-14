import unittest

from GraphAlgo import GraphAlgo
from DiGraph import *


class TestDiGraph(unittest.TestCase):

    def test_equals(self):
        g1 = DiGraph()
        g2 = DiGraph()
        for i in range(8):
            g1.add_node(i)
            g2.add_node(i)
        g1.add_edge(0, 1, 4.65)
        g2.add_edge(0, 1, 4.65)
        g1.add_edge(1, 2, 7.235)
        g2.add_edge(1, 2, 7.235)
        g1.add_edge(2, 0, 0.8645)
        g2.add_edge(2, 0, 0.8645)
        g1.add_edge(2, 7, 12.7524)
        g2.add_edge(2, 7, 12.7524)
        g1.add_edge(3, 5, 2.134)
        g2.add_edge(3, 5, 2.134)
        g1.add_edge(3, 6, 5.1236)
        g2.add_edge(3, 6, 5.1236)
        g1.add_edge(4, 1, 6.823645)
        g2.add_edge(4, 1, 6.823645)
        g1.add_edge(4, 3, 3.713)
        g2.add_edge(4, 3, 3.713)
        g1.add_edge(5, 6, 2.27854)
        g2.add_edge(5, 6, 2.27854)
        g1.add_edge(6, 3, 5.42)
        g2.add_edge(6, 3, 5.42)
        g1.add_edge(7, 1, 16.3245)
        g2.add_edge(7, 1, 16.3245)
        self.assertEqual(g1, g2, "")

    def test_v_size(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
            self.assertEqual(g.v_size(), i+1, "v_size=" + str(g.v_size()))

    def test_e_size(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
            self.assertEqual(g.e_size(), 0, "e_size=" + str(g.e_size()))
        counter = 0
        for i in range(30):
            for j in range(30):
                g.add_edge(i,j,1)
                counter = counter + 1
                self.assertEqual(g.e_size(),counter, "e_size=" + str(g.e_size()))

    def test_get_mc(self):
        counter = 0
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
            counter = counter + 1
            self.assertEqual(g.get_mc(), counter, "mc=" + str(g.get_mc()))
        for i in range(30):
            for j in range(30):
                g.add_edge(i, j, 1)
                counter = counter + 1
                self.assertEqual(g.get_mc(), counter, "mc=" + str(g.get_mc()))

    def test_get_all_v(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
        nodes = g.get_all_v()
        for i in range(30):
            self.assertIsNotNone(nodes.get(i),"")

    def test_add_node(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
            nodes = g.get_all_v()
            self.assertIsNotNone(nodes.get(i),"")

    def test_add_edge(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
        for i in range(29):
            g.add_edge(i,i+1,1)
            self.assertIsNotNone(g.all_out_edges_of_node(i).get(i+1))

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
        for i in range(29):
            g.add_edge(i,i+1,1)
        for i in range(1,30,1):
            in_edges = g.all_in_edges_of_node(i)
            self.assertEqual(len(in_edges),1)
            self.assertIsNotNone(in_edges.get(i-1))


    def test_all_out_edges_of_node(self):
        g = DiGraph()
        for i in range(30):
            g.add_node(i)
        for i in range(29):
            g.add_edge(i, i + 1, 1)
        for i in range(29):
            out_edges = g.all_out_edges_of_node(i)
            self.assertEqual(len(out_edges), 1)
            self.assertIsNotNone(out_edges.get(i+1))

    def test_remove_node(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_edge(0,1,2.3)
        g.add_edge(0,2,3.5)
        g.add_edge(1,0,1.243)
        g.add_edge(1,2,5.6)
        g.add_edge(2,0,3.45)
        self.assertTrue(g.remove_node(0))
        two_out_edges = g.all_out_edges_of_node(2)
        two_in_edges  = g.all_in_edges_of_node(2)
        self.assertIsNone(two_out_edges.get(0))
        self.assertIsNone(two_in_edges.get(0))
        one_out_edges = g.all_out_edges_of_node(1)
        one_in_edges = g.all_in_edges_of_node(1)
        self.assertIsNone(one_out_edges.get(0))
        self.assertIsNone(one_out_edges.get(0))

    def test_remove_edge(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_edge(0, 1, 2.3)
        g.add_edge(0, 2, 3.5)
        g.add_edge(1, 0, 1.243)
        g.add_edge(1, 2, 5.6)
        g.add_edge(2, 0, 3.45)
        g.remove_edge(0, 1)
        zero_out_edges = g.all_out_edges_of_node(0)
        one_in_edges = g.all_in_edges_of_node(1)
        self.assertIsNone(zero_out_edges.get(1))
        self.assertIsNone(one_in_edges.get(0))
