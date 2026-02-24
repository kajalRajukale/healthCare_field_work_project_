from django.contrib import admin
from .models import MedicalReport


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ["title", "patient", "doctor", "report_type", "report_date"]
    list_filter = ["report_type", "is_confidential"]
    search_fields = ["title", "patient__user__first_name"]
