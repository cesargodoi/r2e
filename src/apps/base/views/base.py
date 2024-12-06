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
    if not file:
        return HttpResponse("No data available for download.", status=400)

    file_name = file["name"]

    tables = [pd.read_json(table_json) for table_json in file["content"]]

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for idx, df in enumerate(tables):
            sheet_name = f"Sheet{idx + 1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    buffer.seek(0)

    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(buffer, content_type=mime)
    response["Content-Disposition"] = f"attachment; filename={file_name}.xlsx"
    return response


def permission_denied_403(request, exception):
    return render(request, "base/generics/403.html", status=403)
