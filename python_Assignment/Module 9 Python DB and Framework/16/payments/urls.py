from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:appointment_id>/', views.initiate_payment, name='initiate_payment'),
    path('paytm-callback/', views.paytm_callback, name='paytm_callback'),
    path('status/<str:order_id>/', views.payment_status, name='payment_status'),
]


