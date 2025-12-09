from django.urls import path
from . import views

urlpatterns = [
    # General Page URLs
    path('', views.index, name='index'),  # Homepage
    path('home/', views.home, name='home'),
    path('search/', views.Search, name='search'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('payment/',views.payment,name='payment'),
    path('products/', views.product_list, name='product_list'),

    # 🛒 Cart URLs
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
]
