from django.db import models
import datetime
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def is_exists(self):
        return Customer.objects.filter(email=self.email).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"



class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Tracks when the category is created

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        return Product.objects.filter(category=category_id) if category_id else Product.get_all_products()
    
    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=250, blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)  # Track if the order is completed
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.name} for {self.customer}"


class PasswordResetToken(models.Model):
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        null=True,  # Allow null values
        blank=True  # Allow blank in forms
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Token is valid for 3 days
        return not self.is_used and self.created_at > timezone.now() - timedelta(days=3)
