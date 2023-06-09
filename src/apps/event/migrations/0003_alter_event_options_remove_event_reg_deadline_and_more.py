# Generated by Django 4.2 on 2023-04-26 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("event", "0002_event"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={
                "ordering": ["-date"],
                "verbose_name": "event",
                "verbose_name_plural": "events",
            },
        ),
        migrations.RemoveField(
            model_name="event",
            name="reg_deadline",
        ),
        migrations.RemoveField(
            model_name="event",
            name="start_date",
        ),
        migrations.AddField(
            model_name="event",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_event",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="date"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="deadline",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="deadline"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="event",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="modified_event",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateField(verbose_name="ends in"),
        ),
    ]
