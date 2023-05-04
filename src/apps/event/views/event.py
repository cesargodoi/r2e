from datetime import datetime
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
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
    extra_context = {"title": "Events"}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Event.objects.all().annotate(num_orders=Count("orders"))
        else:
            date = datetime.strptime(self.request.GET.get("q"), "%m/%Y")
            events = Event.objects.filter(
                date__month=date.month, date__year=date.year
            ).annotate(num_orders=Count("orders"))
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

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Redirect": reverse("event:list")})


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

    def form_valid(self, form):
        form.save()
        return HttpResponse(
            headers={
                "HX-Redirect": reverse("event:detail", args=[self.object.pk])
            }
        )


class EventDelete(DeleteView):
    model = Event
    template_name = "base/generics/confirm_delete.html"
    success_url = reverse_lazy("event:list")
