from django.urls import path

from .. import views
from .center import urlpatterns

urlpatterns += [
    path("building/list/", views.BuildingList.as_view(), name="building_list"),
    path(
        "building/<int:pk>/detail/",
        views.BuildingDetail.as_view(),
        name="building_detail",
    ),
    path(
        "building/create/",
        views.BuildingCreate.as_view(),
        name="building_create",
    ),
    path(
        "building/<int:pk>/update/",
        views.BuildingUpdate.as_view(),
        name="building_update",
    ),
    path(
        "building/<int:pk>/delete/",
        views.BuildingDelete.as_view(),
        name="building_delete",
    ),
]
