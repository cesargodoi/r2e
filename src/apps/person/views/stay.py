from django.urls import reverse_lazy, reverse

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DeleteView
from django.views.generic.edit import FormView
from ..models import Person, PersonStay
from ..forms import StayForm


class StayCreate(FormView):
    form_class = StayForm
    template_name = "person/elements/stay_form.html"
    extra_context = {"title": "Create a new Stay"}
    success_url = reverse_lazy("person:list")

    def get_initial(self):
        initial = super().get_initial()
        initial["person"] = self.kwargs["person_id"]
        return initial

    def form_valid(self, form):
        stay = form.save(commit=False)
        stay.person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.save()
        return HttpResponse(
            render_to_string(
                "person/elements/stay_row.html",
                {"stay": stay, "object": stay.person},
                self.request,
            ),
            headers={
                "HX-Redirect": reverse(
                    "person:detail", args=[self.kwargs["person_id"]]
                ),
            },
        )


class StayUpdate(FormView):
    form_class = StayForm
    template_name = "person/elements/stay_form.html"
    extra_context = {"title": "Update Stay CBV"}
    success_url = reverse_lazy("person:list")

    def get_form_kwargs(self):
        kwargs = super(StayUpdate, self).get_form_kwargs()
        instance = PersonStay.objects.get(pk=self.kwargs["pk"])
        kwargs["instance"] = instance
        return kwargs

    def form_valid(self, form):
        stay = form.save(commit=False)
        stay.person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.save()
        return HttpResponse(
            render_to_string(
                "person/elements/stay_row.html",
                {"stay": stay, "object": stay.person},
                self.request,
            ),
            headers={
                "HX-Redirect": reverse(
                    "person:detail", args=[self.kwargs["person_id"]]
                ),
            },
        )


class StayDelete(DeleteView):
    model = PersonStay
    template_name = "person/elements/confirm_delete.html"

    def get_success_url(self):
        return reverse("person:detail", args=[self.kwargs["person_id"]])
