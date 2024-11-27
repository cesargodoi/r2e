from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
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


@login_required
def get_file(request):
    file = request.session["data_to_file"]
    df = pd.read_json(file["content"])

    if "since" in df.columns:
        df["since"] = df["since"].div(60 * 60 * 24 * 1000)
    if "date" in df.columns:
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    buffer = BytesIO()

    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(buffer, content_type=mime)
    response["Content-Disposition"] = f"attachment; filename={file['name']}"
    return response


def permission_denied_403(request, exception):
    return render(request, "base/generics/403.html", status=403)
