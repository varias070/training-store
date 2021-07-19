from django.urls import path
from . import views


app_name = 'store'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.catalog, name='catalog'),
    path('services/', views.services, name='services'),
    path('product/<int:pk>/', views.product, name='product'),
    path('product/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/(<product_id>)/', views.cart_add, name='cart_add'),
    path('product/remove/(<product_id>)/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
]

