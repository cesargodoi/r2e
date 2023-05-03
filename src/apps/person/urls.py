from django.urls import path
from . import views

app_name = "person"

# person
urlpatterns = [
    path("list/", views.PersonList.as_view(), name="list"),
    path("create/", views.PersonCreate.as_view(), name="create"),
    path("<int:pk>/detail/", views.PersonDetail.as_view(), name="detail"),
    path("<int:pk>/update/", views.PersonUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.PersonDelete.as_view(), name="delete"),
]

# stay
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
