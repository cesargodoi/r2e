from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from r2e.commom import BEDROOM_GENDER, COUNTRIES_CHOICES, phone_format


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
    contact = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="centers",
        verbose_name=_("contact"),
    )

    def save(self, *args, **kwargs):
        self.phone = phone_format(self.phone)
        if self.state:
            self.state = self.state.upper()
        super(Center, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("center:detail", args=[self.pk])

    def __str__(self):
        return f"{self.short_name} ({self.get_country_display()})"

    class Meta:
        verbose_name = _("center")
        verbose_name_plural = _("centers")
        ordering = ["name"]


class Building(models.Model):
    center = models.ForeignKey(
        Center, on_delete=models.SET_NULL, null=True, db_index=True
    )
    name = models.CharField(_("name"), max_length=30)
    is_active = models.BooleanField(_("active"), default=True)

    def __str__(self):
        return f"{self.name} ({self.center.short_name})"

    class Meta:
        verbose_name = _("building")
        verbose_name_plural = _("buildings")
        ordering = ["center", "name"]


class Bedroom(models.Model):
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, db_index=True
    )
    name = models.CharField(_("name"), max_length=20)
    gender = models.CharField(
        _("gender"), max_length=1, choices=BEDROOM_GENDER, default="M"
    )
    floor = models.IntegerField(_("floor"), default=0)
    bottom_beds = models.IntegerField(_("bottom beds"))
    top_beds = models.IntegerField(_("top beds"))
    is_active = models.BooleanField(_("active"), default=True)

    def __str__(self):
        return "{} - {}({})".format(
            self.name,
            self.building.name,
            self.building.center.short_name,
        )

    class Meta:
        verbose_name = _("bedroom")
        verbose_name_plural = _("bedrooms")
        ordering = ["building", "name"]
