from django.contrib import admin
from .models import Doctor
# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone_number', 'email')
    search_fields = ('name', 'specialty')
    list_filter = ('specialty',)
    