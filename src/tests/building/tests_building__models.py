from apps.center.models import Building


def test_add_new_building(create_building):
    create_building()
    assert Building.objects.count() == 1


def test_update_building(create_building):
    create_building()
    building = Building.objects.last()
    building.is_active = False
    building.save()
    assert Building.objects.first().is_active is not True


def test_delete_building(create_building):
    create_building()
    Building.objects.last().delete()
    assert Building.objects.count() == 0
