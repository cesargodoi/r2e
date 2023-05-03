from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from ..models import Event
from ..forms import EventForm


# Event Views
class EventList(ListView):
    model = Event
    paginate = 10

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Event.objects.all()
        else:
            date = datetime.strptime(self.request.GET.get("q"), "%m/%Y")
            events = Event.objects.filter(
                date__month=date.month, date__year=date.year
            )
            return events

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class EventDetail(DetailView):
    model = Event


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("event:list")
    extra_context = {"title": "Create Event"}

    def get_initial(self):
        initial = super().get_initial()
        initial["created_by"] = self.request.user
        initial["modified_by"] = self.request.user
        return initial


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    extra_context = {"title": "Update Event"}

    def get_initial(self):
        initial = super().get_initial()
        initial["modified_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class EventDelete(DeleteView):
    model = Event
    template_name = "event/elements/confirm_delete.html"
    success_url = reverse_lazy("event:list")


class EventSearch(ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Event.objects.all()
        else:
            date = datetime.strptime(self.request.GET.get("q"), "%m/%Y")
            events = Event.objects.filter(
                date__month=date.month, date__year=date.year
            )
            return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
