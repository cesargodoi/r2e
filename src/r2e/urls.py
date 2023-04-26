from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("center/", include("apps.center.urls")),
    path("event/", include("apps.event.urls")),
    path("other/", include("apps.other.urls")),
]
