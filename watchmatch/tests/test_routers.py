from http import HTTPStatus

import pytest
from colorama import init, Fore


init(autoreset=True)


@pytest.mark.django_db
def test_admin_panel_access_for_superuser(admin_client, url_admin_index):
    """
    Проверяет, что суперпользователь имеет доступ к панели администратора.
    """
    response = admin_client.get(url_admin_index)

    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_admin_panel_access_for_anonymous_user(client, url_admin_index):
    """
    Проверяет, что неавторизованный пользователь
    не может попасть на страницу администратора.
    """
    response = client.get(url_admin_index)

    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url


@pytest.mark.django_db
def test_admin_panel_access_for_authenticated_user(auth_user_client, url_admin_index):
    """
    Проверяет, что авторизованный пользователь
    не может попасть на страницу администратора.
    """
    response = auth_user_client.get(url_admin_index)
    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url


@pytest.mark.xfail(reason='Пусть пока падает')
def test_homepage_is_available(client, url_homepage_index):
    """
    Проверяет доступность главной страницы для любого пользователя
    """
    response = client.get(url_homepage_index)
    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')
    assert response.status_code == HTTPStatus.OK
