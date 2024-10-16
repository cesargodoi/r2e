from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import BankFlagForm
from ..models import BankFlag


# BankFlag Views
class BankFlagList(LoginRequiredMixin, ListView):
    model = BankFlag
    template_name = "register/bankflag/list.html"
    extra_context = {"title": _("Bank and Flags")}

    def get_queryset(self):
        if not self.request.GET.get("q"):
            return BankFlag.objects.all()
        return BankFlag.objects.filter(
            name__icontains=self.request.GET.get("q")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context


class BankFlagCreate(LoginRequiredMixin, CreateView):
    model = BankFlag
    form_class = BankFlagForm
    template_name = "register/bankflag/form.html"
    success_url = reverse_lazy("register:bankflag_list")
    extra_context = {"title": _("Create Bank or Flag")}

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class BankFlagUpdate(LoginRequiredMixin, UpdateView):
    model = BankFlag
    form_class = BankFlagForm
    template_name = "register/bankflag/form.html"
    extra_context = {"title": _("Update Bank or Flag")}
    success_url = reverse_lazy("register:bankflag_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(headers={"HX-Refresh": "true"})


class BankFlagDelete(LoginRequiredMixin, DeleteView):
    model = BankFlag
    template_name = "base/generics/confirm_delete.html"
    permission_required = "register.delete_bankflag"
    success_url = reverse_lazy("register:bankflag_list")
