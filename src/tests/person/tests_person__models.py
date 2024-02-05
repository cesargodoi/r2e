from apps.person.models import Person


def test_add_new_person(create_person):
    create_person()
    assert Person.objects.count() == 1


def test_update_person_address_and_UF_format(create_person):
    create_person()
    center = Person.objects.last()
    center.state = "ce"
    center.save()
    assert center.state == "CE"


def test_update_phone_and_phone_format(create_person):
    create_person()
    center = Person.objects.last()
    center.name = "Some New Name"
    center.save()
    assert center.name == "Some New Name"


def test_delete_person(create_person):
    create_person()
    Person.objects.last().delete()
    assert Person.objects.count() == 0
