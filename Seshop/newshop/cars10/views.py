from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Booking, MenuItem, CartItem, Product
from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def home(request):
    return render(request, 'index.html') 

def menu(request):
 
    menu_items = MenuItem.objects.filter(is_available=True).order_by('category', 'name')
    context = {
        'menu_items': menu_items,

    }
    return render(request, 'menu.html', context)

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

        # Create booking without time
        Booking.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            email=email,
            num_persons=num_persons,
            date=date,
            time=form_time,
        )

        # Optional success message
        messages.success(request, "✅ Your table has been booked successfully!")
        return redirect('book')  # Stay on same page and show success message

    return render(request, 'book.html')



def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Or your session/user logic
    total_price = 0
    for item in cart_items:
        item.line_total = item.quantity * item.product.price  # Attach line total to item
        total_price += item.line_total

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

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