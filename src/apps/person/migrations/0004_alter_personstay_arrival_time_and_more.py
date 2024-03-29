# Generated by Django 4.2.8 on 2024-01-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0003_personstay_meals_personstay_take_meals_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personstay",
            name="arrival_time",
            field=models.CharField(
                choices=[
                    ("AEBD", "Eve day, before dinner."),
                    ("AEAD", "Eve day, after dinner."),
                    ("AFBB", "First day, before breakfast."),
                    ("AFBL", "First day, before lunch."),
                    ("AFBD", "First day, before dinner."),
                    ("AFAD", "First day, after dinner."),
                    ("ALBB", "Last day, before breakfast."),
                ],
                default="AFBL",
                max_length=4,
                verbose_name="arrival time",
            ),
        ),
        migrations.AlterField(
            model_name="personstay",
            name="departure_time",
            field=models.CharField(
                choices=[
                    ("DFBL", "First day, before lunch."),
                    ("DFBD", "First day, before dinner."),
                    ("DFAD", "First day, after dinner."),
                    ("DLBB", "Last day, before breakfast."),
                    ("DLBL", "Last day, before lunch."),
                    ("DLAL", "Last day, after lunch."),
                ],
                default="DLAL",
                max_length=4,
                verbose_name="departure time",
            ),
        ),
    ]
