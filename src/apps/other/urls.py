from django.urls import path
from . import views

app_name = "other"

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

# bankflag
urlpatterns += [
    path("bankflag/list/", views.BankFlagList.as_view(), name="bankflag_list"),
    path(
        "bankflag/create/",
        views.BankFlagCreate.as_view(),
        name="bankflag_create",
    ),
    path(
        "bankflag/<int:pk>/update/",
        views.BankFlagUpdate.as_view(),
        name="bankflag_update",
    ),
    path(
        "bankflag/<int:pk>/delete/",
        views.BankFlagDelete.as_view(),
        name="bankflag_delete",
    ),
    path(
        "bankflag/search/",
        views.BankFlagSearch.as_view(),
        name="bankflag_search",
    ),
]
