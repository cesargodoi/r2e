from django.views.generic import ListView
from apps.register.models import Register
from ..models import Accommodation


class BaseReport(ListView):
    model = Accommodation

    def get_object(self, queryset=None):
        event_pk = self.kwargs.get("pk")
        obj = Accommodation.objects.filter(event__pk=event_pk)
        return obj


class MappingByRoom(BaseReport):
    template_name = "event/reports/mapping_by_room.html"
    extra_context = {"title": "Mapping of Accommodations"}


class MappingPerPerson(BaseReport):
    template_name = "event/reports/mapping_per_person.html"
    extra_context = {"title": "Mapping per Person"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(register__isnull=False)
        return queryset


class PeopleAtTheEvent(ListView):
    model = Register
    template_name = "event/reports/people_at_the_event.html"
    extra_context = {"title": "People at the Event"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("person__name")
        return queryset
