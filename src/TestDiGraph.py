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
