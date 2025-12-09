from django.urls import path
from crudapp.views import *

urlpatterns = [
    path("get",get_data,name="get"),
    path("add",add_data,name="add"),
    path("getbyid/<id>",get_data_id,name="getbyid"),
    path("update/<id>",update_data,name="update"),
    path("delete/<id>",delete_data,name="delete"),
]