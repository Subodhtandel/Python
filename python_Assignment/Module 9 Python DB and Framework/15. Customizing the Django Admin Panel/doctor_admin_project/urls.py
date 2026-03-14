"""
URL configuration for doctor_admin_project project.
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Customize admin site headers
admin.site.site_header = "Doctor Management System"
admin.site.site_title = "Doctor Admin"
admin.site.index_title = "Welcome to Doctor Administration Portal"


