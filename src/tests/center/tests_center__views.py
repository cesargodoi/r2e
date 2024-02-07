import pytest
from django.urls import reverse
from ..permissions import permission


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view", [("list"), ("detail"), ("create"), ("update")]
)
def test_unlogged_user_cannot_access__center_(client, create_center, view):
    """unlogged person cannot access any page of center app"""
    center = create_center()
    page = f"center:{view}"
    if view in ("update", "detail"):
        url = reverse(page, args=[str(center.pk)])
    else:
        url = reverse(page)
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__center_list__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access center list"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:list")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__200"])
def test_access__center_detail__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' and 'office' can access center detail"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:detail", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("user_type, status_code", permission["adm_off__403"])
def test_access__center_create__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """only 'superuser' can access center create"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "user_type, status_code", permission["adm__200__off__403"]
)
def test_access__center_update__by_user_type(
    create_center,
    create_user,
    create_person,
    make_login,
    user_type,
    status_code,
):
    """'admin' can access center update"""
    center = create_center()
    user = create_user(group=user_type)
    create_person(user=user, center=center)
    client = make_login(user=user)
    url = reverse("center:update", args=[center.pk])
    response = client.get(url)
    assert response.status_code == status_code
