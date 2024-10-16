from django.urls import path

from .. import views
from .person import urlpatterns

urlpatterns += [
    path(
        "<int:person_id>/stay/create/",
        views.StayCreate.as_view(),
        name="stay_create",
    ),
    path(
        "<int:person_id>/stay/<int:pk>/update/",
        views.StayUpdate.as_view(),
        name="stay_update",
    ),
    path(
        "<int:person_id>/stay/<int:pk>/delete/",
        views.StayDelete.as_view(),
        name="stay_delete",
    ),
]
