from django.urls import path
from .. import views

app_name = "register"

urlpatterns = [
    path(
        "<int:center>/<int:event>/create_order/",
        views.CreateOrder.as_view(),
        name="create_order",
    ),
    path(
        "person/create/",
        views.CreatePerson.as_view(),
        name="create_person",
    ),
    path("search_person/", views.search_person, name="search_person"),
    path("add_person/", views.add_person, name="add_person"),
    path("adj_value/", views.adj_value, name="adj_value"),
    path("del_register/", views.del_register, name="del_register"),
    path(
        "<int:center_id>/<int:person_id>/<str:regid>/stay/add/",
        views.AddStay.as_view(),
        name="add_stay",
    ),
    path(
        "<int:person_id>/stay/<int:pk>/edit/",
        views.EditStay.as_view(),
        name="edit_stay",
    ),
]
