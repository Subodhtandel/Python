from django.urls import path
from Newapp.views import *
urlpatterns = [
    path('',index,name="index"),
    path('payment',payment,name='payment'),
    path('sms',sms,name='sms'),
    path("email",send_email,name="email")
]