from django.contrib import admin
from .models import Doctor, Specialty, Appointment


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'doctor_count']
    search_fields = ['name', 'description']

    def doctor_count(self, obj):
        return obj.doctors.count()
    doctor_count.short_description = 'Number of Doctors'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_specialties', 'city', 'consultation_fee', 'availability_status', 'rating']
    list_filter = ['availability_status', 'specialties', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'license_number']
    filter_horizontal = ['specialties']

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Doctor Name'

    def get_specialties(self, obj):
        return obj.get_specialties_display()
    get_specialties.short_description = 'Specialties'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'patient_name', 'doctor', 'appointment_date', 'appointment_time', 'amount', 'payment_status', 'status']
    list_filter = ['status', 'payment_status', 'appointment_date', 'doctor']
    search_fields = ['patient_name', 'patient_email', 'patient_phone', 'order_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'


