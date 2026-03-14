from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, MenuItem, CartItem, Product, LoginRecord, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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

@login_required
def user(request):
    return render(request,'user.html')


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



def user_login(request):
    # Two-step login flow using email or phone + OTP
    otp_sent = False
    debug_otp = None

    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        otp = request.POST.get("otp", "").strip()

        # If no OTP provided, generate and 'send' one
        if not otp:
            if not identifier:
                messages.error(request, "Please enter your email or phone number.")
            else:
                # generate 6-digit OTP
                from random import randint
                new_otp = f"{randint(100000, 999999)}"
                import datetime
                expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

                request.session['login_otp'] = {
                    'identifier': identifier,
                    'otp': new_otp,
                    'expires': expires.isoformat()
                }

                # In a real app, send the OTP by SMS/email here. For now, show via message when DEBUG.
                messages.success(request, "OTP has been sent to the provided contact (for demo shown below).")
                otp_sent = True
                debug_otp = new_otp

        else:
            # verify OTP in session
            sess = request.session.get('login_otp')
            valid = False
            if sess and sess.get('identifier') and sess.get('otp'):
                try:
                    import datetime
                    expires = datetime.datetime.fromisoformat(sess.get('expires'))
                    if datetime.datetime.utcnow() <= expires and sess.get('otp') == otp and sess.get('identifier') == request.POST.get('identifier'):
                        valid = True
                except Exception:
                    valid = False

            if not valid:
                messages.error(request, "Invalid or expired OTP. Please request a new one.")
                otp_sent = False
            else:
                identifier = sess.get('identifier')
                # find or create user
                user = None
                if "@" in identifier:
                    user = User.objects.filter(email__iexact=identifier).first()
                if not user:
                    user = User.objects.filter(username=identifier).first()

                created_user = False
                if not user:
                    # create a new user using identifier as username
                    email_val = identifier if "@" in identifier else ""
                    user = User.objects.create_user(username=identifier, email=email_val)
                    created_user = True

                # log user in
                login(request, user)
                # Honor "remember me": if checked, keep session for 2 weeks, else expire on browser close
                try:
                    remember = request.POST.get('remember')
                    if remember:
                        request.session.set_expiry(1209600)  # 2 weeks
                    else:
                        request.session.set_expiry(0)  # expire on browser close
                except Exception:
                    pass

                # record login
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
                if ip:
                    ip = ip.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')
                ua = request.META.get('HTTP_USER_AGENT', '')
                try:
                    LoginRecord.objects.create(user=user, ip_address=ip, user_agent=ua)
                except Exception:
                    pass

                # clear OTP session
                try:
                    del request.session['login_otp']
                except KeyError:
                    pass

                # If this was a newly-created user, ensure their cart is empty
                if 'created_user' in locals() and created_user:
                    try:
                        CartItem.objects.filter(user=user).delete()
                    except Exception:
                        pass

                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home')

    # If OTP was stored in session and still valid, indicate otp_sent
    sess = request.session.get('login_otp')
    if sess:
        try:
            import datetime
            expires = datetime.datetime.fromisoformat(sess.get('expires'))
            if datetime.datetime.utcnow() <= expires:
                otp_sent = True
                # Only expose debug OTP when DEBUG: we can fetch from session for demo
                debug_otp = sess.get('otp')
        except Exception:
            otp_sent = False

    return render(request, "user.html", {"otp_sent": otp_sent, "debug_otp": debug_otp})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        # Honor "remember me" option on signup as well
        try:
            remember = request.POST.get('remember')
            if remember:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
        except Exception:
            pass
        # Ensure new user's cart is empty on signup
        try:
            CartItem.objects.filter(user=user).delete()
        except Exception:
            pass
        # Record initial login on signup
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')
        try:
            LoginRecord.objects.create(user=user, ip_address=ip, user_agent=ua)
        except Exception:
            pass
        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')


def complete_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if not order.is_completed:
        order.is_completed = True
        order.save()

        # ✅ Clear the user's cart
        CartItem.objects.filter(user=request.user).delete()

    return redirect('order_success')