from django.core.management.base import BaseCommand
from django.conf import settings
import requests

from movies.models import Genre


class Command(BaseCommand):
    help = "Загружает список жанров с TMDB и сохраняет в базу"

    def handle(self, *args, **options):
        url = (
            f"https://api.themoviedb.org/3/genre/movie/list?"
            f"api_key={settings.TMDB_API_KEY}"
            f"&language=ru-RU"
        )
        response = requests.get(url)
        data = response.json()

        for g in data.get('genres', []):
            Genre.objects.update_or_create(
                id=g['id'],
                defaults={'name': g['name']}
            )

        self.stdout.write(self.style.SUCCESS("Жанры успешно сохранены!"))
