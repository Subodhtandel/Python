from django.contrib import admin
from .models import Category, Product, CartItem, Booking, LoginRecord

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for the Product model."""
    list_display = ('name', 'category', 'price')
    search_fields = ('name',)
    list_filter = ('price', 'category')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for the CartItem model."""
    list_display = ('product', 'user', 'quantity')
    # Use __ to search related model fields
    search_fields = ('product__name', 'user__username') 
    list_filter = ('user',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for the Booking model."""
    list_display = ('customer_name', 'date', 'time', 'num_persons') # Assuming num_persons is the full field name
    list_filter = ('date', 'status', 'num_persons')
    search_fields = ('customer_name', 'phone_number')
    list_display_links = ('customer_name',)
    readonly_fields = ('created_at',)


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'user_agent', 'timestamp')
    list_filter = ('timestamp',)

# @admin.register(user)
# class UserAdmin(admin.ModelAdmin):
#     """Admin configuration for the User model."""
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')