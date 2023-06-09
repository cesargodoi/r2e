# Generated by Django 4.2 on 2023-04-29 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("center", "0004_building_bedroom"),
        ("person", "0003_alter_creditlog_operation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditlog",
            name="description",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="description"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="observations",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="observations"
            ),
        ),
        migrations.CreateModel(
            name="PersonStay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lodge",
                    models.CharField(
                        choices=[("LDG", "Lodge"), ("HSE", "House"), ("HTL", "Hotel")],
                        default="LDG",
                        max_length=3,
                        verbose_name="lodge",
                    ),
                ),
                (
                    "arrival_date",
                    models.CharField(
                        choices=[
                            ("D0", "Eve day"),
                            ("D1", "First day"),
                            ("D2", "Secound day"),
                        ],
                        default="D1",
                        max_length=2,
                        verbose_name="arrival date",
                    ),
                ),
                (
                    "arrival_time",
                    models.CharField(
                        choices=[
                            ("BB", "Before breakfast"),
                            ("BL", "Before lunch"),
                            ("BD", "Before diner"),
                            ("AD", "After diner"),
                        ],
                        default="BL",
                        max_length=2,
                        verbose_name="arrival time",
                    ),
                ),
                (
                    "no_stairs",
                    models.BooleanField(default=False, verbose_name="no stairs"),
                ),
                ("no_bunk", models.BooleanField(default=False, verbose_name="no bunk")),
                ("bedroom", models.IntegerField(default=0, verbose_name="bedroom")),
                (
                    "bedroom_alt",
                    models.IntegerField(default=0, verbose_name="bedroom alt"),
                ),
                (
                    "staff",
                    models.CharField(
                        choices=[
                            ("KIT", "Kitchen"),
                            ("DSW", "Dishwashing"),
                            ("REF", "Refectory"),
                            ("ACC", "Accommodation"),
                            ("EXT", "External Area"),
                            ("AFT", "Aftermath"),
                            ("SNK", "Snack"),
                            ("BRF", "Breakfast"),
                            ("TPL", "Temple"),
                            ("LDR", "Laundry"),
                            ("MTP", "Multiple"),
                            ("CNT", "Center Team"),
                        ],
                        default="STA",
                        max_length=3,
                        verbose_name="staff",
                    ),
                ),
                (
                    "others",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="others"
                    ),
                ),
                (
                    "observations",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="observations",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stays",
                        to="person.person",
                        verbose_name="person",
                    ),
                ),
                (
                    "stay_center",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stays",
                        to="center.center",
                        verbose_name="stay center",
                    ),
                ),
            ],
            options={
                "verbose_name": "person stay",
                "verbose_name_plural": "person stays",
                "ordering": ["person__name_sa"],
            },
        ),
    ]
