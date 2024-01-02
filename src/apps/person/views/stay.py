from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic import DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Person, PersonStay
from ..forms import StayForm

from r2e.commom import get_bedroom_type


class StayCreate(LoginRequiredMixin, FormView):
    form_class = StayForm
    template_name = "person/components/stay_form.html"
    extra_context = {"title": "Create a new Stay"}
    success_url = reverse_lazy("person:list")

    def form_valid(self, form):
        stay = form.save(commit=False)
        stay.person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.bedroom_type = get_bedroom_type(stay)
        stay.save()
        staff_objs = form.cleaned_data["staff"]
        stay.staff.set(staff_objs)
        return HttpResponse(headers={"HX-Refresh": "true"})


class StayUpdate(LoginRequiredMixin, FormView):
    form_class = StayForm
    template_name = "person/components/stay_form.html"
    extra_context = {"title": "Update Stay"}
    success_url = reverse_lazy("person:list")

    def get_form_kwargs(self):
        kwargs = super(StayUpdate, self).get_form_kwargs()
        instance = PersonStay.objects.get(pk=self.kwargs["pk"])
        kwargs["instance"] = instance
        return kwargs

    def form_valid(self, form):
        stay = form.save(commit=False)
        stay.person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.bedroom_type = get_bedroom_type(stay)
        staff_objs = form.cleaned_data["staff"]
        stay.staff.clear()
        stay.staff.set(staff_objs)
        stay.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class StayDelete(LoginRequiredMixin, DeleteView):
    model = PersonStay
    template_name = "base/generics/confirm_delete.html"

    def get_success_url(self):
        return reverse("person:detail", args=[self.kwargs["person_id"]])
