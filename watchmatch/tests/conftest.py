import warnings

from django.test.client import Client
from django.urls import reverse
import pytest


warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def superuser(django_user_model):
    """Создает и возвращает супер юзера."""
    return django_user_model.objects.create_superuser(
        'admin',
        'admin@test.com',
        'password123'
    )


@pytest.fixture
def superuser_client(superuser):
    """Возвращает клиент Django с авторизованным супер юзером."""
    client = Client()
    client.force_login(superuser)
    return client


@pytest.fixture
def url_admin_index():
    """Возвращает URL страницы админки."""
    return reverse('admin:index')
