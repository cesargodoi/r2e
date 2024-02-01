from apps.center.models import Center


def test_add_new_center(create_center):
    create_center()
    assert Center.objects.count() == 1


def test_update_center_address_and_UF_format(create_center):
    create_center()
    center = Center.objects.last()
    center.state = "ce"
    center.save()
    assert center.state == "CE"


def test_update_phone_and_phone_format(create_center):
    create_center()
    center = Center.objects.last()
    center.phone = "(11)987652143"
    center.save()
    assert center.phone == "+55 11 98765-2143"


def test_delete_center(create_center):
    create_center()
    Center.objects.last().delete()
    assert Center.objects.count() == 0
