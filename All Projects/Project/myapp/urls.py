from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),

    path('about/', views.about, name="about"),

    # route without extension; canonical shop URL
    path('index.html', views.home, name="home"),

    # provide legacy URL matching the template filename
    path('shop.html', views.product, name="shop"),

    path('contact.html', views.contact, name="contact"),

    path('shop-details.html', views.shop_details, name='shop-details'),

    path('shopping-cart.html', views.shopping_cart, name="shopping-cart"),

    path('product.html', views.product, name="product"),

    path('about.html', views.about, name="about"),

    path('blog.html', views.blog, name="blog"),

    path('blog-details.html', views.blog_details, name="blog-details"),

    path('checkout.html', views.checkout, name="checkout"),

    path('sign.html', views.sign, name="sign"),

    ]