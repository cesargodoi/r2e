from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from django.views import View
from r2e.commom import clear_session

from apps.event.models import Event
from apps.person.models import Person
from apps.person.views import StayCreate, StayUpdate, PersonCreate


class CreateOrder(View):
    template_name = "register/create_order.html"
    basic_context = {"title": "Create Order"}

    def get(self, *args, **kwargs):
        # clear_session(self.request, ["new_order"])  # coment form multiple
        if self.request.session.get("new_order"):
            if "saved" in self.request.session["new_order"].keys():
                clear_session(self.request, ["new_order"])
                init_session(self.request)
        else:
            init_session(self.request)
        event = Event.objects.get(pk=self.kwargs["event"])
        self.request.session["new_order"]["event"] = event.pk
        self.request.session["new_order"]["center"] = self.kwargs["center"]
        self.request.session["new_order"]["ref_value"] = float(event.ref_value)
        self.request.session.modified = True
        return render(self.request, self.template_name, self.basic_context)


class CreatePerson(PersonCreate):
    def form_valid(self, form):
        person = form.save()
        ref_value = self.request.session["new_order"]["ref_value"]
        register_stay = get_dict_stay(person, None, ref_value)
        self.request.session["new_order"]["registers"].append(register_stay)
        total_registers_add(
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
    register_stay = get_dict_stay(person, stay, ref_value)
    request.session["new_order"]["registers"].append(register_stay)
    total_registers_add(request.session["new_order"], register_stay["value"])
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


def adj_value(request):
    value = float(request.GET.get("value"))
    register = get_register(
        request.session["new_order"], request.GET.get("regid")
    )
    request.session["new_order"]["total_registers"] -= register["value"]
    register["value"] = value
    total_registers_add(request.session["new_order"], value)
    request.session.modified = True
    return HttpResponse(headers={"HX-Refresh": "true"})


def del_register(request):
    register = get_register(
        request.session["new_order"], request.GET.get("regid")
    )
    total_registers_del(request.session["new_order"], register["value"])
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

        old_register = get_register(
            self.request.session["new_order"], self.kwargs["regid"]
        )
        self.request.session["new_order"]["registers"].remove(old_register)

        register_stay = get_dict_stay(
            person, stay, self.request.session["new_order"]["ref_value"]
        )
        self.request.session["new_order"]["registers"].append(register_stay)
        total_registers_add(
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

        old_register = get_register(
            self.request.session["new_order"], self.kwargs["pk"]
        )
        old_value = old_register["value"]
        self.request.session["new_order"]["registers"].remove(old_register)

        _stay = person.stays.get(pk=self.kwargs["pk"])
        register_stay = get_dict_stay(person, _stay, old_value)
        self.request.session["new_order"]["registers"].append(register_stay)

        self.request.session.modified = True
        return HttpResponse(headers={"HX-Refresh": "true"})


# Helpers
def init_session(request):
    request.session["new_order"] = {
        "event": None,
        "center": None,
        "registers": [],
        "payforms": [],
        "ref_value": 0.0,
        "total_registers": 0.0,
        "total_forms_of_payment": 0.0,
        "missing": 0.0,
    }


def get_dict_stay(person, stay, ref_value):
    return dict(
        regid=stay.id if stay else f"{person.name[:3].upper()}{person.id}",
        person=dict(name=person.name, id=person.id),
        lodge=stay.get_lodge_display() if stay else "",
        arrival_date=stay.get_arrival_date_display() if stay else "",
        arrival_time=stay.get_arrival_time_display() if stay else "",
        no_stairs=stay.no_stairs if stay else "",
        no_bunk=stay.no_bunk if stay else "",
        observations=stay.observations if stay else "",
        value=ref_value if stay else 0.0,
    )


def get_register(new_order, regid):
    return [
        reg
        for reg in new_order["registers"]
        if str(reg["regid"]) == str(regid)
    ][0]


def total_registers_add(new_order, value):
    new_order["total_registers"] += value


def total_registers_del(new_order, value):
    new_order["total_registers"] -= value
    if new_order["total_registers"] < 0:
        new_order["total_registers"] = 0.0
