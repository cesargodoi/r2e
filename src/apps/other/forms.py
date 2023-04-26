from django import forms
from .models import Activity, BankFlag


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"


class BankFlagForm(forms.ModelForm):
    class Meta:
        model = BankFlag
        fields = "__all__"
