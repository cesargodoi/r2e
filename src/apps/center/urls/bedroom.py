from django.urls import path

from .. import views
from .center import urlpatterns

urlpatterns += [
    path(
        "building/<int:id>/bedroom/list/",
        views.BedroomList.as_view(),
        name="bedroom_list",
    ),
    path(
        "building/<int:id>/bedroom/create/",
        views.BedroomCreate.as_view(),
        name="bedroom_create",
    ),
    path(
        "building/<int:id>/bedroom/<int:pk>/update/",
        views.BedroomUpdate.as_view(),
        name="bedroom_update",
    ),
    path(
        "building/<int:id>/bedroom/<int:pk>/delete/",
        views.BedroomDelete.as_view(),
        name="bedroom_delete",
    ),
]
