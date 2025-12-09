from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
]
