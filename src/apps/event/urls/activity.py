from django.urls import path

from .. import views
from .event import urlpatterns

urlpatterns += [
    path("activity/list/", views.ActivityList.as_view(), name="activity_list"),
    path(
        "activity/create/",
        views.ActivityCreate.as_view(),
        name="activity_create",
    ),
    path(
        "activity/<int:pk>/update/",
        views.ActivityUpdate.as_view(),
        name="activity_update",
    ),
    path(
        "activity/<int:pk>/delete/",
        views.ActivityDelete.as_view(),
        name="activity_delete",
    ),
]
