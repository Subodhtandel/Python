from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Doctor URLs
    path('doctors/', views.doctor_list, name='doctor-list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor-detail'),
    path('doctors/new/', views.doctor_create, name='doctor-create'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor-update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor-delete'),
    
    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment-list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointments/new/', views.appointment_create, name='appointment-create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment-update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment-delete'),
    
    # API endpoints
    path('api/doctors/', views.api_doctors_json, name='api-doctors'),
    path('api/doctors/<int:pk>/', views.api_doctor_detail_json, name='api-doctor-detail'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
    
    # Patient Registration
    path('register/', views.patient_register, name='patient-register'),
    path('register/success/<int:pk>/', views.registration_success, name='registration-success'),
    
    # Doctor Finder URLs
    path('finder/', views.finder_home, name='finder-home'),
    path('finder/profile/', views.finder_profile, name='finder-profile'),
    path('finder/profile/<int:pk>/', views.finder_profile, name='finder-profile-detail'),
    path('finder/contact/', views.finder_contact, name='finder-contact'),
    
    # Database Management
    path('database/', views.database_info, name='database-info'),
]
