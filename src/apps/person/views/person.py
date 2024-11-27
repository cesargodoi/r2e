from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from r2e.commom import get_pagination_url, us_inter_char

from ..forms import ChangeCenterForm, PersonForm
from ..models import Person


class PersonList(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 15
    extra_context = {"title": _("People")}

    def get_queryset(self):
        # query = Person.objects.all()
        # if not self.request.user.is_superuser:
        query = Person.objects.filter(
            center=self.request.user.person.center, is_active=True
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
    extra_context = {"title": _("Person detail")}

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
    extra_context = {"title": _("Create Person")}

    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = self.request.user.person.center
        initial["created_by"] = self.request.user
        initial["modified_by"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


def check_name(request):
    if len(request.GET.get("name")) < 3:  # noqa: PLR2004
        return HttpResponse()
    typed_name = us_inter_char(request.GET.get("name").lower())
    object_list = Person.objects.filter(name_sa__icontains=typed_name)
    if not object_list:
        return HttpResponse()
    template_name = "person/components/check_name_result.html"
    context = {"object_list": object_list}
    return HttpResponse(render_to_string(template_name, context, request))


class PersonUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Person
    form_class = PersonForm
    permission_required = "person.change_person"
    extra_context = {"title": _("Update Person")}

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.registers.exists():
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            form = self.get_form()
            return self.form_valid(form)


class ChangeCenter(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    form_class = ChangeCenterForm
    template_name = "person/change_center_form.html"
    extra_context = {"title": _("View other center")}

    def test_func(self):
        return (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="manager").exists()
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["modified_by"] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})
