from django.urls import path

from .. import views
from .person import urlpatterns

urlpatterns += [
    path("staff/list/", views.StaffList.as_view(), name="staff_list"),
    path("staff/create/", views.StaffCreate.as_view(), name="staff_create"),
    path(
        "staff/<int:pk>/update/",
        views.StaffUpdate.as_view(),
        name="staff_update",
    ),
    path(
        "staff/<int:pk>/delete/",
        views.StaffDelete.as_view(),
        name="staff_delete",
    ),
]
