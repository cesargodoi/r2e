from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.register.models import Register
from r2e.commom import ASPECTS, EXTRA_MEALS, MEALS, get_age

from ..models import Accommodation, Event
from ..schemas import (
    CollectedByCenterSchema,
    FormsOfPaymentSchema,
    PayerSchema,
    PayersSchema,
)


class ReportByAccommodation(LoginRequiredMixin, ListView):
    model = Accommodation

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.select_related(
                "register",
                "bedroom__building",
                "bedroom__building__center",
                "event",
            )
            .filter(event__pk=self.kwargs.get("pk"))
            .order_by(
                "bedroom__building",
                "bedroom__floor",
                "bedroom__name",
                "-bottom_or_top",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs.get("pk"))
        return context


class ReportByRegister(LoginRequiredMixin, ListView):
    model = Register

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.select_related(
                "person",
                "order__center",
                "accommodation",
                "created_by",
                "updated_by",
            )
            .prefetch_related("order__form_of_payments")
            .filter(order__event__pk=self.kwargs.get("pk"))
            .order_by("person__name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs.get("pk"))
        return context


# Reports
class CashBalance(ReportByRegister):
    template_name = "event/reports/cash_balance.html"
    extra_context = {"title": _("Cash Balance")}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order__center=self.request.user.person.center)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days = self.request.GET.get("days")
        context["days"] = (
            _("today")
            if days == "today"
            else "{} {}".format(
                days if days != "all" else _("every"), _("days")
            )
        )
        form_of_payments = get_form_of_payments(self.object_list, days=days)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order__center=self.request.user.person.center)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = sum(x.value for x in self.object_list)
        return context


class TotalCollectedInTheCenter(ReportByRegister):
    template_name = "event/reports/total_collected_in_the_center.html"
    extra_context = {"title": _("Total collected in the center")}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order__center=self.request.user.person.center)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payers_by_type"] = get_payers_by_type(self.object_list)
        context["totals"] = get_totals(context["payers_by_type"])
        return context


class EmergencyContacts(ReportByRegister):
    template_name = "event/reports/emergency_contacts.html"
    extra_context = {"title": _("Emergency contacts")}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(order__center=self.request.user.person.center)


class MappingByRoom(ReportByAccommodation):
    template_name = "event/reports/mapping_by_room.html"
    extra_context = {"title": _("Mapping of Accommodations")}


class MappingPerPerson(ReportByRegister):
    template_name = "event/reports/mapping_per_person.html"
    extra_context = {"title": _("Mapping per Person")}


class PeopleAtTheEvent(ReportByRegister):
    template_name = "event/reports/people_at_the_event.html"
    extra_context = {"title": _("People at the Event")}


