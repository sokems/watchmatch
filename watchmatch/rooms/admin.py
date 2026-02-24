from django.contrib import admin

from .models import Room, Participant


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'count_participants',
        'get_genres',
        'get_between_years',
        'adult',
        'vote_average',
    )
    search_fields = ('name',)
    filter_horizontal = ('genres',)
    list_display_links = ('name',)

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])

    get_genres.short_description = "Жанры"

    def get_between_years(self, obj):
        if obj.year_start == obj.year_end:
            return obj.year_start
        elif obj.year_start > obj.year_end:
            return f"{obj.year_end} - {obj.year_start}"
        else:
            return f"{obj.year_start} - {obj.year_end}"

    get_between_years.short_description = "Годы релиза"


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'room_id',
    )
    list_filter = ('room_id',)
    list_display_links = ('name',)
    readonly_fields = ('room_id',)


admin.site.register(Room, RoomAdmin)
admin.site.register(Participant, ParticipantAdmin)
