import os
from django.test import TestCase

import networkx as netx

from core.views import Store, Service


class TestRotaService(TestCase):
    def __init__(self):
        self.graphs = netx.Graph()
        self.store = Store(graphs=self.graphs, file_routes=os.path.dirname(os.path.abspath("tests.csv"))
        self.service = Service(store=self.store)

    def test_add_one_route_get_better_route(self):
        self.store.clear_base()

        self.service.new_route('GRU', 'BRC', 1)
        best_route = self.service.get_best_route('GRU', 'BRC')

        self.assertEqual(len(best_route), 1)

        path = best_route[0]
        self.assertEqual(path.get_departure(), 'GRU')
        self.assertEqual(path.get_arrival(), 'BRC')
        self.assertEqual(path.get_price(), 1)

    def test_get_better_route_without_registered_airport_departure(self):
        self.store.clear_base()
        try:
            best_route = self.service.get_best_route('GRU', 'BRC')
        except Exception as error:
            self.assertEqual(str(error), 'Aeroporto de origem não encontrado')

    def test_get_better_route_without_registered_airport_arrival(self):
        self.store.clear_base()
        self.service.new_route('GRU', 'ORL', 1)
        try:
            best_route = self.service.get_best_route('GRU', 'BRC')
        except Exception as error:
            self.assertEqual(str(error), 'Aeroporto de destino não encontrado')

    def test_add_multiple_routes_get_better_route(self):
        self.store.clear_base()
        self.service.new_route('GRU', 'ORL', 5)
        self.service.new_route('ORL', 'BRC', 4)
        self.service.new_route('GRU', 'BRC', 10)
        best_route = self.service.get_best_route('GRU', 'BRC')

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
        self.store.clear_base()
        self.service.new_route('GRU', 'ORL', 5)
        self.service.new_route('ORL', 'BRC', 5)
        self.service.new_route('GRU', 'BRC', 10)
        best_route = self.service.get_best_route('GRU', 'BRC')

        self.assertEqual(len(best_route), 1)

        first_path = best_route[0]
        self.assertEqual(first_path.get_departure(), 'GRU')
        self.assertEqual(first_path.get_arrival(), 'BRC')
        self.assertEqual(first_path.get_price(), 10)
