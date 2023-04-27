from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from r2e.commom import COUNTRIES_CHOICES, phone_format


class Center(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    short_name = models.CharField(_("short name"), max_length=20, unique=True)
    city = models.CharField(_("city"), max_length=50, null=True, blank=True)
    state = models.CharField(_("state"), max_length=2, null=True, blank=True)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES_CHOICES, default="BR"
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)
    contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("contact"),
    )

    def save(self, *args, **kwargs):
        self.phone = phone_format(self.phone)
        super(Center, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("center:detail", args=[self.pk])

    def __str__(self):
        return f"{self.short_name} ({self.country})"

    class Meta:
        verbose_name = _("center")
        verbose_name_plural = _("centers")
        ordering = ["name"]
