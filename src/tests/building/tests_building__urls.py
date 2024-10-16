from django.urls import reverse


def test_building_list_url_is_correct():
    assert reverse("center:building_list") == "/center/building/list/"


def test_building_detail_url_is_correct():
    building_detail = reverse("center:building_detail", kwargs={"pk": 1})
    result = "/center/building/1/detail/"
    assert building_detail == result


def test_building_create_url_is_correct():
    assert reverse("center:building_create") == "/center/building/create/"


def test_building_update_info_url_is_correct():
    building_update = reverse("center:building_update", kwargs={"pk": 1})
    result = "/center/building/1/update/"
    assert building_update == result
