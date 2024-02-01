import random
import pytest

from faker import Faker
from django.utils import timezone
from django.contrib.auth.models import Group, Permission

from apps.center.models import Center, Building, Bedroom
from apps.person.models import Person
from apps.event.models import Event

from r2e.commom import us_inter_char, ASPECTS

fake = Faker("pt_BR")
get_gender = random.choice(["M", "F"])


@pytest.fixture
def create_user(db, django_user_model, create_group):
    def make_user(**kwargs):
        new_user = {
            "email": kwargs.get("email") or fake.email(),
            "password": kwargs.get("password") or "1q2w3e.",
        }
        user = django_user_model.objects.create_user(**new_user)

        if kwargs.get("group"):
            user.groups.add(create_group(kwargs.get("group")))
        return user

    return make_user


@pytest.fixture
def make_login(db, client):
    def login(**kwargs):
        user = kwargs.get("user")
        client.login(email=user.email, password="1q2w3e.")
        return client

    return login


@pytest.fixture
def create_user_and_make_login(db, create_user, make_login):
    def make_auto_login(**kwargs):
        user = kwargs.get("user") or create_user()
        client = make_login(user=user)
        return client, user

    return make_auto_login


@pytest.fixture
def create_center(db, create_user):
    def make_center(**kwargs):
        name = (
            kwargs.get("name")
            or f"Center {fake.pyint(min_value=1, max_value=100)}"
        )
        new = dict(
            name=name,
            short_name=f"C-{name.split()[1]}",
            city=fake.city(),
            state=fake.estado_sigla(),
            country=fake.current_country_code(),
            phone=fake.phone_number(),
            email=kwargs.get("email") or fake.email(),
        )
        center = Center.objects.create(**new)
        contact = kwargs.get("user") or create_user()
        center.contact.add(contact)
        center.save()

        return center

    return make_center


@pytest.fixture
def create_building(db, create_center, create_user):
    def make_building(**kwargs):
        name = (
            kwargs.get("name")
            or f"Building {fake.pyint(min_value=1, max_value=20)}"
        )
        center = kwargs.get("center") or create_center()
        contact = kwargs.get("user") or create_user()
        center.contact.add(contact)
        center.save()

        new = dict(
            center=center,
            name=name,
        )
        return Building.objects.create(**new)

    return make_building


@pytest.fixture
def create_bedroom(db, create_building):
    def make_bedroom(**kwargs):
        building = kwargs.get("building") or create_building()
        name = (
            kwargs.get("name")
            or f"Bedrom {fake.pyint(min_value=1, max_value=20)}"
        )
        new = dict(
            building=building,
            name=name,
            gender=random.choice(["M", "F", "X"]),
            floor=fake.pyint(min_value=-1, max_value=2),
            bottom_beds=4,
            top_beds=4,
        )
        return Bedroom.objects.create(**new)

    return make_bedroom


@pytest.fixture
def create_person(db, create_user, create_center):
    def make_person(**kwargs):
        user = kwargs.get("user") or create_user()
        name = kwargs.get("name") or fake.name()
        birth = fake.date_of_birth(minimum_age=18, maximum_age=80, tzinfo=None)
        new = dict(
            user=user,
            center=kwargs.get("center") or create_center(),
            name=name,
            name_sa=us_inter_char(name),
            gender=kwargs.get("gender") or get_gender,
            birth=birth,
            aspect=random.choice([asp[0] for asp in ASPECTS]),
            city=fake.city(),
            state=fake.estado_sigla(),
            country=fake.current_country_code(),
            email=user.email,
            phone=fake.phone_number(),
        )
        return Person.objects.create(**new)

    return make_person


#  Groups and Permissions
@pytest.fixture
def create_group(db, get_perms):
    def make_group(name):
        group = Group.objects.create(name=name)
        perms = get_perms[name]
        group.permissions.set(perms)
        group.save()
        return group

    return make_group


@pytest.fixture
def get_perms(db):
    office = [
        "view_center",  # center
        "view_event",  # event
        "view_building",  # building
        "view_bedroom",  # bedroom
        "view_activity",  # activity
        "view_event",  # event
        "view_accommodation",  # accommodation
        "view_person",  # person
        "add_person",
        "change_person",
        "view_staff",  # staff
        "view_personstay",  # personstay
        "add_personstay",
        "change_personstay",
        "delete_personstay",
        "view_bankflag",  # bankflag
        "view_order",  # order
        "add_order",
        "change_order",
        "delete_order",
        "view_register",  # register
        "add_register",
        "change_register",
        "view_formofpayment",  # formofpayment
        "add_formofpayment",
        "change_formofpayment",
        "delete_formofpayment",
    ]

    perms = {
        "admin": [perm for perm in Permission.objects.all()],
        "office": [Permission.objects.get(codename=perm) for perm in office],
    }

    return perms
