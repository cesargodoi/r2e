from django.urls import path
from .event import urlpatterns
from .. import views

urlpatterns += [
    path(
        "<int:pk>/accommodations/",
        views.Accommodations.as_view(),
        name="accommodations",
    ),
    # path(
    #     "<int:event_id>/accommodations/generate_mapping/",
    #     views.generate_mapping,
    #     name="generate_mapping",
    # ),
    path(
        "<int:event_id>/accommodations/rebuild_the_mapping/",
        views.RebuildTheMapping.as_view(),
        name="rebuild_the_mapping",
    ),
    #     path(
    #         "<int:event_id>/accommodations/buildings/",
    #         views.BuildingsView.as_view(),
    #         name="buildings",
    #     ),
]
