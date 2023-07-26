# Generated by Django 4.2 on 2023-07-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("person", "0012_remove_person_short_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="person",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]