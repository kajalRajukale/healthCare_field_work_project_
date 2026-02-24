from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone",
        "blood_group",
        "gender",
        "created_at",
    ]
    list_filter = ["gender", "blood_group"]
    search_fields = ["user__first_name", "user__last_name", "user__email", "phone"]
