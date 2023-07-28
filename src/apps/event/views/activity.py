from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from ..models import Activity
from ..forms import ActivityForm


class ActivityList(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "event/activity/list.html"

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Activity.objects.all()
        return Activity.objects.filter(
            name__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class ActivityCreate(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "event/activity/form.html"
    success_url = reverse_lazy("event:activity_list")
    extra_context = {"title": "Create Activity"}


class ActivityUpdate(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "event/activity/form.html"
    success_url = reverse_lazy("event:activity_list")
    extra_context = {"title": "Update Activity"}


class ActivityDelete(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "event/activity/confirm_delete.html"
    success_url = reverse_lazy("event:activity_list")
