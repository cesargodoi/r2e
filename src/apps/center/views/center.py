from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from ..models import Center
from ..forms import CenterForm
from r2e.commom import get_pagination_url


class CenterList(LoginRequiredMixin, ListView):
    model = Center
    paginate_by = 15
    extra_context = {"title": _("Centers")}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Center.objects.all()
        return Center.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagination_url"] = get_pagination_url(self.request)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class CenterDetail(LoginRequiredMixin, DetailView):
    model = Center
    extra_context = {"title": _("Center Detail")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CenterCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Center
    form_class = CenterForm
    extra_context = {"title": _("Create Center")}
    success_url = reverse_lazy("center:list")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class CenterUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Center
    form_class = CenterForm
    permission_required = "center.change_center"
    extra_context = {"title": _("Update Center")}
    success_url = reverse_lazy("center:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})
