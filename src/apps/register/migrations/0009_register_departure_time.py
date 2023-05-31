# Generated by Django 4.2 on 2023-05-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0008_remove_register_bedroom_register_accommodation"),
    ]

    operations = [
        migrations.AddField(
            model_name="register",
            name="departure_time",
            field=models.CharField(
                choices=[
                    ("BL1", "Before 1st lunch"),
                    ("AL1", "After 1st lunch"),
                    ("BDN", "Before dinner"),
                    ("ADN", "After dinner"),
                    ("BL2", "Before 2nd lunch"),
                    ("AL2", "After 2nd lunch"),
                    ("END", "End of event"),
                ],
                default="END",
                max_length=3,
                verbose_name="departure time",
            ),
        ),
    ]