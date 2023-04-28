from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("center/", include("apps.center.urls")),
    path("person/", include("apps.person.urls")),
    path("event/", include("apps.event.urls")),
    path("register/", include("apps.register.urls")),
]
