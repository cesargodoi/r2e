# Generated by Django 4.2.8 on 2024-02-17 21:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0005_alter_person_aspect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="id_card",
            field=models.CharField(
                blank=True, max_length=40, null=True, verbose_name="id card"
            ),
        ),
    ]
