from django.urls import path, include

from .views import CreateUserView


app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/',
        CreateUserView.as_view(),
        name='registration',
    ),
]
