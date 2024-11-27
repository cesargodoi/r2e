from datetime import datetime

import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.person.models import Person
from apps.register.models import Register
from r2e.commom import ASPECTS, short_name

aspects = dict(ASPECTS)


def annual_frequency(request):
    current_year = datetime.now().year
    template_name = "base/reports/show_report.html"
    registers = (
        Register.objects.select_related(
            "person",
            "person__center",
            "order",
            "order__event",
            "order__event__activity",
        )
        .values(
            "person__id",
            "person__name",
            "person__aspect",
            "person__city",
            "person__state",
            "order__event__date",
        )
        .filter(person__center=request.user.person.center)
        .filter(order__event__date__year=current_year)
        .order_by("person__aspect", "person__name_sa", "order__event__date")
    )

    frequents_ids = [fid["person__id"] for fid in registers]
    frequents_ids.append(1)

    no_presences = (
        Person.objects.filter(center=request.user.person.center)
        .values("name", "aspect", "city", "state")
        .exclude(id__in=frequents_ids)
        .order_by("aspect", "name_sa")
    )

    registers = cleaned_registers(registers)
    no_presences = cleaned_registers(no_presences)

    all_people = registers + no_presences

    normalized_objects = normalize_objects(all_people)

    normalized_objects = sorted(
        normalized_objects, key=lambda x: (x["Aspect"], x["Name"])
    )

    report_data = pd.DataFrame(normalized_objects)
    report_data["Aspect"] = report_data["Aspect"].astype(str)
    report_data["Name"] = report_data["Name"].apply(short_name)
    report_data.index += 1
    totals = report_data[
        ["Feb", "Mar", "Apr", "May", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ].sum()
    report_data.loc[""] = ["", "", "Totals: ", *totals, ""]

    # prepare file.xslx
    request.session["data_to_file"] = {
        "name": get_report_file_title(
            request, f"annual-frequency_{current_year}"
        ),
        "content": report_data.to_json(orient="records"),
    }

    context = {
        "title": "{} - {} | {}".format(
            request.user.person.center, _("Annual frequency"), current_year
        ),
        "report_data": report_data.to_html(classes="pandas-table"),
        "goback": reverse("base:tools"),
        "get_file": reverse("base:get_file"),
        "search": "base/reports/searchs/period.html",
    }
    return render(request, template_name, context)


def get_register_dict(register):
    reg_dict = {}
    if register.get("person__name"):
        reg_dict["name"] = register["person__name"]
        reg_dict["aspect"] = (
            aspects[register["person__aspect"]]
            if register.get("person__aspect")
            else "---"
        )
        reg_dict["city"] = register["person__city"]
        reg_dict["state"] = register["person__state"]
        reg_dict["month"] = register["order__event__date"].strftime("%b")
    else:
        reg_dict["name"] = register["name"]
        reg_dict["aspect"] = (
            aspects[register["aspect"]] if register.get("aspect") else "---"
        )
        reg_dict["city"] = register["city"]
        reg_dict["state"] = register["state"]
        reg_dict["month"] = None
    return reg_dict


def cleaned_registers(registers):
    objects = []
    for register in registers:
        obj = get_register_dict(register)
        objects.append(obj)
    return objects


def normalize_objects(registers):
    objects = []
    name = ""
    reg = {}
    for i, obj in enumerate(registers):
        if obj["name"] != name:
            if reg != {}:
                objects.append(reg)
            name = obj["name"]
            city = f"{obj['city']} ({obj['state']})" if obj["city"] else ""
            reg = {
                "Name": obj["name"],
                "Aspect": obj["aspect"],
                "City": city,
                "Feb": 0,
                "Mar": 0,
                "Apr": 0,
                "May": 0,
                "Jun": 0,
                "Aug": 0,
                "Sep": 0,
                "Oct": 0,
                "Nov": 0,
                "Dec": 0,
                "Total": 0,
            }
            if obj["month"]:
                reg["Total"] += 1
                reg[obj["month"]] += 1
        else:  # noqa: PLR5501
            if obj["month"]:
                reg["Total"] += 1
                reg[obj["month"]] += 1
        if i == len(registers) - 1:
            objects.append(reg)
    return objects


def get_report_file_title(request, report_name):
    return "{0}_{1}.xlsx".format(
        "-".join(request.user.person.center.name.split()),
        report_name,
    )
