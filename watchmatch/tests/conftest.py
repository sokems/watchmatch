import warnings

from django.test.client import Client
from django.urls import reverse
import pytest


warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def auth_user(django_user_model):
    """Создает зарегистрированного пользователя."""
    return django_user_model.objects.create(username='sokem')


@pytest.fixture
def auth_user_client(auth_user):
    """Возвращает клиент Django с авторизованным пользователем."""
    client = Client()
    client.force_login(auth_user)

    return client


@pytest.fixture
def url_admin_index():
    """Возвращает URL страницы админки."""
    return reverse('admin:index')


@pytest.fixture
def url_homepage_index():
    """Возвращает URL главной страницы"""
    return reverse('core:index')
