from django.contrib import admin
from .models import Person, CreditLog, PersonStay

admin.site.register(Person)
admin.site.register(CreditLog)
admin.site.register(PersonStay)
