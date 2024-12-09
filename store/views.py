from datetime import timedelta, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from django.views import View
from .models import Customer, Product, Category, Order
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from allauth.socialaccount.models import SocialAccount
from django.core.mail import send_mail
from .models import PasswordResetToken
import uuid
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator


def landing_page(request):
    return render(request, 'landing.html')

class PasswordResetView(View):
    def get(self, request):
        # Render the password reset page for GET requests
        return render(request, 'store/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        
        try:
            customer = Customer.get_customer_by_email(email)
            
            if customer:
                # Create reset token
                reset_token = PasswordResetToken.objects.create(customer=customer)
                
                # Construct reset link
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', 
                            kwargs={'token': str(reset_token.token)}
                    )
                )
                
                try:
                    # Send email
                    send_mail(
                        'Password Reset Request',
                        f'Click the link below to reset your password:\n{reset_link}',
                        'noreply@yourproject.local',  # Sender email
                        [email],
                        fail_silently=False,
                    )
                    
                    return render(request, 'store/password_reset.html', {
                        'message': 'Password reset link sent to your email.'
                    })
                
                except Exception as email_error:
                    print(f"Email sending error: {email_error}")
                    return render(request, 'store/password_reset.html', {
                        'error': 'Unable to send reset email. Please contact support.'
                    })
            
            else:
                return render(request, 'store/password_reset.html', {
                    'error': 'No account found with this email address.'
                })
        
        except Exception as e:
            print(f"Password Reset Error: {e}")
            return render(request, 'store/password_reset.html', {
                'error': 'An unexpected error occurred. Please try again.'
            })
        
""" class PasswordResetView(View):
    def get(self, request):
        return render(request, 'store/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        
        try:
            # Use the custom method to get customer by email
            customer = Customer.get_customer_by_email(email)
            
            # Check if customer exists before creating token
            if customer:
                # Create a new password reset token
                reset_token = PasswordResetToken.objects.create(customer=customer)
                
                # Construct reset link
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', 
                            kwargs={'token': str(reset_token.token)}
                    )
                )
                
                # Send email
                send_mail(
                    'Password Reset Request',
                    f'Click the link below to reset your password:\n{reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                return render(request, 'store/password_reset.html', {
                    'message': 'Password reset link sent to your email.'
                })
            else:
                return render(request, 'store/password_reset.html', {
                    'error': 'No account found with this email address.'
                })
        
        except Exception as e:
            # Log the error for debugging
            print(f"Password Reset Error: {e}")
            return render(request, 'store/password_reset.html', {
                'error': 'An error occurred. Please try again.'
            })

"""

""" 
class PasswordResetConfirmView(View):
    def get(self, request, token):
        current_time = timezone.now()
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token, 
                is_used=False,
                created_at__gt=timezone.now() - timedelta(days=3)
            )
            return render(request, 'store/password_reset_confirm.html', {
                'token': token
            }, {'current_time': current_time})
        except PasswordResetToken.DoesNotExist:
            return render(request, 'store/password_reset.html', {
                'error': 'Invalid or expired reset link.'
            })

    def post(self, request, token):
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Passwords do not match',
                'token': token
            })

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token, 
                is_used=False,
                created_at__gt=timezone.now() - timedelta(days=3)
            )
            
            # Update customer password
            customer = reset_token.customer
            customer.password = make_password(new_password)
            customer.save()

            # Mark token as used
            reset_token.is_used = True
            reset_token.save()

            return render(request, 'store/login.html', {
                'message': 'Password successfully reset. Please log in.'
            })
        
        except PasswordResetToken.DoesNotExist:
            return render(request, 'store/password_reset.html', {
                'error': 'Invalid or expired reset link.'
            })
"""

