from django import forms
from .models import Person, PersonStay


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


# class StayFormGet(forms.ModelForm):
#     person = forms.IntegerField(widget=forms.HiddenInput)

#     class Meta:
#         model = PersonStay
#         exclude = ("bedroom", "bedroom_alt")
#         widgets = {
#             "others": forms.Textarea(attrs={"rows": 2}),
#             "observations": forms.Textarea(attrs={"rows": 2}),
#         }


class StayForm(forms.ModelForm):
    class Meta:
        model = PersonStay
        exclude = ["person", "bedroom", "bedroom_alt"]
        widgets = {
            "others": forms.Textarea(attrs={"rows": 2}),
            "observations": forms.Textarea(attrs={"rows": 2}),
        }
