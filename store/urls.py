from django.urls import path
from . import views
from .views import *

app_name = 'store'
urlpatterns = [
    path('', Catalog.as_view(), name='catalog'),
    path('product/<int:pk>/', views.show_product, name='product'),
    path('product/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/(<product_id>)/', views.cart_add, name='cart_add'),
    path('product/remove/(<product_id>)/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('personal-cabinet/<int:pk>/', ShowPersonalCabinet.as_view(), name='personal_cabinet'),
    path('change_personal_info/<int:pk>/', ChangePersonalInformation.as_view(), name='change_personal_info'),
    path('info/', ShowInfo.as_view(), name='info'),
    path('change-password/<int:pk>/', ChangePassword.as_view(), name='change-password'),
    path('personal_order/<int:pk>/', views.show_personal_order, name='show_personal_order')
]

handler404 = page_not_found
