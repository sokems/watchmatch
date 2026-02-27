from http import HTTPStatus

import pytest
from colorama import init, Fore
from django.urls import reverse

from movies.models import Movie

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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'core:index',
        'core:about',
        'movies:list_movies',
        'rooms:create_room',
        'rooms:join_room',
        )
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_args_pages_availability_for_anonymous_user(client, movie, monkeypatch):
    def mock_get_movie_tmdb(movie_id):
        return {
            'id': movie.id,
            'title': movie.title,
            'original_title': movie.title,
            'adult': False,
            'vote_average': 5,
            'overview': 'Описание',
            'poster_path': None,
            'backdrop_path': None,
            'genres': [],
        }

    monkeypatch.setattr('movies.views.get_movie_tmdb', mock_get_movie_tmdb)

    url = reverse('movies:detail_movie', args=(movie.id,))
    response = client.get(url)

    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')

    assert response.status_code == 200


@pytest.mark.django_db
def test_play_room_availability_for_participant(client, room, participant, movie, monkeypatch):
    monkeypatch.setattr(
        'swipes.views.get_movie_tmdb',
        lambda movie_id: {
            'id': movie.id,
            'title': movie.title,
            'original_title': movie.original_title,
            'adult': movie.adult,
            'vote_average': movie.vote_average,
            'overview': movie.overview,
            'poster_path': None,
            'backdrop_path': None,
            'genre_ids': [g.id for g in movie.genres.all()]
        }
    )

    monkeypatch.setattr(
        'swipes.views.create_and_return_movie',
        lambda data: movie
    )

    monkeypatch.setattr(
        'swipes.views.get_movies_from_tmdb_by_room',
        lambda room_obj: [{
            'id': movie.id,
            'title': movie.title,
            'original_title': movie.original_title,
            'adult': movie.adult,
            'vote_average': movie.vote_average,
            'overview': movie.overview,
            'poster_path': None,
            'backdrop_path': None,
            'genre_ids': [g.id for g in movie.genres.all()]
        }]
    )

    url = reverse('swipes:play_room', args=(room.id, participant.id))
    response = client.get(url)

    print(f'\n{Fore.BLUE}request: {Fore.MAGENTA}{response.request}{Fore.RESET}')
    print(f'{Fore.BLUE}response: {Fore.MAGENTA}{response}{Fore.RESET}\n')

    assert response.status_code == HTTPStatus.OK
