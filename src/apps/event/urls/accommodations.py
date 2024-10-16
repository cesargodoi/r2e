from django.urls import path

from .. import views
from .event import urlpatterns

urlpatterns += [
    path(
        "<int:pk>/accommodations/",
        views.Accommodations.as_view(),
        name="accommodations",
    ),
    path(
        "<int:pk>/accommodations/bedrooms-on-event/",
        views.BedroomsOnEvent.as_view(),
        name="bedrooms_on_event",
    ),
    path(
        "<int:event_id>/accommodations/<int:bedroom_id>/bedroom_details/",
        views.bedroom_details,
        name="bedroom_details",
    ),
    path(
        "accommodations/<int:reg_id>/remove_from_bedroom/",
        views.RemoveFromBedroom.as_view(),
        name="remove_from_bedroom",
    ),
    path(
        "accommodations/<int:event_id>/add_to_bedroom/<int:reg_id>",
        views.AddToBedroom.as_view(),
        name="add_to_bedroom",
    ),
    path(
        "<int:event_id>/accommodations/get_buildings_by_gender/",
        views.get_buildings_by_gender,
        name="get_buildings_by_gender",
    ),
    path(
        "<int:event_id>/accommodations/get_bedrooms_by_building/",
        views.get_bedrooms_by_building,
        name="get_bedrooms_by_building",
    ),
    path(
        "<int:event_id>/accommodations/get_bedroom_mapping/",
        views.get_bedroom_mapping,
        name="get_bedroom_mapping",
    ),
    path("force_top_bed/", views.force_top_bed, name="force_top_bed"),
    path(
        "<int:reg_id>/change_stay/",
        views.ChangeStay.as_view(),
        name="change_stay",
    ),
    path(
        "<int:reg_id>/managing_staff/",
        views.ManagingStaff.as_view(),
        name="managing_staff",
    ),
    path(
        "<int:event_id>/accommodations/rebuild_the_mapping/",
        views.RebuildTheMapping.as_view(),
        name="rebuild_the_mapping",
    ),
    path(
        "<int:event_id>/accommodations/reload_the_mapping/",
        views.ReloadTheMapping.as_view(),
        name="reload_the_mapping",
    ),
    path(
        "<int:evenid>/reload-session/",
        views.reload_session,
        name="reload_session",
    ),
    path(
        "<int:evenid>/reload-session-bedrooms/",
        views.reload_session_bedrooms,
        name="reload_session_bedrooms",
    ),
]
