import json
from django.shortcuts import render, redirect, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic import DetailView

from ..forms import StaffForm

from apps.event.models import Event, Accommodation
from apps.person.models import PersonStay
from apps.register.models import Register
from apps.center.models import Bedroom

from r2e.commom import clear_session, get_pagination_url, get_paginator


class Accommodations(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DetailView,
):
    model = Event
    template_name = "event/accommodation/list.html"
    permission_required = "event.view_accommodation"

    def test_func(self):
        return self.request.user.is_superuser or (
            self.request.user.person.center == self.get_object().center
        )

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        context = super().get_context_data(**kwargs)

        queryset = get_queryset_and_totals(
            self.request,
            self.object.pk,
            q=self.request.GET.get("q"),
        )

        if self.request.GET.get("filter") in ["HSE", "HTL"]:
            queryset = queryset.filter(lodge=self.request.GET.get("filter"))
        elif self.request.GET.get("filter") == "alloc":
            queryset = queryset.filter(
                lodge="LDG", accommodation__isnull=False
            )
        elif self.request.GET.get("filter") == "unalloc":
            queryset = queryset.filter(lodge="LDG", accommodation__isnull=True)

        page_obj = get_paginator(self.request, queryset)

        context["title"] = _("Accommodation management")
        context["event_id"] = self.object.pk
        context["filter"] = self.request.GET.get("filter") or "all"
        context["q"] = self.request.GET.get("q", "")
        context["pagination_url"] = get_pagination_url(self.request)
        context["page_obj"] = page_obj
        context["registers"] = list(page_obj.object_list)
        return context


class BedroomsOnEvent(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    DetailView,
):
    model = Event
    template_name = "event/accommodation/list_of_bedrooms.html"
    permission_required = "event.view_accommodation"

    def test_func(self):
        return self.request.user.is_superuser or (
            self.request.user.person.center == self.get_object().center
        )

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        filter = self.request.GET.get("filter") or None
        context = super().get_context_data(**kwargs)

        queryset = get_queryset_and_totals_of_bedrooms(
            self.request,
            self.object.pk,
            q=self.request.GET.get("q"),
        )

        if filter and filter in "MFX":
            queryset = queryset.filter(gender=filter)

        bedrooms = get_bedrooms(queryset)
        total_used, total_unused = 0, 0
        for bedroom in bedrooms:
            total_used += bedroom["used"]
            total_unused += bedroom["unused"]

        context["title"] = _("Bedrooms on event")
        context["event_id"] = self.object.pk
        context["filter"] = self.request.GET.get("filter") or "all"
        context["q"] = self.request.GET.get("q", "")
        context["pagination_url"] = get_pagination_url(self.request)
        context["bedrooms"] = bedrooms
        context["total_used"] = total_used
        context["total_unused"] = total_unused
        return context


def get_bedrooms(queryset):
    # add 'used' status in each accommodation
    for accommodation in queryset:
        try:
            if accommodation.register:
                accommodation.used = True
        except Exception:
            accommodation.used = False

    bedrooms = []
    bed_id = 0
    for i, row in enumerate(queryset):
        if row.bedroom.id != bed_id:
            if bed_id != 0:
                bedrooms.append(bedroom)
            bedroom = dict(
                building=row.bedroom.building.name,
                id=row.bedroom.id,
                name=row.bedroom.name,
                gender=row.gender,
                floor=row.bedroom.floor,
                bottom=1 if row.bottom_or_top == "B" else 0,
                bottom_used=1
                if (row.bottom_or_top == "B" and row.used)
                else 0,
                bottom_free=1
                if (row.bottom_or_top == "B" and not row.used)
                else 0,
                top=1 if row.bottom_or_top == "T" else 0,
                top_used=1 if (row.bottom_or_top == "T" and row.used) else 0,
                top_free=1
                if (row.bottom_or_top == "T" and not row.used)
                else 0,
                used=1 if row.used else 0,
                unused=1 if not row.used else 0,
            )
            bed_id = row.bedroom.id
        else:
            bedroom["bottom"] += 1 if row.bottom_or_top == "B" else 0
            bedroom["bottom_used"] += (
                1 if (row.bottom_or_top == "B" and row.used) else 0
            )
            bedroom["bottom_free"] += (
                1 if (row.bottom_or_top == "B" and not row.used) else 0
            )
            bedroom["top"] += 1 if row.bottom_or_top == "T" else 0
            bedroom["top_used"] += (
                1 if (row.bottom_or_top == "T" and row.used) else 0
            )
            bedroom["top_free"] += (
                1 if (row.bottom_or_top == "T" and not row.used) else 0
            )
            bedroom["used"] += 1 if row.used else 0
            bedroom["unused"] += 1 if not row.used else 0
            if i == len(queryset) - 1:
                bedrooms.append(bedroom)
    return bedrooms


class RebuildTheMapping(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, View
):
    permission_required = "event.add_accommodation"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        event = Event.objects.get(id=self.kwargs.get("event_id"))
        return self.request.user.person.center == event.center

    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_rebuild.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        kill_mapping(kwargs["event_id"])
        generate_mapping(kwargs["event_id"])
        return redirect("event:accommodations", kwargs["event_id"])


