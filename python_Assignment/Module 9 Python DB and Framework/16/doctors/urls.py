from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('appointment/<int:appointment_id>/confirmation/', views.appointment_confirmation, name='appointment_confirmation'),
]


