from django.urls import path, include

from .views import CreateUserView, GetTokenView


app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'registration/',
        CreateUserView.as_view(),
        name='registration',
    ),
    path('get-api-token/', GetTokenView.as_view(), name='get-api-token'),
]
