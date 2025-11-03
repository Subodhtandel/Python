from django.contrib import admin

from .models import MenuItem, Booking , Product , CartItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'category', 'price', 'is_available')
    
    list_filter = ('category', 'is_available')
    
    search_fields = ('name', 'description')
   
    list_editable = ('price', 'is_available')

    ordering = ('category', 'price',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date', 'time', 'num_persons', 'status', 'created_at')
    
    list_filter = ('date', 'status', 'num_persons')
    
    search_fields = ('customer_name', 'phone_number')

    list_display_links = ('customer_name',)
    
    readonly_fields = ('created_at',)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity')
    search_fields = ('product_name', 'user_username')
    list_filter = ('user',)