from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("store.urls")),
    path('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()