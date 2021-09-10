from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('product/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/(<product_id>)/', views.cart_add, name='cart_add'),
    path('product/remove/(<product_id>)/', views.cart_remove, name='cart_remove'),
]
