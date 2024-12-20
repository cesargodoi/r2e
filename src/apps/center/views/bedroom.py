from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from r2e.commom import get_pagination_url

from ..forms import BedroomForm
from ..models import Bedroom, Building


class BedroomList(LoginRequiredMixin, ListView):
    model = Bedroom
    paginate_by = 15
    extra_context = {"title": _("Bedrooms")}
    template_name = "center/bedroom/list.html"

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Bedroom.objects.filter(
                building_id=self.kwargs["id"]
            ).order_by("floor", "name")
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
    extra_context = {"title": _("Create Bedroom")}

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
    extra_context = {"title": _("Update Bedroom")}

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
