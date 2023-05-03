from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.center.models import Center
from r2e.commom import (
    GENDER,
    COUNTRIES_CHOICES,
    ASPECTS,
    CREDIT_OPERATIONS,
    LODGE_TYPES,
    ARRIVAL_DATE,
    ARRIVAL_TIME,
    STAFFS,
    us_inter_char,
    short_name,
    phone_format,
)


class Person(models.Model):
    center = models.ForeignKey(
        Center, on_delete=models.SET_NULL, related_name="persons", null=True
    )
    name = models.CharField(_("name"), max_length=50, unique=True)
    name_sa = models.CharField(max_length=50, editable=False)
    short_name = models.CharField(max_length=30, editable=False)
    id_card = models.CharField(_("id card"), max_length=40, unique=True)
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER, default="M"
    )
    birth = models.DateField(_("birth"))
    city = models.CharField(_("city"), max_length=50, null=True, blank=True)
    state = models.CharField(_("state"), max_length=2, null=True, blank=True)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES_CHOICES, default="BR"
    )
    aspect = models.CharField(
        _("aspect"), max_length=20, choices=ASPECTS, default="PW"
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)
    sos_contact = models.CharField(
        _("sos contact"), max_length=50, null=True, blank=True
    )
    sos_phone = models.CharField(
        _("sos phone"), max_length=20, null=True, blank=True
    )
    credit = models.DecimalField(
        _("credit"), max_digits=7, decimal_places=2, default=0.0
    )
    observations = models.CharField(
        _("observations"), max_length=255, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_person",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="modified_person",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name_sa = us_inter_char(self.name)
        self.short_name = short_name(self.name)
        self.phone = phone_format(self.phone) if self.phone else None
        self.sos_phone = (
            phone_format(self.sos_phone) if self.sos_phone else None
        )
        super(Person, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("person:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name} - {self.city} ({self.state}-{self.country})"

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
        ordering = ["name_sa"]


class CreditLog(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="credit_logs"
    )
    credit = models.DecimalField(
        _("credit"), max_digits=7, decimal_places=2, default=0.0
    )
    operation = models.CharField(
        _("operation"), max_length=3, choices=CREDIT_OPERATIONS, default="ADJ"
    )
    description = models.CharField(
        _("description"), max_length=255, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_credit_log",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="modified_credit_log",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.person.name} - ${self.credit} ({self.operation})"

    class Meta:
        verbose_name = _("credit log")
        verbose_name_plural = _("credit logs")
        ordering = ["-created_on"]


class PersonStay(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stays",
        verbose_name=_("person"),
    )
    stay_center = models.ForeignKey(
        Center,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stays",
        verbose_name=_("stay center"),
    )
    lodge = models.CharField(
        _("lodge"), max_length=3, choices=LODGE_TYPES, default="LDG"
    )
    arrival_date = models.CharField(
        _("arrival date"), max_length=2, choices=ARRIVAL_DATE, default="D1"
    )
    arrival_time = models.CharField(
        _("arrival time"), max_length=2, choices=ARRIVAL_TIME, default="BL"
    )
    no_stairs = models.BooleanField(_("no stairs"), default=False)
    no_bunk = models.BooleanField(_("no bunk"), default=False)
    bedroom = models.IntegerField(_("bedroom"), default=0)
    bedroom_alt = models.IntegerField(_("bedroom alt"), default=0)
    staff = models.CharField(
        _("staff"), max_length=3, choices=STAFFS, default="STA"
    )
    others = models.CharField(
        _("others"), max_length=255, null=True, blank=True
    )
    observations = models.CharField(
        _("observations"), max_length=255, null=True, blank=True
    )

    def __str__(self):
        return "{} | {} | [{}, {}]".format(
            self.person.name,
            self.get_lodge_display(),
            self.get_arrival_date_display(),
            self.get_arrival_time_display(),
        )

    class Meta:
        verbose_name = _("person stay")
        verbose_name_plural = _("person stays")
        ordering = ["person__name_sa"]
