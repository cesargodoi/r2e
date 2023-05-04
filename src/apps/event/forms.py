from django import forms
from .models import Activity, Event


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("is_active",)
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "end_date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "deadline": forms.widgets.DateInput(
                format="%Y-%m-%d %H:%M:%S", attrs={"type": "datetime-local"}
            ),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }
