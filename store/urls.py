from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.catalog, name='catalog'),
    path('services/', views.services, name='services'),
    path('product/<int:pk>/', views.product, name='product'),
]

