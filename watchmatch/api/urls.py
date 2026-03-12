from django.urls import path, include

from .v1.urls import router_v1


app_name = 'api'

urlpatterns = [
    path('', include(router_v1.urls)),
]