class PasswordResetConfirmView(View):
    def get(self, request, token):
        try:
            # Convert token to UUID if it's a string
            token_uuid = uuid.UUID(str(token))
            
            # Find the token, ensure it's not used and not expired
            reset_token = PasswordResetToken.objects.get(
                token=token_uuid, 
                is_used=False,
                created_at__gt=timezone.now() - timedelta(days=3)
            )
            
            # Context to pass the token to the template
            context = {
                'token': token,
                'email': reset_token.customer.email  # Optional: pre-fill email
            }
            
            return render(request, 'store/password_reset_confirm.html', context)
        
        except (ValueError, PasswordResetToken.DoesNotExist):
            # Handle invalid or expired token
            return render(request, 'store/password_reset.html', {
                'error': 'Invalid or expired reset link. Please request a new password reset.'
            })

    def post(self, request, token):
        # Get form data
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate password match
        if new_password != confirm_password:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Passwords do not match',
                'token': token
            })
        
        # Validate password strength (optional but recommended)
        if len(new_password) < 8:
            return render(request, 'store/password_reset_confirm.html', {
                'error': 'Password must be at least 8 characters long',
                'token': token
            })
        
        try:
            # Convert token to UUID
            token_uuid = uuid.UUID(str(token))
            
            # Find the valid, unused token
            reset_token = PasswordResetToken.objects.get(
                token=token_uuid, 
                is_used=False,
                created_at__gt=timezone.now() - timedelta(days=3)
            )
            
            # Get the associated customer
            customer = reset_token.customer
            
            # Update password
            customer.password = make_password(new_password)
            customer.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            # Redirect to login with success message
            return render(request, 'store/login.html', {
                'message': 'Password successfully reset. Please log in with your new password.'
            })
        
        except PasswordResetToken.DoesNotExist:
            # Handle invalid or expired token
            return render(request, 'store/password_reset.html', {
                'error': 'Invalid or expired reset link. Please request a new password reset.'
            })
        
        except Exception as e:
            # Log any unexpected errors
            print(f"Password Reset Confirm Error: {e}")
            return render(request, 'store/password_reset.html', {
                'error': 'An unexpected error occurred. Please try again.'
            })


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Check if the logged-in user has a corresponding Customer record
            try:
                customer = Customer.objects.get(email=request.user.email)
                request.session['customer'] = customer.id
                return redirect('homepage')
            except Customer.DoesNotExist:
                # Create a new Customer if not exists
                customer = Customer.objects.create(
                    email=request.user.email,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name
                )
                request.session['customer'] = customer.id
                return redirect('homepage')
        
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer.get_customer_by_email(email)

        if customer and check_password(password, customer.password):
            request.session['customer'] = customer.id
            return redirect('homepage')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid email or password'})


class RegisterView(View):
    def get(self, request):
        return render(request, 'store/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email,
                            password=make_password(password))

        if customer.is_exists():
            return render(request, 'store/register.html', {'error': 'Email already exists'})
        customer.register()
        return redirect('login')

# Home Page view
class IndexView(View):
    def get(self, request):
        if not request.session.get('customer'):
            return redirect('login')  # If not logged in, redirect to login
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_category_id(categoryID)
        else:
            products = Product.get_all_products()

        return render(request, 'store/index.html', {'products': products, 'categories': categories})

# Cart Detail view
class CartView(View):
    def post(self, request):
        cart = request.session.get('cart', {})
        product_id = request.POST.get('product')
        action = request.POST.get('action')

        if product_id in cart:
            if action == 'increase':
                cart[product_id]['quantity'] += 1
            elif action == 'decrease' and cart[product_id]['quantity'] > 1:
                cart[product_id]['quantity'] -= 1
            elif action == 'remove':
                cart.pop(product_id)

        request.session['cart'] = cart
        return redirect('cart')

    def get(self, request):
        if not request.session.get('customer'):
            return redirect('login')
        cart = request.session.get('cart', {})
        total_price = 0
        cart_items = []

        # Loop through the cart and fetch product details
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = float(item['price']) * item['quantity']  # Ensure float multiplication
            total_price += item_total
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item_total,
                'image': product.image.url  # Include image URL
            })

        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Checkout View
