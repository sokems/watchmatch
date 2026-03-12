from django.urls import path, include

from .v1.urls import urlpatterns_v1


app_name = 'api'

urlpatterns = [
    path('', include(urlpatterns_v1)),
]
