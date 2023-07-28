from decimal import Decimal
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Accommodation

from apps.register.models import Register

from r2e.commom import get_age


class ReportByAccommodation(LoginRequiredMixin, ListView):
    model = Accommodation

    def get_object(self, queryset=None):
        return Accommodation.objects.filter(event__pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.object_list.first().event
        return context


class ReportByRegister(LoginRequiredMixin, ListView):
    model = Register

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("person__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.object_list.first().order.event
        return context


class MappingByRoom(ReportByAccommodation):
    template_name = "event/reports/mapping_by_room.html"
    extra_context = {"title": "Mapping of Accommodations"}


class MappingPerPerson(ReportByAccommodation):
    template_name = "event/reports/mapping_per_person.html"
    extra_context = {"title": "Mapping per Person"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(register__isnull=False)
        return queryset


class PeopleAtTheEvent(ReportByRegister):
    template_name = "event/reports/people_at_the_event.html"
    extra_context = {"title": "People at the Event"}


class Staff(ReportByRegister):
    template_name = "event/reports/staff.html"
    extra_context = {"title": "Staff"}

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
    extra_context = {"title": "Cash Balance"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_of_payments = get_form_of_payments(self.object_list)
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
    extra_context = {"title": "Payment per Person"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = sum(x.value for x in self.object_list)
        return context


class TotalCollectedInTheCenter(ReportByRegister):
    template_name = "event/reports/total_collected_in_the_center.html"
    extra_context = {"title": "Total collected in the center"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payers_by_type"] = get_payers_by_type(self.object_list)
        context["totals"] = get_totals(context["payers_by_type"])
        return context


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


#  helpers
def get_form_of_payments(object_list):
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
