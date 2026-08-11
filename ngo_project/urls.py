from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    # Expose custom media paths for dev FIRST so they don't get shadowed by MEDIA_URL
    urlpatterns += static('/media/background/', document_root=settings.BACKGROUND_DIR)
    urlpatterns += static('/media/gallery/', document_root=settings.GALLERY_DIR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
