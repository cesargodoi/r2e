# Generated by Django 4.2 on 2023-04-26 22:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("center", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="center",
            name="country",
            field=models.CharField(
                choices=[("BR", "Brazil"), ("US", "United States")],
                default="BR",
                max_length=2,
                verbose_name="country",
            ),
        ),
    ]
