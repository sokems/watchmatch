from django.contrib import admin
from django.urls import path, include
from django.conf import settings

handler400 = 'core.views.bad_request'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('movies/', include('movies.urls')),
    path('rooms/', include('rooms.urls')),
    path('play_room/', include('swipes.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
