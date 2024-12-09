from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    LoginView, 
    PasswordResetView, 
    PasswordResetConfirmView
)

urlpatterns = [
    path('', views.landing_page, name='landing-page'), 
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('home/', views.IndexView.as_view(), name='homepage'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment'),
    path('logout/', views.logout, name='logout'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uuid:token>/', 
         PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
