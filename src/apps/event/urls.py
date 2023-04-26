from django.urls import path
from . import views

app_name = "event"

# activity
urlpatterns = [
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
    path(
        "activity/search/",
        views.ActivitySearch.as_view(),
        name="activity_search",
    ),
]


# Event
urlpatterns += [
    path("list/", views.EventList.as_view(), name="list"),
    path("<int:pk>/detail/", views.EventDetail.as_view(), name="detail"),
    path("create/", views.EventCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.EventUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.EventDelete.as_view(), name="delete"),
    path("search/", views.EventSearch.as_view(), name="search"),
]
