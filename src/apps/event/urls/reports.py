from django.urls import path
from .event import urlpatterns
from .. import views


urlpatterns += [
    path(
        "<int:pk>/report/mapping_by_room/",
        views.MappingByRoom.as_view(),
        name="report_mapping_by_room",
    ),
    path(
        "<int:pk>/report/mapping_per_person/",
        views.MappingPerPerson.as_view(),
        name="report_mapping_per_person",
    ),
    path(
        "<int:pk>/report/people_at_the_event/",
        views.PeopleAtTheEvent.as_view(),
        name="report_people_at_the_event",
    ),
]
