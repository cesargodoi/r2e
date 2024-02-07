import pytest
from django.contrib import auth

new_user = dict(email="new@user.com", password="secret", group="office")


@pytest.mark.django_db
def test_user_dont_get_logged_is(client):
    client.login(email="outsider@gmail.com", password="$536wen.")
    user = auth.get_user(client)
    assert user.is_authenticated is False


def test_add_new_user_and_try_to_login(create_user_and_make_login):
    client, user = create_user_and_make_login()
    assert user.is_authenticated is True


def test_user_get_logged_out(create_user_and_make_login):
    client, user = create_user_and_make_login()
    client.logout()
    user = auth.get_user(client)
    assert user.is_authenticated is False


def test_add_new_user(create_user, django_user_model):
    create_user(**new_user)
    assert django_user_model.objects.count() == 1


def test_edit_user(create_user, django_user_model):
    user = create_user(**new_user)
    user.email = "edited@user.com"
    user.save()
    edited_user = django_user_model.objects.last()
    assert edited_user.email == "edited@user.com"


def test_delete_user(create_user, django_user_model):
    create_user()
    assert django_user_model.objects.count() == 1
    django_user_model.objects.last().delete()
    assert django_user_model.objects.count() == 0
