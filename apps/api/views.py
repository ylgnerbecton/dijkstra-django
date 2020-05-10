from rest_framework import status, generics, views, viewsets
from rest_framework.response import Response
from django.http import JsonResponse

from apps.api import serializers
from apps.core.models import Route
from apps.core.views import Service, IocContainer


class GetBestRoute(views.APIView):
    def __init__(self):
        self.container = IocContainer
        self.service = Service = self.container.service()

    def get(self, request, *args, **kwargs):
        departure = kwargs.get("departure", "").upper()
        arrival = kwargs.get("arrival", "").upper()

        try:
            empty_response = {"rpstConsultar": 'Abreviações dos aeroportos devem ser um texto'}
            if not isinstance(departure, str):
                return JsonResponse({"rpstConsultar": empty_response},
                            status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')

            if not isinstance(arrival, str):
                return JsonResponse({"rpstConsultar": empty_response},
                            status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')

            empty_response = self.service.get_best_route_str(departure, arrival)
            return JsonResponse({"rpstConsultar": empty_response},
                            status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')
        except Exception as error: 
            empty_response = str(error)
            return JsonResponse({"rpstConsultar": empty_response},
                            status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')


class CreateBestRoute(generics.GenericAPIView):
    serializer_class = serializers.RouteSerializer

    def __init__(self):
        self.container = IocContainer
        self.service = Service = self.container.service()

    def post(self, request, format=None):
        serializer = serializers.RouteSerializer(data=request.data)

        if serializer.is_valid():
            departure = serializer.data.get('departure').upper()
            arrival = serializer.data.get('arrival').upper()
            price = float(serializer.data.get('price'))

            try:
                empty_response = {"rpstConsultar": 'Abreviações dos aeroportos devem ser um texto'}
                if not isinstance(departure, str):
                    return JsonResponse({"rpstConsultar": empty_response},
                                status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')

                if not isinstance(arrival, str):
                    return JsonResponse({"rpstConsultar": empty_response},
                                status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')

                if not float(price) > 0:
                    empty_response = {"rpstConsultar": 'Preço tem que ser maior que 0'}
                    return JsonResponse({"rpstConsultar": empty_response},
                                status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')

                self.service.new_route(departure, arrival, price)
                return JsonResponse({"rpstConsultar": 'Cadastro realizado com sucesso'},
                                status=status.HTTP_201_CREATED,
                                content_type='application/json; charset=utf-8')

            except Exception as error:
                return JsonResponse({"rpstConsultar": f"{str(error)}"},
                                status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
                            
        return JsonResponse({"rpstConsultar": f"{str(serializer.errors)}"},
                        status=status.HTTP_200_OK,
                        content_type='application/json; charset=utf-8')

