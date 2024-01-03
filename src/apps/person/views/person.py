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
    UserPassesTestMixin,
)

from ..models import Person
from ..forms import PersonForm

from r2e.commom import get_pagination_url


class PersonList(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10
    extra_context = {"title": "People"}

    def get_queryset(self):
        query = Person.objects.all()
        if not self.request.user.is_superuser:
            query = query.filter(
                center=self.request.user.person.center
            ).exclude(user__id=1)
        if self.request.GET.get("q"):
            return query.filter(name_sa__icontains=self.request.GET.get("q"))
        return query

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "people"
        context = super().get_context_data(**kwargs)
        context["pagination_url"] = get_pagination_url(self.request)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class PersonDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person
    extra_context = {"title": "Person detail"}

    def test_func(self):
        return self.request.user.is_superuser or (
            self.request.user.person.center == self.get_object().center
            and self.get_object().pk > 1
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class PersonUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Person
    form_class = PersonForm
    permission_required = "person.change_person"
    extra_context = {"title": "Update Person"}

    def test_func(self):
        return self.request.user.is_superuser or (
            self.request.user.person.center == self.get_object().center
            and self.get_object().pk > 1
        )

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


class PersonDelete(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Person
    template_name = "base/generics/confirm_delete.html"
    permission_required = "person.delete_person"
    success_url = reverse_lazy("person:list")

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return (
            self.request.user.person.center == self.get_object().center
            and self.get_object().pk > 1
            and "admin"
            in self.request.user.groups.values_list("name", flat=True)
        )
