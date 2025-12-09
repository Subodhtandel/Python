from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, MenuItem, CartItem, Product
from cars10.models import *
import razorpay

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,"index.html",{"categories":categories,"products":products})

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def menu(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def Search(request):
    return render(request,'Search.html')

def cart(request):
    return render(request,'cart.html')

def book(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        num_persons = request.POST.get('num_persons')
        date = request.POST.get('date')
        form_time = request.POST.get('time')

        Booking.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            email=email,
            num_persons=num_persons,
            date=date,
            time=form_time,
        )
        
        # FIX: These two lines were moved back one indentation level
        messages.success(request, "✅ Your table has been booked successfully!")
        return redirect('book') 

    return render(request, 'book.html')

def cart_view(request):
    # Show items only for the logged-in user
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    # Calculate total (subtotal and grand total are the same here)
    total = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 0  # you can customize later
    grand_total = total + shipping

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'grand_total': grand_total,
    })

def update_cart_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = max(quantity, 1)
        item.save()
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_view')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')

# @login_required
# def cart_view(request):
#     # Get all cart items from the DATABASE for the current user
#     cart_items = CartItem.objects.filter(user=request.user)
    
#     # Calculate the total price from the database items
#     total = sum(item.total_price for item in cart_items)
    
#     context = {
#         'cart_items': cart_items,  # Your template loops over 'cart_items'
#         'total': total,
#     }
#     return render(request, 'cart.html', context)

def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_view')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_view')

def checkout_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})


def payment(request):
    amt = request.GET.get("amt", 0)

    amt = int(float(amt)) * 100     # ₹ to paise

    client = razorpay.Client(auth=("rzp_test_RZXLQPG4IXJQB3", "uUv2G43kTlNJVVUGd0DfZzjA"))

    order = client.order.create({
        "amount": amt,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse(order)