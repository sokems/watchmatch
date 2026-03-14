from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

handler400 = 'core.views.bad_request'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'


schema_view = get_schema_view(
   openapi.Info(
      title='WatchMatch API',
      default_version='v1',
      description='Документация для проекта WatchMatch.',
      contact=openapi.Contact(email="sokems@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('api/', include('api.urls')),
    path('movies/', include('movies.urls')),
    path('rooms/', include('rooms.urls')),
    path('play_room/', include('swipes.urls')),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
