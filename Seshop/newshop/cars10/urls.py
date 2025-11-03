from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('search/', views.Search, name='search'),
    path('cart/', views.cart, name='cart_view'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.product_list, name='product_list'),
]