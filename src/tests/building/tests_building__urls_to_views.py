from django.urls import resolve, reverse
from apps.center import views


def test_does_building_list_point_to_correct_view():
    view = resolve(reverse("center:building_list"))
    assert view.func.view_class is views.BuildingList


def test_does_building_detail_point_to_correct_view():
    view = resolve(reverse("center:building_detail", kwargs={"pk": 1}))
    assert view.func.view_class is views.BuildingDetail


def test_does_building_create_point_to_correct_view():
    view = resolve(reverse("center:building_create"))
    assert view.func.view_class is views.BuildingCreate


def test_does_building_update_point_to_correct_view():
    view = resolve(reverse("center:building_update", kwargs={"pk": 1}))
    assert view.func.view_class is views.BuildingUpdate
