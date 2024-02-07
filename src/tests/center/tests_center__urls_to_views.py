from django.urls import resolve, reverse
from apps.center import views


def test_does_center_list_point_to_correct_view():
    view = resolve(reverse("center:list"))
    assert view.func.view_class is views.CenterList


def test_does_center_detail_point_to_correct_view():
    view = resolve(reverse("center:detail", kwargs={"pk": 1}))
    assert view.func.view_class is views.CenterDetail


def test_does_center_create_point_to_correct_view():
    view = resolve(reverse("center:create"))
    assert view.func.view_class is views.CenterCreate


def test_does_center_update_point_to_correct_view():
    view = resolve(reverse("center:update", kwargs={"pk": 1}))
    assert view.func.view_class is views.CenterUpdate
