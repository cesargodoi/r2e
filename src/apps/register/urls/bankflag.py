from django.urls import path
from .register import urlpatterns
from .. import views


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
