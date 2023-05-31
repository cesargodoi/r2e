import json
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic import DetailView
from django.core.paginator import Paginator

from apps.event.models import Event, Accommodation

from apps.person.models import PersonStay
from apps.register.models import Register
from apps.center.models import Bedroom

from ..forms import StaffForm

from r2e.commom import clear_session, get_pagination_url


class Accommodations(DetailView):
    model = Event
    template_name = "event/accommodation/list.html"

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        context = super().get_context_data(**kwargs)

        queryset = get_queryset_and_totals(
            self.request, self.object.pk, q=self.request.GET.get("q")
        )

        if self.request.GET.get("filter") in ["HSE", "HTL"]:
            queryset = queryset.filter(lodge=self.request.GET.get("filter"))
        elif self.request.GET.get("filter") == "alloc":
            queryset = queryset.filter(
                lodge="LDG", accommodation__isnull=False
            )
        elif self.request.GET.get("filter") == "unalloc":
            queryset = queryset.filter(lodge="LDG", accommodation__isnull=True)

        items_per_page = 10
        paginator = Paginator(queryset, items_per_page)
        page_number = self.request.GET.get("page") or 1
        page_obj = paginator.get_page(page_number)

        context["title"] = "Accommodation management"
        context["event_id"] = self.object.pk
        context["filter"] = self.request.GET.get("filter") or "all"
        context["q"] = self.request.GET.get("q", "")
        context["pagination_url"] = get_pagination_url(self.request)
        context["page_obj"] = page_obj
        context["registers"] = list(page_obj.object_list)
        return context


class RebuildTheMapping(View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_rebuild.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        kill_mapping(kwargs["event_id"])
        generate_mapping(kwargs["event_id"])
        return redirect("event:accommodations", kwargs["event_id"])


def bedroom_details(request, bedroom_id):
    template_name = "event/accommodation/bedroom_details.html"
    bedroom = Accommodation.objects.filter(bedroom_id=bedroom_id).order_by(
        "bottom_or_top"
    )
    context = {
        "bedroom": bedroom[0],
        "tops": [b for b in bedroom if b.bottom_or_top == "T"],
        "bottoms": [b for b in bedroom if b.bottom_or_top == "B"],
    }
    return render(request, template_name, context)


class AddToBedroom(View):
    def get(self, request, *args, **kwargs):
        register = Register.objects.get(id=kwargs["reg_id"])
        clear_session(request, ["add_to_bedroom"])
        request.session["add_to_bedroom"] = {
            "reg_id": register.id,
            "person_id": register.person.id,
            "center_id": register.order.event.center.id,
            "event_id": register.order.event.id,
        }
        context = {
            "event_id": register.order.event_id,
            "gender": {
                "id": register.person.gender,
                "name": register.person.get_gender_display(),
            },
        }
        template_name = "event/accommodation/add_to_bedroom.html"
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        to_bedroom = request.session["add_to_bedroom"]
        bedroom_type = (
            "T"
            if to_bedroom.get("force_top_bed")
            else to_bedroom["bedroom_type"]
        )
        accommodations = Accommodation.objects.filter(
            bedroom_id=to_bedroom["bedroom_id"],
            bottom_or_top=bedroom_type,
            register__isnull=True,
        )
        if not accommodations and bedroom_type == "T":
            accommodations = Accommodation.objects.filter(
                bedroom_id=to_bedroom["bedroom_id"],
                bottom_or_top="B",
                register__isnull=True,
            )
        if not accommodations:
            return HttpResponse(
                "Bedroom is no longer available. Please choose another one.",
                headers={
                    "HX-Retarget": "#warning",
                    "HX-Trigger": json.dumps({"showWarning": True}),
                },
            )
        selected_accommodation = accommodations[0]
        register = Register.objects.get(id=to_bedroom["reg_id"])
        register.accommodation = selected_accommodation
        register.save()
        stay = PersonStay.objects.get(id=to_bedroom["stay_id"])
        if selected_accommodation.event.alt_mapping:
            stay.bedroom_alt = to_bedroom["bedroom_id"]
        else:
            stay.bedroom = to_bedroom["bedroom_id"]
        stay.save()
        get_queryset_and_totals(
            request, register.order.event.id, get_totals=True
        )
        return HttpResponse(headers={"HX-Refresh": "true"})


def get_buildings_by_gender(request, event_id):
    template_name = "event/accommodation/elements/building_list.html"
    _buildings = Accommodation.objects.filter(
        event_id=event_id, gender=request.GET["gender"], register__isnull=True
    ).order_by("bedroom__building__name")
    buildings = {
        (b.bedroom.building.id, b.bedroom.building.name) for b in _buildings
    }
    context = {
        "buildings": buildings,
        "event_id": event_id,
        "gender": request.GET["gender"],
    }
    return HttpResponse(
        render_to_string(template_name, context, request),
        headers={"HX-Trigger": json.dumps({"hideSubmitButton": True})},
    )


def get_bedrooms_by_building(request, event_id):
    template_name = "event/accommodation/elements/bedroom_list.html"
    _bedrooms = Accommodation.objects.filter(
        event_id=event_id,
        gender=request.GET["gender"],
        register__isnull=True,
        bedroom__building_id=request.GET["building_id"],
    ).order_by("bedroom__name")
    bedrooms = {(b.bedroom.id, b.bedroom.name) for b in _bedrooms}
    context = {
        "bedrooms": bedrooms,
        "event_id": event_id,
        "gender": request.GET["gender"],
    }
    return HttpResponse(
        render_to_string(template_name, context, request),
        headers={"HX-Trigger": json.dumps({"hideSubmitButton": True})},
    )


def get_bedroom_mapping(request, event_id):
    template_name = "event/accommodation/elements/bedroom_mapping.html"
    request.session["add_to_bedroom"]["bedroom_id"] = ""
    request.session["add_to_bedroom"]["bedroom_id"] = int(
        request.GET["bedroom_id"]
    )
    _stay = PersonStay.objects.get(
        person=request.session["add_to_bedroom"]["person_id"],
        stay_center=request.session["add_to_bedroom"]["center_id"],
    )
    request.session["add_to_bedroom"]["stay_id"] = _stay.id
    request.session["add_to_bedroom"]["bedroom_type"] = _stay.bedroom_type
    request.session.modified = True
    _bedroom = Accommodation.objects.filter(
        event_id=event_id, bedroom_id=request.GET["bedroom_id"]
    )
    bottom_beds = _bedroom.filter(bottom_or_top="B").exclude(
        register__isnull=False
    )
    force_top_bed = (
        True if not bottom_beds and _stay.bedroom_type == "B" else False
    )
    context = {
        "tops": [b for b in _bedroom if b.bottom_or_top == "T"],
        "bottoms": [b for b in _bedroom if b.bottom_or_top == "B"],
        "force_top_bed": force_top_bed,
    }
    return HttpResponse(
        render_to_string(template_name, context, request),
        headers={
            "HX-Trigger": json.dumps({"showSubmitButton": True})
            if not force_top_bed
            else None
        },
    )


def force_top_bed(request):
    request.session["add_to_bedroom"]["force_top_bed"] = (
        True if request.GET.get("forceTopBed") else False
    )
    request.session.modified = True
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {"showSubmitButton": True}
                if request.GET.get("forceTopBed")
                else {"hideSubmitButton": True}
            )
        },
    )


