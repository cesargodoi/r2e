from django.db import models
from django.utils.translation import gettext_lazy as _
from r2e.commom import ACTIVITY_TYPES


class Activity(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    activity_type = models.CharField(
        _("type"), max_length=3, choices=ACTIVITY_TYPES, default="CNF"
    )

    def __str__(self):
        return f"{self.name} ({self.activity_type})"

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
        ordering = ["name"]


class BankFlag(models.Model):
    name = models.CharField(_("name"), max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("bank flag")
        verbose_name_plural = _("bank flags")
        ordering = ["name"]
