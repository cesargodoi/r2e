from django import forms
from .models import Person, PersonStay, Staff


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = ("user", "is_active")
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"


class StayForm(forms.ModelForm):
    class Meta:
        model = PersonStay
        exclude = ["person"]
        widgets = {
            "others": forms.Textarea(attrs={"rows": 2}),
            "observations": forms.Textarea(attrs={"rows": 2}),
            "bedroom": forms.HiddenInput(),
            "bedroom_alt": forms.HiddenInput(),
            "bedroom_type": forms.HiddenInput(),
        }
