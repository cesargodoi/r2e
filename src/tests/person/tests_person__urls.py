from django.urls import reverse


def test_person_list_url_is_correct():
    assert reverse("person:list") == "/person/"


def test_person_detail_url_is_correct():
    person_detail = reverse("person:detail", kwargs={"pk": 1})
    result = "/person/1/detail/"
    assert person_detail == result


def test_person_create_url_is_correct():
    assert reverse("person:create") == "/person/create/"


def test_person_update_info_url_is_correct():
    person_update = reverse("person:update", kwargs={"pk": 1})
    result = "/person/1/update/"
    assert person_update == result
