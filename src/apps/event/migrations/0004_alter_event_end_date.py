# Generated by Django 4.2 on 2023-04-27 07:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0003_alter_event_options_remove_event_reg_deadline_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateField(verbose_name="end date"),
        ),
    ]