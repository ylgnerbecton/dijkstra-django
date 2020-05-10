from django.urls import include, path, re_path
from rest_framework_swagger.views import get_swagger_view
from apps.api import views

schema_view = get_swagger_view(title='API BEXS')

urlpatterns = [
    path('', schema_view, name="api"),
    path('route/<slug:departure>/<slug:arrival>/', views.GetBestRoute.as_view(), name="get-best-route"),
    path('route/', views.CreateBestRoute.as_view(), name="create-best-route"),
]