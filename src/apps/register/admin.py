from django.contrib import admin

from .models import BankFlag, FormOfPayment, Order, Register

admin.site.register(BankFlag)


class RegisterAdmin(admin.ModelAdmin):
    search_fields = ("person__name",)
    list_display = (
        "person",
        "lodge",
        "no_stairs",
        "no_bunk",
        "arrival_time",
        "departure_time",
        "housed",
        "value",
    )
    list_filter = ("lodge", "housed", "arrival_time", "departure_time")

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(Register, RegisterAdmin)


class FormOfPaymentAdmin(admin.ModelAdmin):
    search_fields = ("person__name",)
    list_display = ("person", "payment_type", "bank_flag", "ctrl", "value")
    list_filter = ("payment_type", "bank_flag")

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(FormOfPayment, FormOfPaymentAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "center",
        "event",
        "value",
        "late_payment",
        "canceled_payment",
    )
    list_filter = (
        "late_payment",
        "canceled_payment",
        "center",
        "event",
    )
    # filter_horizontal = ["registers", "form_of_payments"]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(Order, OrderAdmin)
