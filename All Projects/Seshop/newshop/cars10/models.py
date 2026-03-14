from django.db import models
from django.contrib.auth.models import User
# from .models import Product


class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="cat_img")

    def __str__(self):
        return self.name

# -----------------------------
# Product model
# -----------------------------
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Burger', 'Burger'),
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Fries', 'Fries'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    qty = models.IntegerField() 
# -----------------------------
# CartItem model
# -----------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ allow null for guest carts
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

# -----------------------------
# MenuItem model
# -----------------------------
class MenuItem(models.Model):
    CATEGORY_CHOICES = (
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Sides', 'Sides'),
        ('Drinks', 'Drinks'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Pizza')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


# -----------------------------
# Booking model
# -----------------------------
class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    num_persons = models.IntegerField(verbose_name="Number of Persons")

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"Booking for {self.customer_name} on {self.date} at {self.time}"


class LoginRecord(models.Model):
    """Simple model to record each user login for admin auditing."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"