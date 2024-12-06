from django.urls import path

from .. import views
from .event import urlpatterns

urlpatterns += [
    path(
        "<int:pk>/report/cash_balance/",
        views.CashBalance.as_view(),
        name="report_cash_balance",
    ),
    path(
        "<int:pk>/report/payment_per_person/",
        views.PaymentPerPerson.as_view(),
        name="report_payment_per_person",
    ),
    path(
        "<int:pk>/report/total_collected_in_the_center/",
        views.TotalCollectedInTheCenter.as_view(),
        name="report_total_collected_in_the_center",
    ),
    path(
        "<int:pk>/report/emergency-contacts/",
        views.EmergencyContacts.as_view(),
        name="emergency_contacts",
    ),
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
    path(
        "<int:pk>/report/staff/",
        views.Staff.as_view(),
        name="report_staff",
    ),
    path(
        "<int:pk>/report/people-per-aspect/",
        views.PeoplePerAspect.as_view(),
        name="report_people_per_aspect",
    ),
    path(
        "<int:pk>/report/people-per-center/",
        views.PeoplePerCenter.as_view(),
        name="report_people_per_center",
    ),
    path(
        "<int:pk>/report/new-pupils-per-center/",
        views.NewPupilsPerCenter.as_view(),
        name="report_new_pupils_per_center",
    ),
    path(
        "<int:pk>/report/golden-head/",
        views.GoldenHead.as_view(),
        name="reports_golden_head",
    ),
    path(
        "<int:pk>/report/people-per-meal/",
        views.PeoplePerMeal.as_view(),
        name="report_people_per_meal",
    ),
    path(
        "<int:pk>/report/people-who-cannot-eat-gluten/",
        views.PeopleWhoCannotEatGluten.as_view(),
        name="report_people_who_cannot_eat_gluten",
    ),
    path(
        "<int:pk>/report/sos-contacts/",
        views.SOSContacts.as_view(),
        name="report_sos_contacts",
    ),
    path(
        "<int:pk>/report/total-collected-by-centers/",
        views.TotalCollectedByCenters.as_view(),
        name="report_total_collected_by_centers",
    ),
]
