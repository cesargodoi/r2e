from django.views.decorators.http import require_http_methods
from django.http import QueryDict
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from r2e.commom import clear_session

from ..models import Order, Register, FormOfPayment
from ..forms import FormOfPaymentForm
from . import utils

from apps.event.models import Event
from apps.person.models import Person
from apps.person.views import StayCreate, StayUpdate, PersonCreate


class CreateOrder(View):
    template_name = "register/create_order.html"
    basic_context = {"title": "Create Order"}

    def get(self, request, *args, **kwargs):
        # clear_session(request, ["new_order"])  # coment form multiple
        if self.request.session.get("new_order"):
            if "saved" in request.session["new_order"].keys():
                clear_session(request, ["new_order"])
                utils.init_session(request)
        else:
            utils.init_session(request)
        event = Event.objects.get(pk=kwargs["event"])
        request.session["new_order"]["event"] = event.pk
        request.session["new_order"]["center"] = kwargs["center"]
        request.session["new_order"]["deadline"] = event.deadline.strftime(
            "%Y-%m-%d %H:%M"
        )
        request.session["new_order"]["ref_value"] = float(event.ref_value)
        request.session.modified = True
        return render(request, self.template_name, self.basic_context)

    def post(self, request, *args, **kwargs):
        new_order = request.session["new_order"]
        # Order
        order_dict = utils.get_dict_order_to_db(request, new_order)
        order = Order(**order_dict)
        order.save()
        # Register
        for reg in new_order["registers"]:
            register_dict = utils.get_dict_register_to_db(
                request, reg, order.id
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


#  Registers  #################################################################
class CreatePerson(PersonCreate):
    def form_valid(self, form):
        person = form.save()
        ref_value = self.request.session["new_order"]["ref_value"]
        register_stay = utils.get_dict_register(person, None, ref_value)
        self.request.session["new_order"]["registers"].append(register_stay)
        utils.total_registers_add(
            self.request.session["new_order"], register_stay["value"]
        )
        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


@require_http_methods(["GET"])
def search_person(request):
    template_name = "register/elements/search_results.html"
    results = (
        Person.objects.filter(
            name_sa__icontains=request.GET.get("term"),
            center=request.user.centers.first(),
        )[:10]
        if request.GET.get("term")
        else None
    )
    context = {"results": results}
    return render(request, template_name, context)


@require_http_methods(["GET"])
def add_person(request):
    person = Person.objects.get(pk=request.GET.get("id"))
    stay = person.stays.filter(
        stay_center__pk=request.session["new_order"]["center"],
    ).first()
    ref_value = request.session["new_order"]["ref_value"]
    register_stay = utils.get_dict_register(person, stay, ref_value)
    request.session["new_order"]["registers"].append(register_stay)
    utils.total_registers_add(
        request.session["new_order"], register_stay["value"]
    )
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


def adj_register_value(request):
    value = float(request.GET.get("value"))
    register = utils.get_register(
        request.session["new_order"], request.GET.get("regid")
    )
    utils.total_registers_del(request.session["new_order"], register["value"])
    register["value"] = value
    utils.total_registers_add(request.session["new_order"], value)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


def del_register(request):
    register = utils.get_register(
        request.session["new_order"], request.GET.get("regid")
    )
    utils.total_registers_del(request.session["new_order"], register["value"])
    request.session["new_order"]["registers"].remove(register)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


class AddStay(StayCreate):
    def get_initial(self):
        initial = super().get_initial()
        initial["stay_center"] = self.kwargs["center_id"]
        return initial

    def form_valid(self, form):
        stay = form.save(commit=False)
        person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.person = person
        stay.save()

        old_register = utils.get_register(
            self.request.session["new_order"], self.kwargs["regid"]
        )
        self.request.session["new_order"]["registers"].remove(old_register)

        register_stay = utils.get_dict_register(
            person, stay, self.request.session["new_order"]["ref_value"]
        )
        self.request.session["new_order"]["registers"].append(register_stay)
        utils.total_registers_add(
            self.request.session["new_order"], register_stay["value"]
        )
        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


class EditStay(StayUpdate):
    def form_valid(self, form):
        stay = form.save(commit=False)
        person = Person.objects.get(pk=self.kwargs["person_id"])
        stay.person = person
        stay.save()

        old_register = utils.get_register(
            self.request.session["new_order"], self.kwargs["pk"]
        )
        old_value = old_register["value"]
        self.request.session["new_order"]["registers"].remove(old_register)

        _stay = person.stays.get(pk=self.kwargs["pk"])
        register_stay = utils.get_dict_register(person, _stay, old_value)
        self.request.session["new_order"]["registers"].append(register_stay)

        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


#  Forms of Payment  ##########################################################
class AddPayForm(View):
    template_name = "register/elements/payform_form.html"
    basic_context = {"title": "Add Form of Payment"}

    def get(self, *args, **kwargs):
        people = [
            (reg["person"]["id"], reg["person"]["name"])
            for reg in self.request.session["new_order"]["registers"]
        ]
        form = FormOfPaymentForm()
        form.fields["person"].choices = people
        form.fields["person"].initial = people[0][0] if people else None
        form.fields["value"].initial = abs(
            self.request.session["new_order"]["missing"]
        )
        self.basic_context["form"] = form
        return render(self.request, self.template_name, self.basic_context)

    def post(self, *args, **kwargs):
        _payform = QueryDict(self.request.body).dict()
        form = FormOfPaymentForm(_payform)
        if form.is_valid():
            payform = utils.get_dict_payform(_payform)
            self.request.session["new_order"]["payforms"].append(payform)
            utils.total_payforms_add(
                self.request.session["new_order"], payform["value"]
            )
            self.request.session.modified = True
            return HttpResponse(headers={"HX-Refresh": "true"})
        else:
            self.basic_context["form"] = form
            return render(self.request, self.template_name, self.basic_context)


def adj_payform_value(request):
    value = float(request.GET.get("value"))
    payform = utils.get_payform(
        request.session["new_order"], request.GET.get("pfid")
    )
    utils.total_payforms_del(request.session["new_order"], payform["value"])
    payform["value"] = value
    utils.total_payforms_add(request.session["new_order"], value)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


def del_payform(request):
    payform = utils.get_payform(
        request.session["new_order"], request.GET.get("pfid")
    )
    utils.total_payforms_del(request.session["new_order"], payform["value"])
    request.session["new_order"]["payforms"].remove(payform)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})
