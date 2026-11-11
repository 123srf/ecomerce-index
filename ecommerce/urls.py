"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from customer import views as customer_views
from shop import views as shop_views
from payment import views as payment_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path(settings.ADMIN_URL, admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),
    # Autentifikasiya səhifələri (kök URL-lər)
    path('register/', customer_views.register, name='register'),
    path('login/', customer_views.login_view, name='login'),
    path('logout/', customer_views.logout_view, name='logout'),
    path('customer/', include('customer.urls')),
    path('payment/', include('payment.urls')),
    # Səhifələrin qısa / birbaşa URL-ləri
    path('contact/', customer_views.contact, name='contact'),
    path('checkout/', payment_views.checkout, name='checkout'),
    path('cart/', payment_views.cart, name='cart'),
    # Valyuta seçimi — şablonlarda {% url 'set_currency' %} namespace-siz işləsin deyə
    path('set-currency/', shop_views.set_currency, name='set_currency'),
    path('', include('shop.urls')),

    # .html genişlənməsi ilə olan istəklər üçün ehtiyat (fallback) keçidləri
    path('shop.html', shop_views.product_list),
    path('detail.html', shop_views.product_detail_default),
    path('contact.html', customer_views.contact),
    path('checkout.html', payment_views.checkout),
    path('cart.html', payment_views.cart),
    path('index.html', shop_views.home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
