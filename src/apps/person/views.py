from django.urls import reverse_lazy, reverse

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.views.generic.edit import FormView
from .models import Person, PersonStay
from .forms import PersonForm, StayForm


class PersonList(ListView):
    model = Person
    paginate = 10
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
        context["q"] = self.request.GET.get("q")
        return context


class PersonDetail(DetailView):
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
        return context


class PersonCreate(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy("person:list")
    extra_context = {"title": "Create Person"}

    def get_initial(self):
        initial = super().get_initial()
        initial["created_by"] = self.request.user
        initial["modified_by"] = self.request.user
        return initial


class PersonUpdate(UpdateView):
    model = Person
    form_class = PersonForm
    extra_context = {"title": "Update Person"}

    def get_initial(self):
        initial = super().get_initial()
        initial["modified_by"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class PersonDelete(DeleteView):
    model = Person
    template_name = "person/elements/confirm_delete.html"
    success_url = reverse_lazy("person:list")


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
