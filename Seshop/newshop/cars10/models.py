from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Product model
# -----------------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Optional fields you can add later (e.g. image, description)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# -----------------------------
# CartItem model
# -----------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def line_total(self):
        return self.quantity * self.product.price


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
