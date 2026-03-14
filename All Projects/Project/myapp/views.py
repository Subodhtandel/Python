from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib3 import request
import requests

# Create your views here.
def home(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'index.html')

def shop_details(request):
    return render(request, 'shop-details.html')

def shopping_cart(request):
    return render(request, 'shopping-cart.html')

def product(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def blog_details(request):
    return render(request, 'blog-details.html')

def checkout(request):
    return render(request, 'checkout.html')

def shopping_cart(request):
    return render(request, 'shopping-cart.html')

def sign(request):
    return render(request, 'sign.html')