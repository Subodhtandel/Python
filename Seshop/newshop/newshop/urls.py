from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("cars10.urls"))
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    from django.contrib.staticfiles.views import serve
    urlpatterns += [
        path(settings.STATIC_URL + '<path:path>', serve),
    ]