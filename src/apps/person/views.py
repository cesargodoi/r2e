from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Person  # , CreditLog
from .forms import PersonForm


class PersonList(ListView):
    model = Person
    paginate = 10


class PersonDetail(DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["credit_log"] = self.object.credit_logs.all().order_by(
            "created_on"
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
    success_url = reverse_lazy("person:list")


class PersonSearch(ListView):
    model = Person
    paginate_by = 10

    def get_queryset(self):
        return Person.objects.filter(
            name_sa__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
