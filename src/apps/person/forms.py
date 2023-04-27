from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "is_active": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }
