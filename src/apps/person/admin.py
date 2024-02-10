from django.contrib import admin
from .models import Person, Staff, PersonStay

# admin.site.register(Person)
admin.site.register(Staff)
admin.site.register(PersonStay)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ["aspect", "center", "center", "city", "is_active"]
    search_fields = ["name", "email"]
    list_display = ["name", "aspect", "center", "city", "state"]

    readonly_fields = (
        "created_on",
        "modified_on",
        "created_by",
        "modified_by",
    )

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
