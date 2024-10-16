from django import forms

from .models import BankFlag, FormOfPayment


class BankFlagForm(forms.ModelForm):
    class Meta:
        model = BankFlag
        fields = "__all__"


class FormOfPaymentForm(forms.ModelForm):
    class Meta:
        model = FormOfPayment
        fields = ["person", "payment_type", "bank_flag", "ctrl", "value"]