class CheckoutView(View):
    def get(self, request):
        if not request.session.get('customer'):
            return redirect('login')
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')  # If cart is empty, redirect to cart page
        
        # Calculate the total price
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        return render(request, 'store/checkout.html', {'cart': cart, 'total_price': total_price})

    def post(self, request):
        # Retrieve session data
        customer_id = request.session.get('customer')
        cart = request.session.get('cart', {})

        # Check if cart is empty
        if not cart:
            return redirect('cart')

        # Debug: Print out all POST data
        # print("POST Data:", request.POST)

        # Collect customer and shipping info
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Validate that both address and phone are provided
        if not address:
            return render(request, 'store/checkout.html', {
                'error': 'Address is required',
                'cart': cart
            })

        if not phone:
            return render(request, 'store/checkout.html', {
                'error': 'Phone number is required',
                'cart': cart
            })

        # Validate phone number length
        if len(phone) > 20:
            return render(request, 'store/checkout.html', {
                'error': 'Phone number is too long. Maximum length is 20 characters.',
                'cart': cart
            })

        # Place the order for each product in the cart
        try:
            for product_id, item in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    order = Order(
                        customer_id=customer_id,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price'],
                        address=address,
                        phone=phone
                    )
                    order.place_order()  # Assuming place_order handles saving the order
                except Product.DoesNotExist:
                    return render(request, 'store/checkout.html', {
                        'error': f'Product with ID {product_id} not found.',
                        'cart': cart
                    })

            # Clear the cart after placing the order
            request.session['cart'] = {}
            return redirect('orders')

        except Exception as e:
            # Log the full error for debugging
            import traceback
            print(traceback.format_exc())
            return render(request, 'store/checkout.html', {
                'error': f'An error occurred while processing your order: {str(e)}',
                'cart': cart
            })

# Order View
class OrderView(View):
    def get(self, request):
        if not request.session.get('customer'):
            return redirect('login')
        
        customer_id = request.session.get('customer')
        all_orders = Order.get_orders_by_customer(customer_id)
        
        # Calculate the total price for each order
        for order in all_orders:
            order.total_price = order.price * order.quantity
        
        # Pagination
        paginator = Paginator(all_orders, 5)  # Show 10 orders per page
        page_number = request.GET.get('page', 1)
        orders = paginator.get_page(page_number)
        
        context = {
            'orders': orders,
            'total_orders': len(all_orders)
        }
        
        return render(request, 'store/orders.html', context)


class ShopView(View):
    def get(self, request):
        # Fetch all products and categories with product count
        products = Product.objects.all()
        categories = Category.objects.annotate(product_count=Count('products'))
        
        return render(request, 'store/shop.html', {'products': products, 'categories': categories})

    def post(self, request):
        product_id = request.POST.get('product')
        product = Product.objects.get(id=product_id)

        # Get the cart from the session, or initialize an empty cart
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {
                'name': product.name,
                'quantity': 1,
                'price': float(product.price),  # Convert Decimal figures
            }

        # Save the updated cart to the session
        request.session['cart'] = cart

        return redirect('cart')


class PaymentView(View):
    def get(self, request, order_id):
        if not request.session.get('customer'):
            return redirect('login')
        order = get_object_or_404(Order, id=order_id)
        total_price = order.product.price * order.quantity
        return render(request, 'store/payment.html', {'order': order, 'total_price': total_price})

    def post(self, request, order_id):
        payment_method = request.POST.get('payment_method')
        order = get_object_or_404(Order, id=order_id)

        if payment_method:
            try:
                # Process payment logic here
                order.status = True
                order.payment_method = payment_method
                order.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Payment processed successfully!',
                        'redirect_url': reverse('orders')
                    })
                return redirect('orders')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
                return render(request, 'store/payment.html', {
                    'error': str(e),
                    'order': order,
                    'total_price': order.product.price * order.quantity,
                })
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Please select a payment method.'
            }, status=400)
        
        return render(request, 'store/payment.html', {
            'error': 'Please select a payment method.',
            'order': order,
            'total_price': order.product.price * order.quantity,
        })


def logout(request):
    if request.session.get('customer'):
        del request.session['customer']
    return redirect('landing-page')

