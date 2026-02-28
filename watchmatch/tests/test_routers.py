from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_admin_redirect_anonymous(client, url_admin_index):
    """Анонимный пользователь перенаправляется со страницы админки."""
    response = client.get(url_admin_index)
    assert response.status_code == 302


@pytest.mark.django_db
def test_admin_forbidden_for_regular_user(auth_user_client, url_admin_index):
    """Обычные пользователи не имеют доступа к админке (302 или 403)."""
    response = auth_user_client.get(url_admin_index)
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_admin_available_for_staff(admin_client, url_admin_index):
    """Администраторы могут просматривать страницу админки (200)."""
    response = admin_client.get(url_admin_index)
    assert response.status_code == 200


@pytest.mark.parametrize(
    'client_fixture, url_fixture, expected_status',
    [
        ('client', 'url_homepage_index', HTTPStatus.OK),
        ('client', 'url_about', HTTPStatus.OK),
        ('client', 'url_create_room', HTTPStatus.FOUND),
        ('client', 'url_join_room', HTTPStatus.FOUND),
        ('client', 'url_list_rooms', HTTPStatus.FOUND),
        ('client', 'url_list_movies', HTTPStatus.FOUND),
        ('auth_user_client', 'url_homepage_index', HTTPStatus.OK),
        ('auth_user_client', 'url_about', HTTPStatus.OK),
        ('auth_user_client', 'url_create_room', HTTPStatus.OK),
        ('auth_user_client', 'url_join_room', HTTPStatus.OK),
        ('auth_user_client', 'url_list_rooms', HTTPStatus.OK),
        ('auth_user_client', 'url_list_movies', HTTPStatus.OK),
    ]
)
@pytest.mark.django_db
def test_pages_access(
        request,
        client_fixture,
        url_fixture,
        expected_status,
        mock_tmdb_list
):
    """
    Проверка доступа к страницам для
    анонимного и авторизованного пользователей.
    """
    client = request.getfixturevalue(client_fixture)
    url = request.getfixturevalue(url_fixture)

    response = client.get(url)
    assert response.status_code == expected_status

    if expected_status == HTTPStatus.FOUND:
        assert '/login/' in response.url


@pytest.mark.parametrize(
    'client_fixture, expected_status',
    [
        ('client', HTTPStatus.FOUND),
        ('auth_user_client', HTTPStatus.OK),
    ]
)
@pytest.mark.django_db
def test_detail_movie_access(
        request,
        client_fixture,
        movie,
        expected_status,
        mock_tmdb_movie
):
    """
    Проверка доступа к странице фильма:
    редирект для анонимов, 200 для авторизованных.
    """
    client = request.getfixturevalue(client_fixture)
    url_detail_movie = reverse('movies:detail_movie', kwargs={'movie_id': movie.pk})
    response = client.get(url_detail_movie)

    if client_fixture == 'client':
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url_detail_movie}'
        assertRedirects(response, expected_url)
    else:
        assert response.status_code == expected_status
