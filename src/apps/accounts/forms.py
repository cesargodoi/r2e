# from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]
