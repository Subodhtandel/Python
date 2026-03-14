from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about.html'),
    path('contact/', views.contact, name='contact.html'),
    path('services/', views.services, name='services.html'),
]
