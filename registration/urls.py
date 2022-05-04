from django.urls import path
from .tasks import *

app_name = 'registration'
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
]