class ReloadTheMapping(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, View
):
    permission_required = "event.add_accommodation"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        event = Event.objects.get(id=self.kwargs.get("event_id"))
        return self.request.user.person.center == event.center

    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_reload.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        accommodations = Accommodation.objects.filter(
            event_id=kwargs["event_id"]
        )
        bedrooms = Bedroom.objects.filter(
            building__center=accommodations[0].event.center, is_active=True
        )
        accs = list({(acc.bedroom_id, acc.gender) for acc in accommodations})
        accs.sort(key=lambda x: x[0])
        beds = [(bed.id, bed.gender) for bed in bedrooms]

        if beds == accs:
            return redirect("event:accommodations", kwargs["event_id"])

        if len(beds) >= len(accs):
            for bed in beds:
                for acc in accs:
                    if bed[0] == acc[0]:
                        if bed[1] != acc[1]:
                            remove_from_mapp(acc[0], accommodations)
                            add_to_mapp(kwargs["event_id"], bed[0], bedrooms)
                        break
                else:
                    add_to_mapp(kwargs["event_id"], bed[0], bedrooms)

        else:
            for acc in accs:
                for bed in beds:
                    if acc[0] == bed[0]:
                        if acc[1] != bed[1]:
                            remove_from_mapp(bed[0], accommodations)
                            add_to_mapp(kwargs["event_id"], acc[0], bedrooms)
                        break
                else:
                    remove_from_mapp(acc[0], accommodations)

        return redirect("event:accommodations", kwargs["event_id"])


def remove_from_mapp(bedroom_id, accommodations):
    accommodations.filter(bedroom_id=bedroom_id).delete()


def add_to_mapp(event_id, bedroom_id, bedrooms):
    bed = bedrooms.filter(id=bedroom_id).first()
    new_acc = {
        "event_id": event_id,
        "bedroom": bed,
        "gender": bed.gender,
    }
    for _ in range(bed.bottom_beds):
        bottom_bed = new_acc.copy()
        bottom_bed["bottom_or_top"] = "B"
        Accommodation(**bottom_bed).save()
    for _ in range(bed.top_beds):
        top_bed = new_acc.copy()
        top_bed["bottom_or_top"] = "T"
        Accommodation(**top_bed).save()


@login_required
def bedroom_details(request, event_id, bedroom_id):
    template_name = "event/accommodation/bedroom_details.html"
    accommodations = Accommodation.objects.filter(
        event_id=event_id, bedroom_id=bedroom_id
    ).order_by("bottom_or_top")
    context = {
        "bedroom": accommodations[0],
        "tops": [b for b in accommodations if b.bottom_or_top == "T"],
        "bottoms": [b for b in accommodations if b.bottom_or_top == "B"],
    }
    return render(request, template_name, context)


class AddToBedroom(LoginRequiredMixin, View):
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


@login_required
def reload_session(request, evenid):
    get_queryset_and_totals(request, evenid, get_totals=True)
    return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
def reload_session_bedrooms(request, evenid):
    get_queryset_and_totals_of_bedrooms(request, evenid, get_totals=True)
    return HttpResponse(headers={"HX-Refresh": "true"})


@login_required
def get_buildings_by_gender(request, event_id):
    template_name = "event/accommodation/components/buildings.html"
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


@login_required
def get_bedrooms_by_building(request, event_id):
    template_name = "event/accommodation/components/bedrooms.html"
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


@login_required
def get_bedroom_mapping(request, event_id):
    template_name = "event/accommodation/components/bedroom_mapping.html"
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


@login_required
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


class RemoveFromBedroom(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_to_remove.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        register = Register.objects.get(id=kwargs["reg_id"])
        event_id = register.accommodation.event_id
        register.accommodation = None
        register.save()
        return redirect("event:accommodations", event_id)


class ManagingStaff(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/managing_staff.html"
        register = Register.objects.get(id=kwargs["reg_id"])
        stay = register.person.stays.get(
            stay_center=register.order.event.center
        )
        form = StaffForm(instance=stay)
        context = {"title": _("Managing Staff"), "form": form}
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
    for bed in Bedroom.objects.filter(
        building__center=event.center, is_active=True
    ):
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


def get_queryset_and_totals_of_bedrooms(
    request, evenid, q=None, get_totals=False
):
    queryset = Accommodation.objects.filter(
        event=evenid, bedroom__building__name__icontains=q if q else ""
    ).order_by("bedroom__name")

    if get_totals:
        del request.session["bedrooms_on_event"]
    if "bedrooms_on_event" not in request.session or get_totals:
        request.session["bedrooms_on_event"] = {}
        request.session["bedrooms_on_event"]["all"] = len(queryset)
        request.session["bedrooms_on_event"]["M"] = len(
            [r for r in queryset if r.gender == "M"]
        )
        request.session["bedrooms_on_event"]["F"] = len(
            [r for r in queryset if r.gender == "F"]
        )
        request.session["bedrooms_on_event"]["X"] = len(
            [r for r in queryset if r.gender == "X"]
        )

    return queryset if not get_totals else None
