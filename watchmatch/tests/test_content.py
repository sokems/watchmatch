from http import HTTPStatus

import pytest


@pytest.mark.django_db
#@pytest.mark.xfail(reason='Пусть пока падает')
def test_admin_panel_access_for_superuser(admin_client, url_admin_index):
    """
    Проверяет, что суперпользователь имеет доступ к панели администратора.
    """

    response = admin_client.get(url_admin_index)

    print(f'response: {response}')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_admin_panel_access_for_anonymous_user(client, url_admin_index):
    """
    Проверяет, что неавторизованный пользователь
    не может попасть на страницу администратора.
    """
    response = client.get(url_admin_index)

    print(f'response: {response}')
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url


@pytest.mark.django_db
def test_admin_panel_access_for_authenticated_user(auth_user_client, url_admin_index):
    """
    Проверяет, что авторизованный пользователь
    не может попасть на страницу администратора.
    """
    response = auth_user_client.get(url_admin_index)

    print(f'response: {response}')
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url