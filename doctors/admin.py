from django.contrib import admin
from .models import Doctor, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'department', 'experience_years', 'consultation_fee', 'is_active']
    list_filter = ['is_active', 'department']
    search_fields = ['first_name', 'last_name', 'specialization']
    list_editable = ['is_active']
