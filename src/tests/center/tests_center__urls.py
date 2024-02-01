from django.urls import reverse


def test_center_list_url_is_correct():
    assert reverse("center:list") == "/center/"


def test_center_detail_url_is_correct():
    center_detail = reverse("center:detail", kwargs={"pk": 1})
    result = f"/center/1/detail/"
    assert center_detail == result


def test_center_create_url_is_correct():
    assert reverse("center:create") == "/center/create/"


def test_center_update_info_url_is_correct():
    center_update = reverse("center:update", kwargs={"pk": 1})
    result = f"/center/1/update/"
    assert center_update == result
