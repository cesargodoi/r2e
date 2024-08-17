from datetime import datetime
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.cache import add_never_cache_headers
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from ..models import Event
from ..forms import EventForm
from ..views.accommodations import generate_mapping

from apps.register.models import Register

from r2e.commom import (
    clear_session,
    get_pagination_url,
    get_paginator,
    LODGE_TYPES,
    ARRIVAL_TIME,
    DEPARTURE_TIME,
)


# Event Views
class EventList(LoginRequiredMixin, ListView):
    model = Event
    paginate_by = 15
    extra_context = {"title": _("Events")}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset.select_related("created_by", "modified_by")
            .filter(is_active=True)
            .annotate(registers=Count("orders__registers"))
            .order_by("-date")
        )

        if self.request.GET.get("q"):
            date = datetime.strptime(self.request.GET.get("q"), "%m/%y")
            queryset = queryset.filter(
                date__month=date.month, date__year=date.year
            )

        return queryset

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q") or ""
        context["pagination_url"] = get_pagination_url(self.request)
        return context


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    extra_context = {"title": _("Records management")}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("activity", "center").filter(
            is_active=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        if "accommodation" in self.request.session:
            del self.request.session["accommodation"]
        clear_session(self.request, ["order"])
        self.request.session["nav_item"] = "event"
        user_center = self.request.user.person.center
        context = super().get_context_data(**kwargs)

        context["user_center"] = user_center.id
        q = self.request.GET.get("q")

        queryset = (
            Register.objects.select_related("person")
            .filter(
                order__event=self.kwargs.get("pk"),
                person__name__icontains=q if q else "",
            )
            .values("person__name", "order__id", "pk", "value")
            .order_by("person")
        )

        page_obj = get_paginator(
            self.request, queryset.filter(order__center=user_center), 20
        )

        context["total_registers"] = len(queryset)
        context["q"] = self.request.GET.get("q", "")
        context["pagination_url"] = get_pagination_url(self.request)
        context["page_obj"] = page_obj
        context["registers"] = list(page_obj.object_list)
        context["center_registers"] = Register.objects.filter(
            order__center=user_center, order__event=self.kwargs.get("pk")
        ).count()
        context["delete_link"] = reverse("event:delete", args=[self.object.pk])
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("event:list")
    extra_context = {"title": _("Create Event")}

    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = self.request.user.person.center
        initial["created_by"] = self.request.user
        initial["modified_by"] = self.request.user
        return initial

    def form_valid(self, form):
        event = form.save()
        generate_mapping(event.id)
        return HttpResponse(headers={"HX-Redirect": reverse("event:list")})


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    extra_context = {"title": _("Update Event")}

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


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "base/generics/confirm_delete.html"
    success_url = reverse_lazy("event:list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.orders.exists():
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            form = self.get_form()
            return self.form_valid(form)
