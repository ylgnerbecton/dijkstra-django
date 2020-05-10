import os
from django.test import TestCase

import networkx as netx

from apps.core.views import Store


class TestRotaRepository(TestCase):

    def __init__(self):
        self.graphs = netx.Graph()
        self.store = Store(graphs=self.graphs, file_routes=os.path.dirname(os.path.abspath("tests.csv"))

    def test_add_one_route_get_better_route(self):
        self.graphs.clear()
        self.store.new_route('GRU', 'BRC', 1)
        self.assertTrue(self.store.has_airport('GRU'))
        self.assertTrue(self.store.has_airport('BRC'))
        best_route = self.store.get_best_route('GRU', 'BRC')

        self.assertEqual(len(best_route), 1)

        path = best_route[0]
        self.assertEqual(path.get_departure(), 'GRU')
        self.assertEqual(path.get_arrival(), 'BRC')
        self.assertEqual(path.get_price(), 1)

    def test_add_multiple_routes_get_better_route(self):
        self.graphs.clear()
        self.store.new_route('GRU', 'ORL', 5)
        self.store.new_route('ORL', 'BRC', 4)
        self.store.new_route('GRU', 'BRC', 10)
        self.assertTrue(self.store.has_airport('GRU'))
        self.assertTrue(self.store.has_airport('BRC'))
        self.assertTrue(self.store.has_airport('ORL'))
        best_route = self.store.get_best_route('GRU', 'BRC')

        self.assertEqual(len(best_route), 2)

        first_path = best_route[0]
        self.assertEqual(first_path.get_departure(), 'GRU')
        self.assertEqual(first_path.get_arrival(), 'ORL')
        self.assertEqual(first_path.get_price(), 5)

        second_path = best_route[1]
        self.assertEqual(second_path.get_departure(), 'ORL')
        self.assertEqual(second_path.get_arrival(), 'BRC')
        self.assertEqual(second_path.get_price(), 4)

    def test_add_multiple_routes_similar_prices_get_better_route(self):
        self.graphs.clear()
        self.store.new_route('GRU', 'ORL', 5)
        self.store.new_route('ORL', 'BRC', 5)
        self.store.new_route('GRU', 'BRC', 10)
        self.assertTrue(self.store.has_airport('GRU'))
        self.assertTrue(self.store.has_airport('BRC'))
        self.assertTrue(self.store.has_airport('ORL'))
        best_route = self.store.get_best_route('GRU', 'BRC')

        self.assertEqual(len(best_route), 1)

        first_path = best_route[0]
        self.assertEqual(first_path.get_departure(), 'GRU')
        self.assertEqual(first_path.get_arrival(), 'BRC')
        self.assertEqual(first_path.get_price(), 10)
