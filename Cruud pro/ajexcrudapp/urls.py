

from django.urls import path
from ajexcrudapp.views import *

urlpatterns = [
    path("",index, name="index"),
    path("register",register,name="register"),
    path("display",display,name="display"),
    path("deptdisplay",deptdisplay,name="deptdisplay"),
    path("delete",delete_std,name="delete"),
    path("databyid",databyid,name="databyid")
]