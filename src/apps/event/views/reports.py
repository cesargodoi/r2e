from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Accommodation, Event

from apps.register.models import Register

from r2e.commom import get_age, MEALS


class ReportByAccommodation(LoginRequiredMixin, ListView):
    model = Accommodation

    def get_object(self, queryset=None):
        return Accommodation.objects.filter(event__pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs.get("pk"))
        return context


class ReportByRegister(LoginRequiredMixin, ListView):
    model = Register

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            order__event__pk=self.kwargs.get("pk")
        ).order_by("person__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs.get("pk"))
        return context


# Reports
class MappingByRoom(ReportByAccommodation):
    template_name = "event/reports/mapping_by_room.html"
    extra_context = {"title": _("Mapping of Accommodations")}


class MappingPerPerson(ReportByAccommodation):
    template_name = "event/reports/mapping_per_person.html"
    extra_context = {"title": _("Mapping per Person")}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(register__isnull=False)
        return queryset


class PeopleAtTheEvent(ReportByRegister):
    template_name = "event/reports/people_at_the_event.html"
    extra_context = {"title": _("People at the Event")}


class Staff(ReportByRegister):
    template_name = "event/reports/staff.html"
    extra_context = {"title": _("Staff")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_list = []
        for item in self.object_list:
            if item.staff:
                for stf in item.staff.split(" | "):
                    staff_list.append({"stf": stf, "person": item.person.name})
        context["staff_list"] = sorted(staff_list, key=lambda x: x["stf"])
        return context


class CashBalance(ReportByRegister):
    template_name = "event/reports/cash_balance.html"
    extra_context = {"title": _("Cash Balance")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days = self.request.GET.get("days")
        context["days"] = days if days == "today" else f"{days} days"
        object_list = self.object_list.filter(
            order__center=self.request.user.person.center
        )
        form_of_payments = get_form_of_payments(object_list, days=days)
        summary = {"total": 0, "types": []}
        for fpay in form_of_payments:
            summary["types"].append(
                {"type": fpay["type"], "total": fpay["total"]}
            )
            summary["total"] += fpay["total"]
        context["summary"] = summary
        context["object_list"] = form_of_payments
        return context


class PaymentPerPerson(ReportByRegister):
    template_name = "event/reports/payment_per_person.html"
    extra_context = {"title": _("Payment per Person")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = sum(x.value for x in self.object_list)
        return context


class TotalCollectedInTheCenter(ReportByRegister):
    template_name = "event/reports/total_collected_in_the_center.html"
    extra_context = {"title": _("Total collected in the center")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payers_by_type"] = get_payers_by_type(self.object_list)
        context["totals"] = get_totals(context["payers_by_type"])
        return context


class PeoplePerMeal(ReportByRegister):
    template_name = "event/reports/people_per_meal.html"
    extra_context = {"title": _("People per meal")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = get_people_per_meal(self.object_list)
        return context


#  helpers
def get_people_per_meal(registers):
    meals = [
        [MEALS["MED"], 0],
        [MEALS["MFB"], 0],
        [MEALS["MFL"], 0],
        [MEALS["MFD"], 0],
        [MEALS["MLB"], 0],
        [MEALS["MLL"], 0],
    ]
    for register in registers:
        meals[0][1] += register.meals[0]
        meals[1][1] += register.meals[1]
        meals[2][1] += register.meals[2]
        meals[3][1] += register.meals[3]
        meals[4][1] += register.meals[4]
        meals[5][1] += register.meals[5]

    return meals


def get_totals(payers_by_type):
    return dict(
        payed=sum(x["payed"] for x in payers_by_type),
        expected=sum(x["expected"] for x in payers_by_type),
        difference=sum(x["difference"] for x in payers_by_type),
    )


def get_payers_by_type(records):
    payers = get_payers(records)
    payers_by_type = []
    pg_type = ""
    for payer in sorted(payers, key=lambda x: x["pg_type"]):
        if payer["pg_type"] != pg_type:
            pg_type = payer["pg_type"]
            _payers = [x for x in payers if x["pg_type"] == pg_type]
            dict_payers = dict(pg_type=pg_type)
            dict_payers["payers"] = [
                x for x in _payers if x["pg_type"] == pg_type
            ]
            dict_payers["payed"] = sum(x["payed"] for x in _payers)
            dict_payers["expected"] = sum(x["expected"] for x in _payers)
            dict_payers["difference"] = (
                dict_payers["payed"] - dict_payers["expected"]
            )
            payers_by_type.append(dict_payers)
    return payers_by_type


def get_payers(records):
    payers = []
    for r in records:
        pg_type = payer_type(get_age(r.person.birth), r.value)
        match pg_type:
            case "free":
                expected = Decimal(0.00)
            case "half":
                expected = r.order.event.min_value / 2
            case "full":
                expected = r.order.event.min_value
        payer = dict(
            person=r.person.name,
            age=get_age(r.person.birth),
            pg_type=pg_type,
            expected=expected,
            payed=r.value,
        )
        payers.append(payer)
    return payers


def payer_type(age, payed):
    if (not age or age >= 18) and payed == 0.0 or age < 7:
        return "free"
    elif not age or age >= 18:
        return "full"
    elif age >= 7 and age < 18:
        return "half"


def get_form_of_payments(object_list, days):
    if days:
        today = timezone.now().date()
        if days == "today":
            object_list = object_list.filter(created_on__date=today)
        elif days != "all":
            older_date = today - timedelta(days=int(days) - 1)
            object_list = object_list.filter(
                created_on__date__range=(older_date, today)
            )

    form_of_payments = []
    for item in object_list:
        if item.order.pk not in [x["order"] for x in form_of_payments]:
            for fpay in item.order.form_of_payments.all().order_by(
                "-updated_on"
            ):
                form_of_payment = dict(
                    order=item.order.pk,
                    type=fpay.get_payment_type_display(),
                    bank_flag=fpay.bank_flag,
                    ctrl=fpay.ctrl,
                    user=fpay.updated_by,
                    on=fpay.updated_on,
                    value=fpay.value,
                )
                form_of_payments.append(form_of_payment)
    type = ""
    objects = []
    for fpay in sorted(form_of_payments, key=lambda x: x["type"]):
        if type != fpay["type"]:
            type = fpay["type"]
            total = sum(
                x["value"] for x in form_of_payments if x["type"] == type
            )
            new_dict = dict(type=type, total=total, objects=[])
            for _fpay in [fp for fp in form_of_payments if fp["type"] == type]:
                new_dict["objects"].append(_fpay)
            objects.append(new_dict)

    return objects
