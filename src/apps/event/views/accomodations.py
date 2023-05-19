from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import DetailView

from apps.event.models import Event, Accommodation

from apps.register.models import Register
from apps.center.models import Bedroom

# from r2e.commom import clear_session


class Accommodations(DetailView):
    model = Event
    template_name = "event/accommodation/list.html"

    def get_context_data(self, **kwargs):
        self.request.session["nav_item"] = "event"
        context = super().get_context_data(**kwargs)
        context["title"] = "Accommodation management"
        registers = Register.objects.filter(
            order__event=self.object.pk
        ).order_by("person")
        context["registers"] = registers
        context["housed"] = len(
            [r for r in registers if r.accommodation or r.lodge != "LDG"]
        )
        context["not_housed"] = len(
            [r for r in registers if not r.accommodation and r.lodge == "LDG"]
        )
        return context


# class Accommodations(View):
#     def get(self, request, *args, **kwargs):
#         template_name = "event/accommodation/list.html"
#         event = Event.objects.get(id=kwargs["event_id"])
#         context = {"tittle": "Accommodations", "event": event}
#         return render(request, template_name, context)


class RebuildTheMapping(View):
    def get(self, request, *args, **kwargs):
        template_name = "event/accommodation/confirm_rebuild.html"
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        kill_mapping(kwargs["event_id"])
        generate_mapping(kwargs["event_id"])
        return redirect("event:accommodations", kwargs["event_id"])


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


# def get_bedroom_dict(event, bedroom):
#     return {
#         "event": event,
#         "bedroom": bedroom,
#         "gender": bedroom.gender,
#         "up_down": [0 for _ in range(bedroom.beds)],
#         "bunks": [0 for _ in range(bedroom.bunks)],
#         "building_name": bedroom.building.name,
#         "building_id": bedroom.building.id,
#     }


# def get_mapping_from_db(request, event_id):
#     template_name = "event/accommodations/mapp.html"
#     put_mapping_in_session(request, event_id)
#     male = [
#         bed
#         for bed in get_mapping_from_session(request)
#         if bed["gender"] == "X"
#     ]
#     context = {
#         "tittle": "Pegando do banco de dados",
#         "accommodations": male,
#     }
#     return render(request, template_name, context)


# def put_mapping_in_session(request, event_id):
#     clear_session(request, ["accommodations"])
#     accommodations = BedroomMapping.objects.get(event_id=event_id)
#     request.session["accommodations"] = accommodations.mapping
#     request.session.modified = True
#     return accommodations


# def get_mapping_from_session(request):
#     return request.session["accommodations"]
