from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from r2e.commom import (
    PAYMENT_TYPES,
    LODGE_TYPES,
    ARRIVAL_DATE,
    ARRIVAL_TIME,
    STAFFS,
)


class BankFlag(models.Model):
    name = models.CharField(_("name"), max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("bank flag")
        verbose_name_plural = _("bank flags")
        ordering = ["name"]


class Order(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name=_("center"),
    )
    event = models.ForeignKey(
        "event.Event",
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
    )
    value = models.DecimalField(_("value"), max_digits=7, decimal_places=2)
    credit_launch = models.BooleanField(_("credit launch"), default=False)
    late_payment = models.BooleanField(_("late payment"), default=False)
    canceled_payment = models.BooleanField(
        _("canceled payment"), default=False
    )
    observations = models.CharField(
        _("observations"), max_length=250, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders_created",
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders_updated",
    )

    def __str__(self):
        return "{} ${} | cr:{} | lt:{} | cc:{} | at:{}".format(
            self.event,
            self.value,
            self.credit_launch,
            self.late_payment,
            self.canceled_payment,
            self.created_on.strftime("%m/%d/%Y %H:%M:%S"),
        )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-created_on"]


class Register(models.Model):
    person = models.ForeignKey(
        "person.Person",
        on_delete=models.SET_NULL,
        null=True,
        related_name="registers",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registers",
        verbose_name=_("order"),
    )
    lodge = models.CharField(
        _("lodge"), max_length=3, choices=LODGE_TYPES, default="LDG"
    )
    no_stairs = models.BooleanField(_("no stairs"), default=False)
    no_bunk = models.BooleanField(_("no bunk"), default=False)
    arrival_date = models.CharField(
        _("arrival date"), max_length=2, choices=ARRIVAL_DATE, default="D1"
    )
    arrival_time = models.CharField(
        _("arrival time"), max_length=2, choices=ARRIVAL_TIME, default="BL"
    )
    bedroom = models.ForeignKey(
        "center.Bedroom",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("bedroom"),
    )
    housed = models.BooleanField(_("housed"), default=False)
    staff = models.CharField(
        _("staff"), max_length=3, choices=STAFFS, null=True, blank=True
    )
    description = models.CharField(
        _("description"), max_length=250, null=True, blank=True
    )
    value = models.DecimalField(_("value"), max_digits=7, decimal_places=2)
    observations = models.CharField(
        _("observations"), max_length=250, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registers_created",
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registers_updated",
    )

    def __str__(self):
        return "{} | ${} | {}".format(
            self.person.name,
            self.value,
            self.created_on.strftime("%m/%d/%Y %H:%M:%S"),
        )

    class Meta:
        verbose_name = _("register")
        verbose_name_plural = _("registers")
        ordering = ["-created_on"]


class FormOfPayment(models.Model):
    person = models.ForeignKey(
        "person.Person",
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_of_payments",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_of_payments",
        verbose_name=_("order"),
    )
    payment_type = models.CharField(
        _("payment type"), max_length=3, choices=PAYMENT_TYPES, default="CSH"
    )
    bank_flag = models.ForeignKey(
        "BankFlag",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="form_of_payments",
    )
    ctrl = models.CharField(
        _("control number"), max_length=50, null=True, blank=True
    )
    value = models.DecimalField(_("value"), max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_of_payments_created",
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_of_payments_updated",
    )

    def __str__(self):
        if self.payment_type == "CSH":
            return "{} | {} ${} at:{}".format(
                self.person.name,
                self.payment_type,
                self.value,
                self.created_on.strftime("%m/%d/%Y %H:%M:%S"),
            )
        return "{} | {} {} {} ${} at:{}".format(
            self.person.name,
            self.payment_type,
            self.bank_flag.name,
            self.ctrl,
            self.value,
            self.created_on.strftime("%m/%d/%Y %H:%M:%S"),
        )

    class Meta:
        verbose_name = _("form of payment")
        verbose_name_plural = _("form of payments")
        ordering = ["-created_on"]
