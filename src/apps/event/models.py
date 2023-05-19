from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.center.models import Center
from r2e.commom import (
    ACTIVITY_TYPES,
    EVENT_STATUS,
    BEDROOM_GENDER,
    BEDROOM_TYPE,
)


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


class Event(models.Model):
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.SET_NULL, null=True
    )
    description = models.CharField(
        _("description"), max_length=255, null=True, blank=True
    )
    date = models.DateField(_("date"))
    end_date = models.DateField(_("end date"))
    deadline = models.DateTimeField(_("deadline"))
    ref_value = models.DecimalField(
        _("reference value"), max_digits=7, decimal_places=2
    )
    min_value = models.DecimalField(
        _("minimum value"), max_digits=7, decimal_places=2
    )
    status = models.CharField(
        _("status"), max_length=3, choices=EVENT_STATUS, default="OPN"
    )
    alt_mapping = models.BooleanField(_("alternate mapping"), default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_event",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="modified_event",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("event:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.activity} -> {self.date} ({self.center.short_name})"

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ["-date"]


class Accommodation(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="accommodations",
        on_delete=models.CASCADE,
        null=True,
    )
    bedroom = models.ForeignKey(
        "center.Bedroom",
        related_name="accommodations",
        on_delete=models.SET_NULL,
        null=True,
    )
    gender = models.CharField(
        _("gender"), max_length=1, choices=BEDROOM_GENDER, default="M"
    )
    bottom_or_top = models.CharField(
        _("bottom or topn"), max_length=1, choices=BEDROOM_TYPE, default="B"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} ({}) - {} | {} ({}) | {} | {}".format(
            self.event.activity.name,
            self.event.center.short_name,
            self.event.date,
            self.bedroom.name,
            self.bedroom.building.name,
            self.get_gender_display(),
            self.get_bottom_or_top_display(),
        )

    class Meta:
        verbose_name = _("accommodation")
        verbose_name_plural = _("accommodations")
        ordering = ["-event__date", "bedroom__building__name", "bedroom__name"]
