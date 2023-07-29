from django.urls import reverse_lazy, reverse
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

from ..models import Person
from ..forms import PersonForm

from r2e.commom import get_pagination_url


class PersonList(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10
    extra_context = {"title": "People"}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return Person.objects.all()
        else:
            return Person.objects.filter(
                name_sa__icontains=self.request.GET.get("q")
            )

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "people"
        context = super().get_context_data(**kwargs)
        context["pagination_url"] = get_pagination_url(self.request)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person
    extra_context = {"title": "Person detail"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["credit_log"] = self.object.credit_logs.all().order_by(
            "created_on"
        )
        context["stays"] = self.object.stays.all().order_by(
            "stay_center__name"
        )
        context["registers"] = self.object.registers.all().order_by(
            "-created_on"
        )
        context["delete_link"] = reverse(
            "person:delete", args=[self.object.pk]
        )
        return context


class PersonCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    permission_required = "person.add_person"
    success_url = reverse_lazy("person:list")
    extra_context = {"title": "Create Person"}

    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = self.request.user.person.center
        initial["created_by"] = self.request.user
        initial["modified_by"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class PersonUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    permission_required = "person.change_person"
    extra_context = {"title": "Update Person"}

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
        return HttpResponse(headers={"HX-Refresh": "true"})


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Person
    template_name = "base/generics/confirm_delete.html"
    permission_required = "person.delete_person"
    success_url = reverse_lazy("person:list")
