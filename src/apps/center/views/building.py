from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from ..models import Building
from ..forms import BuildingForm

from r2e.commom import get_pagination_url


class BuildingList(LoginRequiredMixin, ListView):
    model = Building
    paginate_by = 10
    extra_context = {"title": "Buildings"}
    template_name = "center/building/list.html"

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Building.objects.all()
        return Building.objects.filter(
            name__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagination_url"] = get_pagination_url(self.request)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class BuildingDetail(LoginRequiredMixin, DetailView):
    model = Building
    extra_context = {"title": "Building Detail"}
    template_name = "center/building/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BuildingCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = "center/building/form.html"
    permission_required = "center.add_building"
    extra_context = {"title": "Create Building"}
    success_url = reverse_lazy("center:building_list")

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class BuildingUpdate(LoginRequiredMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = "center/building/form.html"
    extra_context = {"title": "Update Building"}
    success_url = reverse_lazy("center:building_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class BuildingDelete(LoginRequiredMixin, DeleteView):
    model = Building
    template_name = "base/generics/confirm_delete.html"
    permission_required = "center.delete_building"
    success_url = reverse_lazy("center:building_list")
