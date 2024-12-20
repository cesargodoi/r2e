from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import StaffForm
from ..models import Staff


# Staff Views
class StaffList(LoginRequiredMixin, ListView):
    model = Staff
    template_name = "person/staff/list.html"
    extra_context = {"title": _("Staff")}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Staff.objects.all()
        return Staff.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class StaffCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "person/staff/form.html"
    success_url = reverse_lazy("person:staff_list")
    extra_context = {"title": _("Create Staff")}

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class StaffUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = "person/staff/form.html"
    extra_context = {"title": _("Update Staff")}
    success_url = reverse_lazy("person:staff_list")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class StaffDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Staff
    template_name = "base/generics/confirm_delete.html"
    success_url = reverse_lazy("person:staff_list")

    def test_func(self):
        return self.request.user.is_superuser
