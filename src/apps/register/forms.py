from django import forms
from .models import BankFlag


class BankFlagForm(forms.ModelForm):
    class Meta:
        model = BankFlag
        fields = "__all__"
