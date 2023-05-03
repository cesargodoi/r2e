# Generated by Django 4.2 on 2023-05-02 08:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0004_alter_creditlog_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="sos_contact",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="sos contact"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="sos_phone",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="sos phone"
            ),
        ),
    ]
