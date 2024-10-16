from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.event.models import Event


@login_required
def home(request):
    context = {
        "title": _("Open Events"),
        "object_list": Event.objects.filter(
            status="OPN", is_active=True
        ).annotate(registers=Count("orders__registers")),
    }
    return render(request, "base/home.html", context)


@login_required
def tools(request):
    return render(request, "base/tools.html", context={"title": _("Tools")})


def permission_denied_403(request, exception):
    return render(request, "base/generics/403.html", status=403)
