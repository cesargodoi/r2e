# Generated by Django 4.2 on 2023-05-18 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0008_remove_accommodation_up_down_and_more"),
        ("register", "0006_alter_register_bedroom"),
    ]

    operations = [
        migrations.AlterField(
            model_name="register",
            name="bedroom",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="register",
                to="event.accommodation",
                verbose_name="accommodation",
            ),
        ),
    ]
