from django.contrib import admin
from .models import Activity, Event, Accommodation
from apps.register.models import Register


admin.site.register(Activity)
admin.site.register(Event)


class RegisterInline(admin.TabularInline):
    model = Register
    fields = ["person"]


class AccommodationAdmin(admin.ModelAdmin):
    search_fields = ("register__person__name", "bedroom__name")
    list_display = (
        "bedroom_name",
        "gender",
        "bottom_or_top",
        "registered_person",
    )

    inlines = (RegisterInline,)

    def bedroom_name(self, obj):
        return f"{obj.bedroom.name} ({obj.bedroom.building.name})"

    def registered_person(self, obj):
        return obj.register.person


admin.site.register(Accommodation, AccommodationAdmin)
