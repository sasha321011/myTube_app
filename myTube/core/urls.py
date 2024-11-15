from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include("service.urls")),
    path("api-users/", include("clients.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
