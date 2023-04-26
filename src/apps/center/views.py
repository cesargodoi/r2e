# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Center
from .forms import CenterForm


class CenterList(ListView):
    model = Center
    paginate_by = 10


class CenterCreate(CreateView):
    model = Center
    form_class = CenterForm
    extra_context = {"title": "Create Center"}
    success_url = reverse_lazy("center:list")


class CenterUpdate(UpdateView):
    model = Center
    form_class = CenterForm
    extra_context = {"title": "Update Center"}
    success_url = reverse_lazy("center:list")


class CenterDelete(DeleteView):
    model = Center
    success_url = reverse_lazy("center:list")


class CenterSearch(ListView):
    model = Center
    paginate_by = 10

    def get_queryset(self):
        return Center.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
