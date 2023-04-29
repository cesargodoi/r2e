from django.contrib import admin
from .models import Activity, Event, BedroomMapping


admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(BedroomMapping)
