from django import forms
from .models import Center, Building, Bedroom


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = "__all__"


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = "__all__"


class BedroomForm(forms.ModelForm):
    class Meta:
        model = Bedroom
        fields = "__all__"
        widgets = {"building": forms.HiddenInput()}
