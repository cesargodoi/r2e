from django.contrib import admin

from .models import Bedroom, Building, Center

admin.site.register(Center)
admin.site.register(Building)
admin.site.register(Bedroom)
