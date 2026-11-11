from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('set-currency/', views.set_currency, name='set_currency'),
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('products', views.product_list),
    path('shop/', views.product_list, name='shop'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>', views.product_detail),
    path('detail/', views.product_detail_default, name='product-detail-default'),
]
