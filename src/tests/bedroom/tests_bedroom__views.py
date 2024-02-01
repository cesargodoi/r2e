import pytest
from django.urls import reverse
from ..permissions import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view", [("list"), ("create"), ("update"), ("delete")]
)
def test_unlogged_user_cannot_access__bedroom_(
    client, create_center, create_building, create_bedroom, view
):
    """unlogged person cannot access any page of bedroom app"""
    center = create_center()
    building = create_building(center=center)
    bedroom = create_bedroom(building=building)
    page = f"center:bedroom_{view}"
    if view in ("update", "delete"):
        url = reverse(
            page, kwargs={"id": str(building.id), "pk": str(bedroom.pk)}
        )
    else:
        url = reverse(page, kwargs={"id": str(building.id)})
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__bedroom_list__by_user_type(
    create_center,
    create_building,
    create_bedroom,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access bedroom list"""
    center = create_center()
    building = create_building(center=center)
    create_bedroom(building=building)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:bedroom_list", kwargs={"id": str(building.id)})
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__bedroom_create__by_user_type(
    create_center,
    create_building,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access bedroom create"""
    center = create_center()
    building = create_building(center=center)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:bedroom_create", kwargs={"id": str(building.id)})
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__bedroom_update__by_user_type(
    create_center,
    create_building,
    create_bedroom,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access bedroom update"""
    center = create_center()
    building = create_building(center=center)
    bedroom = create_bedroom(building=building)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse(
        "center:bedroom_update",
        kwargs={"id": str(building.id), "pk": str(bedroom.pk)},
    )
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__bedroom_update__by_user_type(
    create_center,
    create_building,
    create_bedroom,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access bedroom delete"""
    center = create_center()
    building = create_building(center=center)
    bedroom = create_bedroom(building=building)
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse(
        "center:bedroom_delete",
        kwargs={"id": str(building.id), "pk": str(bedroom.pk)},
    )
    response = client.get(url)
    assert response.status_code == status_code
