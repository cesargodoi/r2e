from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Activity
from .forms import ActivityForm


class ActivityList(ListView):
    model = Activity
    template_name = "other/activity/list.html"


class ActivityCreate(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "other/activity/form.html"
    success_url = reverse_lazy("other:activity_list")
    extra_context = {"title": "Create Center"}


class ActivityUpdate(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "other/activity/form.html"
    success_url = reverse_lazy("other:activity_list")
    extra_context = {"title": "Update Center"}


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
