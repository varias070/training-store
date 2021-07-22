from django.urls import path, include
from . import views
from .views import *

app_name = 'store'
urlpatterns = [
    path('search/', Searcher.as_view(), name='search'),
    path('', Catalog.as_view(), name='catalog'),
    path('product/<int:pk>/', views.product, name='product'),
    path('product/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/(<product_id>)/', views.cart_add, name='cart_add'),
    path('product/remove/(<product_id>)/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('personal-cabinet/<int:pk>/', ShowPersonalCabinet.as_view(), name='personal_cabinet')
]

handler404 = page_not_found