class PeoplePerAspect(ReportByRegister):
    template_name = "event/reports/people_per_aspect.html"
    extra_context = {"title": _("People per Aspect")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aspect_list = []
        aspects = dict(ASPECTS)
        for item in self.object_list.order_by(
            "person__aspect", "person__name"
        ):
            for aspect in aspects:
                if item.person.aspect == aspect:
                    aspect_list.append(
                        {"aspect": aspects[aspect], "person": item.person.name}
                    )
        context["aspect_list"] = aspect_list
        # sorted(aspect_list, key=lambda x: x["aspect"])
        return context


class NewPupilsPerCenter(ReportByRegister):
    template_name = "event/reports/new_pupils_per_center.html"
    extra_context = {"title": _("New pupils per center")}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(person__aspect__in=["21", "A1"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_pupils_per_center = []
        aspects = dict(ASPECTS)
        for item in self.object_list.order_by(
            "person__center", "person__aspect", "person__name"
        ):
            for aspect in aspects:
                if item.person.aspect == aspect:
                    new_pupils_per_center.append(
                        {
                            "center": "{} ({})".format(
                                item.person.center.name,
                                item.person.center.country,
                            ),
                            "aspect": aspects[aspect],
                            "aspect_id": aspect,
                            "person": item.person.name,
                        }
                    )
        context["new_pupils_per_center"] = new_pupils_per_center
        return context


class GoldenHead(ReportByRegister):
    template_name = "event/reports/golden_head.html"
    extra_context = {"title": _("Golden Head pupils")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aspect_list = []
        aspects = dict(ASPECTS)
        totals = {"A5": 0, "A6": 0}
        for item in self.object_list.filter(
            person__aspect__in=["A5", "A6"]
        ).order_by("person__aspect", "person__name"):
            for aspect in aspects:
                if item.person.aspect == aspect:
                    totals[aspect] += 1
                    aspect_list.append(
                        {"aspect": aspect, "person": item.person.name}
                    )
        context["aspects"] = aspects
        context["aspect_list"] = aspect_list
        context["totals"] = totals
        return context


class PeoplePerMeal(ReportByRegister):
    template_name = "event/reports/people_per_meal.html"
    extra_context = {"title": _("People per meal")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = get_people_per_meal(self.object_list)
        return context


class PeopleWhoCannotEatGluten(ReportByRegister):
    template_name = "event/reports/people_who_cannot_eat_gluten.html"
    extra_context = {"title": _("People who cannot eat gluten")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gluten_free = self.object_list.filter(no_gluten=True)
        context["object_list"] = (
            get_people_per_meal(gluten_free) if gluten_free else None
        )
        return context


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


class SOSContacts(ReportByRegister):
    template_name = "event/reports/sos_contacts.html"
    extra_context = {"title": _("SOS Contacts")}


class TotalCollectedByCenters(ReportByRegister):
    template_name = "event/reports/total_collected_by_centers.html"
    extra_context = {"title": _("Total collected by centers")}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("order__center")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tax = self.object_list[0].order.event.min_value
        payers = get_payers(self.object_list, full=True)

        centers, center, center_name = [], None, ""

        for n, payer in enumerate(payers):
            if center_name != payer.center:
                center_name = payer.center
                if center and center.center != center_name:
                    centers.append(center)

                center = CollectedByCenterSchema(tax=tax, center=center_name)

            match payer.pg_type:
                case "free":
                    center.free += 1
                case "half":
                    center.half += 1
                case "full":
                    center.full += 1

            if len(payers) == n + 1:
                centers.append(center)

        context["centers"] = centers
        context["total"] = sum([cnt.total for cnt in centers])
        return context


#  helpers  ###################################################################
def get_people_per_meal(registers):
    meals = [[MEALS[meal], 0, []] for meal in MEALS]
    _extras = list(EXTRA_MEALS.keys())

    if len(registers[0].meals) > 6:  # noqa: PLR2004
        extra_meals = [
            [EXTRA_MEALS[m], 0, []]
            for m in _extras[0 : len(registers[0].meals) - 6]
        ]
        meals[4:4] = extra_meals

    for register in registers:
        for i in range(len(register.meals)):
            meals[i][1] += register.meals[i]
            if register.meals[i]:
                meals[i][2].append(register.person.name)

    return meals


def get_totals(payers_by_type):
    return {
        "payed": sum(x.payed for x in payers_by_type),
        "expected": sum(x.expected for x in payers_by_type),
        "difference": sum(x.difference for x in payers_by_type),
    }


def get_payers_by_type(records):
    payers = get_payers(records)
    payers_by_type = []
    pg_type = ""
    for payer in sorted(payers, key=lambda x: x.pg_type):
        if payer.pg_type != pg_type:
            pg_type = payer.pg_type

            _payers = [x for x in payers if x.pg_type == pg_type]
            by_type = PayersSchema(
                pg_type=pg_type,
                payers=[x for x in _payers if x.pg_type == pg_type],
                payed=sum(x.payed for x in _payers),
                expected=sum(x.expected for x in _payers),
            )
            payers_by_type.append(by_type)

    return payers_by_type


def get_payers(records, full=False):
    payers = []
    for r in records:
        age = get_age(r.person.birth)
        pg_type = payer_type(age, r.value)
        match pg_type:
            case "free":
                expected = Decimal(0.00)
            case "half":
                expected = r.order.event.min_value / 2
            case "full":
                expected = r.order.event.min_value

        payer = PayerSchema(
            center=f"{r.order.center.name}",
            pg_type=pg_type,
            expected=expected,
            person=None,
            age=None,
            payed=None,
        )
        if not full:
            payer.person = r.person.name
            payer.age = age
            payer.payed = r.value

        payers.append(payer)
    return payers


def payer_type(age, payed):
    ADULT = 18
    CHILD = 12

    if (not age or age > ADULT) and payed == 0.0 or age < CHILD:
        return "free"
    elif not age or age >= ADULT:
        return "full"
    elif age >= CHILD and age < ADULT:
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
        if item.order.pk not in [x.order for x in form_of_payments]:
            for fpay in item.order.form_of_payments.all().order_by(
                "-updated_on"
            ):
                form_of_payment = FormsOfPaymentSchema(
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
    for fpay in sorted(form_of_payments, key=lambda x: x.type):
        if type != fpay.type:
            type = fpay.type
            total = sum(x.value for x in form_of_payments if x.type == type)
            new_dict = {"type": type, "total": total, "objects": []}
            for _fpay in [fp for fp in form_of_payments if fp.type == type]:
                new_dict["objects"].append(_fpay)
            objects.append(new_dict)

    return objects
