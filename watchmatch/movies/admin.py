from django.contrib import admin

from .models import Genre, Movie


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_display_links = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'original_title',
        'get_genres',
        'release_date',
        'adult',
        'vote_average',
    )
    search_fields = (
        'id',
        'title',
        'original_title',
        'adult',
    )
    list_filter = ('genres', 'release_date', 'vote_average')
    filter_horizontal = ('genres',)
    list_display_links = ('title',)

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])

    get_genres.short_description = "Жанры"


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
