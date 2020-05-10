import sys

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from apps.core.models import Route

import networkx as netx


class Store():

    def __init__(self, graphs=netx.Graph, file_routes=None):
        if not isinstance(graphs, netx.Graph):
            raise Exception('Os gráficos devem ser um objeto do tipo Graph')
        if not isinstance(file_routes, str) or file_routes.__len__() < 1:
            raise Exception('as rotas do arquivo devem ser preenchidas com o nome da rota do arquivo para carregar e salvar as rotas')

        self.graphs = graphs
        self.file_routes = file_routes
        self.import_file_routes()

    def new_route(self, airport_departure, airport_arrival, price_route, only_memory=False):
        if not self.graphs.has_node(airport_departure):
            self.graphs.add_node(airport_departure)

        if not self.graphs.has_node(airport_arrival):
            self.graphs.add_node(airport_arrival)

        if self.graphs.has_edge(airport_departure, airport_arrival):
            if self.graphs.get_edge_data(airport_departure, airport_arrival).__contains__('price'):
                raise Exception(f'Rota já registrada: {airport_departure}-{airport_arrival}')
            self.graphs.remove_edge(airport_departure, airport_arrival)

        self.graphs.add_edge(airport_departure, airport_arrival, price=float(price_route))

        if not only_memory:
            file_route = open(self.file_routes, 'a')
            file_route.writelines(f'\n{airport_departure}, {airport_arrival}, {price_route}')
            file_route.close()

    def import_file_routes(self):
        file_route = open(self.file_routes, 'r')
        for line in file_route.read().splitlines():
            fields = line.split(',')
            if fields.__len__() != 3:
                raise Exception("Insira o arquivo para carregamento")
            self.new_route(fields[0], fields[1], fields[2], only_memory=True)
        file_route.close()

    def has_airport(self, airport):
        return self.graphs.has_node(airport)

    def get_best_route(self, airport_departure, airport_arrival):
        suggested_path = []

        path = netx.shortest_path(self.graphs, airport_departure, airport_arrival, weight='price')
        flights = list(netx.utils.pairwise(path))
        for flight in flights:
            airport_departure_path = flight[0]
            airport_arrival_path = flight[1]
            edge = self.graphs.get_edge_data(airport_departure_path, airport_arrival_path)
            price_path = edge['price']
            flight_model = Route(airport_departure_path, airport_arrival_path, price_path)
            suggested_path.append(flight_model)

        return suggested_path

    def clear_base(self):
        self.graphs.clear()
        file_route = open(self.file_routes, 'w')
        file_route.write('')
        file_route.close()


class Service():
    def __init__(self, store=Store):
        self.store = store

    def new_route(self, airport_departure, airport_arrival, price):
        self.store.new_route(airport_departure, airport_arrival, price, only_memory=False)

    def get_best_route(self, airport_departure, airport_arrival):
        if not (self.store.has_airport(airport_departure)):
            raise Exception('Aeroporto de origem não encontrado')

        if not (self.store.has_airport(airport_arrival)):
            raise Exception('Aeroporto de destino não encontrado')

        return self.store.get_best_route(airport_departure, airport_arrival)

    def get_best_route_str(self, airport_departure, airport_arrival):
        best_route_result = self.get_best_route(airport_departure, airport_arrival)
        airports = ' - '.join([c.get_departure() for c in best_route_result]) + ' - ' + best_route_result[-1].get_arrival()
        amount = sum(c.get_price() for c in best_route_result)

        return 'best route: {airports} > ${amount}'.format(airports=airports, amount=amount)


class Console():

    def __init__(self, service=Service):
        self.service = service

    def main(self):

        while True:
            try:
                route = input("Insira a rota ou para sair insira 'exit':").upper()
                if route == 'EXIT':
                    exit()

                airports = route.split('-')

                if len(airports) != 2:
                    raise Exception('Insira dois aeroportos Ex: SCL-ORL')

                departure = airports[0]
                arrival = airports[1]

                print(self.service.get_best_route_str(departure, arrival))
            except Exception as error:
                print(f"Erro: {error}")


class IocContainer(containers.DeclarativeContainer):
    try:
        if len(sys.argv) < 3:
            raise Exception('O arquivo para carregamento deve ser especificado')

        file_route = sys.argv[2]
    except:
        file_route = 'routes-file.csv'

    graphs = providers.Singleton(netx.Graph)
    store = providers.Singleton(Store, graphs=graphs, file_routes=file_route)
    service = providers.Factory(Service, store=store)
    console = providers.Factory(Console, service=service)
    console_main = providers.Callable(console().main)
