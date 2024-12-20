from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import HttpResponse, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_http_methods

from apps.event.models import Event
from apps.person.models import Person
from apps.person.views import PersonCreate, StayCreate, StayUpdate
from r2e.commom import clear_session, get_bedroom_type, get_meals

from ..forms import FormOfPaymentForm
from ..models import FormOfPayment, Order, Register
from . import utils


class CreateOrder(LoginRequiredMixin, View):
    template_name = "register/order_form.html"
    basic_context = {"title": _("Create Order")}

    def get(self, request, *args, **kwargs):
        if request.session.get("order"):
            if "saved" in request.session["order"].keys():
                clear_session(request, ["order"])
        if not request.session.get("order"):
            utils.init_session(request)
        event = Event.objects.get(pk=kwargs["event"])
        request.session["order"]["event"] = event.pk
        request.session["order"]["event_center"] = event.center.pk
        request.session["order"]["alt_mapping"] = event.alt_mapping
        request.session["order"]["center"] = kwargs["center"]
        request.session["order"]["deadline"] = event.deadline.strftime(
            "%Y-%m-%d %H:%M"
        )
        request.session["order"]["ref_value"] = float(event.ref_value)
        request.session.modified = True
        return render(request, self.template_name, self.basic_context)

    def post(self, request, *args, **kwargs):
        if request.session["order"]["order"]:
            Order.objects.filter(pk=request.session["order"]["order"]).delete()
        new_order = request.session["order"]
        event_id = new_order["event"]
        # Order
        order_dict = utils.get_dict_order_to_db(request, new_order)
        order = Order(**order_dict)
        order.save()
        # Register
        for reg in new_order["registers"]:
            register_dict = utils.get_dict_register_to_db(
                request, reg, order.id, event_id
            )
            register = Register(**register_dict)
            register.save()
        # Form of payment
        for payf in new_order["payforms"]:
            payform_dict = utils.get_dict_payforn_to_db(
                request, payf, order.id
            )
            payform = FormOfPayment(**payform_dict)
            payform.save()
        new_order["saved"] = True
        request.session.modified = True
        return redirect("event:detail", pk=new_order["event"])


def show_stay(request, reg_id):
    register = Register.objects.get(pk=reg_id)
    context = {"register": register, "title": "Stay"}
    return render(request, "register/stay_show.html", context)


def show_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {
        "order": order,
        "registers": order.registers.all(),
        "payforms": order.form_of_payments.all(),
        "title": "Order",
    }
    return render(request, "register/order_show.html", context)


class UpdateOrder(CreateOrder):
    basic_context = {"title": _("Update Order")}

    def get(self, request, *args, **kwargs):
        if request.session.get("order"):
            if "saved" in request.session["order"].keys():
                clear_session(request, ["order"])
        if not request.session.get("order"):
            utils.init_session(request)
            order = Order.objects.get(pk=kwargs["pk"])
            # adjusting section
            request.session["order"]["update"] = True
            request.session["order"]["order"] = order.pk
            request.session["order"]["event"] = order.event.pk
            request.session["order"]["event_center"] = order.event.center.pk
            request.session["order"]["alt_mapping"] = order.event.alt_mapping
            request.session["order"]["center"] = order.center.pk
            request.session["order"]["deadline"] = (
                order.event.deadline.strftime("%Y-%m-%d %H:%M")
            )
            request.session["order"]["observations"] = order.observations
            request.session["order"]["ref_value"] = float(
                order.event.ref_value
            )
            for register in order.registers.all():
                request.session["order"]["registers"].append(
                    utils.get_dict_register_update(
                        register,
                        order.event.center.pk,
                        order.event.alt_mapping,
                    )
                )
                utils.total_registers_add(
                    request.session["order"], float(register.value)
                )
            for payform in order.form_of_payments.all():
                request.session["order"]["payforms"].append(
                    utils.get_dict_payform_update(payform)
                )
                utils.total_payforms_add(
                    request.session["order"], float(payform.value)
                )
            request.session.modified = True
        return render(request, self.template_name, self.basic_context)


class DeleteOrder(LoginRequiredMixin, View):
    template_name = "register/order_delete.html"
    basic_context = {"title": _("Delete Order")}

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs["pk"])
        self.basic_context["registers"] = order.registers.all()
        self.basic_context["payforms"] = order.form_of_payments.all()
        return render(request, self.template_name, self.basic_context)

    def post(self, request, *args, **kwargs):
        Order.objects.get(pk=kwargs["pk"]).delete()
        return redirect("event:detail", pk=kwargs["event"])


#  Registers  #################################################################
class CreatePerson(PersonCreate):
    def form_valid(self, form):
        person = form.save()
        ref_value = self.request.session["order"]["ref_value"]
        alt_mapping = self.request.session["order"]["alt_mapping"]
        register_stay = utils.get_dict_register(
            person, None, ref_value, alt_mapping
        )
        self.request.session["order"]["registers"].append(register_stay)
        utils.total_registers_add(
            self.request.session["order"], register_stay["value"]
        )
        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
@require_http_methods(["GET"])
def search_person(request):
    template_name = "register/components/search_results.html"
    event_id = request.session["order"]["event"]
    registers = [
        reg.person_id
        for reg in Register.objects.filter(order__event_id=event_id)
    ]

    results = None
    if request.GET.get("term"):
        results = Person.objects.filter(
            center=request.user.person.center,
            name_sa__icontains=request.GET.get("term"),
            is_active=True,
        ).exclude(user__id=1)
        results = results[:10]

    context = {"results": results, "registers": registers}

    return render(request, template_name, context)


