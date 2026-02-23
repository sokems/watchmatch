from django.contrib import admin

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'count_participants',
        'get_genres',
        'get_between_years',
        'adult',
        'vote_average',
    )
    search_fields = ('name',)
    filter_horizontal = ('genres',)


    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])

    def get_between_years(self, obj):
        if obj.year_start == obj.year_end:
            return obj.year_start
        elif obj.year_start > obj.year_end:
            return f"{obj.year_end} - {obj.year_start}"
        else:
            return f"{obj.year_start} - {obj.year_end}"


admin.site.register(Room, RoomAdmin)
