from django.contrib import admin
from .models import Doctor, Appointment, Patient


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin interface for Doctor model
    """
    list_display = ['get_full_name', 'specialization', 'email', 'phone', 'experience_years', 'is_available']
    list_filter = ['specialization', 'is_available', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'license_number', 'experience_years')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"Dr. {obj.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Appointment model
    """
    list_display = ['patient_name', 'doctor', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'doctor']
    search_fields = ['patient_name', 'patient_email', 'doctor__first_name', 'doctor__last_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('doctor', 'appointment_date', 'status')
        }),
        ('Patient Information', {
            'fields': ('patient_name', 'patient_email')
        }),
        ('Notes', {
            'fields': ('reason', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin interface for Patient model
    """
    list_display = ['get_full_name', 'email', 'phone', 'date_of_birth', 'created_at']
    list_filter = ['created_at', 'date_of_birth']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Patient Name'
