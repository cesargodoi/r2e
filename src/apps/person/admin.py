from django.contrib import admin
from .models import Person, CreditLog, Staff, PersonStay

admin.site.register(Person)
admin.site.register(CreditLog)
admin.site.register(Staff)
admin.site.register(PersonStay)