class RemoveFromBedroom(View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_to_remove.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        register = Register.objects.get(id=kwargs["reg_id"])
        event_id = register.accommodation.event_id
        register.accommodation = None
        register.save()
        return redirect("event:accommodations", event_id)


class ManagingStaff(View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/managing_staff.html"
        register = Register.objects.get(id=kwargs["reg_id"])
        stay = register.person.stays.get(
            stay_center=register.order.event.center
        )
        form = StaffForm(instance=stay)
        context = {"title": "Managing Staff", "form": form}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        register = Register.objects.get(id=kwargs["reg_id"])
        stay = register.person.stays.get(
            stay_center=register.order.event.center
        )
        form = StaffForm(request.POST, instance=stay)
        if form.is_valid():
            staff = form.cleaned_data["staff"]
            stay.staff.clear()
            stay.staff.set(staff)
            stay.save()
            staff_on_register = " | ".join([s.name for s in staff])
            register.staff = staff_on_register
            register.save()
            return HttpResponse(headers={"HX-Refresh": "true"})


#  helpers  ###################################################################
def generate_mapping(event_id):
    event = Event.objects.get(id=event_id)
    for bed in Bedroom.objects.filter(building__center=event.center):
        bedroom = {"event": event, "bedroom": bed, "gender": bed.gender}
        for _ in range(bed.bottom_beds):
            bottom_bed = bedroom.copy()
            bottom_bed["bottom_or_top"] = "B"
            Accommodation(**bottom_bed).save()
        for _ in range(bed.top_beds):
            top_bed = bedroom.copy()
            top_bed["bottom_or_top"] = "T"
            Accommodation(**top_bed).save()


def kill_mapping(event_id):
    Accommodation.objects.filter(event_id=event_id).delete()


def get_queryset_and_totals(request, evenid, q=None, get_totals=False):
    queryset = Register.objects.filter(
        order__event=evenid, person__name__icontains=q if q else ""
    ).order_by("person")
    if get_totals:
        del request.session["accommodation"]
    if "accommodation" not in request.session or get_totals:
        request.session["accommodation"] = {}
        request.session["accommodation"]["total_registers"] = len(queryset)
        request.session["accommodation"]["allocated"] = len(
            [r for r in queryset if r.accommodation]
        )
        request.session["accommodation"]["unallocated"] = len(
            [r for r in queryset if not r.accommodation and r.lodge == "LDG"]
        )
        request.session["accommodation"]["house"] = len(
            [r for r in queryset if r.lodge == "HSE"]
        )
        request.session["accommodation"]["hotel"] = len(
            [r for r in queryset if r.lodge == "HTL"]
        )
    return queryset if not get_totals else None
