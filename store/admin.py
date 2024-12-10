from django.contrib import admin
from .models import Customer, Category, Product, Order, PasswordResetToken

# Registering the Customer model with custom admin display
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')  # Columns to display
    search_fields = ('first_name', 'last_name', 'email')  # Searchable fields
    list_filter = ('created_at',)  # Filter options
    ordering = ('-created_at',)  # Default ordering by creation date (newest first)


# Registering the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Columns to display
    search_fields = ('name',)  # Searchable fields
    list_filter = ('created_at',)  # Filter options


# Registering the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')  # Columns to display
    search_fields = ('name', 'category__name')  # Searchable fields
    list_filter = ('category', 'created_at')  # Filter options
    ordering = ('-created_at',)  # Default ordering by creation date


# Registering the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'quantity', 'price', 'status', 'date', 'ordered_at')  # Columns to display
    search_fields = ('product__name', 'customer__first_name', 'customer__last_name')  # Searchable fields
    list_filter = ('status', 'date', 'ordered_at')  # Filter options
    ordering = ('-ordered_at',)  # Default ordering by order date


# Registering the PasswordResetToken model
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'customer', 'created_at', 'is_used')  # Columns to display
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')  # Searchable fields
    list_filter = ('is_used', 'created_at')  # Filter options
    ordering = ('-created_at',)  # Default ordering by creation date

# admin.site.register(PasswordResetToken)
