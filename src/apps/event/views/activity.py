from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
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
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class ActivityCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    CreateView,
):
    model = Activity
    form_class = ActivityForm
    template_name = "event/activity/form.html"
    permission_required = "event.add_activity"
    success_url = reverse_lazy("event:activity_list")
    extra_context = {"title": "Create Activity"}

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class ActivityUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Activity
    form_class = ActivityForm
    template_name = "event/activity/form.html"
    permission_required = "event.change_activity"
    success_url = reverse_lazy("event:activity_list")
    extra_context = {"title": "Update Activity"}

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class ActivityDelete(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Activity
    template_name = "base/generics/confirm_delete.html"
    permission_required = "event.delete_activity"
    success_url = reverse_lazy("event:activity_list")

    def test_func(self):
        return self.request.user.is_superuser
