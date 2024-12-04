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
    centers = "JAR CPS SOR SAN SPA CCP SJC".split()
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
            "person__center__abbr",
            "order__event__date",
        )
        # .filter(person__center=request.user.person.center)
        .filter(person__center__abbr__in=centers)
        .filter(order__event__date__year=current_year)
        .order_by(
            "person__center",
            "person__aspect",
            "person__name_sa",
            "order__event__date",
        )
        # .order_by("person__aspect", "person__name_sa", "order__event__date")
    )

    frequents_ids = [fid["person__id"] for fid in registers]
    frequents_ids.append(1)

    no_presences = (
        # Person.objects.filter(center=request.user.person.center)
        Person.objects.filter(center__abbr__in=centers)
        .values("name", "aspect", "city", "state", "center__abbr")
        .exclude(id__in=frequents_ids)
        .order_by("center", "aspect", "name_sa")
    )

    registers = cleaned_registers(registers)
    no_presences = cleaned_registers(no_presences)

    all_people = registers + no_presences

    normalized_objects = normalize_objects(all_people)

    normalized_objects = sorted(
        normalized_objects, key=lambda x: (x["Center"], x["Aspect"], x["Name"])
    )

    months = "Feb Mar Apr May Jun Aug Sep Oct Nov Dec".split()

    # basic tabel
    basic_table = pd.DataFrame(normalized_objects)
    basic_table["Aspect"] = basic_table["Aspect"].astype(str)
    basic_table["Name"] = basic_table["Name"].apply(short_name)
    basic_table.index += 1

    # sumario
    aspect_counts = basic_table["Aspect"].value_counts().sort_index()
    summary = aspect_counts.reset_index()
    summary.columns = ["Aspect", "Total"]
    summary.index += 1
    for month in months:
        summary[month] = basic_table.groupby("Aspect")[month].sum().values

    # add totals to basic table
    totals = basic_table[months].sum()
    basic_table.loc[""] = ["", "", "", "Totals: ", *totals, ""]

    # prepare file.xslx
    request.session["data_to_file"] = {
        "name": get_report_file_title(
            request, f"annual-frequency_{current_year}"
        ),
        "content": [
            summary.to_json(orient="records"),
            basic_table.to_json(orient="records"),
        ],
    }

    title = "{} - {} | {}".format(
        request.user.person.center, _("Annual frequency"), current_year
    )
    html_summary = "<caption>{} - summary</caption>{}".format(
        title, summary.to_html()
    )
    html_basic_table = "<caption>{}</caption>{}".format(
        title, basic_table.to_html(classes="pandas-annual-frequency")
    )

    context = {
        "title": title,
        "summary": html_summary,
        "report_data": html_basic_table,
        "goback": reverse("base:tools"),
        "get_file": reverse("base:get_file"),
        "search": "base/reports/searchs/period.html",
    }
    return render(request, template_name, context)


def get_register_dict(register):
    reg_dict = {}
    aspect = "---"
    if register.get("person__name"):
        reg_dict["name"] = register["person__name"]
        if (
            register.get("person__aspect")
            and register.get("person__aspect") != "--"
        ):
            aspect = aspects[register["person__aspect"]]
        reg_dict["aspect"] = aspect
        reg_dict["city"] = register["person__city"]
        reg_dict["state"] = register["person__state"]
        reg_dict["center"] = register["person__center__abbr"]  # comment!
        reg_dict["month"] = register["order__event__date"].strftime("%b")
    else:
        reg_dict["name"] = register["name"]
        if register.get("aspect") and register.get("aspect") != "--":
            aspect = aspects[register["aspect"]]
        reg_dict["aspect"] = aspect
        reg_dict["city"] = register["city"]
        reg_dict["state"] = register["state"]
        reg_dict["center"] = register["center__abbr"]  # comment!
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
                "Center": obj["center"],  # comment!
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
