from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

static_urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
static_urlpatterns = [path(f'api{pattern.pattern}', pattern.callback, pattern.default_args, pattern.name) for pattern in static_urlpatterns]
urlpatterns += static_urlpatterns

media_urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
media_urlpatterns = [path(f'api{pattern.pattern}', pattern.callback, pattern.default_args, pattern.name) for pattern in media_urlpatterns]
urlpatterns += media_urlpatterns