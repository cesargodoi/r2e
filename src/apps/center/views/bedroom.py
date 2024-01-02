from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from ..models import Building, Bedroom
from ..forms import BedroomForm

from r2e.commom import get_pagination_url


class BedroomList(LoginRequiredMixin, ListView):
    model = Bedroom
    paginate_by = 10
    extra_context = {"title": "Bedrooms"}
    template_name = "center/bedroom/list.html"

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Bedroom.objects.filter(building_id=self.kwargs["id"])
        return Bedroom.objects.filter(
            building_id=self.kwargs["id"],
            name__icontains=self.request.GET.get("q"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagination_url"] = get_pagination_url(self.request)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class BedroomCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    CreateView,
):
    model = Bedroom
    form_class = BedroomForm
    template_name = "center/bedroom/form.html"
    permission_required = "center.add_bedroom"
    extra_context = {"title": "Create Bedroom"}

    def test_func(self):
        return self.request.user.is_superuser

    def get_initial(self):
        initial = super().get_initial()
        initial["building"] = Building.objects.get(pk=self.kwargs["id"])
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})

    def get_success_url(self):
        return str(
            reverse_lazy(
                "center:building_detail", kwargs={"pk": self.kwargs["id"]}
            )
        )


class BedroomUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bedroom
    form_class = BedroomForm
    template_name = "center/bedroom/form.html"
    extra_context = {"title": "Update Bedroom"}

    def test_func(self):
        return self.request.user.is_superuser

    def get_initial(self):
        initial = super().get_initial()
        initial["building"] = Building.objects.get(pk=self.kwargs["id"])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})

    def get_success_url(self):
        return str(
            reverse_lazy(
                "center:building_detail", kwargs={"pk": self.kwargs["id"]}
            )
        )


class BedroomDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bedroom
    template_name = "base/generics/confirm_delete.html"
    permission_required = "center.delete_bedroom"

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return str(
            reverse_lazy(
                "center:building_detail", kwargs={"pk": self.kwargs["id"]}
            )
        )
