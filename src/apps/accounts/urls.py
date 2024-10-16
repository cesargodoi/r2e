from django.urls import path

from . import views as v

app_name = "accounts"

urlpatterns = [
    path("login/", v.CustomLogin.as_view(), name="login"),
    path("logout/", v.CustomLogout.as_view(), name="logout"),
    path(
        "password/change/",
        v.CustomPasswordChange.as_view(),
        name="password_change",
    ),
]
