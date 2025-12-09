from django.urls import path
from myapp.views import *

urlpatterns=[
    path('getusers',get_users,name="getusers"),
    path('postusers',post_users,name="postusers"),
    path('putusers',put_users,name="putusers"),
    path('deleteusers',delete_users,name="deleteusers"),
    path('students', StudentView.as_view(), name='students'),
    path("students<id>",StudentViewId.as_view())
]   