@login_required
@require_http_methods(["GET"])
def add_person(request):
    in_session = [
        reg["person"]["id"] for reg in request.session["order"]["registers"]
    ]
    if int(request.GET.get("id")) in in_session:
        return HttpResponse(headers={"HX-Refresh": "true"})

    person = Person.objects.get(pk=request.GET.get("id"))
    stay = person.stays.filter(
        stay_center__pk=request.session["order"]["event_center"],
    ).first()
    ref_value = request.session["order"]["ref_value"]
    alt_mapping = request.session["order"]["alt_mapping"]
    register_stay = utils.get_dict_register(
        person,
        stay,
        ref_value,
        alt_mapping,
        event_id=request.session["order"]["event"],
    )
    request.session["order"]["registers"].append(register_stay)
    utils.total_registers_add(request.session["order"], register_stay["value"])
    request.session.modified = True

    return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
def adj_register_value(request):
    _value = request.GET.get("value")
    value = (
        float(_value)
        if request.LANGUAGE_CODE == "en"
        else float(_value.replace(",", "."))
    )
    register = utils.get_register(
        request.session["order"], request.GET.get("regid")
    )
    utils.total_registers_del(request.session["order"], register["value"])
    register["value"] = value
    utils.total_registers_add(request.session["order"], value)
    request.session.modified = True

    return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
def del_register(request):
    register = utils.get_register(
        request.session["order"], request.GET.get("regid")
    )
    utils.total_registers_del(request.session["order"], register["value"])
    request.session["order"]["registers"].remove(register)
    request.session.modified = True

    return HttpResponse(headers={"HX-Refresh": "true"})


class AddStay(StayCreate):
    def get_initial(self):
        initial = super().get_initial()
        initial["stay_center"] = self.kwargs["center_id"]
        return initial

    def form_valid(self, form):
        stay = form.save(commit=False)
        stay.person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.bedroom_type = get_bedroom_type(stay)
        stay.meals = get_meals(stay)
        stay.save()
        staff_objs = form.cleaned_data["staff"]
        stay.staff.set(staff_objs)
        stay.save()

        old_register = utils.get_register(
            self.request.session["order"], self.kwargs["regid"]
        )
        self.request.session["order"]["registers"].remove(old_register)

        ref_value = self.request.session["order"]["ref_value"]
        alt_mapping = self.request.session["order"]["alt_mapping"]
        register_stay = utils.get_dict_register(
            stay.person,
            stay,
            ref_value,
            alt_mapping,
            event_id=self.request.session["order"]["event"],
        )
        self.request.session["order"]["registers"].append(register_stay)
        utils.total_registers_add(
            self.request.session["order"], register_stay["value"]
        )
        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


class EditStay(StayUpdate):
    def form_valid(self, form):
        stay = form.save(commit=False)
        person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.bedroom_type = get_bedroom_type(stay)
        stay.person = person
        staff_objs = form.cleaned_data["staff"]
        stay.staff.clear()
        stay.staff.set(staff_objs)
        stay.meals = get_meals(stay)
        stay.save()

        old_register = utils.get_register(
            self.request.session["order"], self.kwargs["pk"]
        )
        old_value = old_register["value"]
        self.request.session["order"]["registers"].remove(old_register)

        _stay = person.stays.get(pk=self.kwargs["pk"])
        alt_mapping = self.request.session["order"]["alt_mapping"]
        register_stay = utils.get_dict_register(
            person,
            _stay,
            old_value,
            alt_mapping,
            event_id=self.request.session["order"]["event"],
        )
        self.request.session["order"]["registers"].append(register_stay)

        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


#  Forms of Payment  ##########################################################
class AddPayForm(LoginRequiredMixin, View):
    template_name = "register/components/payform_form.html"
    basic_context = {"title": _("Add Form of Payment")}

    def get(self, *args, **kwargs):
        people = [
            (reg["person"]["id"], reg["person"]["name"])
            for reg in self.request.session["order"]["registers"]
        ]
        form = FormOfPaymentForm()
        form.fields["person"].choices = people
        form.fields["person"].initial = people[0][0] if people else None
        form.fields["value"].initial = abs(
            self.request.session["order"]["missing"]
        )
        self.basic_context["form"] = form
        return render(self.request, self.template_name, self.basic_context)

    def post(self, *args, **kwargs):
        _payform = QueryDict(self.request.body).dict()
        form = FormOfPaymentForm(_payform)
        if form.is_valid():
            payform = utils.get_dict_payform(_payform)
            if payform["payment_type"]["id"] == "FRE":
                self.request.session["order"]["free"] = "true"
            if payform["payment_type"]["id"] == "PND":
                self.request.session["order"]["pending"] = "true"
            self.request.session["order"]["payforms"].append(payform)
            utils.total_payforms_add(
                self.request.session["order"], payform["value"]
            )
            self.request.session.modified = True
            return HttpResponse(headers={"HX-Refresh": "true"})
        else:
            self.basic_context["form"] = form
            return render(self.request, self.template_name, self.basic_context)


@login_required
def adj_payform_value(request):
    _value = request.GET.get("value")
    value = (
        float(_value)
        if request.LANGUAGE_CODE == "en"
        else float(_value.replace(",", "."))
    )
    payform = utils.get_payform(
        request.session["order"], request.GET.get("pfid")
    )
    utils.total_payforms_del(request.session["order"], payform["value"])
    payform["value"] = value
    utils.total_payforms_add(request.session["order"], value)
    request.session.modified = True

    return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
def del_payform(request):
    payform = utils.get_payform(
        request.session["order"], request.GET.get("pfid")
    )
    utils.total_payforms_del(request.session["order"], payform["value"])
    request.session["order"]["payforms"].remove(payform)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})
