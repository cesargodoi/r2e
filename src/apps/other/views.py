from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Activity, BankFlag
from .forms import ActivityForm, BankFlagForm


# Activity Views
class ActivityList(ListView):
    model = Activity
    template_name = "other/activity/list.html"


class ActivityCreate(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "other/activity/form.html"
    success_url = reverse_lazy("other:activity_list")
    extra_context = {"title": "Create Activity"}


class ActivityUpdate(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "other/activity/form.html"
    success_url = reverse_lazy("other:activity_list")
    extra_context = {"title": "Update Activity"}


class ActivityDelete(DeleteView):
    model = Activity
    template_name = "other/activity/confirm_delete.html"
    success_url = reverse_lazy("other:activity_list")


class ActivitySearch(ListView):
    model = Activity
    paginate_by = 10
    template_name = "other/activity/list.html"

    def get_queryset(self):
        return Activity.objects.filter(
            name__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context


# BankFlag Views
class BankFlagList(ListView):
    model = BankFlag
    template_name = "other/bankflag/list.html"


class BankFlagCreate(CreateView):
    model = BankFlag
    form_class = BankFlagForm
    template_name = "other/bankflag/form.html"
    success_url = reverse_lazy("other:bankflag_list")
    extra_context = {"title": "Create Bank or Flag"}


class BankFlagUpdate(UpdateView):
    model = BankFlag
    form_class = BankFlagForm
    template_name = "other/bankflag/form.html"
    success_url = reverse_lazy("other:bankflag_list")
    extra_context = {"title": "Update Bank or Flag"}


class BankFlagDelete(DeleteView):
    model = BankFlag
    template_name = "other/bankflag/confirm_delete.html"
    success_url = reverse_lazy("other:bankflag_list")


class BankFlagSearch(ListView):
    model = BankFlag
    paginate_by = 10
    template_name = "other/bankflag/list.html"

    def get_queryset(self):
        return BankFlag.objects.filter(
            name__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
