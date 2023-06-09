# Generated by Django 4.2 on 2023-05-12 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "register",
            "0004_remove_order_form_of_payments_remove_order_registers_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="formofpayment",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="form_of_payments",
                to="register.order",
                verbose_name="order",
            ),
        ),
        migrations.AlterField(
            model_name="register",
            name="arrival_date",
            field=models.CharField(
                choices=[("D0", "Eve day"), ("D1", "1st day"), ("D2", "2nd day")],
                default="D1",
                max_length=2,
                verbose_name="arrival date",
            ),
        ),
        migrations.AlterField(
            model_name="register",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registers",
                to="register.order",
                verbose_name="order",
            ),
        ),
    ]
