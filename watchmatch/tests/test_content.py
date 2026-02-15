from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_admin_access_for_superuser(superuser_client, url_admin_index):
    """
    Проверяет, что суперпользователь имеет доступ к панели администратора.
    """

    response = superuser_client.get(url_admin_index)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_admin_access_for_anonymous_user(client, url_admin_index):
    """
    Проверяет, что для неавторизованного пользователь
    не может попасть на страницу администратора.
    """
    response = client.get(url_admin_index)
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url
