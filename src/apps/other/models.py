from django.db import models
from django.utils.translation import gettext_lazy as _


class BankFlag(models.Model):
    name = models.CharField(_("name"), max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("bank flag")
        verbose_name_plural = _("bank flags")
        ordering = ["name"]
