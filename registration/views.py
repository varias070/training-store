import django_registration
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django_registration.backends.activation.views import REGISTRATION_SALT
from .forms import RegisterUserForm


class RegisterUser(django_registration.backends.activation.views.RegistrationView):
    form_class = RegisterUserForm
    template_name = 'django_registration/register.html'


