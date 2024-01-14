from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("", include("apps.base.urls")),
    path("center/", include("apps.center.urls")),
    path("person/", include("apps.person.urls")),
    path("event/", include("apps.event.urls")),
    path("register/", include("apps.register.urls")),
]

handler403 = "apps.base.views.permission_denied_403"
