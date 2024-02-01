from django.urls import resolve, reverse
from apps.center import views


def test_does_bedroom_list_point_to_correct_view():
    view = resolve(reverse("center:bedroom_list", kwargs={"id": 1}))
    assert view.func.view_class is views.BedroomList


def test_does_bedroom_create_point_to_correct_view():
    view = resolve(reverse("center:bedroom_create", kwargs={"id": 1}))
    assert view.func.view_class is views.BedroomCreate


def test_does_bedroom_update_point_to_correct_view():
    view = resolve(reverse("center:bedroom_update", kwargs={"id": 1, "pk": 1}))
    assert view.func.view_class is views.BedroomUpdate


def test_does_bedroom_delete_point_to_correct_view():
    view = resolve(reverse("center:bedroom_delete", kwargs={"id": 1, "pk": 1}))
    assert view.func.view_class is views.BedroomDelete
