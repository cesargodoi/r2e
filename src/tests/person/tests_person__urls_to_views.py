from django.urls import resolve, reverse
from apps.person import views


def test_does_person_list_point_to_correct_view():
    view = resolve(reverse("person:list"))
    assert view.func.view_class is views.PersonList


def test_does_person_detail_point_to_correct_view():
    view = resolve(reverse("person:detail", kwargs={"pk": 1}))
    assert view.func.view_class is views.PersonDetail


def test_does_person_create_point_to_correct_view():
    view = resolve(reverse("person:create"))
    assert view.func.view_class is views.PersonCreate


def test_does_person_update_point_to_correct_view():
    view = resolve(reverse("person:update", kwargs={"pk": 1}))
    assert view.func.view_class is views.PersonUpdate
