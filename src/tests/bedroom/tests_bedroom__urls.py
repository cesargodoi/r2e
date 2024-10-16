from django.urls import reverse


def test_bedroom_list_url_is_correct():
    bedroom_list = reverse("center:bedroom_list", kwargs={"id": 1})
    result = "/center/building/1/bedroom/list/"
    assert bedroom_list == result


def test_bedroom_create_url_is_correct():
    bedroom_list = reverse("center:bedroom_create", kwargs={"id": 1})
    assert bedroom_list == "/center/building/1/bedroom/create/"


def test_bedroom_update_info_url_is_correct():
    bedroom_update = reverse(
        "center:bedroom_update", kwargs={"id": 1, "pk": 1}
    )
    result = "/center/building/1/bedroom/1/update/"
    assert bedroom_update == result


def test_bedroom_delete_info_url_is_correct():
    bedroom_delete = reverse(
        "center:bedroom_delete", kwargs={"id": 1, "pk": 1}
    )
    result = "/center/building/1/bedroom/1/delete/"
    assert bedroom_delete == result
