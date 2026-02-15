from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_admin_access_for_superuser(client, django_user_model):
    """
    Проверяет, что суперпользователь имеет доступ к панели администратора.
    """
    user = django_user_model.objects.create_superuser('admin', 'admin@test.com', 'password123')
    client.force_login(user)

    url = reverse('admin:index')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
