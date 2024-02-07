import pytest
from django.urls import reverse
from ..permissions import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view", [("list"), ("detail"), ("create"), ("update")]
)
def test_unlogged_user_cannot_access__building_(
    client, create_center, create_building, view
):
    """unlogged person cannot access any page of building app"""
    center = create_center()
    building = create_building(center=center)
    page = f"center:building_{view}"
    if view in ("update", "detail"):
        url = reverse(page, args=[str(building.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__building_list__by_user_type(
    create_center,
    create_building,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access building list"""
    center = create_center()
    create_building(center=center)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:building_list")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__building_detail__by_user_type(
    create_center,
    create_building,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access center detail"""
    center = create_center()
    building = create_building(center=center)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:building_detail", args=[building.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__building_create__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access building create"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:building_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__building_update__by_user_type(
    create_center,
    create_building,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access building update"""
    center = create_center()
    building = create_building(center=center)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:building_update", args=[building.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__building_delete__by_user_type(
    create_center,
    create_building,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access building delete"""
    center = create_center()
    building = create_building(center=center)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:building_delete", args=[building.pk])
    response = client.get(url)
    assert response.status_code == status_code
