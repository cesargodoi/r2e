from apps.center.models import Bedroom


def test_add_new_bedroom(create_bedroom):
    create_bedroom()
    assert Bedroom.objects.count() == 1


def test_update_bedroom(create_bedroom):
    create_bedroom()
    bedroom = Bedroom.objects.last()
    bedroom.is_active = False
    bedroom.save()
    assert Bedroom.objects.first().is_active is not True


def test_delete_bedroom(create_bedroom):
    create_bedroom()
    Bedroom.objects.last().delete()
    assert Bedroom.objects.count() == 0
