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
        "<int:pk>/update_order/",
        views.UpdateOrder.as_view(),
        name="update_order",
    ),
    path(
        "<int:event>/<int:pk>/delete_order/",
        views.DeleteOrder.as_view(),
        name="delete_order",
    ),
    path(
        "<int:reg_id>/show_stay/",
        views.show_stay,
        name="show_stay",
    ),
    path(
        "<int:pk>/show_order/",
        views.show_order,
        name="show_order",
    ),
    path(
        "person/create/",
        views.CreatePerson.as_view(),
        name="create_person",
    ),
    path("search_person/", views.search_person, name="search_person"),
    path("add_person/", views.add_person, name="add_person"),
    path(
        "adj_register_value/",
        views.adj_register_value,
        name="adj_register_value",
    ),
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
    # form of payment
    path("payform/add/", views.AddPayForm.as_view(), name="add_payform"),
    path(
        "adj_payform_value/",
        views.adj_payform_value,
        name="adj_payform_value",
    ),
    path("del_payform/", views.del_payform, name="del_payform"),
]
