import pytest
from django.urls import reverse
from ..permissions import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view", [("list"), ("create"), ("detail"), ("update"), ("delete")]
)
def test_unlogged_user_cannot_access__person_(client, create_person, view):
    """unlogged person cannot access any page of person app"""
    person = create_person()
    page = f"person:{view}"
    if view in ("detail", "update", "delete"):
        url = reverse(page, args=[str(person.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__person_list__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access person list"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("person:list")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__person_create__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access person create"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("person:create")
    response = client.get(url)
    assert response.status_code == status_code


# @pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
# def test_access__person_detail__by_user_type(
#     create_center,
#     create_user,
#     create_person,
#     make_login,
#     user_type,
#     status_code,
# ):
#     """'admin' and 'office' can access person detail"""
#     center = create_center()
#     user = create_user(group=user_type)
#     user2 = create_user(group=user_type)
#     create_person(user=user, center=center)
#     person = create_person(user=user2, center=center)
#     client = make_login(user=user)
#     url = reverse("person:detail", args=[person.pk])
#     response = client.get(url)
#     assert response.status_code == status_code


# @pytest.mark.parametrize(
#     "user_type, status_code", permission["adm__200__off__403"]
# )
# def test_access__center_update__by_user_type(
#     create_center,
#     create_user,
#     create_person,
#     make_login,
#     user_type,
#     status_code,
# ):
#     """'admin' can access center update"""
#     center = create_center()
#     user = create_user(group=user_type)
#     create_person(user=user, center=center)
#     client = make_login(user=user)
#     url = reverse("center:update", args=[center.pk])
#     response = client.get(url)
#     assert response.status_code == status_code
