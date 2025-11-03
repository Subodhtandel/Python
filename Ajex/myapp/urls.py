from django.urls import path
from myapp.views import*
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.search,name='search'),

    path('countries',countries,name="countries"),
    path("states",states,name="states"),
    path("cities",cities,name="cities"),

]