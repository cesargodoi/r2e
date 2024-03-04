from django import forms
from .models import Activity, Event
from apps.person.models import PersonStay
from apps.register.models import Register


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


class StayForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = (
            "person",
            "lodge",
            "arrival_time",
            "departure_time",
            "take_meals",
            "no_stairs",
            "no_bunk",
            "no_gluten",
            "snorer",
            "accommodation",
        )
        # exclude = (
        #     "stay_center",
        #     "bedroom",
        #     "bedroom_alt",
        #     "bedroom_type",
        #     "staff",
        #     "observations",
        # )
        # labels = {"staff": ""}
        widgets = {
            "accommodation": forms.HiddenInput(),
            #     "bedroom": forms.HiddenInput(),
            #     "bedroom_alt": forms.HiddenInput(),
            #     "bedroom_type": forms.HiddenInput(),
            #     "staff": forms.HiddenInput(),
            #     "observations": forms.HiddenInput(),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = PersonStay
        fields = ["staff"]
        labels = {"staff": ""}
        widgets = {"staff": forms.widgets.CheckboxSelectMultiple}
