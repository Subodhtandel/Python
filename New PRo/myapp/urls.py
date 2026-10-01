from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index1'),
    path('api/members/', views.get_members, name='get_members'),
    path('api/attendance/<int:member_id>/<str:year_month>/', views.get_attendance, name='get_attendance'),
    path('api/attendance/toggle/', views.toggle_attendance, name='toggle_attendance'),
]