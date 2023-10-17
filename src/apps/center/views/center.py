from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from ..models import Center
from ..forms import CenterForm


class CenterList(LoginRequiredMixin, ListView):
    model = Center
    paginate_by = 10
    extra_context = {"title": "Centers"}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Center.objects.all()
        return Center.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class CenterDetail(LoginRequiredMixin, DetailView):
    model = Center
    extra_context = {"title": "Center Detail"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CenterCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Center
    form_class = CenterForm
    permission_required = "center.add_center"
    extra_context = {"title": "Create Center"}
    success_url = reverse_lazy("center:list")

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class CenterUpdate(LoginRequiredMixin, UpdateView):
    model = Center
    form_class = CenterForm
    extra_context = {"title": "Update Center"}
    success_url = reverse_lazy("center:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})
