from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy


class CustomLogin(LoginView):
    template_name = "accounts/login.html"


class CustomLogout(LogoutView):
    next_page = "accounts:login"


class CustomPasswordChange(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:login")
