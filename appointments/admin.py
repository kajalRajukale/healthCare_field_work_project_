from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_type', 'appointment_date']
    list_editable = ['status']
    search_fields = ['patient__user__first_name', 'doctor__first_name']
