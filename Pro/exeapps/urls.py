from django.urls import path
from exeapps.views import *

urlpatterns = [
    path("",index,name="index"),
    path("reg",reg,name="reg"),
    path("display",display,name="display"),
    path("delete/<int:id>/",delete_student,name="delete"),
    path("update/<int:id>/", update_student, name="update"),
]